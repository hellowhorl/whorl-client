import os
import sys
import types
import base64
import requests
import importlib
import narrator

from dotenv import load_dotenv
from .Instance import Instance

load_dotenv()

class Give:

    def __init__(self, item_name, item_receiver):
        self.item_name = item_name
        self.item_receiver = item_receiver
        item_record = self.__search_inventory()
        if not item_record:
            print(f"You don't seem to have any {self.item_name}!")
            sys.exit(1)
        self.__give_item(item_record)

    def __search_inventory(self) -> dict:
        item = requests.post(
            f"{os.getenv('API_URL')}:{os.getenv('API_PORT')}/v1/inventory/search/",
            data = {
                "charname": os.getenv('GITHUB_USER'),
                "item_name": self.item_name
            }
        )
        if item.status_code == 200:
            return item.json()
        return {}

    def __confirm_transfer(self) -> bool:
        # TODO: Could substitute with YesNoQuestion (from narrator)
        q = narrator.Question({
            "question": f"Give {self.item_name} to {self.item_receiver}?",
            "responses": [
                {"choice": "yes", "outcome": True},
                {"choice": "no", "outcome": False}
            ]
        })
        return q.ask()

    def __give_item(self, item_record) -> None:
        response = self.__confirm_transfer()
        if not response:
            print("Transfer cancelled.")
            sys.exit(0)
        result = requests.patch(
            f"{os.getenv('API_URL')}:{os.getenv('API_PORT')}/v1/inventory/transfer/{self.item_receiver}",
            data = {
                "charname": os.getenv('GITHUB_USER'),
                "item_name": self.item_name
            }
        )
        if result.status_code == 200:
            print("Transfer successful!")
            sys.exit(0)
        print("Transfer not successful")
        sys.exit(1)

def cmd():
    Give(*sys.argv[1:3])
