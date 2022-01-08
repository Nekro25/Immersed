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
        self.frames = []
        self.get_frames(PLAYER_ANIMATION_img, 5, 50)
        self.cur_frame_num = 0
        self.cur_frame = None
        self.image = PLAYER_img
        self.animate_event = pygame.USEREVENT + 2
        pygame.time.set_timer(self.animate_event, SECOND // 10)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.x = int(x)  # позиция на карте по кординатам массива
        self.y = int(y)
        self.speed = 800
        self.cell_x = 0  # позиция относительно клетки внутри которой игрок
        self.cell_y = 0
        self.map_x = int(x) * BLOCK_SIZE  # Позиция относительно всей карты
        self.map_y = int(y) * BLOCK_SIZE

    def get_frames(self, sheet, length, size):
        self.rect = pygame.Rect(0, 0, size, size)
        for i in range(length):
            self.frames.append(sheet.subsurface((size * i, 0, size, size)))
        self.frames_45 = [pygame.transform.rotate(i, 45) for i in self.frames]
        self.frames_90 = [pygame.transform.rotate(i, 90) for i in self.frames]
        self.frames_315 = [pygame.transform.rotate(i, 315) for i in self.frames]
        self.frames_180 = [pygame.transform.flip(i, True, False) for i in self.frames]
        self.frames_135 = [pygame.transform.flip(i, True, False) for i in self.frames_45]
        self.frames_225 = [pygame.transform.flip(i, True, False) for i in self.frames_315]
        self.frames_275 = [pygame.transform.flip(i, True, True) for i in self.frames_90]

    def update(self, dict):
        if any(dict.values()):
            if dict[pygame.K_w] and dict[pygame.K_a]:
                self.cur_frame = self.frames_315
            elif dict[pygame.K_w] and dict[pygame.K_d]:
                self.cur_frame = self.frames_225
            elif dict[pygame.K_s] and dict[pygame.K_a]:
                self.cur_frame = self.frames_45
            elif dict[pygame.K_s] and dict[pygame.K_d]:
                self.cur_frame = self.frames_135
            elif dict[pygame.K_w]:
                self.cur_frame = self.frames_275
            elif dict[pygame.K_a]:
                self.cur_frame = self.frames
            elif dict[pygame.K_s]:
                self.cur_frame = self.frames_90
            elif dict[pygame.K_d]:
                self.cur_frame = self.frames_180
        else:
            self.cur_frame = None
        if self.cur_frame:
            self.cur_frame_num = (self.cur_frame_num + 1) % 5
            self.image = self.cur_frame[self.cur_frame_num]
        else:
            self.image = PLAYER_img

    # движение игрока в пространстве
    def move_up(self, group):
        self.map_y -= self.speed / FPS
        self.rect.y -= self.speed // 50
        if pygame.sprite.spritecollideany(self, group):
            self.rect.y += self.speed // 50
            self.map_y += self.speed / FPS
            return
        self.rect.y += self.speed // 50
        self.y = int(self.map_y) // BLOCK_SIZE
        self.cell_y = int(self.map_y) % BLOCK_SIZE

    def move_down(self, group):
        self.map_y += self.speed / FPS
        self.rect.y += self.speed // 50
        if pygame.sprite.spritecollideany(self, group):
            self.rect.y -= self.speed // 50
            self.map_y -= self.speed / FPS
            return
        self.rect.y -= self.speed // 50
        self.y = int(self.map_y) // BLOCK_SIZE
        self.cell_y = int(self.map_y) % BLOCK_SIZE

    def move_left(self, group):
        self.map_x -= self.speed / FPS
        self.rect.x -= self.speed // 50
        if pygame.sprite.spritecollideany(self, group):
            self.rect.x += self.speed // 50
            self.map_x += self.speed / FPS
            return
        self.rect.x += self.speed // 50
        self.x = int(self.map_x) // BLOCK_SIZE
        self.cell_x = int(self.map_x) % BLOCK_SIZE

    def move_right(self, group):
        self.map_x += self.speed / FPS
        self.rect.x += self.speed // 50
        if pygame.sprite.spritecollideany(self, group):
            self.rect.x -= self.speed // 50
            self.map_x -= self.speed / FPS
            return
        self.rect.x -= self.speed // 50
        self.x = int(self.map_x) // BLOCK_SIZE
        self.cell_x = int(self.map_x) % BLOCK_SIZE


class Structure(pygame.sprite.Sprite):
    def __init__(self, x, y, img, *args, ship_num=None):
        super().__init__(*args)
        self.x = x
        self.y = y
        self.ship_num = ship_num
        self.image = img
        self.rect = self.image.get_rect().move(50 * self.x, 50 * self.y)
