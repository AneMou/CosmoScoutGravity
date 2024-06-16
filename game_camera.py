

# chargement des modules
import pygame
from pygame.math import Vector2
from configuration import DISPLAY_WIDTH, DISPLAY_HEIGHT


# initialisation de pygame
if not pygame.get_init():
    pygame.init()


# classe Camera
class Camera:

	def __init__(self, **kwargs):

		# récupère les arguments
		self.position = kwargs.get("position", Vector2(0, 0))
		self.offset = Vector2(DISPLAY_WIDTH//2, DISPLAY_HEIGHT//2)

	def update(self, player):
		self.position.move_towards_ip(player.position - self.offset, (self.position.distance_to(player.position)) / 10 )

camera = Camera()

