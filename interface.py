import pygame
from CONSTANTS import LIFEBAR_img, HEIGHT, SECOND


class LifeBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = LIFEBAR_img
        self.rect = self.image.get_rect().move(50, HEIGHT - 300)
        self.oxygen_lvl = 100
        self.oxygen_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.oxygen_event, SECOND)
        self.health_lvl = 100

    def draw_ox_lvl(self):
        ox_lvl_img = pygame.Surface((60, 200))
        ox_lvl_img.fill((30, 30, 60))
        pygame.draw.rect(ox_lvl_img, (0, 150, 255),
                         (0, 200 - self.oxygen_lvl * 2, 60, self.oxygen_lvl * 2))
        ox_lvl = pygame.sprite.Sprite()
        ox_lvl.image = ox_lvl_img
        ox_lvl.rect = ox_lvl_img.get_rect().move(100, HEIGHT - 275)
        return ox_lvl

    def draw_hp_lvl(self):
        hp_lvl_img = pygame.Surface((60, 200))
        hp_lvl_img.fill((60, 30, 30))
        pygame.draw.rect(hp_lvl_img, (150, 0, 0),
                         (0, 200 - self.health_lvl * 2, 60, self.health_lvl * 2))
        hp_lvl = pygame.sprite.Sprite()
        hp_lvl.image = hp_lvl_img
        hp_lvl.rect = hp_lvl_img.get_rect().move(190, HEIGHT - 275)
        return hp_lvl
