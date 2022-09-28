from json import loads

""" Contains the Loader class. """


class Loader:
    """ Loads relevant non-graphic game files. """

    def load_level_config(level: int) -> dict:
        """ Loads the level dictionary. """

        with open(f'hardest-game-ever-2\level-{level}.json', 'r') as file:
            config_dict = loads(file.read())

        return config_dict
