import os
import sys
import base64
import inspect
import getpass
import importlib

from .specs import ItemSpec

class Instance:
    """A class to handle item instances in the inventory system.

    This class validates, loads and processes item files before they are added
    to the inventory system. It handles file validation, property enumeration,
    and preparation of item data for transmission to the API.

    Attributes:
        valid (bool): Whether the item file is valid
        name (str): Name of the item module
        object (module): Loaded Python module for the item
        mod (class): Item class from the module
        source (str): Source code of the item class
        binary (file): Binary file handle for the item
        transmit (dict): Dictionary of item properties for API transmission
    """

    def __init__(self, filename: str = ""):
        """Initialize an item instance from a file.

        Args:
            filename (str, optional): Path to item file. Defaults to empty string.

        Raises:
            SystemExit: If file validation fails or file not found
            AttributeError: If item module cannot be loaded
            FileNotFoundError: If item file does not exist
        """
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
        """Validate an item file by checking module structure and inheritance.

        Args:
            filename (str, optional): Name of file to validate. Defaults to empty string.

        Raises:
            Exception: If file does not meet item specification requirements
            ImportError: If module cannot be imported
            AttributeError: If required attributes are missing
        """
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
        """Enumerate and collect item properties for API transmission.

        Collects item properties and maps them to API field names, creating
        a dictionary ready for transmission to the inventory API.

        Note:
            Properties are mapped according to to_transmit dictionary
        """
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
