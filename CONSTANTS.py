import pygame
import pygame_gui as gui
import os
import sys
import sqlite3

pygame.init()
WIDTH, HEIGHT = pygame.display.get_desktop_sizes()[0]
screen = pygame.display.set_mode((WIDTH, HEIGHT))


class FileError(Exception):
    pass


def load_image(filename, color_key=None):
    fullname = os.path.join('data', filename)

    if not os.path.isfile(fullname):
        raise FileError(f"Файл с изображением '{fullname}' не найден")
    image = pygame.image.load(fullname)
    if color_key:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


def terminate():
    pygame.quit()
    sys.exit()


WATER = 0
GROUND = 1
ICE = 2
PLAYER = 7
ICE_bg = 3
GROUND_bg = 4
OXYGEN_FILLER = 5
REACTOR = 6
MAIN_SHIP = 12
SHIP_1 = 8
SHIP_2 = 9
SHIP_3 = 10
SHIP_4 = 11
MONSTER_1 = 13

GRAY = (150, 150, 150, 255)
BLUE = (0, 0, 255, 255)
BLACK_BLUE = (0, 0, 100, 255)
BROWN = (70, 40, 0, 255)
BLACK_BROWN = (35, 20, 0, 255)
YELLOW = (255, 255, 0, 255)
BLACK_RED = (125, 0, 0, 255)
DIRTY_GREEN = (70, 70, 0, 255)
GREEN_0 = (0, 255, 0, 255)
GREEN_1 = (0, 255, 1, 255)
GREEN_2 = (0, 255, 2, 255)
GREEN_3 = (0, 255, 3, 255)
GREEN_4 = (0, 255, 4, 255)
RED_1 = (255, 1, 0, 255)

BLOCKS = {
    GRAY: WATER,
    BROWN: GROUND,
    YELLOW: PLAYER,
    BLUE: ICE,
    BLACK_BLUE: ICE_bg,
    BLACK_BROWN: GROUND_bg,
    BLACK_RED: REACTOR,
    DIRTY_GREEN: OXYGEN_FILLER,
    GREEN_0: MAIN_SHIP,
    GREEN_1: SHIP_1,
    GREEN_2: SHIP_2,
    GREEN_3: SHIP_3,
    GREEN_4: SHIP_4,
    RED_1: MONSTER_1
}

MAP_NAME = 'map.png'
FPS = 60


BLOCK_SIZE = 50
PLAYER_SIZE = 50
SECOND = 1000
create_monster_event = pygame.USEREVENT + 4
pygame.time.set_timer(create_monster_event, SECOND * 50)

CLOCK = pygame.time.Clock()

GROUND_img = load_image('ground.png')
PLAYER_img = load_image('Player.png')
WATER_img = load_image('water.png')
BACKGROUND_img = pygame.transform.scale(load_image('all_image(shallow water).png'),
                                        (WIDTH * 1.5, HEIGHT * 1.5))
LIFEBAR_img = load_image('lifebar.png')
ICE_img = load_image('ice.png')
ICE_CAVE_BG_img = pygame.transform.scale(load_image('ice_cave_background.png'),
                                         (WIDTH * 1.5, HEIGHT * 1.5))
GROUND_CAVE_BG_img = pygame.transform.scale(load_image('cave_background.png'),
                                            (WIDTH * 1.5, HEIGHT * 1.5))
OXYGEN_FILLER_img = load_image('oxygen_filler.png')
REACTOR_img = load_image('reactor.png')
EMPTY_DISPLAY_img = load_image('empty_display.png')
PLAYER_ANIMATION_img = load_image('player_animation.png')
MAIN_MENU_BACKGROUND_img = pygame.transform.scale(
    load_image('all_image(shallow water).png'), (WIDTH, HEIGHT))
END_SCREEN_BACKGROUND_img = pygame.transform.scale(load_image('end_screen.png'),
                                                   (WIDTH, HEIGHT))
SHIP_1_img = load_image('spaceship_1.png')
SHIP_2_img = load_image('spaceship_2.png')
SHIP_3_img = load_image('spaceship_3.png')
SHIP_4_img = load_image('spaceship_4.png')
MAIN_SHIP_img = load_image('main_spaceship.png')
PURPLE_SHARK_img = load_image('purple_shark(monster).png')
PURPLE_SHARK_ANIMATION_img = load_image('purple_shark_animation.png')
JELLYFISH_img = load_image('eye_jellyfish(monster).png')
JELLYFISH_ANIMATION_img = load_image('eye_jellyfish_animation.png')
BABY_CTULHU_img = load_image('baby_ctulhu(monster).png')
BABY_CTULHU_ANIMATION_img = load_image('baby_ctulhu_animation.png')

FONT_PATH = 'Fonts/font.png'
FONT_IMG_WIDTH = 815
FONT_IMG_HEIGHT = 8
FONT_BLOCK_WIDTH = 5
FONT_BLOCK_HEIGHT = 8
FONT_BARRIER = 1

MAIN_MENU_BUTTON_WIDTH = 130
MAIN_MENU_BUTTON_HEIGHT = 50
MAIN_MENU_BUTTON_X_MARGIN = (WIDTH / 2) - MAIN_MENU_BUTTON_WIDTH * 2 - 45
MAIN_MENU_BUTTON_Y_MARGIN = HEIGHT / 2
MAIN_MENU_BUTTON_SPACING = 30

