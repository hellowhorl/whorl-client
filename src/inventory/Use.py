import os
import sys
import types
import base64
import getpass
import requests
import importlib

from dotenv import load_dotenv
from .Instance import Instance

load_dotenv()

class Usage:

    def __init__(self, item_name: str = "", to_use: bool = True):
        self.item_name = item_name
        item_record = self.__search_inventory()
        if not item_record:
            print(f"ERROR: You don't seem to have any {item_name}!")
            sys.exit(1)
        self.__decode_item_file(item_record)
        if to_use:
            self.__use_item()
        else:
            self.__get_info()

    def __search_inventory(self, item_name: str = "") -> dict:
        item = requests.post(
            f"{os.getenv('API_URL')}:{os.getenv('API_PORT')}/v1/inventory/search/",
            data = {
                "charname": os.getenv('GITHUB_USER') or getpass.getuser(),
                "item_name": self.item_name
            }
        )
        if item.status_code == 200:
            return item.json()
        return {}

    def __decode_item_file(self, item_record: dict = {}) -> None:
        self.source = bytes.fromhex(
            item_record['item_bytestring']
        ).decode('utf-8')

    def __use_item(self):
        mod = types.ModuleType(self.item_name)
        exec(self.source, mod.__dict__)
        getattr(mod, self.item_name)().use()
        status = requests.patch(
            f"{os.getenv('API_URL')}:{os.getenv('API_PORT')}/v1/inventory/reduce/",
            data = {
                "item_name": self.item_name,
                "item_owner": os.getenv('GITHUB_USER') or getpass.getuser()
            }
        )

    def __get_info(self):
        mod = types.ModuleType(self.item_name)
        exec(self.source, mod.__dict__)
        print(f"You look at {self.item_name}. {getattr(mod, self.item_name)()}")

def cmd_use():
    Usage(item_name = sys.argv[1])

def cmd_info():
    Usage(item_name = sys.argv[1], to_use = False)
