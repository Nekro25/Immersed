import pygame
import pygame_gui as gui
import copy

import sys
import os
import shutil

from CONSTANTS import *

# Словарь, содержащий все нужные символы в качестве ключей. Первый элемент массива, являющимся значением к ключу -
# это количество пикселей, которое занимает нарисованный вариант символа в ширину.
font = {'A': [3], 'B': [3], 'C': [3], 'D': [3], 'E': [3], 'F': [3], 'G': [3], 'H': [3], 'I': [3], 'J': [3],
        'K': [3], 'L': [3], 'M': [5], 'N': [3], 'O': [3], 'P': [3], 'Q': [3], 'R': [3], 'S': [3], 'T': [3],
        'U': [3], 'V': [3], 'W': [5], 'X': [3], 'Y': [3], 'Z': [3],
        'a': [3], 'b': [3], 'c': [3], 'd': [3], 'e': [3], 'f': [3], 'g': [3], 'h': [3], 'i': [1], 'j': [2],
        'k': [3], 'l': [3], 'm': [5], 'n': [3], 'o': [3], 'p': [3], 'q': [3], 'r': [2], 's': [3], 't': [3],
        'u': [3], 'v': [3], 'w': [5], 'x': [3], 'y': [3], 'z': [3],
        '.': [1], '-': [3], ',': [2], ':': [1], '+': [3], '\'': [1], '!': [1], '?': [3],
        '0': [3], '1': [3], '2': [3], '3': [3], '4': [3], '5': [3], '6': [3], '7': [3], '8': [3], '9': [3],
        '(': [2], ')': [2],
        'А': [3], 'Б': [3], 'В': [3], 'Г': [3], 'Д': [5], 'Е': [3], 'Ж': [5], 'З': [3], 'И': [4], 'Й': [5],
        'К': [3], 'Л': [3], 'М': [5], 'Н': [3], 'О': [3], 'П': [3], 'Р': [3], 'С': [3], 'Т': [3], 'У': [3],
        'Ф': [5], 'Х': [3], 'Ц': [4], 'Ч': [3], 'Ш': [5], 'Щ': [5], 'Ъ': [5], 'Ы': [5], 'Ь': [4], 'Э': [3],
        'Ю': [5], 'Я': [3],
        'а': [3], 'б': [3], 'в': [3], 'г': [3], 'д': [5], 'е': [3], 'ж': [5], 'з': [3], 'и': [3], 'й': [3],
        'к': [3], 'л': [3], 'м': [5], 'н': [3], 'о': [3], 'п': [3], 'р': [3], 'с': [3], 'т': [3], 'у': [3],
        'ф': [5], 'х': [3], 'ц': [4], 'ч': [3], 'ш': [5], 'щ': [5], 'ъ': [5], 'ы': [5], 'ь': [4], 'э': [3],
        'ю': [5], 'я': [3]
        }

manager = gui.UIManager((WIDTH, HEIGHT))

# ---- кнопки в главном меню ----
new_game_button = gui.elements.UIButton(
    relative_rect=pygame.Rect(
        (MAIN_MENU_BUTTON_X_MARGIN, MAIN_MENU_BUTTON_Y_MARGIN),
        (MAIN_MENU_BUTTON_WIDTH, MAIN_MENU_BUTTON_HEIGHT)
    ),
    text="НОВАЯ ИГРА",
    manager=manager
)
continue_button = gui.elements.UIButton(
    relative_rect=pygame.Rect(
        (MAIN_MENU_BUTTON_X_MARGIN + MAIN_MENU_BUTTON_WIDTH + MAIN_MENU_BUTTON_SPACING, MAIN_MENU_BUTTON_Y_MARGIN),
        (MAIN_MENU_BUTTON_WIDTH, MAIN_MENU_BUTTON_HEIGHT)
    ),
    text="ПРОДОЛЖИТЬ",
    manager=manager
)
exit_button = gui.elements.UIButton(
    relative_rect=pygame.Rect(
        (
            MAIN_MENU_BUTTON_X_MARGIN + 2 * (MAIN_MENU_BUTTON_WIDTH + MAIN_MENU_BUTTON_SPACING),
            MAIN_MENU_BUTTON_Y_MARGIN),
        (MAIN_MENU_BUTTON_WIDTH, MAIN_MENU_BUTTON_HEIGHT)
    ),
    text="ВЫЙТИ",
    manager=manager
)
settings_button = gui.elements.UIButton(
    relative_rect=pygame.Rect(
        (
            MAIN_MENU_BUTTON_X_MARGIN + 3 * (MAIN_MENU_BUTTON_WIDTH + MAIN_MENU_BUTTON_SPACING),
            MAIN_MENU_BUTTON_Y_MARGIN),
        (MAIN_MENU_BUTTON_WIDTH, MAIN_MENU_BUTTON_HEIGHT)
    ),
    text="НАСТРОЙКИ",
    manager=manager
)


