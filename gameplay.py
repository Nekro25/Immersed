import pygame
import sys

from CONSTANTS import *
from picture2matrix import picture_to_matrix
from wallpapers import *


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, img, *args):
        super().__init__(*args)
        self.x = x
        self.y = y
        self.image = img
        self.rect = self.image.get_rect().move(50 * self.x, 50 * self.y)
        self.screen_x = 0  # позиция относительно экрана
        self.screen_y = 0


class Player(pygame.sprite.Sprite):
    def __init__(self, y, x, *args):
        super().__init__(*args)
        self.x = x
        self.y = y
        self.speed = 10
        self.cell_x = 600
        self.cell_y = 350
        self.screen_x = 0
        self.screen_y = 0
        self.image = PLAYER_img
        self.rect = self.image.get_rect().move(600, 350)

    def move_up(self, sprite_group):
        self.cell_y -= self.speed
        if pygame.sprite.spritecollideany(self, sprite_group):
            self.cell_y += self.speed

    def move_down(self, sprite_group):
        self.cell_y += self.speed
        if pygame.sprite.spritecollideany(self, sprite_group):
            self.cell_y -= self.speed

    def move_left(self, sprite_group):
        self.cell_x -= self.speed
        if pygame.sprite.spritecollideany(self, sprite_group):
            self.cell_x += self.speed

    def move_right(self, sprite_group):
        self.cell_x += self.speed
        if pygame.sprite.spritecollideany(self, sprite_group):
            self.cell_x -= self.speed


class Camera:
    def __init__(self):
        self.x_coef = 0  # коэффициент для выравнивания по камере
        self.y_coef = 0

    def update(self, object):
        object.x += self.x_coef
        object.y += self.y_coef

    def track(self, object):
        self.x_coef = WIDTH // 2 - object.x
        self.y_coef = HEIGHT // 2 - object.y


def draw_screen(screen, player, map):
    screen_group = pygame.sprite.Group()
    bg = pygame.sprite.Sprite(screen_group)
    bg.image = pygame.transform.scale(load_image('all_image(shallow water).png'),
                                      (1250, 750))
    bg.rect = bg.image.get_rect()
    coef_y = -1  # расположение относительно экрана
    for y in range(player.y - 8, player.y + 9):
        coef_x = -2
        for x in range(player.x - 14, player.x + 15):
            if map[x][y] == GROUND:
                block = Block(coef_x, coef_y, GROUND_img, screen_group)
            elif map[x][y] == PLAYER:
                block = Block(coef_x, coef_y, WATER_img, screen_group)
            elif map[x][y] == WATER:
                block = Block(coef_x, coef_y, WATER_img, screen_group)
            coef_x += 1
        coef_y += 1
    screen_group.add(player)
    screen_group.draw(screen)


def game_loop():
    pygame.init()
    pygame.display.set_caption('Immersed')
    size = WIDTH, HEIGHT

    screen = pygame.display.set_mode(size)

    running = True
    is_main_menu = True

    all_sprites = pygame.sprite.Group()
    ground_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()

    game_map, pos = picture_to_matrix()
    player = Player(*pos)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_w]:
                    player.move_up(ground_group)
                if pygame.key.get_pressed()[pygame.K_a]:
                    player.move_left(ground_group)
                if pygame.key.get_pressed()[pygame.K_s]:
                    player.move_down(ground_group)
                if pygame.key.get_pressed()[pygame.K_d]:
                    player.move_right(ground_group)

            if is_main_menu:
                main_menu(event, screen)

            MANAGER.process_events(event)
        MANAGER.update()
        player.rect = player.image.get_rect().move(player.cell_x, player.cell_y)
        draw_screen(screen, player, game_map)

        pygame.display.flip()
    pygame.quit()
