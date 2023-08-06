"""Package / module functions."""
import importlib.resources
from importlib.resources.abc import Traversable
import os
from pathlib import Path

def copy(module: str, dst: Path, pth: Path=None):
    """Given a module in the form: 'module.sub_module', copy all items at the
    pth to the destination, dst. If no path given, the module from the root
    level is copied.
    """
    def copy_aux(current_level: Traversable, current_path: Path):
        new_path = os.path.join(current_path, current_level.name)
        if current_level.is_dir():
            os.mkdir(new_path)
            for item in current_level.iterdir():
                copy_aux(item, new_path)
        else:
            with open(new_path, "wb") as new_file:
                new_file.write(current_level.read_bytes())
    start = importlib.resources.files(module)
    if pth:
        for_split = pth.split(os.path.sep)
        for level in for_split:
            start = start.joinpath(level)
    copy_aux(start, dst)
