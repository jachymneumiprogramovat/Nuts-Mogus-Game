""" Contains the Graphics class. """

from pygame import Surface, SCALED
from pygame.display import set_mode, update
from pygame.image import load

from config import Config


class Graphics:
    """ Class for basic graphics handling. """
    
    def __init__(self):
        self.canvas_width = Config.WINDOW_WIDTH
        self.canvas_height = Config.WINDOW_HEIGHT
        self.canvas: Surface = None
        self.background: Surface = None
        self.textures: dict[str, Surface] = {}
        self.initialized = False

    def init_graphics(self) -> None:
        """ Initializes game graphics. """

        self.canvas = set_mode((self.canvas_width, self.canvas_height), SCALED)
        self.background = Surface(self.canvas.get_size())
        self.background.fill(Config.BG_COLOR)
        self.background = self.background.convert()
        self.canvas.blit(self.background, (0, 0))
        update()

        self.initialized = True

    def __load_texture(self, name: str, filename: str) -> None:
        """ Loads texture given by 'filename' and saves it to textures under
        the key 'name'. """

        texture = load(filename).convert()
        self.textures[name] = texture

    def load_object_textures(self) -> None:
        """ Loads textures for all game objects. """

        for name, filename in Config.IMAGE_FILES.items():
            self.__load_texture(name, filename)

        # create goal texture
        goal_texture = Surface(self.canvas.get_size())
        goal_texture.fill(Config.GOAL_COLOR)
        goal_texture.convert()
        self.textures['goal'] = goal_texture

        # create wall texture
        wall_texture = Surface(self.canvas.get_size())
        wall_texture.fill(Config.WALL_COLOR)
        wall_texture.convert()
        self.textures['wall'] = wall_texture