# ---- кнопки в главном меню ----


def generate_custom_font(image, fnt, color, block_width=5, block_height=8, barrier=1):
    """
    Функция генерирует кастомный шрифт, нарисованный по пикселям.

    :param image:   картинка с нарисованными символами;
    :param fnt:     словарь с символами;
    :param color:   цвет шрифта;
    :param block_width:   ширина ячейки с символом;
    :param block_height:  высота ячейки с символом;
    :param barrier: толщина перегородки между символами на рисунке;
    :return:
    """

    # создаем копию словаря с символами, чтобы не изменять исходный вариант
    all_symbols = copy.deepcopy(fnt)

    # создаем дополнительный холст, для нанесения "трафарета" из символов кастомного шрифта
    extra_surface = pygame.Surface(image.get_size()).convert()
    extra_surface.fill(color)
    extra_surface.blit(image, (0, 0))

    image = extra_surface.copy()
    image.set_colorkey((255, 255, 255))

    num = 0

    for char in all_symbols.keys():
        image.set_clip(
            pygame.Rect(((block_width + barrier) * num), 0, all_symbols[char][0] * (block_width / 5), block_height))
        symbol_image = image.subsurface(image.get_clip())

        all_symbols[char].append(symbol_image)
        num += 1

    all_symbols['Height'] = block_height

    return all_symbols


def next_word(text):
    for sym in ['.', ',', '!', '?', ' ']:
        word = text[:text.find(sym)]
        if ' ' not in word:
            return word


def render_text(text, margin_x, margin_y, spacing, max_width, font, screen, space_length=3,
                waiting_time=0, step_by_step=False):
    """
    Функция рендерит заданный текст с кастомным шрифтом.

    :param text:         текст для вывода;
    :param margin_x:     величина горизонтального отступа от левой границы холста;
    :param margin_y:     величина вертикального отступа от верхней границы холста;
    :param spacing:      расстояние между символами;
    :param max_width:    максимальная длина строки(в пикселях);
    :param font:         шрифт;
    :param screen:       холст;
    :param space_length: длина пробела(в пикселях);
    :param waiting_time: продолжительность ожидания после выведения каждой буквы(в миллисекундах);
    :param step_by_step: выводит текст букву за буквой, если установлено значение True;
    :return:
    """

    text += ' '
    origin_x = margin_x
    word = ''
    next_word_length = 0

    for idx, char in enumerate(text):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return

        if char not in [' ', '\n']:
            try:
                image = font[str(char)][1]
                word += char
            except KeyError:
                pass
        else:
            # длина слова(в пикселях) вместе с символами пустой строки и пропусками
            next_word_length = sum(map(lambda s: font[s][0] + spacing, next_word(text[idx + 1:])))

            if word != '':
                last_sym = word[-1]

            # отображаем символы по одному в положенном месте на экране
            for sym in word:
                image = font[sym][1]
                screen.blit(image, (margin_x, margin_y))
                if step_by_step:
                    pygame.display.flip()
                    pygame.time.wait(waiting_time)
                margin_x += font[sym][0] + spacing

            if char == ' ':
                margin_x += space_length + spacing

            word = ''
            a = margin_x - origin_x > max_width
            if char == '\n' and last_sym not in ['.', ','] or margin_x - origin_x > max_width:
                margin_x = origin_x
                margin_y += font['Height']

        if margin_x - origin_x + next_word_length > max_width:
            margin_x = origin_x
            margin_y += font['Height']


