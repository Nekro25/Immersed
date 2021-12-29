import pygame


WATER = 0
FIRE = 1
ELSE = 2
PLAYER = 7

BLUE = (0, 0, 255, 255)
BLACK = (0, 0, 0, 0)
RED = (255, 0, 0, 255)
YELLOW = (255, 255, 0, 255)

BLOCKS = {
    BLUE: WATER,
    RED: FIRE,
    BLACK: ELSE
}

MAP_NAME = 'immersed in ice.png'
WIDTH = 1250
HEIGHT = 750
FPS = 60

clock = pygame.time.Clock()
