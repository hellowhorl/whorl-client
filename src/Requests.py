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

    def __get(self) -> Dict:
        response = requests.get(self.url, self.headers)
        return response

    def __post(self) -> Dict:
        # TODO: for post this needs to be json data
        response = requests.post(self.url, self.headers)
        return response

    # def __patch(self) -> Dict:
    #     response = requests.patch(self.url, self.headers, json=data)
    #     return response
    
    # def __delete(self) -> Dict:
    #     return response

    # def __update(self) -> Dict:
    #     return response

    def call_method(self):

        token = os.getenv('GITHUB_TOKEN')
        if not token:
            raise ValueError("GitHub token not found in environment variables")

        # Get GitHub username and add authentication headers
        self.headers = {
            'Authorization': f"token {token}",
        }

        response = requests.get('https://api.github.com/user', headers=headers)
        response.raise_for_status()

        # add the username to headers
        username = response.json()['login']
        self.headers['User'] = username

        # print("here")
        # Call the GET method
        if self.method == 'GET':
            return self.__get(url, headers)

        # Call the POST method
        elif self.method == 'POST':
            return self.__post(url, headers)

        # Call the PATCH method
        elif self.method == 'PATCH':
            return self.__patch(url, headers)

        # Call the DELETE method
        elif self.method == 'DELETE':
            return self.__delete(url, headers)

        # Call the UPDATE method
        elif self.method == 'UPDATE':
            return self.__update(url, headers)

        # display nothing if a 403 is returned
        elif response.status_code == 403:
            sys.exit(1) # exit the program and return nothing if the response is 403

        else:
            return "Invalid method name"