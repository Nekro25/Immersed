import copy
import pygame

from CONSTANTS import *


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


# # Словарь, содержащий все нужные символы в качестве ключей. Первый элемент массива, являющимся значением к ключу -
# # это количество пикселей, которое занимает нарисованный вариант символа в ширину.
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

medium_font_image = pygame.transform.scale(
    load_image(FONT_PATH, color_key=(0, 0, 0)),
    (FONT_IMG_WIDTH * 3, FONT_IMG_HEIGHT * 3)
)
small_font_image = pygame.transform.scale(
    load_image(FONT_PATH, color_key=(0, 0, 0)),
    (FONT_IMG_WIDTH * 2, FONT_IMG_HEIGHT * 2)
)
big_font_image = pygame.transform.scale(
    load_image(FONT_PATH, color_key=(0, 0, 0)),
    (FONT_IMG_WIDTH * 6, FONT_IMG_HEIGHT * 6)
)

medium_font = generate_custom_font(
    medium_font_image, font, (255, 254, 255),
    block_width=FONT_BLOCK_WIDTH * 3,
    block_height=FONT_BLOCK_HEIGHT * 3,
    barrier=FONT_BARRIER * 3
)
small_font = generate_custom_font(
    small_font_image, font, (255, 254, 255),
    block_width=FONT_BLOCK_WIDTH * 2,
    block_height=FONT_BLOCK_HEIGHT * 2,
    barrier=FONT_BARRIER * 2
)
title_font = generate_custom_font(
    big_font_image, font, (255, 254, 255),
    block_width=FONT_BLOCK_WIDTH * 6,
    block_height=FONT_BLOCK_HEIGHT * 6,
    barrier=FONT_BARRIER * 6
)