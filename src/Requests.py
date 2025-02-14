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
        self.method = str
        self.url = str
        self.headers = {}
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
            sys.exit(1)

    def __get(self) -> Dict:
        response = requests.get(self.url, self.headers)
        return response

    def __post(self) -> Dict:
        # TODO: for post this needs to be json data
        response = requests.post(self.url, self.headers)
        return response

    def __patch(self, url: str, headers: Dict) -> Dict:
        response = requests.patch(url, headers=headers, json=data)
        return response

    def __delete(self, url: str, headers: Dict) -> Dict:
        return response

    def __update(self, url: str, headers: Dict) -> Dict:
        return response
