from pyfairsim.utils.load_settings import create_settings_file
from pyfairsim.utils.argparse import parse_args_create_settings_file

if __name__ == "__main__":
    args = parse_args_create_settings_file()
    filename = (
        args.filename if args.filename.endswith(".json") else (args.filename + ".json")
    )
    create_settings_file(filename)
