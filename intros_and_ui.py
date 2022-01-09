import pygame
import pygame_gui as gui

from CONSTANTS import *
from data_base import *
from ready_fonts import *
from sounds_and_music import play_music, set_volume_for_effects

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
    manager=end_screen_manager,
    object_id=gui.core.ObjectID(class_id='@menu_screen',
                                object_id='#menu_buttons')
)
start_over_button = gui.elements.UIButton(
    relative_rect=pygame.Rect(
        (END_SCREEN_BUTTON_X_MARGIN, END_SCREEN_BUTTON_Y_MARGIN + END_SCREEN_BUTTON_SPACING + END_SCREEN_BUTTON_HEIGHT),
        (END_SCREEN_BUTTON_WIDTH, END_SCREEN_BUTTON_HEIGHT)
    ),
    text="НАЧАТЬ ЗАНОВО",
    manager=end_screen_manager,
    object_id=gui.core.ObjectID(class_id='@menu_screen',
                                object_id='#menu_buttons')
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
        count_for_music = get_music_volume() * 10
        count_for_effects = get_effects_volume() * 10

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
                    return
            if event.type == pygame.USEREVENT:
                if event.user_type == gui.UI_BUTTON_PRESSED:
                    BUTTON_SOUND.play()
                    if event.ui_element == turn_up_effects_volume:
                        if get_effects_volume() < 0.9:
                            set_effects_volume(0.1)
                    if event.ui_element == turn_down_effects_volume:
                        if get_effects_volume() > 0.1:
                            set_effects_volume(-0.1)
                    if event.ui_element == turn_up_music_volume:
                        if get_music_volume() < 0.9:
                            set_music_volume(0.1)
                    if event.ui_element == turn_down_music_volume:
                        if get_music_volume() > 0:
                            set_music_volume(-0.1)

                    BUTTON_SOUND.set_volume(get_effects_volume())
                    set_volume_for_effects(get_effects_volume())

            settings_menu_manager.process_events(event)

        settings_menu_manager.update(tick)
        settings_menu_manager.draw_ui(screen)
        pygame.display.flip()
        CLOCK.tick(FPS)


def win_screen(screen):
    text = """Ваши старания прошли не зря! Корабль наконец-то отремонтирован и вы можете взлетать с планеты.
                    """ \
           "...Но вот досада! Слой льда перед вами слишком толстый и просто так его не пробить, " \
           """активируйте щиты!
""" \
           "...Отлично! Еле-еле, но лед вы все таки пробили. Теперь, вероятно, вы уже знаете, что если бы не добыли " \
           """батарейку из реактора, то вскоре замерзли бы насмерть.
                   """ \
           "Отличная работа! Теперь вы можете возвращаться домой. Счастливого пути!"

    pygame.mixer.music.stop()

    screen.blit(PLANET_img, (0, 0))
    screen.blit(EMPTY_DISPLAY_img, (WIDTH / 2 - 350, HEIGHT / 2 - 245))
    render_text(COMMAND_text, WIDTH / 2 - 300, HEIGHT / 2 - 286, 8, 800, small_font, screen, space_length=3)
    pygame.display.flip()

    play_music(BEEP_SOUNDTRACK_PATH, -1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                pygame.mixer.music.stop()
                statistics_screen(screen)
                return

        render_text(text, WIDTH / 2 - 293, HEIGHT / 2 - 184, 12, 600, medium_font, screen,
                    space_length=5, step_by_step=True, waiting_time=60)
        pygame.mixer.music.stop()

        pygame.display.flip()
        CLOCK.tick(FPS)


def lose_screen(screen):
    text = """Ваши старания прошли не зря! Корабль наконец-то отремонтирован и вы можете взлетать с планеты.
                    """ \
           "...Но вот досада! Слой льда перед вами слишком толстый и просто так его не пробить, " \
           """активируйте щиты!
  """ \
           "...Плохие новости..... Энергия на исходе, а вы пробили только половину слоя льда. Теперь, вероятно, " \
           "вы поняли, зачем нужна батарейка из реактора. Если бы вы ее взяли, то смогли бы преодолеть это " \
           "препятствие и не замерзнуть.                             " \
           "Теперь вам поможет только чудо..."

    pygame.mixer.music.stop()

    screen.blit(PLANET_img, (0, 0))
    screen.blit(EMPTY_DISPLAY_img, (WIDTH / 2 - 350, HEIGHT / 2 - 245))
    render_text(COMMAND_text, WIDTH / 2 - 300, HEIGHT / 2 - 286, 8, 800, small_font, screen, space_length=3)
    pygame.display.flip()

    play_music(BEEP_SOUNDTRACK_PATH, -1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                pygame.mixer.music.stop()
                statistics_screen(screen)
                return

        render_text(text, WIDTH / 2 - 293, HEIGHT / 2 - 184, 12, 600, medium_font, screen,
                    space_length=5)
        pygame.mixer.music.stop()

        pygame.display.flip()
        CLOCK.tick(FPS)


def statistics_screen(screen):
    statistic_word = "Статистика"
    total_stats = get_statistics()
    info_text = [f"Пройдено метров:  {total_stats['steps']}", f"Пережито монстров:  {total_stats['monsters']}",
                 f"Время прохождения:  {total_stats['time']}", f"Укусов получено:  {total_stats['bites']}"]

    pygame.mixer.music.stop()

    screen.blit(PLANET_img, (0, 0))
    screen.blit(EMPTY_DISPLAY_img, (WIDTH / 2 - 350, HEIGHT / 2 - 245))
    render_text(statistic_word, WIDTH / 2 - 150, HEIGHT / 2 - 170, 30, 1000, title_font, screen)

    for num, text in enumerate(info_text):
        render_text(text, WIDTH / 2 - 130, HEIGHT / 2 + num * 50, 12, 600, medium_font, screen, space_length=5)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                pygame.mixer.music.stop()
                return

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

    idx = 0
    show_preview = True
    skip_pressed = False

    pygame.mixer.music.stop()

    screen.blit(PLANET_img, (0, 0))
    pygame.display.flip()
    pygame.time.wait(4 * SECOND)
    screen.fill((0, 0, 0))

    play_music(SIREN_SOUNDTRACK_PATH, fade_ms=4 * SECOND)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                pygame.mixer.music.stop()
                return

        if show_preview:
            render_text(COMMAND_text, WIDTH / 2 - 300, HEIGHT / 2 - 286, 8, 800, small_font, screen, space_length=3)
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

                play_music(BEEP_SOUNDTRACK_PATH, -1)

                render_text(intro_text, WIDTH / 2 - 293, HEIGHT / 2 - 184, 12, 600, medium_font, screen,
                            space_length=5, step_by_step=True, waiting_time=60)

                pygame.mixer.music.stop()

                show_preview = False

                if skip_pressed:
                    return

            if idx % 23 == 0:
                list_of_darkened_frames = list_of_darkened_frames[::-1]

        pygame.time.wait(150)
        pygame.display.flip()
        CLOCK.tick(FPS)


def death_screen(screen):
    end_text = "Вы умерли!"

    background = END_SCREEN_BACKGROUND_img
    render_text(end_text, (WIDTH - 136) / 2, HEIGHT / 2 - 200, 12, 300, medium_font, background, space_length=5)
    screen.blit(END_SCREEN_BACKGROUND_img, (0, 0))

    play_music(AFTER_DEATH_SOUNDTRACK_PATH, -1)

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
    if not pygame.mixer.music.get_busy():
        play_music(MAIN_MENU_SOUNDTRACK_PATH, -1)

    if start_new_game:
        start_screen(screen)

        play_music(DEFAULT_BIOM_SOUNDTRACK_PATH, -1)

        return new_game()

    # ---- цикл главного меню ----
    while True:
        screen.blit(MAIN_MENU_BACKGROUND_img, (0, 0))
        tick = CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == gui.UI_BUTTON_PRESSED:
                    BUTTON_SOUND.play()
                    if event.ui_element == new_game_button:
                        start_screen(screen)

                        play_music(DEFAULT_BIOM_SOUNDTRACK_PATH, -1)

                        return new_game()
                    if event.ui_element == continue_button:
                        pos, ox, hp, progress, was_died = get_save()
                        if not was_died:
                            play_music(DEFAULT_BIOM_SOUNDTRACK_PATH, -1)
                            game_statistics = get_statistics()
                            return pos, ox, hp, progress, game_statistics
                    if event.ui_element == settings_button:
                        settings_screen(screen)
                    if event.ui_element == exit_button:
                        terminate()

            main_menu_manager.process_events(event)

        main_menu_manager.update(tick)
        main_menu_manager.draw_ui(screen)
        pygame.display.flip()
        CLOCK.tick(FPS)
