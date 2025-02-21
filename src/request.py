"""Processes and sends the GitHub Token for authentication in the server."""

import getpass
import os
import requests
from dotenv import load_dotenv, set_key
import sys
from typing import Dict

load_dotenv()

class Request:
    """Defining a request class which uses different methods to return different parameters to the server."""

    def __init__(
        self, method: str, url: str, files={}, data: Dict = {}, headers: Dict = {}
    ):
        """Initialize RequestProcessor with the incoming request."""
        self.method = method
        self.url = url
        self.data = data
        self.headers = headers
        self.files = files
        self.__create_auth_header()

    def __call__(self) -> requests.Response:
        response: requests.Response = getattr(
            self, f"_Request__{self.method.lower()}"
        )()
        # load in the login field from the env file
        dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
        load_dotenv(dotenv_path)
        try:
            response.raise_for_status()
            # set the login env variable to true
            self.__update_env_variable("LOGIN", "true")
            return response
        except requests.HTTPError as e:
            if response.status_code == 403:
                self.__update_env_variable("LOGIN", "false")
            print(f"Something went wrong: {e}")
            sys.exit(1)

    def __create_auth_header(self):
        token = os.getenv("GITHUB_TOKEN")
        user = os.getenv("GITHUB_USER") or getpass.getuser()
        if not token:
            raise ValueError("GitHub token not found in environment variables")
        # Get GitHub username and add authentication headers
        self.headers["Authorization"] = f"token {token}"
        self.headers["user"] = user

    def __get(self) -> requests.Response:
        response = requests.get(
            url=self.url, files=self.files, params=self.data, headers=self.headers
        )
        return response

    def __post(self) -> requests.Response:
        response = requests.post(
            self.url, files=self.files, data=self.data, headers=self.headers
        )
        return response

    def __patch(self) -> requests.Response:
        response = requests.patch(
            self.url, files=self.files, data=self.data, headers=self.headers, json={}
        )
        return response

    def __delete(self) -> requests.Response:
        response = requests.delete(
            self.url, files=self.files, params=self.data, headers=self.headers
        )
        return response

    def __update(self) -> requests.Response:
        response = requests.put(
            self.url, files=self.files, params=self.data, headers=self.headers
        )
        return response

    def __update_env_variable(self, key: str, value: str):
        """Update the environment variable in the .env file."""
        dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
        set_key(dotenv_path, key, value)
