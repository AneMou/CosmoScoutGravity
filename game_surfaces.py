

# chargement des modules
import pygame
from configuration import *


# initialisation de pygame
if not pygame.get_init():
    pygame.init()


#  window et display
window = pygame.display.set_mode(WINDOW_SIZE, WINDOW_FLAGS)
pygame.display.set_caption(WINDOW_TITLE)
display = pygame.Surface(DISPLAY_SIZE)


# horloge pygame pour limiter le sfps
clock = pygame.time.Clock()

