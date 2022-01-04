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
        self.image = PLAYER_img
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.x = x
        self.y = y
        self.speed = 5
        self.cell_x = 0
        self.cell_y = 0
        self.map_x = x * BLOCK_SIZE
        self.map_y = y * BLOCK_SIZE

    def move_up(self, group):
        self.map_y -= self.speed
        self.rect.y -= self.speed
        if pygame.sprite.spritecollideany(self, group):
            self.rect.y += self.speed
            self.map_y += self.speed
            return
        self.rect.y += self.speed
        self.y = self.map_y // BLOCK_SIZE
        self.cell_y = self.map_y % BLOCK_SIZE

    def move_down(self, group):
        self.map_y += self.speed
        self.rect.y += self.speed * 2
        if pygame.sprite.spritecollideany(self, group):
            self.rect.y -= self.speed * 2
            self.map_y -= self.speed
            return
        self.rect.y -= self.speed
        self.y = self.map_y // BLOCK_SIZE
        self.cell_y = self.map_y % BLOCK_SIZE

    def move_left(self, group):
        self.map_x -= self.speed
        self.rect.x -= self.speed * 2
        if pygame.sprite.spritecollideany(self, group):
            self.rect.x += self.speed * 2
            self.map_x += self.speed
            return
        self.rect.x += self.speed
        self.x = self.map_x // BLOCK_SIZE
        self.cell_x = self.map_x % BLOCK_SIZE

    def move_right(self, group):
        self.map_x += self.speed
        self.rect.x += self.speed * 2
        if pygame.sprite.spritecollideany(self, group):
            self.rect.x -= self.speed * 2
            self.map_x -= self.speed
            return
        self.rect.x -= self.speed
        self.x = self.map_x // BLOCK_SIZE
        self.cell_x = self.map_x % BLOCK_SIZE

    def colliding(self, game_map):
        if (game_map[(self.map_x + PLAYER_SIZE) // BLOCK_SIZE][self.y] or
            game_map[self.map_x // BLOCK_SIZE][self.y] or game_map[self.x][
                (self.map_y + PLAYER_SIZE) // BLOCK_SIZE] or game_map[self.x][
                self.map_y // BLOCK_SIZE]) == GROUND:
            return True
        return False


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


# эта функция перебирает все кординаты вокруг игрока и обновляет только то, что видит игрок,
# благодаря этому игра меньше тормозит и не обрабатывает всю карту
def draw_screen(screen, player, map, camera):
    barier_group = pygame.sprite.Group()
    screen_group = pygame.sprite.Group()
    bg = pygame.sprite.Sprite(screen_group)
    bg.image = pygame.transform.scale(load_image('all_image(shallow water).png'),
                                      (WIDTH, HEIGHT))
    bg.rect = bg.image.get_rect()
    coef_y = 0
    for y in range(player.y - HEIGHT % BLOCK_SIZE // 2 - 1,
                   player.y + HEIGHT % BLOCK_SIZE // 2 + 4):
        coef_x = -3
        for x in range(player.x - WIDTH % BLOCK_SIZE // 2,
                       player.x + HEIGHT % BLOCK_SIZE // 2 + 10):
            if map[x][y] == GROUND:
                block = Block(coef_x, coef_y, GROUND_img, screen_group)
                barier_group.add(block)
            elif map[x][y] == PLAYER:
                block = Block(coef_x, coef_y, WATER_img, screen_group)
            elif map[x][y] == WATER:
                block = Block(coef_x, coef_y, WATER_img, screen_group)
            coef_x += 1
        coef_y += 1
    screen_group.add(bg)
    screen_group.add(player)
    camera.track(player)
    for obj in screen_group:
        if obj != bg:
            camera.update(obj)
    screen_group.draw(screen)
    return barier_group


def game_loop():
    pygame.init()
    pygame.display.set_caption('Immersed')
    size = WIDTH, HEIGHT

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    running = True
    is_main_menu = True

    all_sprites = pygame.sprite.Group()
    barier_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()

    manager = gui.UIManager((WIDTH, HEIGHT))

    game_map, pos = picture_to_matrix()
    player = Player(*pos)
    camera = Camera()

    big_font_picture = pygame.transform.scale(load_image('Fonts/font.png', color_key=(0, 0, 0)), (2586, 48))
    title_font = generate_custom_font(big_font_picture, font, (255, 254, 255),
                                      block_width=30, block_height=48, barrier=6)

    while running:
        tick = CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if any(pygame.key.get_pressed()):
                if pygame.key.get_pressed()[pygame.K_w]:
                    player.move_up(barier_group)
                if pygame.key.get_pressed()[pygame.K_a]:
                    player.move_left(barier_group)
                if pygame.key.get_pressed()[pygame.K_s]:
                    player.move_down(barier_group)
                if pygame.key.get_pressed()[pygame.K_d]:
                    player.move_right(barier_group)
                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    is_main_menu = True

        if is_main_menu:
            is_main_menu = main_menu(screen, manager, title_font)

        player.rect = player.image.get_rect().move(
            WIDTH // BLOCK_SIZE * BLOCK_SIZE // 2 + player.cell_x,
            HEIGHT // BLOCK_SIZE * BLOCK_SIZE // 2 + player.cell_y - PLAYER_SIZE // 2)
        barier_group = draw_screen(screen, player, game_map, camera)

        pygame.display.flip()
    pygame.quit()
