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
    request['headers'] = {
        'Authorization': f"Bearer {os.getenv('API_TOKEN')}",
        'User': os.getenv('GITHUB_USER')
    }

    # Send the request to the server
    response = requests.post(
        f"{os.getenv('API_URL')}:{os.getenv('API_PORT')}/v1/endpoint",
        json=request
    )

    return response
