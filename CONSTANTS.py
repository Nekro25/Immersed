import pygame
import pygame_gui as gui
import os
import sys


class FileError(Exception):
    pass


def load_image(filename, color_key=None):
    fullname = os.path.join('data', filename)

    if not os.path.isfile(fullname):
        raise FileError(f"Файл с изображением '{fullname}' не найден")
    image = pygame.image.load(fullname)
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


def terminate():
    pygame.quit()
    sys.exit()


WATER = 0
GROUND = 1
ICE = 2
PLAYER = 7
ICE_bg = 3
GROUND_bg = 4

GRAY = (150, 150, 150, 255)
BLUE = (0, 0, 255, 255)
BLACK_BLUE = (0, 0, 100, 255)
BROWN = (70, 40, 0, 255)
BLACK_BROWN = (35, 20, 0, 255)
YELLOW = (255, 255, 0, 255)

BLOCKS = {
    GRAY: WATER,
    BROWN: GROUND,
    YELLOW: PLAYER,
    BLUE: ICE,
    BLACK_BLUE: ICE_bg,
    BLACK_BROWN: GROUND_bg
}

MAP_NAME = 'map.png'
pygame.init()
WIDTH, HEIGHT = pygame.display.get_desktop_sizes()[0]
FPS = 60

BLOCK_SIZE = 50
PLAYER_SIZE = 50

CLOCK = pygame.time.Clock()

GROUND_img = load_image('ground.png')
PLAYER_img = load_image('Player.png')
WATER_img = load_image('water.png')
BACKGROUND_img = load_image('all_image(shallow water).png')

FONT_PATH = 'Fonts/font.png'
FONT_IMG_WIDTH = 815
FONT_IMG_HEIGHT = 8
FONT_BLOCK_WIDTH = 5
FONT_BLOCK_HEIGHT = 8
FONT_BARRIER = 1

MAIN_MENU_BUTTON_WIDTH = 130
MAIN_MENU_BUTTON_HEIGHT = 50
MAIN_MENU_BUTTON_X_MARGIN = (WIDTH / 2) - MAIN_MENU_BUTTON_WIDTH * 2 - 45
MAIN_MENU_BUTTON_Y_MARGIN = HEIGHT / 2
MAIN_MENU_BUTTON_SPACING = 30
