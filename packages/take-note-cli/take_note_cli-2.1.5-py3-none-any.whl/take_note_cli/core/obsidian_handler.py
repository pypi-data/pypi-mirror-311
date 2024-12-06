from subprocess import call
import sys

import urllib


def create_handler(config, note_path):
    if sys.platform == "linux":
        app = "xdg-open"
    elif sys.platform == "darwin":
        app = "open"
    else:
        app = "start"

    command = f"obsidian://open?path={note_path}"
    url = urllib.parse.quote(command, safe="/:?=&", encoding=None, errors=None)
    args = [app, url]

    if config["verbose"]:
        print(f"Opening file with args: {args}")

    return lambda: call(args)
