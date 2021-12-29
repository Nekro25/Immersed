import pygame
import os
from CONSTANTS import *
from gameplay import terminate


class FileError(Exception):
    pass


def load_image(filename, color_key=None):
    fullname = os.path.join('data', filename)

    if not os.path.isfile(fullname):
        raise FileError(f"Файл с изображением '{fullname}' не найден")
    image = pygame.image.load(fullname)
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


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


def ShowText(text, x, y, spacing, max_width, font, screen):
    text += ' '
    xx = x
    yy = y
    word = ''
    for char in text:
        if char not in [' ', '\n']:
            try:
                image = font[str(char)][1]
                word += char
            except KeyError:
                pass
        else:
            WordTotal = 0
            for char2 in word:
                WordTotal += font[char2][0]
                WordTotal += spacing
            if WordTotal + x - xx > max_width:
                x = xx
                y += font['Height']
            for char2 in word:
                image = font[str(char2)][1]
                screen.blit(image, (x, y))
                x += font[char2][0]
                x += spacing
            if char == ' ':
                x += font['A'][0]
                x += spacing
            else:
                x = xx
                y += font['Height']
            word = ''
        if x - xx > max_width:
            x = xx
            y += font['Height']
    return x, y


def start_screen(screen):
    intro_text = "IMMERSED"

    fon = pygame.transform.scale(load_image('background_start_screen.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 200
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


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
        '(': [2], ')': [2]}
custom_font = generate_custom_font('Fonts/small_font.png', font, (255, 255, 255))


def new_game_screen(screen):
    pass
