from rich.console import Console
from rich.markdown import Markdown

class NotHereError(Exception):

    def __init__(self, *args, **kwargs):
        console = Console()
        print(*args, **kwargs)

class NotAnEgo(Exception):

    pass