END_SCREEN_BUTTON_WIDTH = 260
END_SCREEN_BUTTON_HEIGHT = 50
END_SCREEN_BUTTON_X_MARGIN = (WIDTH - END_SCREEN_BUTTON_WIDTH) / 2
END_SCREEN_BUTTON_Y_MARGIN = HEIGHT / 2 - 100
END_SCREEN_BUTTON_SPACING = 30

CON = sqlite3.connect('game_data.db')
CURSOR = CON.cursor()

DISPLAY_FRAMES = [load_image('Display_images/darkened_display_1.png'),
                  load_image('Display_images/darkened_display_2.png'),
                  load_image('Display_images/darkened_display_3.png'),
                  load_image('Display_images/darkened_display_4.png'),
                  load_image('Display_images/darkened_display_5.png'),
                  load_image('Display_images/darkened_display_6.png'),
                  load_image('Display_images/darkened_display_7.png'),
                  load_image('Display_images/darkened_display_8.png'),
                  load_image('Display_images/darkened_display_9.png'),
                  load_image('Display_images/darkened_display_10.png'),
                  load_image('Display_images/darkened_display_11.png'),
                  load_image('Display_images/darkened_display_12.png'),
                  load_image('Display_images/darkened_display_13.png'),
                  load_image('Display_images/darkened_display_14.png'),
                  load_image('Display_images/darkened_display_15.png'),
                  load_image('Display_images/darkened_display_16.png'),
                  load_image('Display_images/darkened_display_17.png'),
                  load_image('Display_images/darkened_display_18.png'),
                  load_image('Display_images/darkened_display_19.png'),
                  load_image('Display_images/darkened_display_20.png'),
                  load_image('Display_images/darkened_display_21.png'),
                  load_image('Display_images/darkened_display_22.png'),
                  load_image('Display_images/darkened_display_23.png'),
                  ]

BUTTON_SOUND = pygame.mixer.Sound("data/SFX/button_pressing_sound.wav")

MAIN_MENU_SOUNDTRACK_PATH = 'data/SFX/menu_soundtrack.mp3'
DEFAULT_BIOM_SOUNDTRACK_PATH = 'data/SFX/default_biom_soundtrack.mp3'
SNOW_BIOM_SOUNDTRACK_PATH = 'data/SFX/snow_biom_soundtrack.mp3'
CAVE_BIOM_SOUNDTRACK_PATH = 'data/SFX/cave_biom_soundtrack.mp3'
SIREN_SOUNDTRACK_PATH = 'data/SFX/siren_sound.mp3'
BEEP_SOUNDTRACK_PATH = 'data/SFX/beep_sound.wav'
AFTER_DEATH_SOUNDTRACK_PATH = 'data/SFX/after_death_soundtrack.mp3'

ship_messages = ['Иследуя мир, вы нашли разрушенный объект.' \
                 'Подходя ближе вы поняли, что это дрон-исследователь.' \
                 'Такие дроны запускает правительство чтобы обследовать не разведаннные територии.' \
                 'По его состоянию понятно что он пролежал тут не мало,' \
                 'но вам удается достать из него рабочий аппарат связи.',
                 'Покаряя глубины планеты, вы натыкаетесь на странное строение,' \
                 'но подойдя ближе понимаете, что это гражданский космический корабль.' \
                 'Такой вид кораблей был изобретен почти сразу же после войны двух государств.' \
                 'Вам стало жалко того кто попал на нем сюда,' \
                 'скорее всего он тоже был притянут сильной гравитацией.' \
                 'В этом корабле вы находите блок управления движением корабля.',
                 'Плывя внутри ледника вы находите останки большого корабля,' \
                 'судя по расцветке, это корабль империи,' \
                 'развившейся от земных предков объединенных стран (NATO).' \
                 'Корабль ,наверняка, попал сюда во время войны.' \
                 'Военные корбали всегда были оснащены надежной защитой,' \
                 'немного покапавшись вы обнаружили генератор защитного поля',
                 'В глубине вы увидели металические проблески, не поверив своим глазам,' \
                 'вы решаетесь подойти ближе. Нет, вам не показалось, это и в правду корабль.' \
                 'Вы никогда не встречали таких кораблей,' \
                 'но по огромнуму отсеку стало понятно, либо этот корабль грузовой,' \
                 'либо пасажирский. Во всяком случае,' \
                 'у таких кораблей должен быть мощный двигатель.' \
                 'Пришлось потрудиться чтобы достать уселитель двигателя.',
                 'Проплывая по пещерам планеты, вы чувствете неприятные колебания воды вокруг.' \
                 'Не понимая чем вызваны эти колебания, вы пытаетесь найти их источник.' \
                 'И в конце концов приближаетесь к непонятному строению,' \
                 'это точно не дело рук человека...' \
                 'Хотя, на объекте начерчены символы которые были в писменах Японии.' \
                 'Но Япония была уничтожена ядерной бомбой, видимо были и выжившие.' \
                 'По значкам изображенных на экране вы понимаете что батарея этого строения переполнена,' \
                 'возможно именно это стало причиной крушения стольких кораьлей.' \
                 'Вы успешно достаете батарею сверхвысокоц емкоси']
PARTS_COLLECTED_text = 'Чтобы починить корабль все запчасти собраны, но вам кажется что заряда оставшегося на корабле может не хватить'
BATTERY_COLLECTED_text = 'Теперь точно все готово, можно улетать'
