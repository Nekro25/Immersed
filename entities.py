import pygame
from CONSTANTS import *


class Camera:
    def __init__(self):
        self.x_coef = 0  # коэффициент для выравнивания по камере
        self.y_coef = 0

    def update(self, object):
        object.rect.x -= self.x_coef
        object.rect.y -= self.y_coef

    def track(self, object):
        self.x_coef = object.cell_x
        self.y_coef = object.cell_y


class Player(pygame.sprite.Sprite):
    def __init__(self, y, x, *args):
        super().__init__(*args)
        self.image = PLAYER_img
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.x = int(x)  # позиция на карте по кординатам массива
        self.y = int(y)
        self.speed = 300
        self.cell_x = 0  # позиция относительно клетки внутри которой игрок
        self.cell_y = 0
        self.map_x = int(x) * BLOCK_SIZE  # Позиция относительно всей карты
        self.map_y = int(y) * BLOCK_SIZE

    # движение игрока в пространстве
    def move_up(self, group):
        self.map_y -= self.speed / FPS
        self.rect.y -= self.speed // 30
        if pygame.sprite.spritecollideany(self, group):
            self.rect.y += self.speed // 30
            self.map_y += self.speed / FPS
            return
        self.rect.y += self.speed // 30
        self.y = int(self.map_y) // BLOCK_SIZE
        self.cell_y = int(self.map_y) % BLOCK_SIZE

    def move_down(self, group):
        self.map_y += self.speed / FPS
        self.rect.y += self.speed // 30
        if pygame.sprite.spritecollideany(self, group):
            self.rect.y -= self.speed // 30
            self.map_y -= self.speed / FPS
            return
        self.rect.y -= self.speed // 30
        self.y = int(self.map_y) // BLOCK_SIZE
        self.cell_y = int(self.map_y) % BLOCK_SIZE

    def move_left(self, group):
        self.map_x -= self.speed / FPS
        self.rect.x -= self.speed // 30
        if pygame.sprite.spritecollideany(self, group):
            self.rect.x += self.speed // 30
            self.map_x += self.speed / FPS
            return
        self.rect.x += self.speed // 30
        self.x = int(self.map_x) // BLOCK_SIZE
        self.cell_x = int(self.map_x) % BLOCK_SIZE

    def move_right(self, group):
        self.map_x += self.speed / FPS
        self.rect.x += self.speed // 30
        if pygame.sprite.spritecollideany(self, group):
            self.rect.x -= self.speed // 30
            self.map_x -= self.speed / FPS
            return
        self.rect.x -= self.speed // 30
        self.x = int(self.map_x) // BLOCK_SIZE
        self.cell_x = int(self.map_x) % BLOCK_SIZE


class Structure(pygame.sprite.Sprite):
    def __init__(self, x, y, img, *args):
        super().__init__(*args)
        self.x = x
        self.y = y
        self.image = img
        self.rect = self.image.get_rect().move(50 * self.x, 50 * self.y)
