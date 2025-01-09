import os
import pickle
import pathlib
import requests

from requests_kerberos import HTTPKerberosAuth
from requests_kerberos.exceptions import KerberosExchangeError

# Word to the homie: 
# https://github.com/requests/requests-kerberos/issues/178

class Auth:

    MODULE_PATH = pathlib.Path(__file__).parent.resolve()

    def __init__(self):
        if not self.__load_session():
            self.session = requests.Session()
            self.session.auth = HTTPKerberosAuth(force_preemptive = True)
            self.__store_session()
    
    def __load_session(self) -> bool:
        if os.path.isfile(f"{self.MODULE_PATH}/.watchdog.session"):
            with open(f"{self.MODULE_PATH}/.watchdog.session", "rb") as fh:
                self.session = pickle.load(fh)
            return True
        return False

    def __store_session(self):
        with open(f"{self.MODULE_PATH}/.watchdog.session", "wb") as fh:
            pickle.dump(self.session, fh)

    def get(self, url, *args, **kwargs):
        return self.session.get(url)