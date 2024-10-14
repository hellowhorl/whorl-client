import os
import sys
import types
import inspect

from rich.console import Console
from rich.markdown import Markdown

class Look:

    def __init__(self, filename: str = ""):
        self.filename = filename
        self.__get_info()

    def __get_info(self):
        console = Console()
        mod = types.ModuleType(self.filename)
        try:
            with open(self.filename, "r") as fh:
                source = fh.read()
            exec(source, mod.__dict__)
            cls = getattr(mod, self.filename)
            console.print(Markdown(f"> {cls(mode = 'look')}"))
        except FileNotFoundError:
            console.print(Markdown(f"> {self.filename} doesn't seem to be present at the moment..."))
        print()

def cmd():
    sys.path.append(os.path.expanduser(os.getcwd()))
    Look(sys.argv[1])
