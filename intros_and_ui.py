import pygame
import pygame_gui as gui

from CONSTANTS import *
import CONSTANTS
from data_base import *
from ready_fonts import *

main_menu_manager = gui.UIManager((WIDTH, HEIGHT), 'theme.json')
end_screen_manager = gui.UIManager((WIDTH, HEIGHT), 'theme.json')
settings_menu_manager = gui.UIManager((WIDTH, HEIGHT), 'theme.json')

# ---- кнопки в главном меню ----
new_game_button = gui.elements.UIButton(
    relative_rect=pygame.Rect(
        (MAIN_MENU_BUTTON_X_MARGIN, MAIN_MENU_BUTTON_Y_MARGIN),
        (MAIN_MENU_BUTTON_WIDTH, MAIN_MENU_BUTTON_HEIGHT)
    ),
    text="НОВАЯ ИГРА",
    manager=main_menu_manager,
    object_id=gui.core.ObjectID(class_id='@menu_screen',
                                object_id='#menu_buttons')
)
continue_button = gui.elements.UIButton(
    relative_rect=pygame.Rect(
        (MAIN_MENU_BUTTON_X_MARGIN + MAIN_MENU_BUTTON_WIDTH + MAIN_MENU_BUTTON_SPACING, MAIN_MENU_BUTTON_Y_MARGIN),
        (MAIN_MENU_BUTTON_WIDTH, MAIN_MENU_BUTTON_HEIGHT)
    ),
    text="ПРОДОЛЖИТЬ",
    manager=main_menu_manager,
    object_id=gui.core.ObjectID(class_id='@menu_screen',
                                object_id='#menu_buttons')
)
exit_button = gui.elements.UIButton(
    relative_rect=pygame.Rect(
        (MAIN_MENU_BUTTON_X_MARGIN + 2 * (MAIN_MENU_BUTTON_WIDTH + MAIN_MENU_BUTTON_SPACING),
         MAIN_MENU_BUTTON_Y_MARGIN),
        (MAIN_MENU_BUTTON_WIDTH, MAIN_MENU_BUTTON_HEIGHT)
    ),
    text="ВЫЙТИ",
    manager=main_menu_manager,
    object_id=gui.core.ObjectID(class_id='@menu_screen',
                                object_id='#menu_buttons')
)
settings_button = gui.elements.UIButton(
    relative_rect=pygame.Rect(
        (MAIN_MENU_BUTTON_X_MARGIN + 3 * (MAIN_MENU_BUTTON_WIDTH + MAIN_MENU_BUTTON_SPACING),
         MAIN_MENU_BUTTON_Y_MARGIN),
        (MAIN_MENU_BUTTON_WIDTH, MAIN_MENU_BUTTON_HEIGHT)
    ),
    text="НАСТРОЙКИ",
    manager=main_menu_manager,
    object_id=gui.core.ObjectID(class_id='@menu_screen',
                                object_id='#menu_buttons')
)
# ---- кнопки в главном меню ----

# ---- кнопки на экране смерти ----
go_to_main_menu_button = gui.elements.UIButton(
    relative_rect=pygame.Rect(
        (END_SCREEN_BUTTON_X_MARGIN, END_SCREEN_BUTTON_Y_MARGIN),
        (END_SCREEN_BUTTON_WIDTH, END_SCREEN_BUTTON_HEIGHT)
    ),
    text="ВЫЙТИ В ГЛАВНОЕ МЕНЮ",
    manager=end_screen_manager
)
start_over_button = gui.elements.UIButton(
    relative_rect=pygame.Rect(
        (END_SCREEN_BUTTON_X_MARGIN, END_SCREEN_BUTTON_Y_MARGIN + END_SCREEN_BUTTON_SPACING + END_SCREEN_BUTTON_HEIGHT),
        (END_SCREEN_BUTTON_WIDTH, END_SCREEN_BUTTON_HEIGHT)
    ),
    text="НАЧАТЬ ЗАНОВО",
    manager=end_screen_manager
)
# ---- кнопки на экране смерти ----

