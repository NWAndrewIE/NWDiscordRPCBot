# NW Discord Rich Presence Status
from pypresence import Presence
import time
    
# Function for RPC initialization
def start_rpc(client_id):
    RPC = Presence(client_id)
    RPC.connect()
    return RPC

# Function for RPC status updating
def update_rpc(RPC, state, details, large_image, small_image, large_text, small_text, buttons, start_time):
    current_time = int(time.time())
    elapsed_time = current_time - start_time
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

# RPC Data
client_id = "Client_ID"
state = "Working and lurking :3"
details = "Logged in as naruwhite"
large_image = "nw_pfp7"
small_image = "nw_valentine"
large_text = "Naru White"
small_text = "Naru White loves you <3"
buttons = [
    {"label": "Naru's News", "url": "https://t.me/naruwhite"},
    {"label": "Naru's All Links", "url": "https://naruwhite.carrd.co"}
]

def normalWork():
    # Init RPC and start a timer
    RPC = start_rpc(client_id)

    # Update a status
    update_rpc(RPC, state, details, large_image, small_image, large_text, small_text, buttons, start_time)

    # For continuing the working of the app
    while True:
        time.sleep(15)  # You can adjust a timer of RPC updating 

start_time = int(time.time())

while True:
    try:
        normalWork()
        pass
    except:
        time.sleep(30)
