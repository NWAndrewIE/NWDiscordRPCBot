# Autostart Guide

This document explains how to make **NWDiscordRPCBot** start automatically after the operating system boots and the user signs in.

Because this project talks to the **desktop Discord client** through Discord Rich Presence, it should be started as a **per-user background app**, not as a system service that runs before login.

## Before you enable autostart

1. Install Python 3.10 or newer.
2. Clone or unpack this repository into a permanent location.
3. Install dependencies:

```bash
pip3 install -r requirements.txt
```

4. Run the setup script once:

```bash
python3 setup_master.py
```

This creates or imports `config.cfg` into the per-user application data directory used by the program:

- **Windows:** `%LOCALAPPDATA%\NW RPC\config.cfg`
- **macOS:** `~/Library/Application Support/NW RPC/config.cfg`
- **Linux:** `~/.local/share/NW RPC/config.cfg`

5. Test the bot manually before enabling autostart:

```bash
python3 nw_richpresence.py
```

If it works, continue with one of the operating-system-specific methods below.

## General recommendation

There are two practical ways to autostart this project:

1. Start the Python script directly.
2. Build a standalone executable first, then autostart that executable.

The first method is simpler. The second is useful if you want a cleaner launcher and do not want your startup item to call `python` directly.

If you want to build a standalone executable, `PyInstaller` is a common option:

```bash
pip3 install pyinstaller
```

Typical build commands:

- **Windows:**
```powershell
pyinstaller --onefile --noconsole nw_richpresence.py
```

- **macOS / Linux:**
```bash
pyinstaller --onefile nw_richpresence.py
```

This usually creates an executable in the `dist/` directory. You can then register that executable for autostart instead of the Python script.

## Windows (up to Windows 11)

For Windows, the most straightforward method is to place a launcher in the user's **Startup** folder.

### Recommended method: shortcut in the Startup folder

1. Keep the project in a fixed directory, for example:

```text
C:\Users\YourName\NWDiscordRPCBot
```

2. Run setup once:

```powershell
py setup_master.py
```

3. Decide what will be started on login:

- the script with `pythonw.exe`
- or a built executable from `dist\`

`pythonw.exe` is preferred over `python.exe` because it runs without opening a console window.

4. Open the Startup folder:

```text
Win + R -> shell:startup
```

5. Create a shortcut there.

If you are starting the Python script directly, set the shortcut like this:

- **Target:**
```text
C:\Path\To\Python\pythonw.exe C:\Users\YourName\NWDiscordRPCBot\nw_richpresence.py
```

- **Start in:**
```text
C:\Users\YourName\NWDiscordRPCBot
```

If you built an executable with PyInstaller, use:

- **Target:**
```text
C:\Users\YourName\NWDiscordRPCBot\dist\nw_richpresence.exe
```

- **Start in:**
```text
C:\Users\YourName\NWDiscordRPCBot\dist
```

6. Sign out and sign back in to test it.

### Optional method: Registry `Run` entry

Instead of the Startup folder, you can create a value under:

```text
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
```

Example command value:

```text
"C:\Path\To\Python\pythonw.exe" "C:\Users\YourName\NWDiscordRPCBot\nw_richpresence.py"
```

This works, but the Startup-folder shortcut is usually easier to inspect and remove.

### Notes for Windows

- Make sure Discord itself also starts on login.
- Do not install this as a Windows service. Rich Presence needs the logged-in desktop session.
- Logs are written under `%LOCALAPPDATA%\NW RPC\logs`.

## macOS (up to Tahoe)

On modern macOS, the correct autostart method for a background user process is a **LaunchAgent** in the user's home directory.

### Recommended method: LaunchAgent

1. Keep the project in a fixed path, for example:

```text
/Users/yourname/NWDiscordRPCBot
```

2. Run setup once:

```bash
python3 setup_master.py
```

3. Create this directory if it does not already exist:

```bash
mkdir -p ~/Library/LaunchAgents
```

4. Create a plist file such as:

```text
~/Library/LaunchAgents/com.naruwhite.nwdiscordrpcbot.plist
```

5. Put the following content into that plist.

### Start the Python script directly

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.naruwhite.nwdiscordrpcbot</string>

    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/yourname/NWDiscordRPCBot/nw_richpresence.py</string>
    </array>

    <key>WorkingDirectory</key>
    <string>/Users/yourname/NWDiscordRPCBot</string>

    <key>RunAtLoad</key>
    <true/>

    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

If you built a standalone executable, replace `ProgramArguments` with the executable path:

```xml
<key>ProgramArguments</key>
<array>
    <string>/Users/yourname/NWDiscordRPCBot/dist/nw_richpresence</string>
