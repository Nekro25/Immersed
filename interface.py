import pygame
from CONSTANTS import LIFEBAR_img, HEIGHT, SECOND


class LifeBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = LIFEBAR_img
        self.rect = self.image.get_rect().move(50, HEIGHT - 250)
        self.oxygen_lvl = 100
        self.oxygen_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.oxygen_event, SECOND)
        self.health_lvl = 100

    # def draw_lvl(self):
    #     ox_lvl_img = pygame.Surface((50, 200))
    #     pygame.draw.rect(ox_lvl_img, 'blue',
    #                      (0, 200 - self.oxygen_lvl * 2, 50, self.oxygen_lvl * 2))
    #     ox_lvl = pygame.sprite.Sprite()
    #     ox_lvl.image = ox_lvl_img
    #     ox_lvl.rect = ox_lvl_img.get_rect()
    #     return ox_lvl