# ---- Функция показывает заставку, когда игрок начал новую игру ----
def start_screen(screen):
    list_of_darkened_frames = DISPLAY_FRAMES
    intro_text = "Вы астронавт-любитель, пытающийся найти драгоценности в открытом космосе. " \
                 "Но в один момент вы сталкиваетесь с целой бандой пиратов, и, стараясь оторваться от них, " \
                 "улетаете в неразведанные места. При попытке сделать трюк вокруг системы планет что-то " \
                 "пошло не по плану: вы слишком близко подлетели к одной из них и не смогли справиться с силой притяжения. " \
                 "После падения ваш корабль сильно пострадал, поэтому вам нужно как можно скорее восстановить " \
                 "его и продолжить свой путь."

    command_text = "Нажмите любую клавишу на клавиатуре, чтобы продолжить."

    idx = 0
    show_preview = True

    screen.fill((0, 0, 0))
    pygame.display.flip()
    pygame.time.wait(4000)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                return

        if show_preview:
            medium_font_image = pygame.transform.scale(
                load_image(FONT_PATH, color_key=(0, 0, 0)),
                (FONT_IMG_WIDTH * 3, FONT_IMG_HEIGHT * 3)
            )
            medium_font = generate_custom_font(medium_font_image, font, (255, 254, 255),
                                               block_width=FONT_BLOCK_WIDTH * 3,
                                               block_height=FONT_BLOCK_HEIGHT * 3,
                                               barrier=FONT_BARRIER * 3)
            small_font_image = pygame.transform.scale(
                load_image(FONT_PATH, color_key=(0, 0, 0)),
                (FONT_IMG_WIDTH * 2, FONT_IMG_HEIGHT * 2)
            )
            small_font = generate_custom_font(small_font_image, font, (255, 254, 255),
                                              block_width=FONT_BLOCK_WIDTH * 2,
                                              block_height=FONT_BLOCK_HEIGHT * 2,
                                              barrier=FONT_BARRIER * 2)

            render_text(command_text, WIDTH / 2 - 300, 670, 8, 800, small_font, screen, space_length=3)
            pygame.display.flip()
            if idx <= 88:
                screen.blit(list_of_darkened_frames[idx % 23], (WIDTH / 2 - 350, HEIGHT / 2 - 245))
                idx += 1
            else:
                pygame.time.wait(1000)
                screen.blit(EMPTY_DISPLAY_img, (WIDTH / 2 - 350, HEIGHT / 2 - 245))
                pygame.display.flip()
                pygame.time.wait(2000)

                render_text(intro_text, 390, 200, 12, 600, medium_font, screen,
                            space_length=5, waiting_time=80, step_by_step=True)
                show_preview = False

            if idx % 23 == 0:
                list_of_darkened_frames = list_of_darkened_frames[::-1]
        else:
            return

        pygame.time.wait(150)
        pygame.display.flip()
        CLOCK.tick(FPS)


def main_menu(screen, background):
    screen.blit(background, (0, 0))

    # ---- цикл главного меню ----
    while True:
        tick = CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == gui.UI_BUTTON_PRESSED:
                    if event.ui_element == new_game_button:
                        start_screen(screen)
                        return
                    if event.ui_element == continue_button:
                        return
                    if event.ui_element == settings_button:
                        pass
                    if event.ui_element == exit_button:
                        terminate()

            manager.process_events(event)

        manager.update(tick)
        manager.draw_ui(screen)
        pygame.display.flip()
        CLOCK.tick(FPS)
