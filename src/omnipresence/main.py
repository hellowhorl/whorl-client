import os
import json
import getpass
import requests

from dotenv import load_dotenv

load_dotenv()

def get():
    response = requests.get(
        f"{os.getenv('API_URL')}:{os.getenv('API_PORT')}/v1/omnipresence",
        params = {
            "charname": os.getenv('GITHUB_USER') or getpass.getuser()
        }
    )
    return response.json()

def post():
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
    data = get()
    if len(data) == 1:
        patch(data[0])
    if len(data) == 0:
        post()
