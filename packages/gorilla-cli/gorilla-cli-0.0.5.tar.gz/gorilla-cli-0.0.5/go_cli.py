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
import sys
import uuid
import requests
import subprocess
import sys
from halo import Halo
import go_questionary

SERVER_URL = "http://34.135.112.197:8000"
__version__ = "0.0.5"  # current version
UPDATE_CHECK_FILE = os.path.expanduser(
    "~/.gorilla-cli-last-update-check"
)


def check_for_updates():
    try:
        with open(UPDATE_CHECK_FILE, "r") as f:
            last_check_date = datetime.datetime.strptime(
                f.read(), "%Y-%m-%d"
            )
    except FileNotFoundError:
        last_check_date = (
            datetime.datetime.now() - datetime.timedelta(days=1)
        )

    if (
        datetime.datetime.now() - last_check_date
        >= datetime.timedelta(days=1)
    ):
        try:
            response = requests.get(
                "https://pypi.org/pypi/gorilla-cli/json"
            )
            latest_version = response.json()["info"]["version"]

            if latest_version > __version__:
                print(
                    f"A new version of gorilla-cli is available: {latest_version}"
                )
        except Exception as e:
            print("Unable to check for updates:", e)

        try:
            with open(UPDATE_CHECK_FILE, "w") as f:
                f.write(datetime.datetime.now().strftime("%Y-%m-%d"))
        except Exception as e:
            print("Unable to write update check file:", e)


def main():
    def execute_command(cmd):
        process = subprocess.run(cmd, shell=True)
        return process.returncode

    args = sys.argv[1:]
    user_input = " ".join(args)

    # Unique user identifier for authentication and load balancing
    # Gorilla-CLI is hosted by UC Berkeley Sky lab for FREE as a 
    #  research prototype. Please don't spam the system or use it
    #  for commercial serving. If you would like to request rate
    #  limit increases for your GitHub handle, please raise an issue.
    try:
        user_id = (
            subprocess.check_output(
                ["git", "config", "--global", "user.email"]
            )
            .decode("utf-8")
            .strip()
        )
    except Exception:
        user_id = str(uuid.uuid4())

    with Halo(text="🦍 Loading", spinner="dots"):
        try:
            data_json = {
                "user_id": user_id,
                "user_input": user_input,
            }
            response = requests.post(
                f"{SERVER_URL}/commands", json=data_json, timeout=30
            )
            commands = response.json()
        except requests.exceptions.RequestException as e:
            print("Server is unreachable.")
            print(
                "Try updating Gorilla-CLI with 'pip install --upgrade gorilla-cli'"
            )
            return

    check_for_updates()

    if commands:
        selected_command = go_questionary.select(
            "", choices=commands, instruction=""
        ).ask()
        exit_code = execute_command(selected_command)

        # Commands failed / succeeded?
        try:
            response = requests.post(
                f"{SERVER_URL}/command-execution-result",
                json={
                    "user_id": user_id,
                    "command": selected_command,
                    "exit_code": exit_code,
                },
                timeout=30,
            )
            if response.status_code != 200:
                print(
                    "Failed to send command execution result to the server."
                )
        except requests.exceptions.Timeout:
            print(
                "Failed to send command execution result to the server: Timeout."
            )


if __name__ == "__main__":
    main()
