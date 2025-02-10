"""Processes and sends {user,token} for authentication in the server."""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def process_request(request):
    """
    Process the incoming request by adding authentication headers and sending it to the server.

    :param request: The incoming request object
    :type request: dict
    :return: The server's response
    :rtype: requests.Response
    """
    # Add authentication headers
    headers = {
        'Authorization': os.getenv('GITHUB_TOKEN'),
        'User': os.getenv('GITHUB_USER')
    }

    method = request.get('method', 'GET').upper()
    url = request.get('url')
    params = request.get('params', {})
    data = request.get('data', {})

    if method == 'GET':
        response = requests.get(url, headers=headers, params=params)
    elif method == 'POST':
        response = requests.post(url, headers=headers, json=data)
    elif method == 'PATCH':
        response = requests.patch(url, headers=headers, json=data)
    else:
        raise ValueError(f"Unsupported HTTP method: {method}")

    return response
