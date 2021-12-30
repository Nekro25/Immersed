import pygame
import os
from CONSTANTS import *
from gameplay import terminate


# генерируем кастомный шрифт, нарисованный по пикселям.
def generate_custom_font(image, all_symbols, color, size_x=5, size_y=8):
    image = load_image(image)

    new_surface = pygame.Surface((image.get_width(), image.get_height())).convert()
    new_surface.fill(color)

    image.set_colorkey((0, 0, 0))
    new_surface.blit(image, (0, 0))

    image = new_surface.copy()
    image.set_colorkey((255, 255, 255))

    num = 0

    for char in all_symbols.keys():
        image.set_clip(pygame.Rect(((size_x + 1) * num), 0, size_x, size_y))
        symbol_image = image.subsurface(image.get_clip())

        all_symbols[char].append(symbol_image)
        num += 1

    all_symbols['Height'] = size_y

    return all_symbols


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

            if word_length + margin_x - origin_x > max_width:
                margin_x = origin_x
                margin_y += font['Height']

            for sym in word:
                image = font[sym][1]
                screen.blit(image, (margin_x, margin_y))
                margin_x += font[sym][0] + spacing

            if char == ' ':
                # пробел занимает 3 пикселя
                margin_x += 3 + spacing
            else:
                margin_x = origin_x
                margin_y += font['Height']

            word = ''

        if margin_x - origin_x > max_width:
            margin_x = origin_x
            margin_y += font['Height']

    return margin_x, margin_y


# Словарь, содержащий все нужные символы в качестве ключей. Первый элемент массива, являющимся значением к ключу -
# это количество пикселей, которое занимает нарисованный вариант символа в ширину.
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
custom_font = generate_custom_font('Fonts/small_font.png', font, (255, 255, 255))
