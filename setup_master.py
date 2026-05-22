"""
NW Discord RPC Bot - a bot program for emulating Discord RPC state
Copyright (C) 2026 Andrew Brownington

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

Contact: contact@naruwhite.lol
"""

import os
import sys
import datetime
import logging

configfile = 'config.cfg'
ver = "1.2.0"

# Determine the app directory based on the operating system
if os.name == 'nt':
    app_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'NW RPC')  # Windows
elif sys.platform == 'darwin':
    app_dir = os.path.expanduser('~/Library/Application Support/NW RPC')  # macOS (X and above)
else:
    app_dir = os.path.expanduser('~/.local/share/NW RPC')  # Linux

log_dir = os.path.join(app_dir, 'logs')

# Create the log directory if it does not exist
os.makedirs(app_dir, exist_ok=True)
os.makedirs(log_dir, exist_ok=True)

# Configure logging
log_file = os.path.join(log_dir, f'nw_discordrpc_setup_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log')
logging.basicConfig(filename=log_file, level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')

# Initial logging info
logging.info(f"~[NW Discord RPC bot setup, ver. {ver}]~")

programdir = os.path.dirname(os.path.abspath(__file__))
sourcepath = os.path.join(programdir, configfile)
config_path = os.path.join(app_dir, configfile)

if os.path.exists(config_path):
    logging.info(f'Found existing config.cfg in {app_dir}')
    print(f'config.cfg already exists in {app_dir}. No setup needed.')
    sys.exit(0)

if os.path.exists(sourcepath):
    if os.name == 'nt':
        copycmd = f'copy "{sourcepath}" "{app_dir}"'
    else:
        copycmd = f'cp "{sourcepath}" "{app_dir}"'
    result = os.system(copycmd)
    if result != 0:
        logging.error("Error importing an existing config.cfg")
        print("Error while importing a config file. Maybe you don't have privileges \non accessing either the directory the script located in or the Application Data folder")
        sys.exit(1)
    logging.info(f"Found config.cfg and imported to {app_dir}")
    print(f"Imported config.cfg into {app_dir}.")
    sys.exit(0)

logging.info("No config file exists. Creating a new one instead...")
print("No config file in this system or nothing to import. \nTo import, place a preconfigured config.cfg file in the \ndirectory your script is located in and restart the script.")
print('Creating a new default config file instead...\nWhat is your bot\'s Client ID?\n(you must take it in Discord Developer Portal)')
newclientid = str(input('> '))
try:
    with open(config_path, "w") as f:
        f.write(
            '{\n'
            f'"client_id": "{newclientid}",\n'
            '"state": "Example state",\n'
            '"details": "Example details",\n'
            '"large_image": "examplelarge",\n'
            '"small_image": "examplesmall",\n'
            '"large_text": "example large text",\n'
            '"small_text": "example small text",\n'
            '"buttons": [\n'
            '{"label": "Test link", "url": "https://google.com"}\n'
            ']\n'
            '}'
        )
    logging.info(f"Created new config.cfg in {app_dir}")
    print(f"Created new config.cfg in {app_dir}.")
except Exception as e:
    logging.error(f"Error creating a new default config: {e}")
    print(f"Error creating a new default config: {e}")
    sys.exit(1)
