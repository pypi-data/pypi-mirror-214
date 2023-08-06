# Copyright 2023 https://github.com/ShishirPatil/gorilla
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import os
import requests
import subprocess
import sys
from halo import Halo
import go_questionary

SERVER_URL = "http://34.135.112.197:8000/commands"
__version__ = '0.0.3'  # current version
UPDATE_CHECK_FILE = os.path.expanduser("~/.gorilla-cli-last-update-check")

def check_for_updates():
    try:
        with open(UPDATE_CHECK_FILE, 'r') as f:
            last_check_date = datetime.datetime.strptime(f.read(), '%Y-%m-%d')
    except FileNotFoundError:
        last_check_date = datetime.datetime.now() - datetime.timedelta(days=1)

    if datetime.datetime.now() - last_check_date >= datetime.timedelta(days=1):
        try:
            response = requests.get('https://pypi.org/pypi/gorilla-cli/json')
            latest_version = response.json()['info']['version']

            if latest_version > __version__:
                print(f"A new version of gorilla-cli is available: {latest_version}")
        except Exception as e:
            print("Unable to check for updates:", e)

        try:
            with open(UPDATE_CHECK_FILE, 'w') as f:
                f.write(datetime.datetime.now().strftime('%Y-%m-%d'))
        except Exception as e:
            print("Unable to write update check file:", e)

def main():
    def execute_command(cmd):
        subprocess.run(cmd, shell=True)

    args = sys.argv[1:]
    user_input = ' '.join(args)

    with Halo(text='🦍 Loading', spinner='dots'):
        try:
            response = requests.post(SERVER_URL, json={'user_input': user_input})
            commands = response.json()
        except requests.exceptions.RequestException as e:
            print("Server is unreachable.")
            print("If the issue persists, please consider updating Gorilla CLI with 'pip install --upgrade gorilla-cli'")
            return

    check_for_updates()

    if commands:
        selected_command = go_questionary.select("", choices=commands, instruction="").ask()
        execute_command(selected_command)


if __name__ == "__main__":
    main()
