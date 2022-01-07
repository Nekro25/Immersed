import pygame
import sys

from CONSTANTS import *
from picture2matrix import picture_to_matrix
# from wallpapers import *
from interface import *
from data_base import *
from entities import *

buttons_pressed = {pygame.K_w: False, pygame.K_a: False, pygame.K_s: False,
                   pygame.K_d: False}


# эта функция перебирает все кординаты вокруг игрока и обновляет только то, что видит игрок,
# благодаря этому игра меньше тормозит и не обрабатывает всю карту
def draw_screen(screen, player, map, camera, lifebar):
    barrier = pygame.sprite.Group()
    oxygen_group = pygame.sprite.Group()
    screen_group = pygame.sprite.Group()
    coef_y = -10
    for y in range(player.y - HEIGHT // BLOCK_SIZE // 2 - 10,
                   player.y + HEIGHT // BLOCK_SIZE // 2 + 10):
        coef_x = -10
        for x in range(player.x - WIDTH // BLOCK_SIZE // 2 - 10,
                       player.x + WIDTH // BLOCK_SIZE // 2 + 10):
            if 0 <= y <= 249 and 0 <= x <= 499:
                if map[x][y] == GROUND:
                    barrier.add(Structure(coef_x, coef_y, GROUND_img, screen_group))
                elif map[x][y] == ICE:
                    barrier.add(Structure(coef_x, coef_y, ICE_img, screen_group))
                elif map[x][y] == OXYGEN_FILLER:
                    Structure(coef_x - 3, coef_y - 3, OXYGEN_FILLER_img, screen_group,
                              oxygen_group)
                    # здесь -3 тк это объект блольше чем обычный блок
                elif map[x][y] == REACTOR:
                    Structure(coef_x - 3, coef_y - 5, REACTOR_img, screen_group,
                              oxygen_group)
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
    return barrier, screen_group, oxygen_group


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


def check_background(player, map):
    if map[player.x][player.y] == (ICE_bg or ICE):
        return ICE_CAVE_BG_img
    elif map[player.x][player.y] == WATER:
        return BACKGROUND_img
    elif map[player.x][player.y] == (GROUND_bg or GROUND):
        return GROUND_CAVE_BG_img
    else:
        return BACKGROUND_img


# Игровой цикл
def game_loop():
    pygame.init()
    pygame.display.set_caption('Immersed')

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    from wallpapers import main_menu, render_text
    from ready_fonts import title_font

    # ---- ресурсы для главного меню ----

    # 231 - половина длины надписи "IMMERSED" в пикселях
    render_text("IMMERSED", WIDTH / 2 - 231, HEIGHT / 3.5, 60, 1000, title_font,
                MAIN_MENU_BACKGROUND_img)
    # ---- ресурсы для главного меню ----

    # позиция игрока, количество кислорода, количество здоровья,
    # [корабль1, корабль2, корабль3, неизвестный реактор]
    pos, ox, hp, progress = main_menu(screen)

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

        barrier_group, screen_group, oxygen_group = draw_screen(screen, player,
                                                                    game_map, camera,
                                                                    lifebar)

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

            if event.type == player.animate_event:
                player.update(buttons_pressed)
        if pygame.sprite.spritecollideany(player, oxygen_group):
            lifebar.oxygen_lvl = 100
        moving(barrier_group, player)

        bg = check_background(player, game_map)

        for i in screen_group:  # оптимизация
            i.kill()
        CLOCK.tick(FPS)
        pygame.display.flip()
    pygame.quit()
