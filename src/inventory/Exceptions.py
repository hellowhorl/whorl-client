class InvalidCommandException(Exception):

    def __init__(self, *args):
        super().__init__(*args)

class InvalidArgumentsException(Exception):

    def __init__(self, *args):
        super().__init__(*args)
