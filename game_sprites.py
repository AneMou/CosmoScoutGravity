

# chargement des modules
import pygame


# initialisation de pygame
if not pygame.get_init():
    pygame.init()


sprite_player_idle = pygame.image.load("assets/images/cosmoscout-idle.png")
sprite_player_walk = pygame.image.load("assets/images/cosmoscout-walk.png")
sprite_player_fly = pygame.image.load("assets/images/cosmoscout-fly.png")
sprite_planet = pygame.image.load("assets/images/planet.png")

