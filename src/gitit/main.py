import requests

from .Config import Config

from fake_useragent import UserAgent

ua = UserAgent()

def get(
      raw_path: str = Config.values["URL"],
      file_type: str = "objects",
      file_name: str = ""
    ) -> None:
    """Download and save a file from a configured URL path.

    Args:
        raw_path (str, optional): Base URL for file downloads. 
            Defaults to Config.values["URL"].
        file_type (str, optional): Type of file/directory to access.
            Defaults to "objects".
        file_name (str, optional): Name of file to download.
            Defaults to empty string.

    Returns:
        None: Function writes file to disk but does not return anything.

    Raises:
        requests.exceptions.RequestException: If the HTTP request fails
        IOError: If there are issues writing the file
    """
    raw = requests.get(
      f"{raw_path}/{file_type}/{file_name}",
     headers = {'User-Agent': ua.chrome}
    )
    text = str(raw.text)
    file = open(file_name, "x")
    file.write(text)
    file.close()
