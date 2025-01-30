class Path:
    """The Path class is used to define the current scene and act so the program knows where to pull from the yaml file.

    :param paths: takes a dictionary to store different acts and scenes for the narrator to know which text to display, defaults to an empty dict
    :type paths: dict(Optional)
    """

    def __init__(self, paths: dict = {}):
        self.act = paths["act"]
        self.scene = list(paths["scene"].keys())[0]

    def get_next_scene(self, paths: dict):
        """If there's another scene stored in the current act then it will go to it.

        :param paths: the dictionary that defines the scene numbers for the current act.
        :type: dict
        """
        scenes = list(paths[self.act])
        try:
            idx = scenes.index(self.scene)
        except ValueError:
            return
        idx += 1
        if idx < len(scenes):
            self.scene = scenes[idx]

    def change(self, path: dict = {"act": 1, "scene": 1}):
        """Change the instance's act and scene.

        :param path: Defines what the classes variables will be changed to, defaults to {"act": 1, "scene": 1}
        :type: dict
        """
        self.act = path["act"]
        self.scene = path["scene"]
