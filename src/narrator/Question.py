class Question:
    """The Question class is used to ask a question and respond accordingly based on the the prompt dictionary given.

    :param prompts: A dictionary that has the questions and the possible responses and there outcomes to know which text to display, defaults to an empty dict.
    :type paths: dict(Optional)
    """

    def __init__(self, prompt: dict = {}):
        self.responses = {}
        self.prompt = prompt["question"]
        for response in prompt["responses"]:
            self.set_opt(response)
        options = [self.responses[val].choice for val in self.responses]
        self.prompt += f" ({'/'.join(options)}): "

    def is_key(self, char: str) -> bool:
        """Checks to see if the specified str or character is in responses.

        :param char: The string to look for in the responses dictionary
        :type char: str

        :return: Returns true if the string is in responses otherwise false
        :rtype: bool
        """
        if char in list(self.responses.keys()):
            return True
        return False

    def set_opt(self, option: dict) -> dict:
        """Takes the choices in the option dict and iterates through them mapping responses to the the first unique character in the choices.

        :param option: Stores the choices and the responses to mapped to a key.
        :type option: dict
        """
        choice = option["choice"]
        for letter in choice:
            if not self.is_key(letter):
                opt = Option(letter, option)
                self.responses[letter] = opt
                break

    def ask(self) -> dict:
        """Asks the user for a input to answer the instances question will loop until a valid response is given.

        :return: Returns the the outcome of the users response to the question if it's an option.
        :rtype: dict
        """
        while True:
            ask = input(self.prompt).lower()
            if ask in self.responses:
                path = self.responses[ask].outcome
                self.choice = self.responses[ask].nice_name
                return path
            print("Enter a valid response option.")


class YesNoQuestion(Question):
    """
    Used for yes or no questions i.e do you like cake? only can have two outcomes and the choices are always yes or no.

    :param prompt: Stores the questions and the yes outcome in the first outcome and the no outcome in the second
    :type prompt: dict
    """

    def __init__(self, prompt: dict):
        if len(prompt["outcomes"]) != 2:
            raise
        super().__init__(
            {
                "question": prompt["question"],
                "responses": [
                    {"choice": "yes", "outcome": prompt["outcomes"][0]},
                    {"choice": "no", "outcome": prompt["outcomes"][1]},
                ],
            }
        )


class Option:
    """Takes the first letter of a str and makes it as a option for the user to choose.

    :param key: The str you want to be an option for the user to choose.
    :type key: str

    :param option: The dictionary for storing the specified outcomes for the choices the users can make.
    :type option: dict
    """

    def __init__(self, key: str, option: dict):
        self.choice = option["choice"].replace(key, f"[{key.upper()}]", 1)
        self.outcome = option["outcome"]
        self.nice_name = option["choice"].lower()
