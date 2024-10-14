import os
import sys
import base64
import pennant
import requests

from dotenv import load_dotenv

from rich.table import Table
from rich.console import Console

load_dotenv()

# TODO: Move this to a specific command file (like others) instead of main

def list():

    allowed = ["item_name", "item_qty", "item_bulk", "item_consumable"]

    api_request = requests.get(
        f"{os.getenv('API_URL')}:{os.getenv('API_PORT')}/v1/inventory/list",
        params = {
            "charname": os.getenv('GITHUB_USER')
        }
    )

    context = api_request.json()

    total_volume = 0
    for item in context:
        total_volume += item['item_bulk']

    table = Table(title=f"""{os.getenv('GITHUB_USER')}'s inventory
({total_volume}/10.0 spaces; {10.0 - total_volume} spaces remain)""")
    table.add_column("Item name")
    table.add_column("Item count")
    table.add_column("Space Occupied")
    table.add_column("Consumable")

    for item in context:
        values = [str(item[field]) for field in item if field in allowed]
        table.add_row(*values)

    Console().print(table)
