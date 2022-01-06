import pygame
import sys

from CONSTANTS import *
from picture2matrix import picture_to_matrix
from wallpapers import *
from interface import *
from data_base import *
from entities import *

buttons_pressed = {pygame.K_w: False, pygame.K_a: False, pygame.K_s: False,
                   pygame.K_d: False}


# эта функция перебирает все кординаты вокруг игрока и обновляет только то, что видит игрок,
# благодаря этому игра меньше тормозит и не обрабатывает всю карту
def draw_screen(screen, player, map, camera, lifebar, bg):
    barrier = pygame.sprite.Group()
    oxygen_group = pygame.sprite.Group()
    screen_group = pygame.sprite.Group()
    coef_y = 0
    for y in range(player.y - HEIGHT % BLOCK_SIZE // 2 - 1,
                   player.y + HEIGHT % BLOCK_SIZE // 2 + 4):
        coef_x = -3
        for x in range(player.x - WIDTH % BLOCK_SIZE // 2,
                       player.x + HEIGHT % BLOCK_SIZE // 2 + 10):
            if 0 <= y <= 249 and 0 <= x <= 499:
                if map[x][y] == GROUND:
                    barrier.add(Structure(coef_x, coef_y, GROUND_img, screen_group))
                elif map[x][y] == ICE:
                    barrier.add(Structure(coef_x, coef_y, ICE_img, screen_group))
                elif map[x][y] == ICE_bg:
                    bg = ICE_CAVE_BG_img
                elif map[x][y] == WATER:
                    bg = BACKGROUND_img
                elif map[x][y] == GROUND_bg:
                    bg = GROUND_CAVE_BG_img
                elif map[x][y] == OXYGEN_FILLER:
                    Structure(coef_x - 3, coef_y - 3, OXYGEN_FILLER_img, screen_group,
                              oxygen_group)
                    # здесь -3 тк это объект блольше чем обычный блок
                elif map[x][y] == REACTOR:
                    Structure(coef_x - 3, coef_y - 5, REACTOR_img, screen_group, oxygen_group)
            coef_x += 1
        coef_y += 1
    screen_group.add(player)
    camera.track(player)
    for obj in screen_group:
        camera.update(obj)
    screen_group.add(lifebar.draw_ox_lvl())
    screen_group.add(lifebar.draw_hp_lvl())
    screen_group.add(lifebar)
    screen_group.draw(screen)
    return barrier, screen_group, bg, oxygen_group


# функция проверяет нажатие клавишь и передвигает персонажа
def moving(group, player):
    global buttons_pressed
    if buttons_pressed[pygame.K_a]:
        player.move_left(group)
    if buttons_pressed[pygame.K_s]:
        player.move_down(group)
    if buttons_pressed[pygame.K_d]:
        player.move_right(group)
    if buttons_pressed[pygame.K_w]:
        player.move_up(group)


# Игровой цикл
def game_loop():
    pygame.init()
    pygame.display.set_caption('Immersed')

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # ---- ресурсы для главного меню ----
    big_font_picture = pygame.transform.scale(
        load_image(FONT_PATH, color_key=(0, 0, 0)),
        (FONT_IMG_WIDTH * 6, FONT_IMG_HEIGHT * 6)
    )
    title_font = generate_custom_font(big_font_picture, font, (255, 254, 255),
                                      block_width=FONT_BLOCK_WIDTH * 6,
                                      block_height=FONT_BLOCK_HEIGHT * 6,
                                      barrier=FONT_BARRIER * 6)

    background = load_image('all_image(shallow water).png')

    # 231 - половина длины надписи "IMMERSED" в пикселях
    render_text("IMMERSED", (WIDTH / 2) - 231, HEIGHT / 3.5, 60, 1000, title_font,
                background)

    # ---- ресурсы для главного меню ----
    # позиция игрока, количество кислорода, количество здоровья,
    # [корабль1, корабль2, корабль3, неизвестный реактор]
    pos, ox, hp, progress = main_menu(screen, background)

    running = True

    game_map = picture_to_matrix()
    camera = Camera()
    player = Player(*pos)
    lifebar = LifeBar(ox, hp)

    bg = BACKGROUND_img

    while running:

        player.rect.x = WIDTH // BLOCK_SIZE * BLOCK_SIZE // 2 + player.cell_x
        player.rect.y = HEIGHT // BLOCK_SIZE * BLOCK_SIZE // 2 + player.cell_y - PLAYER_SIZE // 2
        screen.blit(bg, (-player.x, -player.y))

        barrier_group, screen_group, bg, oxygen_group = draw_screen(screen, player,
                                                                    game_map, camera,
                                                                    lifebar, bg)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            # благодаря разделению игрок движется плавно а не рывками
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
                    new_save(player.y, player.x, lifebar.oxygen_lvl, lifebar.health_lvl,
                             progress)
                    pos, ox, hp, progress = main_menu(screen, background)
                    player = Player(*pos)
                    lifebar.oxygen_lvl = ox
                    lifebar.health_lvl = hp

            if event.type == lifebar.oxygen_event:
                lifebar.oxygen_lvl -= 1
        if pygame.sprite.spritecollideany(player, oxygen_group):
            lifebar.oxygen_lvl = 100
        moving(barrier_group, player)
        for i in screen_group:  # оптимизация
            i.kill()
        CLOCK.tick(FPS)
        pygame.display.flip()
    pygame.quit()
