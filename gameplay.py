import pygame
import sys


def terminate():
    pygame.quit()
    sys.exit()


def game_loop():
    pygame.init()
    pygame.display.set_caption('Name')
    size = width, height = 1250, 750
    screen = pygame.display.set_mode(size)
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
    pygame.quit()
