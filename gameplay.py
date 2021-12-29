import pygame
import sys

from CONSTANTS import *
from picture2matrix import picure_to_matrix


def terminate():
    pygame.quit()
    sys.exit()


class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.screen_x = 0  # позиция относительно экрана
        self.screen_y = 0


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, *args):
        super().__init__(*args)
        self.map_x = x
        self.map_y = y
        self.speed = 10
        self.cell_x = 0
        self.cell_y = 0
        self.screen_x = 0
        self.screen_y = 0

    def move_up(self, sprite_group):
        self.cell_y -= self.speed / FPS
        if pygame.sprite.spritecollideany(self, sprite_group):
            self.cell_y += self.speed / FPS

    def move_down(self, sprite_group):
        self.cell_y += self.speed / FPS
        if pygame.sprite.spritecollideany(self, sprite_group):
            self.cell_y -= self.speed / FPS

    def move_left(self, sprite_group):
        self.cell_x -= self.speed / FPS
        if pygame.sprite.spritecollideany(self, sprite_group):
            self.cell_x += self.speed / FPS

    def move_right(self, sprite_group):
        self.cell_x += self.speed / FPS
        if pygame.sprite.spritecollideany(self, sprite_group):
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


def draw_screen(screen, player, map):
    screen_group = pygame.sprite.Group()
    coef_y = 0
    corf_x = 0
    for y in range(player[1] - 8, player[1] + 9):
        for x in range(player[0] - 14, player[0] + 15):
            if map[y][x] == GROUND:
                pass


def game_loop():
    pygame.init()
    pygame.display.set_caption('Name')
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    running = True
    all_sprites = pygame.sprite.Group
    game_map, pos = picure_to_matrix()
    player = Player(*pos)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_w]:
                    player.move_up(all_sprites)
                if pygame.key.get_pressed()[pygame.K_a]:
                    player.move_left(all_sprites)
                if pygame.key.get_pressed()[pygame.K_s]:
                    player.move_down(all_sprites)
                if pygame.key.get_pressed()[pygame.K_d]:
                    player.move_right(all_sprites)
        pygame.display.flip()
    pygame.quit()
