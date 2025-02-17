"""Processes and sends the GitHub Token for authentication in the server."""

import os
import requests
from dotenv import load_dotenv
import sys
from typing import Dict

load_dotenv()

class Request:
    """Defining a request class which uses different methods to return different parameters to the server."""

    def __init__(self, method: str, url: str, headers: Dict={}):
        """Initialize RequestProcessor with the incoming request."""
        self.method = method
        self.url = url
        self.headers = headers
        if self.__create_auth_header():
            getattr(self, f"_Request__{method.lower()}")(url, headers)

    def __create_auth_header(self):
        token = os.getenv('GITHUB_TOKEN')
        if not token:
            raise ValueError("GitHub token not found in environment variables")
        # Get GitHub username and add authentication headers
        headers = {
            'Authorization': f"token {token}",
        }
        response = requests.get('https://api.github.com/user', headers=headers)
        try:
            response.raise_for_status()
            return True
        except:
            sys.exit(1) # exit if the token is not valid

    def __get(self) -> Dict:
        response = requests.get(self.url, headers=self.headers)
        return response.json()

    def __post(self) -> Dict:
        # TODO: for post this needs to be json data
        response = requests.post(self.url, headers=self.headers)
        return response.json()

    def __patch(self) -> Dict:
        response = requests.patch(self.url, headers=self.headers, json={})
        return response.json()

    def __delete(self) -> Dict:
        response = requests.delete(self.url, headers=self.headers)
        return response.json()

    def __update(self) -> Dict:
        response = requests.put(self.url, headers=self.headers)
        return response.json()

    def climate_info(self) -> Dict:
        return self.__get()
