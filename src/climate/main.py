"""Provide a weather report on local climate."""

import os
import requests
import json

from rich.console import Console
from rich.table import Table
from dotenv import load_dotenv

# Load environment variables from .env file
# TODO: Do we need to provide guarding around this variable
#       once it's in the Codespace (i.e. no env file)?
load_dotenv()

def convert_temp_scale(state: dict = {}) -> None:
    for field in state["main"]:
        if "temp" in field or "feels_like" in field:
            state["main"][field] = int(state["main"][field]) - 273.15
            if os.getenv("TEMP_SCALE") == "F":
                state["main"][field] = (state["main"][field] * 1.8) + 32
        state["main"][field] = round(state["main"][field], 2)

# Import and call the load_dotenv function from the dotenv module (loads environment variables from a .env file)
from dotenv import load_dotenv
load_dotenv()

def main():
    """Display the weather report."""
    # Define api_url and port variables
    api_url = os.getenv("API_URL")
    api_port = os.getenv("API_PORT")

    # Sends a get request to the url and stores the response
    STATE = json.loads(
        requests.get(
            f"{api_url}:{api_port}/v1/climate"
        ).content
    )

    # Convert the temperature scale to environment-defined scale
    convert_temp_scale(STATE)

    # Textual output here that uses rich to format
    weather_emojis = {
        "Clear": "☀️",
        "Clouds": "☁️",
        "Rain": "🌧️",
        "Snow": "❄️",
        "Thunderstorm": "⛈️",
        "Drizzle": "🌦️",
        "Mist": "🌫️"
    }

    temp_scale_symbol = os.getenv("TEMP_SCALE") or "C"

    console = Console()
    table = Table(show_header=False, title="Meadville", title_style="bold magenta")
    table.add_column()
    table.add_column()
    data = [
        ("Weather", f"{weather_emojis.get(STATE['weather'][0]['main'], '')} {STATE['weather'][0]['main']}"),
        ("Temperature", f'{STATE["main"]["temp"]} °{temp_scale_symbol}'),
        ("Feels Like", f'{STATE["main"]["feels_like"]} °{temp_scale_symbol}'),
        ("Min Temp", f'{STATE["main"]["temp_min"]} °{temp_scale_symbol}'),
        ("Max Temp", f'{STATE["main"]["temp_max"]} °{temp_scale_symbol}'),
        ("Pressure", f'{STATE["main"]["pressure"]} hPa'),
        ("Humidity", f'{STATE["main"]["humidity"]}%'),
        ("Visibility", f'{STATE["visibility"]} m'),
        ("Wind Speed", f'{STATE["wind"]["speed"]} m/s'),
        # ("Rain", f'{STATE.get("rain", {}).get("1h", "N/A")} mm'),
        ("Clouds", f'{STATE["clouds"]["all"]}%')
    ]
    for i, (label, value) in enumerate(data):
        table.add_row(label, value)
        if i < len(data) - 1:  # Don't add a line after the last row
            table.add_row()
    console.print("")
    console.print(table)
    console.print("")

if __name__ == "__main__":
    main()
