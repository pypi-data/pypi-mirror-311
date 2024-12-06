from pathlib import Path
from subprocess import call


def create_handler(config, file_path:Path):
    args = [config["editor"], file_path]

    if config["verbose"]:
        print(f"Opening file with args: {args}")

    return lambda: call(args)