</array>
```

6. Load and enable it:

```bash
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.naruwhite.nwdiscordrpcbot.plist
```

If it was already loaded and you changed the file:

```bash
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.naruwhite.nwdiscordrpcbot.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.naruwhite.nwdiscordrpcbot.plist
```

7. Log out and back in, or start it immediately with:

```bash
launchctl kickstart -k gui/$(id -u)/com.naruwhite.nwdiscordrpcbot
```

### Notes for macOS

- Discord must also launch in the same user session.
- A **LaunchAgent** is correct here; a **LaunchDaemon** is not.
- The program stores config and logs in `~/Library/Application Support/NW RPC/`.

## Linux (systemd-based distributions)

For Linux, use a **user service** under `systemd --user`. That makes the program start when the user session starts.

### Recommended method: systemd user service

1. Keep the project in a fixed directory, for example:

```text
/home/yourname/NWDiscordRPCBot
```

2. Run setup once:

```bash
python3 setup_master.py
```

3. Create the user service directory:

```bash
mkdir -p ~/.config/systemd/user
```

4. Create this file:

```text
~/.config/systemd/user/nwdiscordrpcbot.service
```

5. Put the following content into it.

### Start the Python script directly

```ini
[Unit]
Description=NW Discord RPC Bot
After=default.target

[Service]
Type=simple
WorkingDirectory=/home/yourname/NWDiscordRPCBot
ExecStart=/usr/bin/python3 /home/yourname/NWDiscordRPCBot/nw_richpresence.py
Restart=always
RestartSec=15

[Install]
WantedBy=default.target
```

If you built a standalone executable, replace `ExecStart` with:

```ini
ExecStart=/home/yourname/NWDiscordRPCBot/dist/nw_richpresence
```

6. Reload the user manager and enable the service:

```bash
systemctl --user daemon-reload
systemctl --user enable --now nwdiscordrpcbot.service
```

7. Check status:

```bash
systemctl --user status nwdiscordrpcbot.service
```

8. After a reboot, the service should start automatically when that user logs in.

### Notes for Linux

- This should be a **user** service, not a system-wide service.
- Discord must run in the same graphical user session.
- Config and logs are stored in `~/.local/share/NW RPC/`.
- To inspect logs:

```bash
journalctl --user -u nwdiscordrpcbot.service
```

## Which method should you choose?

- Use the **Python script directly** if Python is already installed and managed on the machine.
- Use a **PyInstaller executable** if you want a more self-contained startup target.
- Use **per-user autostart only**. This program depends on a logged-in desktop user session and the Discord desktop app.

## Troubleshooting

If the bot does not appear in Discord after login:

1. Confirm that the desktop Discord client is open.
2. Run `setup_master.py` again and verify that `config.cfg` exists in the user data directory for your OS.
3. Start `nw_richpresence.py` manually from a terminal and check for errors.
4. Check the log directory used by your platform:
   - Windows: `%LOCALAPPDATA%\NW RPC\logs`
   - macOS: `~/Library/Application Support/NW RPC/logs`
   - Linux: `~/.local/share/NW RPC/logs`
5. Verify that your startup item points to the correct Python interpreter or executable path.

## Summary

The safe pattern on all three operating systems is the same:

- prepare `config.cfg` with `setup_master.py`
- verify the script manually
- register it as a **user-session autostart item**
- optionally replace the Python command with a built standalone executable

That gives you automatic startup after boot, once the user logs in and Discord is available.
