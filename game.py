""" Contains the Game class. """

from secrets import token_urlsafe
from tokenize import String
from typing import Tuple

from pygame.sprite import RenderUpdates, spritecollideany, groupcollide
from pygame.time import Clock
from pygame.key import get_pressed
from pygame import Rect, display, transform, K_UP, K_RIGHT, K_LEFT, K_DOWN,K_w,K_a,K_s,K_d,K_e, event, QUIT, quit, time

from random import randint
from graphics import Graphics
from config import Config
from loader import Loader
from game_object import GameObject


class Game:
    """ Manages game objects. """

    def __init__(self, graphics: Graphics):
        self.graphics = graphics
        self.objects: RenderUpdates = None
        self.player: RenderUpdates = None
        self.enemies: RenderUpdates = None
        self.enemy_boundaries: list[RenderUpdates] = []
        self.walls: RenderUpdates = None
        self.goal: RenderUpdates = None
        self.bulet:RenderUpdates = None
        self.running = False
        self.level = Config.STARTING_LEVEL
        self.enemy_paths: list = None
        self.clock: Clock = None

    def __load_textures(self) -> None:
        """ Loads object textures. """

        self.graphics.load_object_textures()

    def __get_level_data(self) -> dict:
        """ Loads the dictionary with object positions. """

        return Loader.load_level_config(self.level)

    def __get_enemy_direction(self, enemy_path: list) -> Tuple[int]:
        start = enemy_path[0]
        end = enemy_path[1]

        direction = (end[0] - start[0], end[1] - start[1])
        direction = (int(direction[0] / abs(direction[0] + direction[1])),
                     int(direction[1] / abs(direction[0] + direction[1])))

        return direction

    def __spawn_all(self) -> None:
        """ Spawns all game objects. """

        level_data = self.__get_level_data()
        self.enemy_paths = level_data['enemy']

        # spawn player
        player_texture = self.graphics.textures['player_standing']
        player_rect = Rect(
            level_data['player'][0] * Config.GAME_UNIT_SIZE,
            level_data['player'][1] * Config.GAME_UNIT_SIZE,
            (Config.OBJECT_SIZE * Config.GAME_UNIT_SIZE)-3,
            (Config.OBJECT_SIZE * Config.GAME_UNIT_SIZE)+7
        )
        player = GameObject(player_texture, player_rect)
        player.speed = level_data['speed']['player']
        self.player = RenderUpdates(player)
        self.objects = RenderUpdates(player)

        # spawn enemies
        self.enemies = RenderUpdates()
        enemy_texture = self.graphics.textures['enemy']
        for index, enemy_position in enumerate(self.enemy_paths):
            enemy_rect = Rect(
                enemy_position[0][0] * Config.GAME_UNIT_SIZE,
                enemy_position[0][1] * Config.GAME_UNIT_SIZE,
                Config.OBJECT_SIZE * Config.GAME_UNIT_SIZE,
                Config.OBJECT_SIZE * Config.GAME_UNIT_SIZE
            )
            enemy = GameObject(enemy_texture, enemy_rect)
            enemy.direction = self.__get_enemy_direction(enemy_position)
            enemy.speed = level_data['speed']['enemy'][index]
            self.enemies.add(enemy)
            self.objects.add(enemy)

            boundary_group = RenderUpdates()
            for i, point in enumerate(enemy_position):
                if i == 0:
                    if enemy.direction[0] > 0:
                        point[0] -= Config.OBJECT_SIZE
                    if enemy.direction[0] < 0:
                        point[0] += Config.OBJECT_SIZE
                    if enemy.direction[1] > 0:
                        point[1] -= Config.OBJECT_SIZE
                    if enemy.direction[1] < 0:
                        point[1] += Config.OBJECT_SIZE
                if i == 1:
                    # FIX THIS TODO
                    if enemy.direction[0] < 0:
                        point[0] -= Config.OBJECT_SIZE
                    if enemy.direction[0] > 0:
                        point[0] += Config.OBJECT_SIZE
                    if enemy.direction[1] < 0:
                        point[1] -= Config.OBJECT_SIZE
                    if enemy.direction[1] > 0:
                        point[1] += Config.OBJECT_SIZE
                point_rect = Rect(point[0] * Config.GAME_UNIT_SIZE,
                                  point[1] * Config.GAME_UNIT_SIZE,
                                  Config.OBJECT_SIZE * Config.GAME_UNIT_SIZE,
                                  Config.OBJECT_SIZE * Config.GAME_UNIT_SIZE)
                point_object = GameObject(None, point_rect)
                boundary_group.add(point_object)

            self.enemy_boundaries.append(boundary_group)

        # spawn walls
        self.walls = RenderUpdates()
        wall_texture = self.graphics.textures['wall']
        for wall_position in level_data['walls']:
            wall_texture =\
                transform.scale(wall_texture,
                                (wall_position[2] * Config.GAME_UNIT_SIZE,
                                 wall_position[3] * Config.GAME_UNIT_SIZE))
            wall_rect = Rect(
                wall_position[0] * Config.GAME_UNIT_SIZE,
                wall_position[1] * Config.GAME_UNIT_SIZE,
                wall_position[2] * Config.GAME_UNIT_SIZE,
                wall_position[3] * Config.GAME_UNIT_SIZE
            )
            wall = GameObject(wall_texture, wall_rect)
            self.walls.add(wall)
            self.objects.add(wall)

        # spawn goal
        self.goal = RenderUpdates()
        goal_texture = self.graphics.textures['goal']
        for goal_position in level_data['goal']:
            goal_texture =\
                transform.scale(goal_texture,
                                (goal_position[2] * Config.GAME_UNIT_SIZE,
                                 goal_position[3] * Config.GAME_UNIT_SIZE))
            goal_rect = Rect(
                goal_position[0] * Config.GAME_UNIT_SIZE,
                goal_position[1] * Config.GAME_UNIT_SIZE,
                goal_position[2] * Config.GAME_UNIT_SIZE,
                goal_position[3] * Config.GAME_UNIT_SIZE
            )
            goal = GameObject(goal_texture, goal_rect)
            self.goal.add(goal)
            self.objects.add(goal)

            # draw everything
        self.objects.draw(self.graphics.canvas)

    def __set_enemy_direction(self, enemy: GameObject,
                             index: int) -> Tuple[int]:
        if spritecollideany(enemy, self.enemy_boundaries[index]):
            enemy.direction = (
                -enemy.direction[0],
                -enemy.direction[1])

    def __change_sprite(self,direction:Tuple[int],player:GameObject):
        if direction==[0,1]:player.image=self.graphics.textures['player_down']
        if direction==[0,-1]:player.image=self.graphics.textures['player_up']
        if direction==[-1,0]:player.image=self.graphics.textures['player_left']
        if direction==[1,0]:player.image=self.graphics.textures['player_right']
        if direction==[0,0]:player.image=self.graphics.textures['player_standing']

    def __shoote(self,shooter:GameObject,direction:Tuple[int]):
        now = time.get_ticks()
        print(now,shooter.last)
        if len(shooter.shoot)<15 and now-shooter.last>=shooter.cooldown:
            start = shooter.rect
            surf = self.graphics.textures["enemy"]
            bullet = GameObject(surf,start)
            bullet.direction=direction
            shooter.shoot.insert(0,bullet)
            self.bulet=RenderUpdates()
            self.bulet.add(bullet)
            self.objects.add(bullet)
        shooter.last=now
        

    def __set_player_direction(self, player: GameObject, keys: dict) -> None:
        direction = [0, 0]
        if keys[K_UP] or keys[K_w]:
            direction[1] = -1
        elif keys[K_DOWN] or keys[K_s]:
            direction[1] = 1

        if keys[K_LEFT] or keys[K_a]:
            direction[0] = -1
        elif keys[K_RIGHT] or keys[K_d]:
            direction[0] = 1

        player.direction = tuple(direction)

        if keys[K_e]:
            self.__shoote(player,direction)

        self.__change_sprite(direction,player)

    def __move_player(self) -> None:
        # move player
        player = self.player.sprites()[0]
        self.__set_player_direction(player, get_pressed())

        current_pos = player.rect
        player.move()
        if groupcollide(self.player, self.walls, False, False):
            player.rect = current_pos
        if groupcollide(self.player, self.enemies, False, False):
            self.__reset_level()
        if groupcollide(self.player, self.goal, False, False):
            self.level += 1
            self.__reset_level()

    def __move_bullets(self,player:GameObject):
        boundaries = Rect(0,0,Config.WINDOW_WIDTH,Config.WINDOW_HEIGHT)
        for i in player.shoot:
            i.move()
            if not boundaries.collidepoint(eval(self.__edge(i))):
                player.shoot.remove(i)

    def __edge(self,bullet:GameObject)->String:
        if bullet.direction==[0,1]:return f'i.rect.midtop'
        if bullet.direction==[0,-1]:return f'i.rect.midbottom'
        if bullet.direction==[-1,0]:return f'i.rect.midright'
        if bullet.direction==[1,0]:return f'i.rect.midleft'
        if bullet.direction==[1,1]:return f'i.rect.topleft'
        if bullet.direction==[-1,-1]:return f'i.rect.bottomright'
        if bullet.direction==[1,-1]:return f'i.rect.bottomleft'
        if bullet.direction==[-1,1]:return f'i.rect.topright'
        if bullet.direction==[0,0]:
            bullet.direction=[randint(-1,1),randint(-1,1)] 
            return self.__edge(bullet)



    def __reset_level(self) -> None:
        self.objects.clear(self.graphics.canvas, self.graphics.background)
        self.objects.empty()
        self.objects = None
        self.player.empty()
        self.player = None
        self.enemies.empty()
        self.enemies = None
        self.walls.empty()
        self.walls = None
        self.goal.empty()
        self.goal = None
        self.bulet.empty()
        self.bulet=None
        for boundary in self.enemy_boundaries:
            boundary.empty()
            boundary = None
        self.enemy_boundaries = []
        self.enemy_paths = []
        self.__spawn_all()
        display.update()

    def __update(self) -> None:
        self.__move_player()

        # move enemies
        for index, enemy in enumerate(self.enemies):
            self.__set_enemy_direction(enemy, index)
            enemy.move()
        #move bullets
        self.__move_bullets(self.player.sprites()[0])

    def run(self) -> None:
        """ Runs the game and keeps it running.  """

        self.__load_textures()
        self.__spawn_all()
        display.update()
        self.clock = Clock()
        self.running = True
        while self.running:
            self.clock.tick(Config.MAX_FPS)
            for ev in event.get():
                if ev.type == QUIT:
                    quit()

            self.__update()

            self.objects.clear(self.graphics.canvas, self.graphics.background)
            changed_rects = self.objects.draw(self.graphics.canvas)
            display.update(changed_rects)
