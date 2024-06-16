

# chargement des modules
import pygame


# initialisation de pygame
if not pygame.get_init():
    pygame.init()


# classe des Inputs
class Inputs:

    # liste des touches clavier pressées
    pressed_keys = dict()

    # liste des touches cliquées
    clicked_keys = dict()

    @classmethod
    def keyDown(cls, key):
        cls.pressed_keys[key] = True

    @classmethod
    def keyUp(cls, key):
        cls.pressed_keys[key] = False
        cls.clicked_keys[key] = True

    @classmethod
    def pressed(cls, key):
        return key in cls.pressed_keys.keys() and cls.pressed_keys[key]

    @classmethod
    def clicked(cls, key):
        return key in cls.clicked_keys.keys() and cls.clicked_keys[key]

    @classmethod
    def update(cls):
        for key in cls.clicked_keys.keys():
            cls.clicked_keys[key] = False
            

