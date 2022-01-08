import pygame
import sys

from CONSTANTS import *
from picture2matrix import picture_to_matrix
# from wallpapers import *
from interface import *
from data_base import *
from entities import *

from ready_fonts import *

buttons_pressed = {pygame.K_w: False, pygame.K_a: False, pygame.K_s: False,
                   pygame.K_d: False}
previous_bg = None


# эта функция перебирает все кординаты вокруг игрока и обновляет только то, что видит игрок,
# благодаря этому игра меньше тормозит и не обрабатывает всю карту
def draw_screen(screen, player, map, camera, lifebar):
    barrier = pygame.sprite.Group()
    oxygen_group = pygame.sprite.Group()
    screen_group = pygame.sprite.Group()
    top_sprites = list()
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
                    top_sprites.append(
                        Structure(coef_x - 3, coef_y - 3, OXYGEN_FILLER_img, oxygen_group))
                    # здесь -3 тк это объект блольше чем обычный блок
                elif map[x][y] == REACTOR:
                    Structure(coef_x - 3, coef_y - 5, REACTOR_img, screen_group,
                              oxygen_group, ship_num=5)
                elif map[x][y] == MAIN_SHIP:
                    top_sprites.append(
                        Structure(coef_x - 5, coef_y - 2, MAIN_SHIP_img, oxygen_group,
                                  ship_num=0))
                elif map[x][y] == SHIP_1:
                    top_sprites.append(
                        Structure(coef_x - 4, coef_y - 2, SHIP_1_img, oxygen_group,
                                  ship_num=1))
                elif map[x][y] == SHIP_2:
                    top_sprites.append(
                        Structure(coef_x - 5, coef_y - 1, SHIP_2_img, oxygen_group,
                                  ship_num=2))
                elif map[x][y] == SHIP_3:
                    top_sprites.append(
                        Structure(coef_x - 13, coef_y - 7, SHIP_3_img, oxygen_group,
                                  ship_num=3))
                elif map[x][y] == SHIP_4:
                    top_sprites.append(
                        Structure(coef_x - 15, coef_y - 10, SHIP_4_img, oxygen_group,
                                  ship_num=4))
            coef_x += 1
        coef_y += 1
    for i in top_sprites:
        screen_group.add(i)
    screen_group.add(player)
    camera.track(player)
    for obj in screen_group:
        camera.update(obj)
    screen_group.add(lifebar.draw_ox_lvl())
    screen_group.add(lifebar.draw_hp_lvl())
    screen_group.add(lifebar)
    screen_group.draw(screen)
    return barrier, screen_group, oxygen_group


# функция проверяет нажатие клавиш и передвигает персонажа
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
    if map[player.x][player.y - 1] == (ICE_bg or ICE):
        if previous_bg != ICE_CAVE_BG_img:
            pygame.mixer.music.load(SNOW_BIOM_SOUNDTRACK_PATH)
            pygame.mixer.music.play(-1)
        return ICE_CAVE_BG_img
    elif map[player.x][player.y - 1] == WATER:
        if previous_bg != BACKGROUND_img:
            pygame.mixer.music.load(DEFAULT_BIOM_SOUNDTRACK_PATH)
            pygame.mixer.music.play(-1)
        return BACKGROUND_img
    elif map[player.x][player.y - 1] == (GROUND_bg or GROUND):
        if previous_bg != GROUND_CAVE_BG_img:
            pygame.mixer.music.load(CAVE_BIOM_SOUNDTRACK_PATH)
            pygame.mixer.music.play(-1)
        return GROUND_CAVE_BG_img
    else:
        return previous_bg


# Игровой цикл
def game_loop():
    pygame.init()
    pygame.display.set_caption('Immersed')

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    from wallpapers import main_menu, render_text, end_screen
    from ready_fonts import title_font

    # ---- ресурсы для главного меню ----
    background = MAIN_MENU_BACKGROUND_img
    # 231 - половина длины надписи "IMMERSED" в пикселях
    render_text("IMMERSED", WIDTH / 2 - 231, HEIGHT / 3.5, 60, 1000, title_font,
                background)
    # ---- ресурсы для главного меню ----

    # позиция игрока, количество кислорода, количество здоровья,
    # [корабль1, корабль2, корабль3, корабль4, неизвестный реактор]
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

        barrier_group, screen_group, oxygen_group = draw_screen(screen, player, game_map,
                                                                camera, lifebar)

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
                             progress, 0)
                    for button in buttons_pressed.keys():
                        buttons_pressed[button] = False
                    pos, ox, hp, progress = main_menu(screen)
                    player = Player(*pos)
                    lifebar.oxygen_lvl = ox
                    lifebar.health_lvl = hp

            if event.type == lifebar.oxygen_event:
                lifebar.oxygen_lvl -= 1

            if event.type == player.animate_event:
                player.update(buttons_pressed)

        if lifebar.health_lvl < 0 or lifebar.oxygen_lvl < 0:
            new_save(player.y, player.x, lifebar.oxygen_lvl, lifebar.health_lvl, progress,
                     1)
            pos, ox, hp, progress = end_screen(screen)
            player = Player(*pos)
            lifebar.oxygen_lvl = ox
            lifebar.health_lvl = hp
            for button in buttons_pressed.keys():
                buttons_pressed[button] = False

        collide_obj = pygame.sprite.spritecollideany(player, oxygen_group)
        if collide_obj:
            lifebar.oxygen_lvl = 100
            if collide_obj.ship_num:
                if progress[collide_obj.ship_num - 1] == 0:
                    render_tablet(screen, render_text, medium_font,
                                  ship_messages[collide_obj.ship_num - 1])
                    if all(progress[:-1]) and not progress[-1]:
                        render_tablet(screen, render_text, medium_font, PARTS_COLLECTED_text)
                    elif all(progress):
                        render_tablet(screen, render_text, medium_font, BATTERY_COLLECTED_text)
                    for button in buttons_pressed.keys():
                        buttons_pressed[button] = False
                    progress[collide_obj.ship_num - 1] = 1

        moving(barrier_group, player)

        global previous_bg
        previous_bg = bg
        bg = check_background(player, game_map)

        for i in screen_group:  # оптимизация
            i.kill()
        CLOCK.tick(FPS)
        pygame.display.flip()
    pygame.quit()
