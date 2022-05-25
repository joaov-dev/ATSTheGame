import pygame 

pygame.init()

WIDTH = 480
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('ats')
game = True
while game:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    window.fill((0, 0, 0))
    pygame.display.update()

pygame.quit()