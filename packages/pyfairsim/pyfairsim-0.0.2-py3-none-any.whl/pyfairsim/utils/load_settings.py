import json
import os

from pyfairsim.sim_algorithm.SIM_Parameters import Parameters


def load_settings(path: str) -> Parameters:
    # try to locate parameter file
    # first check if the path was explicitly given
    if path.endswith(".json"):
        with open(path, encoding="utf8") as f:
            settings = json.load(f)
        return Parameters.from_dict(settings)
    # next check for either image_name.json or parameters.json in the same directory as the image file
    else:
        if path.endswith(".tif"):
            base_file = path[:-4]
        elif path.endswith(".tiff"):
            base_file = path[:-5]
        else:
            raise ValueError(
                f"Unsupported  path: {path}, must either end with .json or .tif/.tiff"
            )
        if os.path.exists(base_file + ".json"):
            with open(path, encoding="utf8") as f:
                settings = json.load(f)
            return Parameters.from_dict(settings)

    base_path = os.path.dirname(path)  # foo/bar/image.tif -> foo/bar
    file_path = os.path.join(base_path, "parameters.json")
    if os.path.exists(file_path):
        with open(file_path, encoding="utf8") as f:
            settings = json.load(f)
        return Parameters.from_dict(settings)
    # load default settings
    default_path = os.path.dirname(os.path.dirname(__file__))
    default_path = os.path.join(default_path, "parameters.json")
    with open(default_path, encoding="utf-8") as f:
        settings = json.load(f)
    return Parameters.from_dict(settings)


def save_settings(settings: Parameters, filename: str, overwrite=False) -> None:
    if os.path.isfile(filename) and not overwrite:
        raise NotImplementedError("File already exists.")
    else:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(settings.as_dict(), f, indent=4)


def merge_dict(primary, secondary):
    for key, value in secondary.items():
        # if the key dosen't exist create it and continue with the next pair
        if key not in primary:
            primary[key] = value
        # if the value is a dict also merge them
        elif isinstance(value, dict):
            if isinstance(primary[key], dict):
                primary[key] = merge_dict(primary[key], value)
            else:
                raise ValueError(f"{value} and {primary[key]} should be both dicts.")
        # else keep the value stored in primary
    return primary


def create_settings_file(filename):
    settings = Parameters.as_descriptive_dict()
    with open(f"{filename}", "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4)
