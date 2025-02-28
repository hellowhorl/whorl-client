import os
import sys
import getpass
import requests
import json

from rich.console import Console
from rich.markdown import Markdown
from dotenv import load_dotenv
from request import Request
import requests


# from process_request import process_request

load_dotenv()

# Define api_url and port variables
# api_url = os.getenv("API_URL")
# api_port = os.getenv("API_PORT")

# url = f"{api_url}:{api_port}/v1/omnipresence"

# post_request = request.Request('POST', url, {})

# # Define api_url and port variables
# api_url = os.getenv("API_URL")
# api_port = os.getenv("API_PORT")


class Who:
    """A class to display active users in the current working directory.

    This class queries the omnipresence API to get a list of users active in the
    current directory and displays them in a formatted list.

    :ivar cwd: Current working directory path
    :type cwd: str
    :ivar user: Current username from GITHUB_USER env var or system username
    :type user: str
    """

    def __init__(self):
        """Initialize Who instance with current directory and user info.

        Gets current directory path and username, then retrieves and displays
        the list of active users.

        :return: None
        :rtype: None
        """
        self.cwd = os.getcwd()
        self.user = os.getenv("GITHUB_USER") or getpass.getuser()
        user_list = self.__get_user_list()
        self.__display_user_list(user_list)

    def __get_user_list(self):
        """Query the omnipresence API for active users in current directory.

        Makes a POST request to the API endpoint with the current directory path
        to get list of active users.

        :return: List of user records from API response JSON
        :rtype: list
        :raises requests.exceptions.RequestException: If the API request fails
        """
        actives = Request(
            method="POST",
            url=f"{os.getenv('API_URL')}:{os.getenv('API_PORT')}/v1/omnipresence/local/",
            data={"cwd": self.cwd},
        )()
        return actives.json()

    def __display_user_list(self, user_list: list = []) -> None:
        """Display formatted list of active users in the current directory.

        Formats and prints a markdown-style message showing active users
        in the current working directory. Uses Rich console for styled output.

        :param user_list: List of user records containing 'charname' keys
        :type user_list: list, optional
        :return: None
        :rtype: None

        **Example**::

            With users:
                > Users active in **/path/to/dir**: `🧙 user1`, `🧙 user2`

            Without users:
                > It appears that you are alone...
        """

        # authenticate
        Request(
            method="POST",
            url=f"{os.getenv('API_URL')}:{os.getenv('API_PORT')}/v1/omnipresence",
            headers={},
        )

        console = Console()
        if len(user_list) > 0:
            # print("user list: ",user_list)
            users_fmt = [f"`🧙 {user['charname']}`" for user in user_list]
            markdown = f"> Users active in **{os.getcwd()}**: {', '.join(users_fmt)}"
            console.print(Markdown(markdown))
            return
        console.print(Markdown(">  It appears that you are alone..."))


def cmd():
    """Command-line entry point for Who functionality.

    Creates an instance of Who class which automatically queries and displays
    active users in current directory.

    :return: None
    :rtype: None

    **Example**::

        $ python -m omnipresence.who
        > Users active in **/current/dir**: `🧙 user1`
    """

    # authenticate
    Request(
        method="POST",
        url=f"{os.getenv('API_URL')}:{os.getenv('API_PORT')}/v1/omnipresence",
        headers={},
    )

    Who()
