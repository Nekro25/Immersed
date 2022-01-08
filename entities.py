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


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, img, animation, anim_x, anim_y, anim_w, anim_h, *args,
                 bite=False, speed=400):
        super().__init__(*args)
        self.w = anim_w
        self.h = anim_h
        self.frames = []
        self.get_frames(animation, anim_x, anim_y, anim_w, anim_h)
        self.cur_frame_num = 0
        self.cur_frame = None
        self.time = 0
        self.bited = False
        self.speed = speed
        self.x = x
        self.y = y
        self.stay_img = img
        self.frames = []
        self.get_frames(animation, anim_x, anim_y, anim_w, anim_h)
        if bite:
            self.get_bite_frames(animation, anim_x, anim_y, anim_w, anim_h)
        # self.bite_monster_event = pygame.USEREVENT + 3
        # pygame.time.set_timer(self.bite_monster_event, SECOND * 10)
        self.bited = False
        self.image = img
        self.rect = self.image.get_rect().move(self.x, self.y)

    def get_frames(self, sheet, anim_x, anim_y, anim_w, anim_h):
        for i in range(anim_x):
            self.frames.append(sheet.subsurface((anim_w * i, 0, anim_w, anim_h)))
        self.frames_45 = [pygame.transform.rotate(i, 45) for i in self.frames]
        self.frames_90 = [pygame.transform.rotate(i, 90) for i in self.frames]
        self.frames_315 = [pygame.transform.rotate(i, 315) for i in self.frames]
        self.frames_180 = [pygame.transform.flip(i, True, False) for i in self.frames]
        self.frames_225 = [pygame.transform.flip(i, True, False) for i in self.frames_45]
        self.frames_135 = [pygame.transform.flip(i, True, False) for i in self.frames_315]
        self.frames_270 = [pygame.transform.flip(i, True, True) for i in self.frames_90]

    def get_bite_frames(self, sheet, anim_x, anim_y, anim_w, anim_h):
        for i in range(anim_x):
            self.bite_frames.append(sheet.subsurface((anim_w * i, anim_h, anim_w, anim_h)))
        self.bite_frames_45 = [pygame.transform.rotate(i, 45) for i in self.bite_frames]
        self.bite_frames_90 = [pygame.transform.rotate(i, 90) for i in self.bite_frames]
        self.bite_frames_315 = [pygame.transform.rotate(i, 315) for i in self.bite_frames]
        self.bite_frames_180 = [pygame.transform.flip(i, True, False) for i in
                                self.bite_frames]
        self.bite_frames_225 = [pygame.transform.flip(i, True, False) for i in
                                self.bite_frames_45]
        self.bite_frames_135 = [pygame.transform.flip(i, True, False) for i in
                                self.bite_frames_315]
        self.bite_frames_270 = [pygame.transform.flip(i, True, True) for i in
                                self.bite_frames_90]

    def update(self):
        if not self.bited:
            if self.rect.y > HEIGHT // 2 + self.h and self.rect.x > WIDTH // 2 + self.w // 2:
                self.cur_frame = self.frames_315
            elif self.rect.y > HEIGHT // 2 + self.h and self.rect.x < WIDTH // 2 - self.w // 2:
                self.cur_frame = self.frames_135
            elif self.rect.y < HEIGHT // 2 - self.h and self.rect.x > WIDTH // 2 + self.w // 2:
                self.cur_frame = self.frames_45
            elif self.rect.y < HEIGHT // 2 - self.h and self.rect.x < WIDTH // 2 - self.w // 2:
                self.cur_frame = self.frames_225
            elif self.rect.y >= HEIGHT // 2 + self.h:
                self.cur_frame = self.frames_270
            elif self.rect.x >= WIDTH // 2 + self.w // 2:
                self.cur_frame = self.frames
            elif self.rect.y <= HEIGHT // 2 - self.h:
                self.cur_frame = self.frames_90
            else:
                self.cur_frame = self.frames_180
        else:
            if self.rect.y > HEIGHT // 2 + self.h and self.rect.x > WIDTH // 2 + self.w // 2:
                self.cur_frame = self.frames_225
            elif self.rect.y > HEIGHT // 2 + self.h and self.rect.x < WIDTH // 2 - self.w // 2:
                self.cur_frame = self.frames_45
            elif self.rect.y < HEIGHT // 2 - self.h and self.rect.x > WIDTH // 2 + self.w // 2:
                self.cur_frame = self.frames_135
            elif self.rect.y < HEIGHT // 2 - self.h and self.rect.x < WIDTH // 2 - self.w // 2:
                self.cur_frame = self.frames_315
            elif self.rect.y >= HEIGHT // 2 + self.h:
                self.cur_frame = self.frames_90
            elif self.rect.x >= WIDTH // 2 + self.w // 2:
                self.cur_frame = self.frames_180
            elif self.rect.y <= HEIGHT // 2 - self.h:
                self.cur_frame = self.frames_270
            else:
                self.cur_frame = self.frames
        self.cur_frame_num = (self.cur_frame_num + 1) % 5
        self.image = self.cur_frame[self.cur_frame_num]
        self.time += 0.1
        if self.time > 10:
            self.bited = True

    def monster_moving(self, group):
        if self.rect.x >= WIDTH // 2 - self.w // 2:
            if not self.bited:
                self.move_left(group)
            else:
                self.move_right(group)
        if self.rect.y <= HEIGHT // 2 - self.h // 2:
            if not self.bited:
                self.move_down(group)
            else:
                self.move_up(group)
        if self.rect.x < WIDTH // 2 - self.w // 2:
            if not self.bited:
                self.move_right(group)
            else:
                self.move_left(group)
        if self.rect.y > HEIGHT // 2 - self.h // 2:
            if not self.bited:
                self.move_up(group)
            else:
                self.move_down(group)

    def move_up(self, group):
        self.rect.y -= self.speed // FPS
        if pygame.sprite.spritecollideany(self, group):
            self.rect.y += self.speed // FPS

    def move_down(self, group):
        self.rect.y += self.speed // FPS
        if pygame.sprite.spritecollideany(self, group):
            self.rect.y -= self.speed // FPS

    def move_left(self, group):
        self.rect.x -= self.speed // FPS
        if pygame.sprite.spritecollideany(self, group):
            self.rect.x += self.speed // FPS

    def move_right(self, group):
        self.rect.x += self.speed // FPS
        if pygame.sprite.spritecollideany(self, group):
            self.rect.x -= self.speed // FPS


