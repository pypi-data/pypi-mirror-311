import pygame
import sys
from .settings import *
from .map import *
from .player import *
from .raycasting import *
from .object_renderer import *
from .sprite_object import *


class Game:
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)
        # create graphical window with the provided resolution
        self.screen = pygame.display.set_mode(RES)
        # set FPS
        self.clock = pygame.time.Clock()
        self.new_game()
        self.delta_time = 1

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.static_sprite = SpriteObject(self)
        self.animated_sprite = AnimatedSprite(self)

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.static_sprite.update()
        self.animated_sprite.update()

        pygame.display.flip()
        self.delta_time = self.clock.tick(FPS)    # why equals??
        pygame.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        # self.screen.fill('black')
        self.object_renderer.draw()
        # self.map.draw()
        # self.player.draw()

    def check_events(self):
        for event in pygame.event.get():
            # close the window if Esc has been pressed
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

    # game loop
    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


