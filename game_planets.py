

# chargement des modules
from random import randrange
import pygame
import pygame.gfxdraw
from pygame.math import Vector2
from game_sprites import *
from game_surfaces import *
from game_camera import *


# initialisation de pygame
if not pygame.get_init():
    pygame.init()


# liste des planètes
planets = list()


# classe Planêtes
class Planet:

    def __init__(self, **kwargs):

        # récupère les arguments
        self.position = kwargs.get("position", Vector2(0, 0))
        self.rotation = kwargs.get("rotation", 0)
        self.rotation_speed = kwargs.get("rotation_speed", 0)
        self.size = kwargs.get("size", 32)
        self.size = max(32, self.size)
        self.gravity_range = kwargs.get("gravity_range", max(self.size*3, 64))
        self.gravity_force = kwargs.get("gravity_force", 0.01)
        self.gravity_alpha = True
        self.gravity_color = pygame.Color(
            randrange(0, 128),
            randrange(0, 128),
            randrange(0, 128),
            128)

    def update(self):

        self.rotation += self.rotation_speed
        if self.rotation <= -360 or self.rotation >= 360:
            self.rotation %= 360
        self.draw()

    def draw(self):

        sprite = pygame.transform.scale(sprite_planet, [self.size * 2, self.size * 2])
        sprite = pygame.transform.rotate(sprite, self.rotation)
        x = self.position.x - sprite.get_width() // 2 - camera.position.x
        y = self.position.y - sprite.get_height() // 2 - camera.position.y
        display.blit(sprite, [x, y])

    def drawGravityRanges(self):
        """ dessine le cercle de la portée de gravitation """

        self.gravity_color.a += 1 if self.gravity_alpha else -1
        if self.gravity_color.a >= 255:
            self.gravity_alpha = False
            self.gravity_color.a = 254
        elif self.gravity_color.a <= 128:
            self.gravity_alpha = True
            self.gravity_color.a = 129
        x = int(self.position.x - camera.position.x)
        y = int(self.position.y - camera.position.y)
        pygame.gfxdraw.circle(display, x, y, self.gravity_range, self.gravity_color)

