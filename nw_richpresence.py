import os
import logging
from pypresence import Presence # type: ignore
import time
import datetime

# Determine the log directory based on the operating system
if os.name == 'nt':  # Windows
    log_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'nw_rpc', 'logs')
else:  # Linux and other Unix-like systems
    log_dir = os.path.expanduser('~/.local/share/nw_rpc/logs')

# Create the log directory if it does not exist
os.makedirs(log_dir, exist_ok=True)

# Configure logging
log_file = os.path.join(log_dir, f'nw_discordrpc_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log')
logging.basicConfig(filename=log_file, level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')

# Function to initialize RPC
def start_rpc(client_id):
    try:
        RPC = Presence(client_id)
        RPC.connect()
        logging.info('Successfully connected to Discord RPC.')
        return RPC
    except Exception as e:
        logging.error(f'Failed to connect to Discord RPC: {e}')
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

# Data for RPC
client_id = "Client_ID"
state = "Working and lurking :3"
details = "Logged in as naruwhite"
large_image = "nw_pfp7"
small_image = "nw_valentine"
large_text = "Naru White"
small_text = "Naru White loves you <3"
buttons = [
    {"label": "Naru's All Links", "url": "https://naruwhite.carrd.co"}
]

def normalWork():
    # Initialize RPC and start timer
    RPC = start_rpc(client_id)

    # Update status
    update_rpc(RPC, state, details, large_image, small_image, large_text, small_text, buttons, start_time)

    # Keep the application running
    while True:
        time.sleep(15)  # You can set a different status update interval

start_time = int(time.time())

while True:
    try:
        normalWork()
    except Exception as e:
        logging.error(f'An error occurred: {e}')
        time.sleep(15)
