

# chargement des modules
# import time
import pygame
from pygame.math import Vector2
from random import randrange
from configuration import *
from game_inputs import *
from game_surfaces import *
from game_camera import *
from game_player import *
from game_planets import *


# initialisation de pygame
if not pygame.get_init():
    pygame.init()
if not pygame.mixer.get_init():
    pygame.mixer.init()


# initialise des objets
planets.append(Planet(position=Vector2(224, 256)))
planets.append(Planet(position=Vector2(128, 128), size=64))
planets.append(Planet(position=Vector2(480, 32), size=96))
planets[1].rotation_speed = 0.2
planets[2].rotation_speed = -0.05
player.position = Vector2(320, 240)


# sons
# --- musique
pygame.mixer.music.load("assets/audio/game-music.wav")
pygame.mixer.music.play(-1)


# boucle principale
running = True
while running:

    # --- logique ---

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            Inputs.keyDown(event.key)
        elif event.type == pygame.KEYUP:
            Inputs.keyUp(event.key)

    if running == False:
        break

    # --- graphismes ---

    display.fill([0, 0, 0])

    for planet in planets:
        planet.drawGravityRanges()

    for planet in planets:
        planet.update()

    player.update()
    camera.update(player)

    window.blit(pygame.transform.scale(display, WINDOW_SIZE), [0, 0])
    pygame.display.update()
    Inputs.update()


# désinitialise les modules pygame
pygame.quit()

