from pathlib import Path


def upath(path):
    if isinstance(path, str) and path.startswith("~"):
        path = str(Path.home()) + path[1:]
    return path


def get_data_type(path):
    assert isinstance(path, str)
    return path.split(".")[-1].lower().replace("yml", "yaml")
