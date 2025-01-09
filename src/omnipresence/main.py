import os
import json
import requests
from requests_kerberos import HTTPKerberosAuth, REQUIRED

from dotenv import load_dotenv

load_dotenv()

def get():
    response = requests.get(
        f"{os.getenv('API_URL')}:{os.getenv('API_PORT')}/v1/omnipresence",
        params = {
            "charname": os.getenv('GITHUB_USER')
        },
        auth=HTTPKerberosAuth(mutual_authentication = REQUIRED, force_preemptive = True)
    )
    print(response.content)
    return response.json()

def post():
    response = requests.post(
        f"{os.getenv('API_URL')}:{os.getenv('API_PORT')}/v1/omnipresence",
        data = {
            "username": os.getenv('GITHUB_USER'),
            "charname": os.getenv('GITHUB_USER'),
            "working_dir": os.getcwd()
        },
        auth=HTTPKerberosAuth(mutual_authentication = REQUIRED, force_preemptive = True)
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
        },
        auth=HTTPKerberosAuth(mutual_authentication = REQUIRED, force_preemptive = True)
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