# ---- кнопки в настройках ----
turn_down_music_volume = gui.elements.UIButton(
    relative_rect=pygame.Rect(
        (VOLUME_DOWN_BUTTON_X_MARGIN, VOLUME_CONTROL_BUTTON_Y_MARGIN),
        (VOLUME_CONTROL_BUTTON_WIDTH, VOLUME_CONTROL_BUTTON_HEIGHT)
    ),
    text="-",
    manager=settings_menu_manager,
    object_id=gui.core.ObjectID(class_id='@settings_screen',
                                object_id='#settings_buttons')
)
turn_up_music_volume = gui.elements.UIButton(
    relative_rect=pygame.Rect(
        (VOLUME_UP_BUTTON_X_MARGIN, VOLUME_CONTROL_BUTTON_Y_MARGIN),
        (VOLUME_CONTROL_BUTTON_WIDTH, VOLUME_CONTROL_BUTTON_HEIGHT)
    ),
    text="+",
    manager=settings_menu_manager,
    object_id=gui.core.ObjectID(class_id='@settings_screen',
                                object_id='#settings_buttons')
)
turn_down_effects_volume = gui.elements.UIButton(
    relative_rect=pygame.Rect(
        (VOLUME_DOWN_BUTTON_X_MARGIN, VOLUME_CONTROL_BUTTON_Y_MARGIN + VOLUME_CONTROL_BUTTON_SPACING),
        (VOLUME_CONTROL_BUTTON_WIDTH, VOLUME_CONTROL_BUTTON_HEIGHT)
    ),
    text="-",
    manager=settings_menu_manager,
    object_id=gui.core.ObjectID(class_id='@settings_screen',
                                object_id='#settings_buttons')
)
turn_up_effects_volume = gui.elements.UIButton(
    relative_rect=pygame.Rect(
        (VOLUME_UP_BUTTON_X_MARGIN, VOLUME_CONTROL_BUTTON_Y_MARGIN + VOLUME_CONTROL_BUTTON_SPACING),
        (VOLUME_CONTROL_BUTTON_WIDTH, VOLUME_CONTROL_BUTTON_HEIGHT)
    ),
    text="+",
    manager=settings_menu_manager,
    object_id=gui.core.ObjectID(class_id='@settings_screen',
                                object_id='#settings_buttons')
)


# ---- кнопки в настройках ----


def settings_screen(screen):
    screen.blit(CROPPED_PLANET_img, (0, 0))
    render_text("Громкость музыки", (WIDTH - 232) / 2, VOLUME_CONTROL_BUTTON_Y_MARGIN - 50,
                12, 600, medium_font, screen, space_length=5)
    render_text("Громкость эффектов", (WIDTH - 262) / 2, VOLUME_CONTROL_BUTTON_Y_MARGIN + 100,
                12, 600, medium_font, screen, space_length=5)

    while True:
        count_for_music = CONSTANTS.MUSIC_VOLUME * 10
        count_for_effects = CONSTANTS.EFFECTS_VOLUME * 10

        music_dash_color = (255, 255, 255)
        effects_dash_color = (255, 255, 255)

        for i in range(1, 11):
            if i > count_for_music:
                music_dash_color = (127, 127, 127)
            if i > count_for_effects:
                effects_dash_color = (127, 127, 127)

            pygame.draw.rect(screen, music_dash_color,
                             (VOLUME_DOWN_BUTTON_X_MARGIN + VOLUME_CONTROL_BUTTON_WIDTH + VOLUME_LEVEL_DASH_SPACING * i,
                              VOLUME_CONTROL_BUTTON_Y_MARGIN + 7,
                              5, 15))
            pygame.draw.rect(screen, effects_dash_color,
                             (VOLUME_DOWN_BUTTON_X_MARGIN + VOLUME_CONTROL_BUTTON_WIDTH + VOLUME_LEVEL_DASH_SPACING * i,
                              VOLUME_CONTROL_BUTTON_Y_MARGIN + VOLUME_CONTROL_BUTTON_SPACING + 7,
                              5, 15))
        tick = CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu(screen)
            if event.type == pygame.USEREVENT:
                if event.user_type == gui.UI_BUTTON_PRESSED:
                    BUTTON_SOUND.play()
                    if event.ui_element == turn_up_effects_volume:
                        CONSTANTS.EFFECTS_VOLUME += 0.1
                    if event.ui_element == turn_down_effects_volume:
                        CONSTANTS.EFFECTS_VOLUME -= 0.1
                    if event.ui_element == turn_up_music_volume:
                        CONSTANTS.MUSIC_VOLUME += 0.1
                    if event.ui_element == turn_down_music_volume:
                        CONSTANTS.MUSIC_VOLUME -= 0.1

            settings_menu_manager.process_events(event)

        settings_menu_manager.update(tick)
        settings_menu_manager.draw_ui(screen)
        pygame.display.flip()
        CLOCK.tick(FPS)


