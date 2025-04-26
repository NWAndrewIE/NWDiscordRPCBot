# NWDiscordRPCBot
 
 ## Overview
 **Naru White's Discord Rich Presence status bot**

This bot shows the Rich Presence for Naru White in Discord.  
It contains the links to his Carrd (all his social network links located there). Also, the bot shows his pic in the left of the status text (you must have it ready).

---
## Requirements
- OS: MS Windows, macOS (Intel and Apple Silicon) or GNU/Linux  
(=> the architecture is x86_64 or ARM)
- Python 3.10 or upper version
- Discord Client (not browser version) opened on this PC
- Internet Connection

--- 
## Installation

1. Download the code. You can use these commands in Terminal of your OS:   
 ```git clone https://github.com/NWAndrewIE/NWDiscordRPCBot```  
 ```cd NWDiscordRPCBot```
or download it from a repository page (by ZIP).

3. Install the depencities by this command:  
 ```pip3 install -r requirements.txt```

4. Create and setup the bot in the [Discord Developer Portal](https://discord.com/developers/applications):
* Click **New Application**
* Type your future bot's name (it will be showed in the status in the first string) and mark the "Agreement" square. Click **Create**
* When in the bot's settings menu, go to **OAuth2** (on the left side) and copy the Client ID (not Client secret!). Paste in the **client_id** string in your **nw_richpresence.py**
* Click **Rich Presence** (on the left side). Assets page will be opened by default. Upload the images according to mine and Discord's requirements (mine is only square-only). If you have different names, you must rename images as you want and copy-paste the files names (without extensions) from Discord Dev interface to the code (cAsE-sEnSiTiVe) to **large_image** and **small_image**   
Example: you have **portrait** and **emote** images. You should edit the code as in the example below:
```
large_image = "portrait"
small_image = "emote"
```

4. Run the code by:  
 ```python3 nw_richpresence.py```

---
## Usage
Running the code by the method I described above means that the bot will work unless you stop it with Ctrl(Cmd)+C or Ctrl+Z (on GNU/Linux). To prevent this, you should use a "shadow run" of this code. It can be made depending on your OS:

### For MS Windows:     
To run: ```pythonw nw_richpresence.py```  
To kill: use **Taskmgr** app or **taskkill** command: ```taskkill /f /im pythonw.exe```  
If **pythonw.exe** is absent in the processes, try **taskkill** with either **python.exe** or **python3.exe**

### For macOS or GNU/Linux:  
To run: ```nohup python3 nw_richpresence.py ;```  
To kill: use the **System Monitor** app or **pkill** command: `pkill python3` (you can replace `python3` with another Python executables you executed this code if you have several versions of Python installed on your PC)

---
## Customizing the bot (visual)
The editing of the Rich Presence (under "RPC data" in the code) text is allowed for your personal tasks.
```
client_id = "Client_ID"
state = "State"
details = "Details"
large_image = "large_pic"
small_image = "small_pic"
large_text = "Large Alt"
small_text = "Small Alt"
buttons = [
    {"label": "Text", "url": "https://website.com"},
    {"label": "Text", "url": "https://website.com"}
]
```
Where:  
- **client_id** is the Client ID you should paste from the bot's Settings page (read *Installation*, par.3)
- **state** is the third line of the status
- **details** is the second line of the status
- **large_image** is located on the left side of the status lines (read *Installation*, par.3)
- **small_image** is located on the right-bottom corner of the **large_image** (read *Installation*, par.3)
- **large_text** appears when you move the cursor to the **large_image**
- **small_text** appears when you move the cursor to the **small_image**
- **buttons** are set up with next formula:  
` {"label": "Text", "url": "https://website.com"}`  
where **Text** (in the "label") is the text which is showed on the button and **website.com** is the website which the button directs to on click. You can make some buttons by just dividing the button constructions with comma

---
## Conclusion & Copyrights
I hope you like this experience :3  

Copyright © 2021, 2025 Andrew B. Naru White is a trademark of Andrew B. and Hywello Studios, LLC. All rights reserved.
