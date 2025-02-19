import os
import json
import getpass
import requests
from request import Request

from dotenv import load_dotenv

load_dotenv()

def get():
    """Get current user's presence record from API.
    
    Makes a GET request to the omnipresence API endpoint to retrieve the 
    presence data for the currently authenticated user.

    :return: API response containing user presence data
    :rtype: dict
    :raises requests.exceptions.RequestException: If the API request fails
    """
    # authenticate
    client = Request(method='GET', url=f"{os.getenv('API_URL')}:{os.getenv('API_PORT')}/v1/omnipresence", headers={}) # Create an instance of the Request class

    response = requests.get(
        f"{os.getenv('API_URL')}:{os.getenv('API_PORT')}/v1/omnipresence",
        params = {
            "charname": os.getenv('GITHUB_USER') or getpass.getuser()
        }
    )
    return response.json()


def post():
    """Create new presence record for current user.
    
    Posts a new presence record to the omnipresence API for the currently 
    authenticated user with their current status.

    :param None: No parameters required
    :return: Success status of the operation
    :rtype: bool
    :raises requests.exceptions.RequestException: If the API request fails
    """

    # authenticate
    client = Request(method='POST', url=f"{os.getenv('API_URL')}:{os.getenv('API_PORT')}/v1/omnipresence", headers={}) # Create an instance of the Request class

    response = requests.post(
        f"{os.getenv('API_URL')}:{os.getenv('API_PORT')}/v1/omnipresence/",
        data = {
            "username": os.getenv('GITHUB_USER') or getpass.getuser(),
            "charname": os.getenv('GITHUB_USER') or getpass.getuser(),
            "working_dir": os.getcwd()
        }
    )
    if response.status_code == 201:
        return True
    return False

def patch(data: dict = {}):
    """Update existing presence record.
    
    Updates an existing presence record in the omnipresence API with new data
    including the current working directory.

    :param data: Record data containing pk and charname
    :type data: dict
    :return: True if update successful, False otherwise
    :rtype: bool
    :raises requests.exceptions.RequestException: If API request fails
    :raises KeyError: If required data fields missing
    """

    # authenticate
    client = Request(method='PATCH', url=f"{os.getenv('API_URL')}:{os.getenv('API_PORT')}/v1/omnipresence", headers={}) # Create an instance of the Request class

    response = requests.patch(
        f"{os.getenv('API_URL')}:{os.getenv('API_PORT')}/v1/omnipresence/update/{data['pk']}/",
        data = {
            "charname": data['charname'],
            "working_dir": os.getcwd(),
            "partial": True
        }
    )
    if response.status_code == 200:
        return True
    return False

def report():
    """Update existing record or create new one.
    
    Gets current presence data and either updates existing record
    or creates new record if none exists.

    :return: None
    :rtype: None
    :raises requests.exceptions.RequestException: If API requests fail
    """

    # authenticate
    client = Request(method='GET', url=f"{os.getenv('API_URL')}:{os.getenv('API_PORT')}/v1/omnipresence", headers={}) # Create an instance of the Request class

    data = get()
    if len(data) == 1:
        patch(data[0])
    if len(data) == 0:
        post()
