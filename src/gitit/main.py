"""This module contains functions to download and save files from a configured URL path."""

from .Config import Config

from request import Request
from pathlib import Path
from fake_useragent import UserAgent

ua = UserAgent()


def get(
    raw_path: str = Config.values["URL"],
    file_type: str = "objects",
    file_name: str = "",
) -> None:
    """Download and save a file from a configured URL path.

    Makes an HTTP GET request to download files from the specified URL path
    and writes them to the local filesystem.

    :param raw_path: Base URL for file downloads
    :type raw_path: str
    :param file_type: Type of file/directory to access
    :type file_type: str
    :param file_name: Name of file to download
    :type file_name: str
    :return: None - Function writes file to disk
    :rtype: None
    :raises requests.exceptions.RequestException: If the HTTP request fails
    :raises IOError: If there are issues writing the file
    """
    raw = Request(
        method="GET",
        url=f"{raw_path}/{file_type}/{file_name}",
        headers={"User-Agent": ua.chrome},
    )()
    text = str(raw.text)
    Path(file_name).touch()
    file = open(file_name, "w")
    file.write(text)
    file.close()
