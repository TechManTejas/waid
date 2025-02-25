import subprocess

def notify(message):
    subprocess.run(["notify-send", "WAID Service", message])