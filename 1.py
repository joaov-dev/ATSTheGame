import pygame 
from classe import *


pygame.init()
still = 0
jumping = 1
falling = 2
climbing = 3
WIDTH = 1000
HEIGHT = 800
gravity = 5
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('ats')
game = True
dk = pygame.image.load('assets/imagensDK/dkForward.png').convert_alpha()
dk = pygame.transform.scale(dk, (60,60))
bg = pygame.image.load('assets/grass.png').convert_alpha()
bg = pygame.transform.scale(bg, (800,700))
ball = pygame.image.load('assets/imagensDK/run-right.png').convert_alpha()
ball = pygame.transform.scale(ball, (40, 40))
escada = pygame.image.load('assets/imagensDK/escada.png').convert_alpha()
parede = pygame.image.load('assets/imagensDK/plataforma.png').convert_alpha()
barrel_img = pygame.image.load("assets/imagensDK/barrel1.png").convert_alpha()
vel_barril = -4


all_barril = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_stairs = pygame.sprite.Group()
blocks = pygame.sprite.Group()


MAP = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  
]

for i in range(len(MAP)):
        incl=0
        for n in range(len(MAP[i])):
            tile_type = MAP[i][n]
            if tile_type == 1:
                tile = Tile(parede, i, n, incl)
                all_sprites.add(tile)
                blocks.add(tile)
            if tile_type == 2:
                tile1 = stair(escada, i, n)
                all_sprites.add(tile1)
                all_stairs.add(tile1)
            incl-=0.8
trator = True
dk = DK(dk)
ball = bola(ball, 12, 4, blocks)
barrel = barril(barrel_img, 12, 4, blocks)
all_sprites.add(ball)
all_sprites.add(barrel)
all_sprites.add(dk)
all_barril.add(barrel)
clock = pygame.time.Clock()
FPS = 60
while game:
    clock.tick(FPS)
    cstr = pygame.sprite.spritecollide(ball, all_stairs, False)
    cbck = pygame.sprite.spritecollide(ball, ball.blocks, False)
    tmp = 0
    if tmp%60 == 0:
        barrel = barril(barrel_img, 12, 4, blocks)
        all_sprites.add(barrel)
        all_barril.add(barrel)
    for event in pygame.event.get():

            if event.type == pygame.QUIT:
                game = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT and ball.state != climbing:
                    ball.speedx -= 8
                elif event.key == pygame.K_RIGHT and ball.state != climbing:
                    ball.speedx += 8
                elif event.key == pygame.K_UP and ball.state != climbing:
                    ball.jump()
                elif event.key == pygame.K_SPACE and cstr != [] and ball.state == still:
                    ball.state = climbing
                    ball.speedx = 0
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and ball.state != climbing:
                    ball.speedx += 8
                elif event.key == pygame.K_RIGHT and ball.state != climbing:
                    ball.speedx -= 8
    if ball.state == climbing:
        if trator == True:
            ball.rect.y = cstr[0].rect.y
            ball.rect.x = cstr[0].rect.x
            trator = False
        ball.state = climbing
        if cstr != [] or cbck != []:
            ball.speedy -= 1
        else:
            ball.state = still
            ball.speedy = 0
            Trator = True
                


    morreu = pygame.sprite.spritecollide(ball, all_barril, False)
    #if morreu != []:
     #   pygame.quit()

    window.fill((0, 0, 0))
    #window.blit(bg, (0, 0))


    all_sprites.update()
    all_sprites.draw(window)
    pygame.display.update()
    tmp +=1

pygame.quit()