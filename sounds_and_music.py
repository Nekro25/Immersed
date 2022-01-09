import pygame
from data_base import get_music_volume
from CONSTANTS import BUTTON_SOUND, SHARK_SOUND, JELLY_SOUND, CTHULHU_SOUND, TABLET_SOUND, DEFAULT_BIOM_SOUNDTRACK_PATH


def play_music(*args, fade_ms=0):
    if not args:
        pygame.mixer.music.load(CURRENT_MUSIC)
    else:
        pygame.mixer.music.load(args[0])

    try:
        pygame.mixer.music.play(args[1], fade_ms=fade_ms)
    except IndexError:
        pygame.mixer.music.play(-1, fade_ms=fade_ms)

    pygame.mixer.music.set_volume(get_music_volume())


def set_volume_for_effects(volume):
    for sound_elem in [BUTTON_SOUND, SHARK_SOUND, JELLY_SOUND, CTHULHU_SOUND, TABLET_SOUND]:
        sound_elem.set_volume(volume)


def set_current_music(path):
    global CURRENT_MUSIC
    CURRENT_MUSIC = path


CURRENT_MUSIC = DEFAULT_BIOM_SOUNDTRACK_PATH
