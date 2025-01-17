import os
import sys
import base64
import inspect
import getpass
import importlib

from .specs import ItemSpec

class Instance:

    def __init__(self, filename: str = ""):
        """ Constructor """
        self.valid = True
        self.__validate_file(filename)
        try:
            self.source = inspect.getsource(self.object)
        except AttributeError:
            # There's already an invalid item warning thrown by validation,
            # so just exit; also should throw an exit in __validate_file?
            sys.exit()
        try:
            self.binary = open(filename, "rb")
        except FileNotFoundError:
            print(f"There doesn't appear to be even a single {filename} around!")
            sys.exit()
        self.__enumerate_properties()

    def __validate_file(self, filename: str = "") -> None:
        """ Validates aspects of a file """
        try:
            # Split name into module name; system rules dictate
            # that enclosing files and classes share the same name
            self.name = filename.split(".")[0]
            self.object = importlib.import_module(self.name)
            # We can't actually call the use method because it may
            # destroy some objects. Could we copy it briefly?
            self.mod = getattr(self.object, self.name)
            self.mod().use
            # Test if the object correctly inherits system specifications
            # in the MRO
            if not ItemSpec in self.mod.__mro__:
                raise
        except Exception as e:
            print(f"{filename} is not a valid item!")
            self.valid = False

    def __enumerate_properties(self) -> None:
        self.transmit = {
            "item_owner": os.getenv("GITHUB_USER") or getpass.getuser(),
            "item_qty": 1,
        }
        instance = self.mod()
        to_transmit = {
            "modname" : "item_name",
            "volume": "item_weight",
            "consumable": "item_consumable",
            "version": "item_version"
        }
        # TODO: Fix for translation table above
        for prop in dir(instance):
            value = getattr(instance, prop)
            if prop in to_transmit:
                prop = to_transmit[prop]
            self.transmit[prop] = value
