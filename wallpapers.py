import pygame
import pygame_gui as gui
import copy

import os

from CONSTANTS import *

font = {'A': [3], 'B': [3], 'C': [3], 'D': [3], 'E': [3], 'F': [3], 'G': [3], 'H': [3],
        'I': [3], 'J': [3],
        'K': [3], 'L': [3], 'M': [5], 'N': [3], 'O': [3], 'P': [3], 'Q': [3], 'R': [3],
        'S': [3], 'T': [3],
        'U': [3], 'V': [3], 'W': [5], 'X': [3], 'Y': [3], 'Z': [3],
        'a': [3], 'b': [3], 'c': [3], 'd': [3], 'e': [3], 'f': [3], 'g': [3], 'h': [3],
        'i': [1], 'j': [2],
        'k': [3], 'l': [3], 'm': [5], 'n': [3], 'o': [3], 'p': [3], 'q': [3], 'r': [2],
        's': [3], 't': [3],
        'u': [3], 'v': [3], 'w': [5], 'x': [3], 'y': [3], 'z': [3],
        '.': [1], '-': [3], ',': [2], ':': [1], '+': [3], '\'': [1], '!': [1], '?': [3],
        '0': [3], '1': [3], '2': [3], '3': [3], '4': [3], '5': [3], '6': [3], '7': [3],
        '8': [3], '9': [3],
        '(': [2], ')': [2]}


# генерируем кастомный шрифт, нарисованный по пикселям.
def generate_custom_font(image, fnt, color, size_x=5, size_y=8):
    all_symbols = copy.deepcopy(fnt)

    image = load_image(image)

    image.fill(color)

    image.set_colorkey((0, 0, 0))
    image.blit(image, (0, 0))

    image = image.copy()
    image.set_colorkey((255, 255, 255))

    num = 0

    for char in all_symbols.keys():
        image.set_clip(pygame.Rect(((size_x + 1) * num), 0, size_x, size_y))
        symbol_image = image.subsurface(image.get_clip())

        all_symbols[char].append(symbol_image)
        num += 1

    all_symbols['Height'] = size_y

    return all_symbols


# Функция рендерит заданный текст с кастомным шрифтом.
# Функция принимает сам текст, величину горизонтального отступа от левого края холста,
# величину вертикального отступа ог верхней границы холста, расстояние между символами,
# максимальную длину строки(в пикселях), шрифт и холст.
def render_text(text, margin_x, margin_y, spacing, max_width, font, screen):
    text += ' '
    origin_x = margin_x
    word = ''

    for char in text:
        if char not in [' ', '\n']:
            try:
                image = font[str(char)][1]
                word += char
            except KeyError:
                pass
        else:
            word_length = sum(map(lambda s: font[s][0] + spacing, word))

            if char == ' ':
                # пробел занимает 3 пикселя
                margin_x += 3 + spacing

            for sym in word:
                image = font[sym][1]
                screen.blit(image, (margin_x, margin_y))
                margin_x += font[sym][0] + spacing

            word = ''
            if char == '\n' or word_length + margin_x - origin_x > max_width:
                margin_x = origin_x
                margin_y += font['Height']

        if margin_x - origin_x > max_width:
            margin_x = origin_x
            margin_y += font['Height']


def start_screen(screen, font):
    intro_text = """Вы астронавт-любитель, пытающийся найти драгоценности в открытом космосе. 
    Но в один момент вы сталкиваетесь с целой бандой пиратов, и, стараясь оторваться от них, 
    улетаете в неразведанные места. При попытке сделать трюк вокруг системы планет что-то 
    пошло не по плану: вы слишком близко подлетели к одной из них и не смогли справиться с силой притяжения. 
    После падения ваш корабль сильно пострадал, поэтому вам нужно как можно скорее восстановить 
    его и продолжить свой путь."""

    command_text = "Нажмите любую клавишу на клавиатуре, чтобы продолжить."

    fon = pygame.Surface(load_image('background_start_screen.png'))
    screen.blit(fon, (0, 0))

    render_text(intro_text, 10, 20, 1, 500, font, screen)
    render_text(command_text, 100, 300, 1, 500, font, screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return

        pygame.display.flip()
        CLOCK.tick(FPS)


def main_menu(screen, manager):
    background = load_image('all_image(shallow water).png')
    title_font = generate_custom_font('Fonts/font.png', font, (255, 255, 255), size_x=15, size_y=24)
    render_text("IMMERSED", 50, 50, 3, 500, title_font, background)
    screen.blit(background, (0, 0))

    new_game_button = gui.elements.UIButton(
        relative_rect=pygame.Rect((420, 320), (100, 50)),
        text="НОВАЯ ИГРА",
        manager=manager
    )
    continue_button = gui.elements.UIButton(
        relative_rect=pygame.Rect((550, 320), (100, 50)),
        text="ПРОДОЛЖИТЬ",
        manager=manager
    )
    exit_button = gui.elements.UIButton(
        relative_rect=pygame.Rect((680, 320), (100, 50)),
        text="ВЫЙТИ",
        manager=manager
    )
    settings_button = gui.elements.UIButton(
        relative_rect=pygame.Rect((810, 320), (100, 50)),
        text="НАСТРОЙКИ",
        manager=manager
    )

    while True:
        tick = CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == gui.UI_BUTTON_PRESSED:
                    if event.ui_element == new_game_button:
                        pass
                    if event.ui_element == continue_button:
                        return False
                    if event.ui_element == settings_button:
                        pass
                    if event.ui_element == exit_button:
                        terminate()
            manager.process_events(event)
        manager.update(tick)
        manager.draw_ui(screen)
        render_text("IMMERSED", 50, 50, 3, 500, title_font, screen)
        pygame.display.flip()
        CLOCK.tick(FPS)


# Словарь, содержащий все нужные символы в качестве ключей. Первый элемент массива, являющимся значением к ключу -
# это количество пикселей, которое занимает нарисованный вариант символа в ширину.
custom_font = generate_custom_font('Fonts/font.png', font, (255, 255, 255))
