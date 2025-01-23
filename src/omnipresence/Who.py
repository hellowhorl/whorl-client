import os
import sys
import getpass
import requests

from rich.console import Console
from rich.markdown import Markdown
from dotenv import load_dotenv

load_dotenv()

class Who:
    """A class to display active users in the current working directory.
    
    This class queries the omnipresence API to get a list of users active in the 
    current directory and displays them in a formatted list.
    
    Attributes:
        cwd (str): Current working directory path
        user (str): Current username from GITHUB_USER env var or system username
    """

    def __init__(self):
        """Initialize Who instance with current directory and user info.
        
        Gets current directory path and username, then retrieves and displays
        the list of active users.
        """
        self.cwd = os.getcwd()
        self.user = os.getenv('GITHUB_USER') or getpass.getuser()
        user_list = self.__get_user_list()
        self.__display_user_list(user_list)

    def __get_user_list(self):
        """Query the omnipresence API for active users in current directory.
        
        Makes a POST request to the API endpoint with the current directory path
        to get list of active users.
        
        Returns:
            list: List of user records from API response JSON
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        actives = requests.post(
            f"{os.getenv('API_URL')}:{os.getenv('API_PORT')}/v1/omnipresence/local/",
            data = {
                "cwd": self.cwd
            }
        )
        return actives.json()

    def __display_user_list(self, user_list: list = []) -> None:
        """Display formatted list of active users in the current directory.
        
        Formats and prints a markdown-style message showing active users
        in the current working directory. Uses Rich console for styled output.
        
        Args:
            user_list (list, optional): List of user records containing 'charname' keys.
                Defaults to empty list.
                
        Returns:
            None
            
        Example:
            With users:
                > Users active in **/path/to/dir**: `🧙 user1`, `🧙 user2`
            
            Without users:
                > It appears that you are alone...
        """
        console = Console()
        if len(user_list) > 0:
            users_fmt = [f"`🧙 {user['charname']}`" for user in user_list]
            markdown = f"> Users active in **{os.getcwd()}**: {', '.join(users_fmt)}"
            console.print(Markdown(markdown))
            return
        console.print(Markdown(">  It appears that you are alone..."))

def cmd():
    """Command-line entry point for Who functionality.
    
    Creates an instance of Who class which automatically queries and displays
    active users in current directory.
    
    Returns:
        None
        
    Example:
        $ python -m omnipresence.who
        > Users active in **/current/dir**: `🧙 user1`
    """
    Who()
