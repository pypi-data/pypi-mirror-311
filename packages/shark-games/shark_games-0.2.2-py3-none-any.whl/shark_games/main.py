"""
 Copyright (C) 2024  sophie (itsme@itssophi.ee)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import asyncio
import aiohttp
import aiofiles

import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s: %(module)s, %(funcName)s: %(message)s")
log = logging.getLogger(__name__)

import json
import time

import signal

import re

from shark_games import __version__

from shark_games.dices import roll
from shark_games.dices import coin
from shark_games.praise import praise

import dice

class Ratelimithandler():
    def __init__ (self, config):
        self.max_retries = config["max_retries"]
        self.base_delay = config["base_delay"]
        self.max_delay = config["max_delay"]
        self.request_delay = config["base_request_delay"]

        self.request_semaphore = asyncio.Semaphore(1)
        self.last_request_time = 0.0

    async def enforce_delay(self):
        elapsed = time.time() - self.last_request_time
        if elapsed < self.request_delay:
            await asyncio.sleep(self.request_delay - elapsed)

    async def handle_request(self, request_func, *args, **kwargs):
        """
        Execute a request with rate limit handling and exponential backoff.
        
        :param request_func: Async function to execute
        :param args: Positional arguments for the request function
        :param kwargs: Keyword arguments for the request function
        :return: Result of the request
        """
        async with self.request_semaphore:

            await self.enforce_delay()

            for attempt in range(self.max_retries + 1):
                response = await request_func(*args, **kwargs)

                if isinstance(response, aiohttp.ClientResponse):
                    if response.status == 429:
                        self.request_delay += 0.2 #you get 503 blocked if hitting too many times a rate limit - in that case higher the normal delay to avoid hitting it again (the rate limit is enforced by a delay)
                        try:
                            respjson = await response.json()
                            reset_time = respjson.get("error", {}).get("info", {}).get("resetMs", None) #in ms

                        except Exception as e:
                            log.error(f"FAILED await response.json() for {e} after 429 response")
                            reset_time = None

                        if reset_time:
                            reset_time = reset_time/1000 #turn into seconds
                            delay = reset_time - time.time() + 0.1
                        else:
                            delay = min(self.base_delay * (2 ** attempt), self.max_delay)

                        log.warning(f"Rate limit hit. Retrying in {delay}")

                        await asyncio.sleep(delay)
                        continue
            
                self.last_request_time = time.time()
                return response


class Noteprocessing():
    def __init__ (self, path):
        self.path = path
        with open(str(path) + "/config.json", "r") as config_file:
            self.data = json.load(config_file)
        self.is_running = True
        self.tasks = set()
        self.usertag_pattern = rf"@{self.data["username"]}"

        self.rate_limit_handler = Ratelimithandler(self.sync_RateLimitHandling())

        self.shutdown_in_progress = False
        
    async def base_url(self):
        return self.data["base_url"]

    async def headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.data["bearer"]}"
        }
    
    async def lastNoteId (self):
        return self.data["lastNoteId"]
    
    async def tell_invalid_command(self):
        return self.data["warnInvalidCommand"]
    
    def sync_RateLimitHandling(self):
        return self.data["RateLimitHandling"]
    
    async def req_json (self):
        if await self.lastNoteId() == None:
            return {
                "limit": 10
            }
        else:
            return {
            "limit": 100,
            "sinceId": await self.lastNoteId()
            }
        
    async def interval(self):
        return self.data["interval"]
    
    def create_add_task(self, task): #not async bacause asyncio.create_task isn't
        actual_task = asyncio.create_task(task)
        self.tasks.add(actual_task)
        actual_task.add_done_callback(self.tasks.discard)

    async def update_lastNoteId(self, noteId:str):
        self.data["lastNoteId"] = noteId
        data_to_write = json.dumps(self.data)
        async with aiofiles.open(str(self.path) + "/config.json", mode="w") as config_file:
            await config_file.write(data_to_write)

    async def return_help_message(self):
        return f"""
