import os
import json

from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

try:
    root_dir = os.path.expanduser(
        os.getenv("FILE_SYSTEM") + os.getenv("RepositoryName")
    )
except TypeError:
    cwd = os.getcwd()
    while cwd != "/":
        path = os.path.join(cwd, ".git")
        if os.path.exists(path):
            root_dir = Path(path).parent.absolute()
        cwd = os.path.dirname(cwd)

from .Path import *


def exists(filepaths: list) -> bool:
    """Take a list of filepaths and checks if the files exist on the computer.

    :param filepaths: a list of paths for program to check if they exist
    :type filepaths: List[Paths]

    :return: returns True if path exists otherwise returns False
    :rtype: bool
    """

    for file in filepaths:
        if not os.path.exists(file):
            return False
    return True


def set_flag(flag: str, val: int = 1) -> None:
    """Creates .flags file if it doesn't already exist otherwise updates and adds current flag values

    :param flag: The name of the flag to be updated
    :type flag: str

    :param val: What value the flag should be changed to should either be a 1 if the flag is true or a 0 if false, defaults to 1
    :type val: int(Optional)
    """
    flags = {}
    if not exists([os.path.expanduser(f"{root_dir}/.flags")]):
        with open(f"{root_dir}/.flags", "w+") as fh:
            fh.write("{}")
    with open(f"{root_dir}/.flags", "r+") as fh:
        flags = json.load(fh)
    flags[flag] = val
    with open(f"{root_dir}/.flags", "w") as fh:
        json.dump(flags, fh, indent = 2)

def unset_flag(flag: str):
    flags = {}
    if not exists([os.path.expanduser(f"{root_dir}/.flags")]):
        with open(f"{root_dir}/.flags", "w+") as fh:
            fh.write("{}")
    with open(f"{root_dir}/.flags", "r+") as fh:
        flags = json.load(fh)
    try:
        del flags[flag]
    except:
        # TODO: DO BETTER
        pass
    with open(f"{root_dir}/.flags", "w") as fh:
        json.dump(flags, fh, indent = 2)

def check_flag(flag: str):
    """Checks the current value of the specified flag

    :param flag: The name of the flag to be checked
    :type flag: st

    :return: Returns the flags value or if an error occurs False
    :rtype: str | bool
    """
    flags = {}
    try:
        with open(f"{root_dir}/.flags", "r+") as fh:
            flags = json.load(fh)
        return flags[flag]
    except:
        return False
