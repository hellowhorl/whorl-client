import re
import sys

class ItemSpec:

    volume = 1
    version = "1.0.0"
    actions = {}
    consumable = True

    def __init__(self, filename):
        self.filename = filename
        self.modname = filename.split(".")[0]
        self.modname = self.modname.split("/")[-1]
        self.__set_cli_flags()

    def __set_cli_flags(self):
        flags = re.findall(
            r"((?<![a-z])-{1,2}[a-z0-9]+)(?:\s)([a-zA-Z0-9_]+)?",
            ' '.join(sys.argv[1:])
        )
        for arg, val in flags:
            arg = arg.replace("-","")
            setattr(self, arg, val)

    def __str__(self) -> str:
        return f"""This particular {self.modname} isn't that special."""

    def use(self, **kwargs) -> None:
        print(f"You try the {self.__module__}, but it doesn't do anything.")
