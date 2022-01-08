import pygame
from data_base import get_music_volume


def play_music(*args, fade_ms=0):
    pygame.mixer.music.load(args[0])
    if len(args) > 1:
        pygame.mixer.music.play(args[1])
    else:
        pygame.mixer.music.play(fade_ms)
    pygame.mixer.music.set_volume(get_music_volume())
