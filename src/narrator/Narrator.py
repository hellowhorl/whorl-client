import yaml
from time import sleep

from .Path import Path


class Narrator:
    """Narrator Class for displaying text for events and interactions within the virtual world.
    Take a yaml file and depending on the flags will display the corresponding text in the yaml to the user.

    :param path_file: path to yaml file narrator should use to display appropriate responses, defaults to .paths.yml
    :type path_file: str(Optional)
    """

    def __init__(self, path_file: str = ".paths.yml"):
        try:
            fh = open(path_file)
            self.paths = yaml.safe_load(fh)
        except:
            # Dummy content to populate paths
            self.paths = {0: {0: ["Lorem ipsum."]}}
        self.path = Path(
            paths={
                "act": list(self.paths.keys())[0],
                "scene": list(self.paths.values())[0],
            }
        )

    def narrate(self, **kwargs):
        """Narrate the text in the classes associated yaml based on the current act and scene specified.

        :param kwargs: Used to specify if all scenes should be played or if specific the scene and act numbers to be displayed.
        :type kwargs: dict[str,Any]
        """
        lines = []
        acts = list(self.paths)

        # Try to choose a given path, if key exists
        try:
            chosen_path = self.paths[self.path.act]
        except KeyError:
            chosen_path = self.paths[acts[0]]

        if "all" in kwargs and kwargs["all"] == True:
            # Play all scenes
            for scenes in list(chosen_path.values()):
                lines += scenes
        elif "scenes" in kwargs:
            # From the current scene, play a number of scenes specified
            try:
                scenes = int(kwargs["scenes"])
            except ValueError:
                print("ERROR: Scene count is not a number!!")
                exit()
            try:
                scene_location = list(chosen_path.keys()).index(self.path.scene)
                for idx in range(scene_location, scene_location + scenes):
                    lines += list(chosen_path.values())[idx]
            except IndexError:
                # If we go beyond the scene boundary, just stop.
                pass
        else:
            # Play only one scene from the selected point
            try:
                lines = chosen_path[self.path.scene]
            except KeyError:
                scenes = list(chosen_path)
                lines = chosen_path[scenes[0]]

        for line in lines:
            print(line)
            sleep(1.5)

        self.path.get_next_scene(self.paths)
