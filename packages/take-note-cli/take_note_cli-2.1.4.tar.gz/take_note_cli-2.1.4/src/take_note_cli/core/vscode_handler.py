from subprocess import call


def create_handler(config, file_path):
    args = [config["editor"], file_path]

    if config["workspace"] is not None:
        args.append(config["notesFolder"].joinpath(config["workspace"]))

    if config["verbose"]:
        print(f"Opening file with args: {args}")
        
    return lambda: call(args)
