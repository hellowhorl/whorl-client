"""Processes and sends the GitHub Token for authentication in the server."""

import os
import requests
from dotenv import load_dotenv
import sys
from typing import Dict

load_dotenv()

def process_request(request):
    """
    Process the incoming request by adding authentication headers and sending it to the server.

    :param request: The incoming request object
    :type request: dict
    :return: The server's response
    :rtype: requests.Response
    """
    # Get GitHub token
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        raise ValueError("GitHub token not found in environment variables")

    # Get GitHub username and add authentication headers
    headers = {
        'Authorization': f"token {token}",
    }
    response = requests.get('https://api.github.com/user', headers=headers)
    response.raise_for_status()
    username = response.json()['login']
    headers['User'] = username

    method = request.get('method', 'GET').upper()
    url = request.get('url')
    params = request.get('params', {})
    data = request.get('data', {})

    # modify the response based on the web method
    # if method == 'GET':
    #     response = requests.get(url, headers=headers, params=params)
    # elif method == 'POST':
    #     response = requests.post(url, headers=headers, json=data)
    # elif method == 'PATCH':
    #     response = requests.patch(url, headers=headers, json=data)
    # else:
    #     raise ValueError(f"Unsupported HTTP method: {method}")
    
    # display nothing if a 403 is returned
    # if response.status_code == 403:
    #     sys.exit(1) # exit the program and return nothing if the response is 403


    return response


class Request:
"""Defining a request class which uses different methods to return different parameters to the server."""

    def __init__(self, method: str, url: str, data: Dict);

        self.method = str
        self.url = str
        self.data = {}

    def __get(self):
        response = requests.get(url, headers=headers, params=params)
        return response

    def __post(self):
        response = requests.post(url, headers=headers, json=data)
        return response

    def __patch(self):
        response = requests.patch(url, headers=headers, json=data)
        return response
    
    def __delete(self):
        return response

    def __update(self):
        return response

    def call_method(self, method_name):
        if method == 'GET':
            return self.__get()
        elif method == 'POST':
            return self.__post()
        elif method == 'PATCH':
            return self.__patch()
        elif method == 'DELETE':
            return self.__delete()
        elif method == 'UPDATE':
            return self.__update()
        # display nothing if a 403 is returned
        elif response.status_code == 403:
            sys.exit(1) # exit the program and return nothing if the response is 403

        else:
            return "Invalid method name"