<center>$[x3 **HELP PAGE**]</center>
$[x2 Usage]
Write the command text and ping the bot. The bot ping can be placed everywhere. The bot will reply with the same visibility (including if federate or not, in case of local users) and cw. The bot will not ping you on reply.
$[x2 Commands]
<required-argument> [optional-argument] (alias)
**help** () - shows this page
**ping** - replies with pong
**pong** - replies with ping
**roll [min:int] [max:int]** - Replies with a random number number between min and max. min and max default to 1 and 100 respectively
**dice <combination:str>** - Replies with the dices. ?[Learn more about the dice notation](https://github.com/borntyping/python-dice?tab=readme-ov-file#notation)
**coin** (flip) - Flips a coin: replies with either Head or Tails
**praise [mention]** (compliment) - compliment person you mention. This will still reply to your note. When no arguments are given, will praise author.
<small>shark-games | version: {__version__} | ?[Source](https://codeberg.org/itssophie/shark-games) | ?[GPL-3.0-or-later](https://codeberg.org/itssophie/shark-games/src/branch/main/LICENSE)</small>
"""

    async def tell_missing_argument(self, n_arguments, command:str):
        return f"ERROR {n_arguments} missing argument(s) in command {command}"
    
    async def get_user_info(self, mention:str, session:aiohttp.ClientSession):
        if mention[0] == "@":
            mention = mention[1:]
        if "@" in mention:
            user_host = mention.split("@")
        else:
            user_host = [mention, None]

        json_req = {
            "username": user_host[0],
            "host": user_host[1]
        }

        async with await self.rate_limit_handler.handle_request(session.post, await self.base_url() + "users/show", json = json_req, headers= await self.headers()) as response:
            if response.status == 200:
                try:
                    return await response.json()
                except Exception as e:
                    log.error(f"FAILED await response.json() for {e}")
                    return None
            else:
                try:
                    respjson =  await response.json()
                except:
                    pass
                log.error(f"API response: {response.status}, {response}, {respjson}")
                return None



    async def execute_command(self, text, author, session:aiohttp.ClientSession):
        try:
            text = re.sub(r"\s+", " ", re.sub(self.usertag_pattern, '', text)).strip()
            splitted_text = text.split()
            length_splitted_text = len(splitted_text)
            if length_splitted_text == 0:
                splitted_text = [""]
            return_text = None
            cw = None
            match splitted_text[0]:
                case "ping":
                    return_text = "pong"
                case "pong":
                    return_text = "ping"
                case "help" | "":
                    return_text = await self.return_help_message()
                case "roll":
                    match length_splitted_text:
                        case 1:
                            return_text = roll.main()
                        case 2:
                            return_text = roll.main(max = int(splitted_text[1]))
                        case 3:
                            return_text = roll.main(min = int(splitted_text[1]), max = int(splitted_text[2]))
                case "dice":
                    if length_splitted_text == 1:
                        return_text = await self.tell_missing_argument(1, "dice")
                    try: 
                        return_text = str(dice.roll(splitted_text[1]))
                    except Exception:
                        return_text = "Error processing dice request. ?[Learn more about the dice notation](https://github.com/borntyping/python-dice?tab=readme-ov-file#notation)"
                case "coin" | "flip":
                    return_text = coin.main()
                case "praise" | "compliment":
                    cw = "Praise"
                    if length_splitted_text == 1:
                        return_text = praise.main(author)
                    else:
                        user_info = await self.get_user_info(splitted_text[1], session)
                        if user_info:
                            return_text = praise.main(user_info)
                        else:
                            log.error("Something went wrong with trying to get user info to praise")
                            return_text = "An error occured trying to get mentioned user info"
                            cw = None
                case _:
                    if await self.tell_invalid_command():
                        return_text = "It seems like you misspelled something. Reply (and mention) `help` to find out about my commands"

        except Exception as e:
            log.error(f"Unknow error processing {text} with Exception: {e}")
            return_text = "An unknown error happened"

        return return_text, cw

        


    async def process_item(self, session:aiohttp.ClientSession, item):
        text, cw = await self.execute_command(item["text"], item["user"], session)
        if not text:
            return
        if not cw:
            cw = item["cw"]
        try:
            json_req = {
                "visibility": item["visibility"],
                "localOnly": item["localOnly"],
                "replyId": item["id"],
                "cw": cw,
                "text": text
            }
            async with await self.rate_limit_handler.handle_request(session.post, await self.base_url() + "notes/create", json = json_req, headers= await self.headers()) as response:
                if response.status == 200:
                    return
                else:
                    try:
                        respjson = await response.json()
                        log.error(f"FAILED responding to command {response.status} {respjson}")
                        return
                    except:
                        log.critical(f"FAILED responding to command, with no json response: {response.status}, {response}")
                        return
        except Exception as e:
            log.error(f"Unexpected error in process_item: {e}")

    async def fetch(self, session:aiohttp.ClientSession):
        async with await self.rate_limit_handler.handle_request(session.post, await self.base_url() + "notes/mentions", json = await self.req_json(), headers= await self.headers()) as response:
            if response.status == 200:
                try:
                    respjson = await response.json()
                except Exception as e:
                    log.error(f"FAILED await response.json() for {e}")
                    return
            else:
                log.error(f"API response: {response.status}, {response}")
                return

        if respjson == [] or respjson[0]["id"] == await self.lastNoteId():
            return
        
        if len(respjson) >= 95:
            log.warning("The amount of new fetched notes is >= 95. You might be getting spammed or you need to lower your fetch interval. You can safely ignore this if it happens after a downtime")
        
        await self.update_lastNoteId(respjson[0]["id"])

        for item in respjson:
            self.create_add_task(self.process_item(session, item))

    async def start(self, session):
        log.info("Started")
        while self.is_running:
            self.create_add_task(self.fetch(session))

            await asyncio.sleep(await self.interval())

    def stop(self):
        if self.shutdown_in_progress:
            return
        self.shutdown_in_progress = True
        self.is_running = False
        log.info("Shutting down…")

    async def shutdown(self):
        if self.tasks:
            previous_len_task = len(self.tasks) + 1
            while self.tasks:
                if previous_len_task != len(self.tasks):
                    previous_len_task = len(self.tasks)
                    log.info(f"There are still {previous_len_task} left. Waiting for them to finish.")
                await asyncio.sleep(0.5)

            log.info("All tasks complete. Proceeding to shutdown")

    async def async_run(self):
        loop = asyncio.get_event_loop()

        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(
                sig, 
                lambda s=sig: self.stop()
            )
        
        async with aiohttp.ClientSession() as session:
            await self.start(session)
            await self.shutdown()

    def run(self):
        log.info("Starting up…")
        asyncio.run(self.async_run())