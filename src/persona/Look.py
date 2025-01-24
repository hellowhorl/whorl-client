import os
import sys
import types
# import inspect

from rich.console import Console
from rich.markdown import Markdown

class Look:
    """A class to look at the descriptions of objects.
    
    This class gets the description of objects and returns 
    to the user what an object looks like.
    
    Attributes:
        filename (str): define a path to a file
    """

    def __init__(self, filename: str = ""):
        self.filename = filename
        self.__get_info()

    def __get_info(self):
        """Query the persona API for active users in current directory.
        
        Returns:
            None
            
        Raises:
            A string that tells the user the file doesn't exist
        """

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
    """Command-line entry point for Look functionality.
    
    Creates an instance of the Ego class which automatically access Look 
    and see if there is an object description.
    """

    sys.path.append(os.path.expanduser(os.getcwd()))
    Look(sys.argv[1])
