import pygame
import pygame_gui as gui

from CONSTANTS import *
from data_base import *
from ready_fonts import *

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
        MAIN_MENU_BUTTON_X_MARGIN + 2 * (MAIN_MENU_BUTTON_WIDTH + MAIN_MENU_BUTTON_SPACING), MAIN_MENU_BUTTON_Y_MARGIN),
        (MAIN_MENU_BUTTON_WIDTH, MAIN_MENU_BUTTON_HEIGHT)
    ),
    text="ВЫЙТИ",
    manager=manager
)
settings_button = gui.elements.UIButton(
    relative_rect=pygame.Rect(
        (
        MAIN_MENU_BUTTON_X_MARGIN + 3 * (MAIN_MENU_BUTTON_WIDTH + MAIN_MENU_BUTTON_SPACING), MAIN_MENU_BUTTON_Y_MARGIN),
        (MAIN_MENU_BUTTON_WIDTH, MAIN_MENU_BUTTON_HEIGHT)
    ),
    text="НАСТРОЙКИ",
    manager=manager
)


# ---- кнопки в главном меню ----


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
                return True

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
    skip_pressed = False

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

                skip_pressed = render_text(intro_text, WIDTH / 2 - 293, HEIGHT / 2 - 184, 12, 600, medium_font, screen,
                                           space_length=5, waiting_time=80, step_by_step=True)
                show_preview = False
                if skip_pressed:
                    return

            if idx % 23 == 0:
                list_of_darkened_frames = list_of_darkened_frames[::-1]

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
                        return new_game()
                    if event.ui_element == continue_button:
                        return get_save()
                    if event.ui_element == settings_button:
                        pass
                    if event.ui_element == exit_button:
                        terminate()

            manager.process_events(event)

        manager.update(tick)
        manager.draw_ui(screen)
        pygame.display.flip()
        CLOCK.tick(FPS)