class Creature(pygame.sprite.Sprite):
    def __init__(self, y, x, img, animation, anim_x, anim_y, anim_w, anim_h, *args,
                 bite=False, speed=400, monster=False):
        super().__init__(*args)
        self.stay_img = img
        self.frames = []
        self.get_frames(animation, anim_x, anim_y, anim_w, anim_h)
        self.cur_frame_num = 0
        self.cur_frame = None
        self.image = img
        self.animate_event = pygame.USEREVENT + 2
        pygame.time.set_timer(self.animate_event, SECOND // 10)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.x = int(x)  # позиция на карте по кординатам массива
        self.y = int(y)
        self.speed = speed
        self.cell_x = 0  # позиция относительно клетки внутри которой игрок
        self.cell_y = 0
        self.map_x = int(x) * BLOCK_SIZE  # Позиция относительно всей карты
        self.map_y = int(y) * BLOCK_SIZE

    def get_frames(self, sheet, anim_x, anim_y, anim_w, anim_h):
        for i in range(anim_y):
            for j in range(anim_x):
                self.frames.append(
                    sheet.subsurface((anim_w * j, anim_h * i, anim_w, anim_h)))
        self.frames_45 = [pygame.transform.rotate(i, 45) for i in self.frames]
        self.frames_90 = [pygame.transform.rotate(i, 90) for i in self.frames]
        self.frames_315 = [pygame.transform.rotate(i, 315) for i in self.frames]
        self.frames_180 = [pygame.transform.flip(i, True, False) for i in self.frames]
        self.frames_225 = [pygame.transform.flip(i, True, False) for i in self.frames_45]
        self.frames_135 = [pygame.transform.flip(i, True, False) for i in self.frames_315]
        self.frames_270 = [pygame.transform.flip(i, True, True) for i in self.frames_90]

    # def get_bite_frames(self, sheet, anim_x, anim_y, anim_w, anim_h):
    #     for i in range(anim_x):
    #         for j in range(1, anim_y):
    #             self.bite_frames.append(
    #                 sheet.subsurface((anim_w * j, anim_h * i, anim_w, anim_h)))
    #     self.bite_frames_45 = [pygame.transform.rotate(i, 45) for i in self.bite_frames]
    #     self.bite_frames_90 = [pygame.transform.rotate(i, 90) for i in self.bite_frames]
    #     self.bite_frames_315 = [pygame.transform.rotate(i, 315) for i in self.bite_frames]
    #     self.bite_frames_180 = [pygame.transform.flip(i, True, False) for i in
    #                             self.bite_frames]
    #     self.bite_frames_225 = [pygame.transform.flip(i, True, False) for i in
    #                             self.bite_frames_45]
    #     self.bite_frames_135 = [pygame.transform.flip(i, True, False) for i in
    #                             self.bite_frames_315]
    #     self.bite_frames_270 = [pygame.transform.flip(i, True, True) for i in
    #                             self.bite_frames_90]

    def update(self, dict):
        if any(dict.values()):
            if dict[pygame.K_w] and dict[pygame.K_a]:
                self.cur_frame = self.frames_315
            elif dict[pygame.K_w] and dict[pygame.K_d]:
                self.cur_frame = self.frames_135
            elif dict[pygame.K_s] and dict[pygame.K_a]:
                self.cur_frame = self.frames_45
            elif dict[pygame.K_s] and dict[pygame.K_d]:
                self.cur_frame = self.frames_225
            elif dict[pygame.K_w]:
                self.cur_frame = self.frames_270
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
            self.image = self.stay_img

    # def monster_moving(self, group, player):
    #     if player.x < self.x:
    #         if not self.bited:
    #             self.move_left(group)
    #         else:
    #             self.move_right(group)
    #     if player.y > self.y:
    #         if not self.bited:
    #             self.move_down(group)
    #         else:
    #             self.move_up(group)
    #     if player.x > self.x:
    #         if not self.bited:
    #             self.move_right(group)
    #         else:
    #             self.move_left(group)
    #     if player.y < self.y:
    #         if not self.bited:
    #             self.move_up(group)
    #         else:
    #             self.move_down(group)

    # движение игрока в пространстве
    def move_up(self, group, monster):
        self.map_y -= self.speed / FPS
        self.rect.y -= self.speed // 50
        if pygame.sprite.spritecollideany(self, group):
            self.rect.y += self.speed // 50
            self.map_y += self.speed / FPS
            return
        self.rect.y += self.speed // 50
        self.y = int(self.map_y) // BLOCK_SIZE
        self.cell_y = int(self.map_y) % BLOCK_SIZE
        if monster:
            monster.rect.y += self.speed // FPS + 1

    def move_down(self, group, monster):
        self.map_y += self.speed / FPS
        self.rect.y += self.speed // 50
        if pygame.sprite.spritecollideany(self, group):
            self.rect.y -= self.speed // 50
            self.map_y -= self.speed / FPS
            return
        self.rect.y -= self.speed // 50
        self.y = int(self.map_y) // BLOCK_SIZE
        self.cell_y = int(self.map_y) % BLOCK_SIZE
        if monster:
            monster.rect.y -= self.speed // FPS + 1

    def move_left(self, group, monster):
        self.map_x -= self.speed / FPS
        self.rect.x -= self.speed // 50
        if pygame.sprite.spritecollideany(self, group):
            self.rect.x += self.speed // 50
            self.map_x += self.speed / FPS
            return
        self.rect.x += self.speed // 50
        self.x = int(self.map_x) // BLOCK_SIZE
        self.cell_x = int(self.map_x) % BLOCK_SIZE
        if monster:
            monster.rect.x += self.speed // FPS + 1

    def move_right(self, group, monster):
        self.map_x += self.speed / FPS
        self.rect.x += self.speed // 50
        if pygame.sprite.spritecollideany(self, group):
            self.rect.x -= self.speed // 50
            self.map_x -= self.speed / FPS
            return
        self.rect.x -= self.speed // 50
        self.x = int(self.map_x) // BLOCK_SIZE
        self.cell_x = int(self.map_x) % BLOCK_SIZE
        if monster:
            monster.rect.x -= self.speed // FPS + 1


class Structure(pygame.sprite.Sprite):
    def __init__(self, x, y, img, *args, ship_num=None):
        super().__init__(*args)
        self.x = x
        self.y = y
        self.ship_num = ship_num
        self.image = img
        self.rect = self.image.get_rect().move(50 * self.x, 50 * self.y)
