import os
import json
import getpass
import requests

from dotenv import load_dotenv

load_dotenv()

def get():
    """Get current user's presence record from API.
    
    Returns:
        dict: API response containing user presence data
        
    Raises:
        requests.exceptions.RequestException: If API request fails
    """
    response = requests.get(
        f"{os.getenv('API_URL')}:{os.getenv('API_PORT')}/v1/omnipresence",
        params = {
            "charname": os.getenv('GITHUB_USER') or getpass.getuser()
        }
    )
    return response.json()

def post():
    """Create new presence record for current user.
    
    Returns:
        bool: True if record created successfully, False otherwise
        
    Raises:
        requests.exceptions.RequestException: If API request fails
    """
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

    Args:
        data (dict): Record data containing pk and charname
    
    Returns:
        bool: True if update successful, False otherwise
        
    Raises:
        requests.exceptions.RequestException: If API request fails
        KeyError: If required data fields missing
    """
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
    
    Returns:
        None
        
    Raises:
        requests.exceptions.RequestException: If API requests fail
    """
    data = get()
    if len(data) == 1:
        patch(data[0])
    if len(data) == 0:
        post()
