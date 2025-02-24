"""Processes and sends the GitHub Token for authentication in the server."""

import getpass
import os
import requests
import sys
from typing import Dict


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
        try:
            response.raise_for_status()
            os.environ['LOGIN'] = 'True'
            return response
        except requests.HTTPError as e:
            if response.status_code == 403:
                os.environ['LOGIN'] = 'False'
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
        """Update the environment variable"""
        os.environ[key] = value
