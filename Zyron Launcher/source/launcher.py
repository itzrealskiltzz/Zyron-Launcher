import os
import subprocess
import minecraft_launcher_lib

ZYRON_DIR = os.path.join(os.path.expanduser("~"), ".zyron_launcher")

def launch_zyron_offline(username="ZyronPlayer", version="26.3"):
    """Launches Minecraft using your local profile credentials."""
    os.makedirs(ZYRON_DIR, exist_ok=True)
    minecraft_launcher_lib.install.install_minecraft_version(version, ZYRON_DIR)

    options = {
        "username": username,
        "uuid": "",
        "token": ""
    }

    command = minecraft_launcher_lib.command.get_minecraft_command(version, ZYRON_DIR, options)
    subprocess.run(command)