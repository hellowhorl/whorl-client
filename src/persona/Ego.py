import os
import sys
import getpass
import requests

from rich.console import Console
from rich.markdown import Markdown
from dotenv import load_dotenv

load_dotenv()

class Ego:

    def __init__(self, type: str = "", name: str = "", mode="talk"):
        self.addressee = os.getenv('GITHUB_USER') or getpass.getuser()
        self.archetype = type
        self.named = name or type
        self.chatterbox = False
        is_registered = requests.get(
            f"{os.getenv('API_URL')}:{os.getenv('API_PORT')}/v1/persona/search/{type}"
        )
        if is_registered.status_code == 200 and mode == "talk":
            self.behave()
            sys.exit(0)

    def __str__(self):
        reference = self.named or self.archetype
        return f"""You look at {reference}. {reference} looks back. It's awkward."""

    def __send_message(self, console, msg: str = ""):
        content = requests.post(
            f"{os.getenv('API_URL')}:{os.getenv('API_PORT')}/v1/persona/generate/{self.archetype}",
            data={
                "charname": os.getenv('GITHUB_USER') or getpass.getuser(),
                "message": msg
            },
            stream=True
        )

        response_text = content.json()["response"].strip()
        attachments = content.json()["attachments"]
        # TODO: Decide what to do with attachments?
        console.print(Markdown(response_text))

        """ DEPRECATED
        # Check if the response contains a Python code snippet
        if "```python" in response_text and "```" in response_text:
            self.handle_python_code(response_text)
        """

        if msg.lower() == "goodbye":
            sys.exit(0)

    """ DEPRECATED
    def handle_python_code(self, response_text: str):
        start = response_text.find("```python") + len("```python")
        end = response_text.find("```", start)
        python_code = response_text[start:end].strip()
        filename_end = response_text.find(".py") + 3
        if filename_end != -1:
            filename_start = filename_end
            while filename_start > 0 and response_text[filename_start - 1] != " ":
                filename_start -= 1
            filename = response_text[filename_start:filename_end].strip()
        else:
            None

        if filename:
            with open(filename, "w") as file:
                file.write(python_code)
            full_path = os.path.abspath(filename)
            print(f"Your item is here: {full_path}")
        else:
            print("Filename not found in the response.")
    """

    def behave(self):
        console = Console()
        if self.chatterbox:
            self.__send_message(console, "")
        while True:
            msg = input("> ")
            self.__send_message(console, msg)
