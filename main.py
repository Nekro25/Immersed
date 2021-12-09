import pygame

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Name')
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
    pygame.quit()
