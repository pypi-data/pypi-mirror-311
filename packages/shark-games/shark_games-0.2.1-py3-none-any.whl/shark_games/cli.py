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

import click
import requests

import json
import re
import os

import asyncio

from shark_games import __version__
from shark_games.main import Noteprocessing

default_data = {
        "v" : "", #gets automatically configured
        "base_url" : "https://woem.men/api/",
        "bearer" : "",
        "username": "",
        "interval" : 10, #currently only changeable directly via file
        "lastNoteId": None,
        "warnInvalidCommand": False, #currently only changeable directly via file
        "RateLimitHandling" : {"max_retries": 5, "base_delay": 1.0, "max_delay": 45.0, "base_request_delay": 1.0} #currently only changeable directly via file
    }

default_data_needstoconfig = ["bearer"]

def config_update_v(data):
    data["v"] = __version__
    return data

@click.group()
def cli():
    pass

@click.command()
def setup():
    data = default_data
    data = config_update_v(data)
    
    previous_attempt:str = ""
    while True:
        attempt = click.prompt("\nPlease enter your base URL", default=data["base_url"])
        if re.match(r"https://.*\.[A-Za-z]+/api/", attempt):
            break
        else:
            if previous_attempt == attempt:
                if click.confirm("Do you want to skip the URL format check? This might break the program later on."):
                    click.echo("You confirmed to skip the base URL check")
                    break
            previous_attempt = attempt
            click.echo("The provided base URL is in an unexpected format. You can skip check by re-entering the same URL again.\nThe URL needs to start via the https protocol (https://) and needs to end with a /. Normally it also ends with /api/")
    
    try:
        response = requests.get(attempt)
    except:
        click.echo("Invalid URL entered")
        click.echo("Exiting…")
        exit()

    data["base_url"] = attempt
    data["bearer"] = click.prompt("\nPlease enter your API token", hide_input=True)
    
    headers = {
        "Authorization": f"Bearer {data["bearer"]}"
    }
    response = requests.post(f"{data["base_url"]}i", headers=headers, json={})
    if response.status_code == 200:
        jsonresponse = response.json()
        data["username"] = jsonresponse["username"]
    else:
        click.echo(f"Invalid token or response: {response.status_code}, {response.json()["error"]["message"]}")
        click.echo("Exiting…")
        exit()
    
    path = os.path.join(os.getcwd(), "shark-games")
    
    if os.path.exists(path):
        if click.confirm("Overwrite existing config"):
            pass
        else:
            click.echo("Aborting")
            exit()
    
    else:
        os.makedirs(path)

    with open(str(path) + "/config.json", "w") as config_file:
        json.dump(data, config_file)

@click.command()
def run():
    path = os.path.join(os.getcwd(), "shark-games")
    data:dict
    with open(str(path) + "/config.json", "r") as config_file:
        data = json.load(config_file)
    if data["v"] != __version__:
        if data["v"] > __version__:
            click.echo("Version downgrading is not supported. Please update to the last version instead.")
            exit()
        
        click.echo("Updating…")
        # removes all the keys that no longer are used
        keys_to_delete = data.keys() - default_data.keys()
        for key in keys_to_delete:
            data.pop(key)

        # adds the new keys with default value
        keys_to_add = default_data.keys() - data.keys()
        for key in keys_to_add:
            if key in default_data_needstoconfig:
                click.echo(f"Can't update config because key ({key}) needs config. Please reconfigure shark-games or consult release notes in case of a breaking change")
                exit()
            data[key] = default_data[key]

        #finally, update the version number
        data = config_update_v(data)

        with open(str(path) + "/config.json", "w") as config_file:
            json.dump(data, config_file)
    
    process = Noteprocessing(path)
    process.run()

cli.add_command(setup)
cli.add_command(run)