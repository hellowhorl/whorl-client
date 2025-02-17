"""Processes and sends the GitHub Token for authentication in the server."""

import getpass
import os
import requests
from dotenv import load_dotenv
import sys
from typing import Dict

load_dotenv()


class Request:
    """Defining a request class which uses different methods to return different parameters to the server."""

    def __init__(self, method: str, url: str, data: Dict = {}, headers: Dict = {}):
        """Initialize RequestProcessor with the incoming request."""
        self.method = method
        self.url = url
        self.data = data
        self.headers = headers
        self.__create_auth_header()

    def __call__(self):
        response: requests.Response = getattr(
            self, f"_Request__{self.method.lower()}"
        )()
        try:
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as e:
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
        response = requests.get(url=self.url, params=self.data, headers=self.headers)
        return response

    def __post(self) -> requests.Response:
        # TODO: for post this needs to be json data
        response = requests.post(self.url, headers=self.headers)
        return response.json()

    def __patch(self) -> requests.Response:
        response = requests.patch(self.url, headers=self.headers, json={})
        return response.json()

    def __delete(self) -> requests.Response:
        response = requests.delete(self.url, headers=self.headers)
        return response.json()

    def __update(self) -> requests.Response:
        response = requests.put(self.url, headers=self.headers)
        return response.json()
