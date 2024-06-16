

# chargement des modules
import math
import time
from random import randrange, choice
import pygame
from pygame.math import Vector2
from configuration import *
from game_inputs import *
from game_surfaces import *
from game_camera import *
from game_sprites import *
from game_planets import *


# initialisation de pygame
if not pygame.get_init():
    pygame.init()


# initialisation de pygame.mixer
if not pygame.mixer.get_init():
    pygame.mixer.init()

# --- bruits de pas
step01_se = pygame.mixer.Sound("assets/audio/step01.flac")
step02_se = pygame.mixer.Sound("assets/audio/step02.flac")


# classe Player
class Player:

    def __init__(self, **kwargs):

        # récupère les arguments

        # --- positions
        self.position = kwargs.get("position", Vector2(0, 0))
        self.rotation = kwargs.get("rotation", 0)
        self.speed = kwargs.get("speed", 0.5)
        self.fly_force = kwargs.get("fly_force", 3)
        self.rect = kwargs.get("rect", pygame.Rect(
            self.position.x,
            self.position.y,
            int(pygame.transform.rotate(sprite_player_idle, self.rotation).get_width() /4),
            pygame.transform.rotate(sprite_player_idle, self.rotation).get_height()))
        self.upward = Vector2(0, 0)
        self.forward = Vector2(0, 0)
        self.backward = Vector2(0, 0)
        self.fly_duration = 90

        # --- animations
        self.animation = kwargs.get("animation", "idle")
        self.current_frame = kwargs.get("current_frame", 0)
        self.number_of_frames = kwargs.get("number_of_frames", 4)
        self.flip_direction = False

        # --- temps
        self.ticks = 0
        self.step_ticks = 0

    def findClosestPlanets(self):
        """ retourne une liste des planètes qui exercent leur gravité sur le joueur """
        
        closest_planets = list()
        for planet in planets:
            distance_to_planet = planet.position.distance_to(self.position)
            if  distance_to_planet <= planet.gravity_range:
                closest_planets.append(planet)
        return closest_planets

    def findClosestPlanet(self, closest_planets):
        """ retourne la planête la plus proche qui exerce sa gravité sur le joueur """
        
        shortest_distance = 142857
        closest_planet = None
        for planet in closest_planets:
            v_distance = (self.position - planet.position)
            v_distance.scale_to_length(planet.size)
            ground_pos = planet.position.copy() + v_distance
            distance = self.position.distance_to(ground_pos)
            if  distance <= shortest_distance:
                closest_planet = planet
                shortest_distance = distance
        return closest_planet

    def update(self):

        # récupères les planètes interactives
        grounded = False
        closest_planets = self.findClosestPlanets()
        closest_planet = self.findClosestPlanet(closest_planets)

        # défini le vecteur forward et backward en fonction de la planête la plus proche
        if closest_planet:
            self.upward = self.position.copy() - closest_planet.position.copy()
            self.upward.scale_to_length(self.fly_force)
            self.forward = self.upward.copy()
            self.forward.scale_to_length(self.speed)
            self.forward = self.forward.rotate(90)
            self.backward = self.forward.copy().rotate(180)

        # rotation joueur <->plus proche planète et repositionnement s'il traverse le sol
        if closest_planet:
            # tourne le joueur vers la planête la plus proche
            angle = closest_planet.position - self.position
            self.rotation = math.degrees(math.atan2(angle.y, angle.x))
            # fixe le joueur au sol
            if self.position.distance_to(closest_planet.position) - self.rect.height / 2 < closest_planet.size:
                # pygame.draw.line(display, [255, 128, 0], self.position, closest_planet.position)
                v_distance = (self.position - closest_planet.position)
                v_distance.scale_to_length(closest_planet.size + (self.rect.height / 2) - 1)
                self.position = closest_planet.position.copy() + v_distance
                grounded = True
                self.fly_duration = 90

        if closest_planets:
            # déplace le joueur vers la surface de la planête
            for planet in closest_planets:
                v_distance = (self.position - planet.position)
                v_distance.scale_to_length(planet.size)
                ground_pos = planet.position.copy() + v_distance
                if not grounded:
                    target = (planet.gravity_range - self.position.distance_to(ground_pos))
                    self.position.move_towards_ip(ground_pos, target * planet.gravity_force)
                else:
                    pass

        # déplacements latéraux
        if Inputs.pressed(pygame.K_LEFT):
            self.animation = "walk"
            self.position = self.position + self.backward
            self.flip_direction = True
            if grounded:
                self.step_ticks += 1
                if self.step_ticks > 50:
                    self.step_ticks = 0
                    step_se = choice([step01_se, step02_se])
                    step_se.set_volume(randrange(40, 80)/100)
                    step_se.play()
        elif Inputs.pressed(pygame.K_RIGHT):
            self.animation = "walk"
            self.position = self.position + self.forward
            self.flip_direction = False
            if grounded:
                self.step_ticks += 1
                if self.step_ticks > 50:
                    self.step_ticks = 0
                    step_se = choice([step01_se, step02_se])
                    step_se.set_volume(randrange(40, 80)/100)
                    step_se.play()
        else:
            self.step_ticks = 0
            self.animation = "idle"

        # action perso qui lévite
        if Inputs.pressed(pygame.K_UP):

            if self.fly_duration > 0:
                self.fly_duration -= 1
                self.animation = "fly"
                self.position = self.position + self.upward

        self.ticks += 1
        delay = 0
        if self.animation == "idle":
            delay = 50
        elif self.animation == "walk":
            delay = 30
        elif self.animation == "fly":
            delay = 12
        if self.ticks > delay:
            self.ticks = 0
            self.current_frame += 1
            if self.current_frame >= self.number_of_frames:
                self.current_frame = 0

        self.draw()

        # commentary
    
    def draw(self):
        sprite = None
        if self.animation == "idle":
            sprite = sprite_player_idle
        elif self.animation == "walk":
            sprite = sprite_player_walk
        elif self.animation == "fly":
            sprite = sprite_player_fly
        sprite = sprite.copy().subsurface(pygame.Rect(
            self.current_frame * self.rect.width, 0,
            self.rect.width, self.rect.height))
        if self.flip_direction:
            sprite = pygame.transform.flip(sprite, False, True)
        sprite = pygame.transform.rotate(sprite, -self.rotation)
        self.rect.x = self.position.x - sprite.get_width() // 2
        self.rect.y = self.position.y - sprite.get_height() // 2
        draw_pos = Vector2(self.rect.x, self.rect.y) - camera.position
        display.blit(sprite, draw_pos)


# player object
player = Player()

