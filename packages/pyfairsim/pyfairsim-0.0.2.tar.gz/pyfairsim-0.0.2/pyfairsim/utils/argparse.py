import argparse


def parse_args_k_estimation() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Running the k-vector estimation on a given image file."
    )
    _register_common_arguments(parser)
    return parser.parse_args()


def parse_args_phase_estimation() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Running the phase estimation on a given image file."
    )
    _register_common_arguments(parser)
    return parser.parse_args()


def parse_args_reconstruction() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Running the sim reconstruction on a given image file."
    )
    _register_common_arguments(parser)
    return parser.parse_args()


def _register_common_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "-f",
        "--filename",
        required=True,
        dest="filename",
        type=str,
        help="Input filename",
    )
    parser.add_argument(
        "-o",
        "--out",
        required=False,
        dest="out_filename",
        type=str,
        help="Output filename if empty output is send to the console",
    )
    parser.add_argument(
        "-s",
        "--settings",
        required=False,
        dest="settings_filename",
        type=str,
        help="Settings filename if empty default settings are used",
    )
    parser.add_argument(
        "-d",
        "--debug_level",
        required=False,
        dest="level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Sets the log level",
    )


def parse_args_create_settings_file() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Running this script will create a settings file with descriptions instead of values as a template."
    )
    parser.add_argument(
        "-f", dest="filename", type=str, help="Filepath/name for the settings file."
    )
    return parser.parse_args()


def parse_args_batch_reconstruction() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a batch parameter estimation and reconstruction on all .tif/.tiff files in the selected folder and all subfolders using one settings file."
    )
    parser.add_argument(
        "-f",
        required=True,
        dest="destination",
        type=str,
        help="Destination folder to run the reconstruction on",
    )
    parser.add_argument(
        "-s",
        "--settings",
        required=False,
        dest="settings_filename",
        type=str,
        help="Settings filename if empty default settings are used",
    )
    parser.add_argument(
        "-d",
        "--debug_level",
        required=False,
        dest="level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Sets the log level",
    )
    return parser.parse_args()
