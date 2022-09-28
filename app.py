from pygame import init


from graphics import Graphics
from game import Game

init()
graphics = Graphics()
graphics.init_graphics()

game = Game(graphics)
game.run()   