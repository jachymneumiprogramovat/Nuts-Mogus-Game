""" Contains the GameObject class. """

from pygame import Surface, Rect
from pygame.sprite import Sprite
from pygame import time
from config import Config


class GameObject(Sprite):
    """ Base class for all game objects. """

    def __init__(self, image: Surface, rect: Rect):
        Sprite.__init__(self)
        self.image = image
        self.rect = rect
        self.shoot:list[GameObject] = []
        self.last = time.get_ticks()
        self.cooldown =20

        self.direction = (1, 0)
        self.speed = 1

    def move(self) -> None:
        """ Moves the object by (x, y). """
        self.rect = self.rect.move(
            self.speed * Config.GAME_UNIT_SIZE * self.direction[0],
            self.speed * Config.GAME_UNIT_SIZE * self.direction[1])
