import os
import json
import requests
from requests_kerberos import OPTIONAL, MutualAuthenticationError, HTTPKerberosAuth

from dotenv import load_dotenv

load_dotenv()

def get():
    # TODO: Remove all "greenlight" requests; remove HTTP principal from
    #       Kerberos server
    kerberos_auth = HTTPKerberosAuth(
        force_preemptive = True,
        delegate = True,
        mutual_authentication = OPTIONAL
    )
    try:
        requests.get(
            f"http://dev.chompe.rs/v1/omnipresence",
             auth = kerberos_auth
        ).content
    except MutualAuthenticationError:
        pass
    response = requests.get(
        f"http://dev.chompe.rs/v1/omnipresence",
        params = {
            "charname": os.getenv('GITHUB_USER')
        },
        auth=kerberos_auth
    )
    return response.json()

def post():
    response = requests.post(
        f"{os.getenv('API_URL')}:{os.getenv('API_PORT')}/v1/omnipresence",
        data = {
            "username": os.getenv('GITHUB_USER'),
            "charname": os.getenv('GITHUB_USER'),
            "working_dir": os.getcwd()
        },
        auth=HTTPKerberosAuth(mutual_authentication = OPTIONAL, force_preemptive = True)
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
