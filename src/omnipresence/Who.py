import os
import sys
import requests

from rich.console import Console
from rich.markdown import Markdown

from dotenv import load_dotenv

load_dotenv()

class Who:

    def __init__(self):
        self.cwd = os.getcwd()
        self.user = os.getenv('GITHUB_USER')
        user_list = self.__get_user_list()
        self.__display_user_list(user_list)

    def __get_user_list(self):
        actives = requests.post(
            f"{os.getenv('API_URL')}:{os.getenv('API_PORT')}/v1/omnipresence/local/",
            data = {
                "cwd": self.cwd
            }
        )
        return actives.json()

    def __display_user_list(self, user_list: list = []) -> None:
        console = Console()
        if len(user_list) > 0:
            users_fmt = [f"`🧙 {user['charname']}`" for user in user_list]
            markdown = f"> Users active in **{os.getcwd()}**: {', '.join(users_fmt)}"
            console.print(Markdown(markdown))
            return
        console.print(Markdown(">  It appears that you are alone..."))

def cmd():
    Who()
