import os, sys
import logging
from pypresence import Presence # type: ignore
import time
import datetime
import json

configfile = 'config.cfg'
ver = "1.2.0"

# Determine the app directory based on the operating system
if os.name == 'nt': app_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'NW RPC')  # Windows
elif sys.platform == 'darwin': app_dir = os.path.expanduser('~/Library/Application Support/NW RPC')  # macOS (X and above)
else: app_dir = os.path.expanduser('~/.local/share/NW RPC')  # Linux

log_dir = os.path.join(app_dir, 'logs')

# Create the log directory if it does not exist
os.makedirs(app_dir, exist_ok=True)
os.makedirs(log_dir, exist_ok=True)

# Configure logging
log_file = os.path.join(log_dir, f'nw_discordrpc_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log')
logging.basicConfig(filename=log_file, level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')

# Initial logging info
logging.info(f"~[NW Discord RPC bot, ver. {ver}]~")
logging.info(f"OS: {os.uname().sysname} {os.uname().release}")
logging.info(f"Python version: {sys.version}")

def start_rpc(client_id):
    try:
        RPC = Presence(client_id)
        RPC.connect()
        logging.info('Successfully connected to Discord RPC.')
        return RPC
    except Exception as e:
        logging.error(f'Failed to connect to Discord RPC: {e}. Trying to connect again in 15 secs...')
        raise

# Function to update RPC status
def update_rpc(RPC, state, details, large_image, small_image, large_text, small_text, buttons, start_time):
    current_time = int(time.time())
    elapsed_time = current_time - start_time
    # print(0xc0000022)
    RPC.update(
        state=state,
        details=details,
        large_image=large_image,
        small_image=small_image,
        large_text=large_text,
        small_text=small_text,
        buttons=buttons,
        start=start_time,
        end=current_time
    )

# searching for config file and, if exists, copy to the app directory. But if not, creates a new default config file instead.

programdir = os.path.dirname(os.path.abspath(__file__))
sourcepath = os.path.join(programdir, configfile)

if not os.path.exists(os.path.join(app_dir, configfile)):
    if os.path.exists(sourcepath):
        if os.name == 'nt': copycmd = f'copy "{sourcepath}" "{app_dir}"'
        else: copycmd = f'cp "{sourcepath}" "{app_dir}"'
        result = os.system(copycmd)
        if result != 0: 
            logging.error("Error importing an existing config.cfg")
            print("Error while importing a config file. Maybe you don't have privileges \non accessing either the directory the script located in or the Application Data folder")
        else: logging.info(f"Found config.cfg and imported to {app_dir}")
    else:
        logging.info("No config file exists. Creating a new one instead...")
        print("No config file in this system or nothing to import. \nTo import, place a preconfigured config.cfg file in the \ndirectory your script is located in and restart the script.")
        print('Creating a new default config file instead...\nWhat is your bot\'s Client ID?\n(you must take it in Discord Developer Portal)')
        newclientid = str(input('> '))
        try:
            with open(os.path.join(app_dir, configfile), "w") as f:
                f.write('{\n"client_id": "', newclientid, '",\n"state": "Example state",\n"details": "Example details",\n"large_image": "examplelarge",\n"small_image": "examplesmall",\n"large_text": "example large text",\n"small_text": "example small text",\n"buttons": [\n{"label": "Test link", "url": "https://google.com"}\n]\n}')
        except Exception as e: logging.error(f"Error creating a new default config: {e}")
else: logging.info(f'Found config.cfg in {app_dir}')

def load_config():
    with open(os.path.join(app_dir, configfile), "r") as file: configData = json.load(file)
    return configData

config = load_config()

# Data for RPC
client_id = config["client_id"]
state = config["state"]
details = config["details"]
large_image = config["large_image"]
small_image = config["small_image"]
large_text = config["large_text"]
small_text = config["small_text"]
buttons = config["buttons"]

def normalWork():
    # Initialize RPC and start timer
    RPC = start_rpc(client_id)

    # Update status
    update_rpc(RPC, state, details, large_image, small_image, large_text, small_text, buttons, start_time)

    # Keep the application running
    while True: time.sleep(15)  # You can set a different status update interval

start_time = int(time.time())

while True:
    try: normalWork()
    except Exception as e:
        logging.error(f'An error occurred: {e}')
        time.sleep(15)
