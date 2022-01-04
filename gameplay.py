import pygame
import sys

from CONSTANTS import *
from picture2matrix import picture_to_matrix
from wallpapers import *

buttons_pressed = {pygame.K_w: False, pygame.K_a: False, pygame.K_s: False,
                   pygame.K_d: False}


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, img, *args):
        super().__init__(*args)
        self.x = x
        self.y = y
        self.image = img
        self.rect = self.image.get_rect().move(50 * self.x, 50 * self.y)


class Player(pygame.sprite.Sprite):
    def __init__(self, y, x, *args):
        super().__init__(*args)
        self.image = PLAYER_img
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.x = x
        self.y = y
        self.speed = 300
        self.cell_x = 0
        self.cell_y = 0
        self.map_x = x * BLOCK_SIZE
        self.map_y = y * BLOCK_SIZE

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
def draw_screen(screen, player, map, camera, bg):
    barrier_group = pygame.sprite.Group()
    screen_group = pygame.sprite.Group(bg, player)
    coef_y = 0
    for y in range(player.y - HEIGHT % BLOCK_SIZE // 2 - 1,
                   player.y + HEIGHT % BLOCK_SIZE // 2 + 4):
        coef_x = -3
        for x in range(player.x - WIDTH % BLOCK_SIZE // 2,
                       player.x + HEIGHT % BLOCK_SIZE // 2 + 10):
            if map[x][y] == GROUND:
                barrier_group.add(Block(coef_x, coef_y, GROUND_img, screen_group))
            elif map[x][y] == PLAYER:
                Block(coef_x, coef_y, WATER_img, screen_group)
            elif map[x][y] == WATER:
                Block(coef_x, coef_y, WATER_img, screen_group)
            coef_x += 1
        coef_y += 1
    camera.track(player)
    for obj in screen_group:
        if obj != bg:
            camera.update(obj)
    screen_group.draw(screen)
    return barrier_group


def moving(dict, group, player):
    if dict[pygame.K_a]:
        player.move_left(group)
    if dict[pygame.K_s]:
        player.move_down(group)
    if dict[pygame.K_d]:
        player.move_right(group)
    if dict[pygame.K_w]:
        player.move_up(group)


def game_loop():
    pygame.init()
    pygame.display.set_caption('Immersed')

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    running = True
    is_main_menu = True

    barrier_group = pygame.sprite.Group()

    game_map, pos = picture_to_matrix()
    player = Player(*pos)
    camera = Camera()
    bg = pygame.sprite.Sprite()
    bg.image = BACKGROUND_img
    bg.rect = bg.image.get_rect()

    # ---- ресурсы для главного меню ----
    manager = gui.UIManager((WIDTH, HEIGHT))
    big_font_picture = pygame.transform.scale(load_image('Fonts/font.png', color_key=(0, 0, 0)), (2586, 48))
    title_font = generate_custom_font(big_font_picture, font, (255, 254, 255),
                                      block_width=30, block_height=48, barrier=6)
    background = load_image('all_image(shallow water).png')
    # 231 - половина длины надписи "IMMERSED" в пикселях
    render_text("IMMERSED", (WIDTH / 2) - 231, HEIGHT / 3.5, 60, 1000, title_font, background)
    # ---- ресурсы для главного меню ----

    main_menu(screen, manager, background)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    buttons_pressed[pygame.K_w] = True
                if event.key == pygame.K_a:
                    buttons_pressed[pygame.K_a] = True
                if event.key == pygame.K_s:
                    buttons_pressed[pygame.K_s] = True
                if event.key == pygame.K_d:
                    buttons_pressed[pygame.K_d] = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    buttons_pressed[pygame.K_w] = False
                if event.key == pygame.K_a:
                    buttons_pressed[pygame.K_a] = False
                if event.key == pygame.K_s:
                    buttons_pressed[pygame.K_s] = False
                if event.key == pygame.K_d:
                    buttons_pressed[pygame.K_d] = False
                if event.key == pygame.K_ESCAPE:
                    main_menu(screen, manager, background)

        # if is_main_menu:
        #     is_main_menu = main_menu(screen, manager, background)

        moving(buttons_pressed, barrier_group, player)

        player.rect.x = WIDTH // BLOCK_SIZE * BLOCK_SIZE // 2 + player.cell_x
        player.rect.y = HEIGHT // BLOCK_SIZE * BLOCK_SIZE // 2 + player.cell_y - PLAYER_SIZE // 2
        barrier_group = draw_screen(screen, player, game_map, camera, bg)

        CLOCK.tick(FPS)
        pygame.display.flip()
    pygame.quit()
