import pygame
import pygame_gui as gui
import os
import sys
import sqlite3


class FileError(Exception):
    pass


def load_image(filename, color_key=None):
    fullname = os.path.join('data', filename)

    if not os.path.isfile(fullname):
        raise FileError(f"Файл с изображением '{fullname}' не найден")
    image = pygame.image.load(fullname)
    if color_key:
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
OXYGEN_FILLER = 5
REACTOR = 6

GRAY = (150, 150, 150, 255)
BLUE = (0, 0, 255, 255)
BLACK_BLUE = (0, 0, 100, 255)
BROWN = (70, 40, 0, 255)
BLACK_BROWN = (35, 20, 0, 255)
YELLOW = (255, 255, 0, 255)
BLACK_RED = (125, 0, 0, 255)
DIRTY_GREEN = (70, 70, 0, 255)

BLOCKS = {
    GRAY: WATER,
    BROWN: GROUND,
    YELLOW: PLAYER,
    BLUE: ICE,
    BLACK_BLUE: ICE_bg,
    BLACK_BROWN: GROUND_bg,
    BLACK_RED: REACTOR,
    DIRTY_GREEN: OXYGEN_FILLER
}

MAP_NAME = 'map.png'
pygame.init()
WIDTH, HEIGHT = pygame.display.get_desktop_sizes()[0]
FPS = 60

BLOCK_SIZE = 50
PLAYER_SIZE = 50
SECOND = 1000

CLOCK = pygame.time.Clock()

GROUND_img = load_image('ground.png')
PLAYER_img = load_image('Player.png')
WATER_img = load_image('water.png')
BACKGROUND_img = load_image('all_image(shallow water).png')
LIFEBAR_img = load_image('lifebar.png')
ICE_img = load_image('ice.png')
ICE_CAVE_BG_img = load_image('ice_cave_background.png')
GROUND_CAVE_BG_img = load_image('cave_background.png')
OXYGEN_FILLER_img = load_image('oxygen_filler.png')
REACTOR_img = load_image('reactor.png')
EMPTY_DISPLAY_img = load_image('empty_display.png')
PLAYER_ANIMATION_img = load_image('player_animation.png')

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

CON = sqlite3.connect('game_data.db')
CURSOR = CON.cursor()

DISPLAY_FRAMES = [load_image('Display_images/darkened_display_1.png'),
                  load_image('Display_images/darkened_display_2.png'),
                  load_image('Display_images/darkened_display_3.png'),
                  load_image('Display_images/darkened_display_4.png'),
                  load_image('Display_images/darkened_display_5.png'),
                  load_image('Display_images/darkened_display_6.png'),
                  load_image('Display_images/darkened_display_7.png'),
                  load_image('Display_images/darkened_display_8.png'),
                  load_image('Display_images/darkened_display_9.png'),
                  load_image('Display_images/darkened_display_10.png'),
                  load_image('Display_images/darkened_display_11.png'),
                  load_image('Display_images/darkened_display_12.png'),
                  load_image('Display_images/darkened_display_13.png'),
                  load_image('Display_images/darkened_display_14.png'),
                  load_image('Display_images/darkened_display_15.png'),
                  load_image('Display_images/darkened_display_16.png'),
                  load_image('Display_images/darkened_display_17.png'),
                  load_image('Display_images/darkened_display_18.png'),
                  load_image('Display_images/darkened_display_19.png'),
                  load_image('Display_images/darkened_display_20.png'),
                  load_image('Display_images/darkened_display_21.png'),
                  load_image('Display_images/darkened_display_22.png'),
                  load_image('Display_images/darkened_display_23.png'),
                  ]