# ---- Функция показывает заставку, когда игрок начал новую игру ----
def start_screen(screen):
    list_of_darkened_frames = DISPLAY_FRAMES
    intro_text = "Вы астронавт-любитель, пытающийся найти драгоценности в открытом космосе. " \
                 "Но в один момент вы сталкиваетесь с целой бандой пиратов, и, стараясь оторваться от них, " \
                 "улетаете в неразведанные места. При попытке сделать трюк вокруг системы планет что-то " \
                 "пошло не по плану: вы слишком близко подлетели к одной из них и не смогли справиться с силой притяжения. " \
                 "После падения ваш корабль сильно пострадал, поэтому вам нужно как можно скорее восстановить " \
                 "его и продолжить свой путь."

    command_text = "Нажмите любую клавишу на клавиатуре, чтобы пропустить."

    idx = 0
    show_preview = True
    skip_pressed = False

    pygame.mixer.music.stop()

    screen.blit(PLANET_img, (0, 0))
    pygame.display.flip()
    pygame.time.wait(4 * SECOND)
    screen.fill((0, 0, 0))

    pygame.mixer.music.load(SIREN_SOUNDTRACK_PATH)
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(fade_ms=4 * SECOND)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                pygame.mixer.music.stop()
                return

        if show_preview:
            render_text(command_text, WIDTH / 2 - 300, 670, 8, 800, small_font, screen, space_length=3)
            pygame.display.flip()
            if idx <= 88:
                screen.blit(list_of_darkened_frames[idx % 23], (WIDTH / 2 - 350, HEIGHT / 2 - 245))
                idx += 1
            else:
                pygame.time.wait(SECOND)
                pygame.mixer.music.stop()
                screen.blit(EMPTY_DISPLAY_img, (WIDTH / 2 - 350, HEIGHT / 2 - 245))
                pygame.display.flip()
                pygame.time.wait(2 * SECOND)

                pygame.mixer.music.load(BEEP_SOUNDTRACK_PATH)
                pygame.mixer.music.play(-1)

                render_text(intro_text, WIDTH / 2 - 293, HEIGHT / 2 - 184, 12, 600, medium_font, screen,
                            space_length=5)

                pygame.mixer.music.stop()
                skip_pressed = True
                pygame.time.wait(SECOND)
                show_preview = False

                if skip_pressed:
                    return

            if idx % 23 == 0:
                list_of_darkened_frames = list_of_darkened_frames[::-1]

        pygame.time.wait(150)
        pygame.display.flip()
        CLOCK.tick(FPS)


def end_screen(screen):
    end_text = "Вы умерли!"

    background = END_SCREEN_BACKGROUND_img
    render_text(end_text, (WIDTH - 136) / 2, HEIGHT / 2 - 200, 12, 300, medium_font, background, space_length=5)
    screen.blit(END_SCREEN_BACKGROUND_img, (0, 0))

    pygame.mixer.music.load(AFTER_DEATH_SOUNDTRACK_PATH)
    pygame.mixer.music.play(-1)

    while True:
        tick = CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == gui.UI_BUTTON_PRESSED:
                    BUTTON_SOUND.play()
                    if event.ui_element == go_to_main_menu_button:
                        pygame.mixer.music.stop()
                        return main_menu(screen)
                    if event.ui_element == start_over_button:
                        pygame.mixer.music.stop()
                        return main_menu(screen, start_new_game=True)

            end_screen_manager.process_events(event)

        end_screen_manager.update(tick)
        end_screen_manager.draw_ui(screen)
        pygame.display.flip()
        CLOCK.tick(FPS)


def main_menu(screen, start_new_game=False):
    screen.blit(MAIN_MENU_BACKGROUND_img, (0, 0))

    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load(MAIN_MENU_SOUNDTRACK_PATH)
        pygame.mixer.music.play(-1)

    if start_new_game:
        start_screen(screen)

        pygame.mixer.music.load(DEFAULT_BIOM_SOUNDTRACK_PATH)
        pygame.mixer.music.play(-1)

        return new_game()

    # ---- цикл главного меню ----
    while True:
        tick = CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == gui.UI_BUTTON_PRESSED:
                    BUTTON_SOUND.play()
                    if event.ui_element == new_game_button:
                        start_screen(screen)

                        pygame.mixer.music.load(DEFAULT_BIOM_SOUNDTRACK_PATH)
                        pygame.mixer.music.play(-1)

                        return new_game()
                    if event.ui_element == continue_button:
                        pos, ox, hp, progress, was_died = get_save()
                        if not was_died:
                            pygame.mixer.music.load(DEFAULT_BIOM_SOUNDTRACK_PATH)
                            pygame.mixer.music.play(-1)

                            return pos, ox, hp, progress
                    if event.ui_element == settings_button:
                        settings_screen(screen)
                    if event.ui_element == exit_button:
                        terminate()

            main_menu_manager.process_events(event)

        main_menu_manager.update(tick)
        main_menu_manager.draw_ui(screen)
        pygame.display.flip()
        CLOCK.tick(FPS)