import pygame
import sys

from CONSTANTS import *


def terminate():
    pygame.quit()
    sys.exit()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, *args):
        super().__init__(*args)
        self.map_x = x
        self.map_y = y
        self.speed = 10
        self.cell_x = 0
        self.cell_y = 0

    def move_up(self):
        global all_sprites
        self.cell_y -= self.speed / FPS
        if pygame.sprite.spritecollideany(self, all_sprites):
            self.cell_y += self.speed / FPS

    def move_down(self):
        global all_sprites
        self.cell_y += self.speed / FPS
        if pygame.sprite.spritecollideany(self, all_sprites):
            self.cell_y -= self.speed / FPS

    def move_left(self):
        global all_sprites
        self.cell_x -= self.speed / FPS
        if pygame.sprite.spritecollideany(self, all_sprites):
            self.cell_x += self.speed / FPS

    def move_right(self):
        global all_sprites
        self.cell_x += self.speed / FPS
        if pygame.sprite.spritecollideany(self, all_sprites):
            self.cell_x -= self.speed / FPS


class Camera:
    def __init__(self):
        self.x_coef = 0
        self.y_coef = 0

    def update(self, object):
        object.x += self.x_coef
        object.y += self.y_coef

    def track(self, object):
        self.x_coef = WIDTH // 2 - object.x
        self.y_coef = HEIGHT // 2 - object.y


def game_loop():
    pygame.init()
    pygame.display.set_caption('Name')
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    running = True
    all_sprites = pygame.sprite.Group
    player = Player(500, 200)
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
    pygame.quit()
