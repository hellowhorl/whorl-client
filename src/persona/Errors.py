# from rich.console import Console
# from rich.markdown import Markdown

class NotHereError(Exception):
    """A class to alert the user that there is an Error.
    
    This class shows that there is an Error and throws
    it using the *args and *kwargs.
    
    Attributes:
        args (??): ??
        kwargs (??): ??
    """
    
    def __init__(self, *args, **kwargs):
        # console = Console()
        print(*args, **kwargs)

class NotAnEgo(Exception):
    """A class to define if there is no active Ego.
    
    This class passes if there is no Ego.
    """

    pass
