""" Contains the Config class. """


class Config:
    """ Contains the game configuration. """

    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 800
    GAME_UNIT_SIZE = 8
    OBJECT_SIZE = 2
    BG_COLOR = 0, 0, 0
    GOAL_COLOR = 0, 255, 0
    WALL_COLOR = 0, 0, 255
    MAX_FPS = 60
    IMAGE_FILES = {
        'player_standing': 'hardest-game-ever-2\player_standing.png',
        'enemy': 'hardest-game-ever-2\enemy.png',
        'player_up':"hardest-game-ever-2\player_up.png",
        'player_right':"hardest-game-ever-2\player_right.png",
        "player_left":"hardest-game-ever-2\player_left.png",
        "player_down":"hardest-game-ever-2\player_down.png"
    }
    STARTING_LEVEL = 0