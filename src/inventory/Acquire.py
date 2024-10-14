import os
import sys
import base64
import pennant
import requests

from .Instance import Instance
from .Exceptions import *

from dotenv import load_dotenv

load_dotenv()

class Acquisition:

    def __init__(self):
        # Accommodate multiple files; acquire each serially
        for file in sys.argv[1:]:
            instance = Instance(file)
            self.__transmit_to_api(instance)

    def __transmit_to_api(self, instance: dict = {}) -> None:
        response = requests.post(
            f"{os.getenv('API_URL')}:{os.getenv('API_PORT')}/v1/inventory/add/",
            data = instance.transmit,
            files = {"item_binary": instance.binary}
        )
        if response.status_code == 409:
            context = response.json()
            print(context['error'])

def cmd():
    # Validate correct use of function
    try:
        if sys.argv[0].split("/")[-1] != "get":
            raise InvalidCommandException(
                "Cannot call Acqusition directly!"
            )
    except InvalidCommandException as e:
        print(e)
        sys.exit(1)
    try:
        if len(sys.argv) < 2:
            raise InvalidArgumentsException(
                "At least one item name required!"
            )
    except InvalidArgumentsException as e:
        print(e)
        sys.exit(1)
    # Failing any issues, add CWD to the path and
    # start Acquisition
    sys.path.append(os.path.expanduser(os.getcwd()))
    Acquisition()
