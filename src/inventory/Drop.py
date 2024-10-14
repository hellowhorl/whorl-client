import os
import sys
import types
import base64
import requests
import importlib

from dotenv import load_dotenv
from .Instance import Instance

load_dotenv()

class Dropped:

    def __init__(self, item_names: list = []):
        for item in item_names:
            self.__drop_item(item)

    def __drop_item(self, item_name: str = "") -> None:
        item_record = self.__search_inventory(item_name)
        item_binary = self.__convert_to_py_file(item_record['item_bytestring'])
        with open(f"{item_name}.py", "w") as fh:
            fh.write(item_binary)
        status = requests.patch(
            f"{os.getenv('API_URL')}:{os.getenv('API_PORT')}/v1/inventory/reduce/",
            data = {
                "item_name": item_name,
                "item_owner": os.getenv('GITHUB_USER'),
                "item_drop": True
            }
        )

    def __search_inventory(self, item_name: str = "") -> dict:
        item = requests.post(
            f"{os.getenv('API_URL')}:{os.getenv('API_PORT')}/v1/inventory/search/",
            data = {
                "charname": os.getenv('GITHUB_USER'),
                "item_name": item_name
            }
        )
        return item.json()

    def __convert_to_py_file(self, item_binary) -> str:
        source = bytes.fromhex(
            item_binary
        ).decode('utf-8')
        return source

def cmd():
    Dropped(sys.argv[1:])
