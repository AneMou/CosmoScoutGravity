

# chargement des modules
import pygame
import json


# charge le fichier json de configuration
config_data = None
with open("configuration.json", "r", encoding="utf-8") as rawfile:
    config_data = json.load(rawfile)


# créer des constantes depuis les données de configuration
# game
GAME_MAX_FPS = config_data["game"]["max_fps"]
# window
WINDOW_TITLE = config_data["window"]["title"]
WINDOW_WIDTH = config_data["window"]["width"]
WINDOW_HEIGHT = config_data["window"]["height"]
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT
WINDOW_FLAGS = 0
if "fullscreen" in config_data["window"]["flags"]:
    WINDOW_FLAGS = WINDOW_FLAGS | pygame.FULLSCREEN

# display
DISPLAY_WIDTH = config_data["display"]["width"]
DISPLAY_HEIGHT = config_data["display"]["height"]
DISPLAY_SIZE = DISPLAY_WIDTH, DISPLAY_HEIGHT

