import pygame 

pygame.init()



WIDTH = 480
HEIGHT = 600
gravity = 5
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('ats')
game = True

bg = pygame.image.load('grass.png').convert_alpha()
bg = pygame.transform.scale(bg, (500,700 ))
ball = pygame.image.load('ball.png').convert_alpha()
ball = pygame.transform.scale(ball, (20, 20))

parede = pygame.image.load('parede.jpeg').convert_alpha()






class Tile(pygame.sprite.Sprite):

    def __init__(self, tile_img, i, n):
        pygame.sprite.Sprite.__init__(self)
        tile_img = pygame.transform.scale(tile_img, (40, 40))
        self.image = tile_img
        self.rect = self.image.get_rect()
        self.rect.x = 40 * n
        self.rect.y = 40 * i

class bola(pygame.sprite.Sprite):
    def __init__(self, img, row, column, blocks):
    
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = column * 40
        self.rect.bottom = 300
        self.blocks = blocks
        self.speedx = 0
        self.speedy = gravity
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        hits = pygame.sprite.spritecollide(self, self.blocks, False)
        for i in hits:
            if self.speedy > 0:
                self.rect.bottom = i.rect.top
                self.speedy = 0
            elif self.speedy < 0:
                self.rect.top = i.rect.bottom
                self.speedy = 0
    



all_sprites = pygame.sprite.Group()
blocks = pygame.sprite.Group()



BLOCK = 0
EMPTY = -1
MAP = [
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, EMPTY, EMPTY, EMPTY],
    [BLOCK, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, BLOCK, EMPTY, EMPTY, EMPTY, BLOCK, BLOCK],
    [EMPTY, EMPTY, BLOCK, EMPTY, BLOCK, BLOCK, BLOCK, BLOCK, EMPTY, BLOCK, BLOCK, BLOCK],
    [BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK],
    [BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK],
]

for i in range(len(MAP)):
        for n in range(len(MAP[i])):
            tile_type = MAP[i][n]
            if tile_type == BLOCK:
                tile = Tile(parede, i, n)
                all_sprites.add(tile)
                blocks.add(tile)
ball = bola(ball, 12, 4, blocks)
all_sprites.add(ball)
clock = pygame.time.Clock()
FPS = 60
while game:
    clock.tick(FPS)

    for event in pygame.event.get():


            if event.type == pygame.QUIT:
                game = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:
                    ball.speedx -= 5
                elif event.key == pygame.K_RIGHT:
                    ball.speedx += 5
                elif event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                    ball.speedy -= 5


            if event.type == pygame.KEYUP:

                if event.key == pygame.K_LEFT:
                    ball.speedx += 5
                elif event.key == pygame.K_RIGHT:
                    ball.speedx -= 5

    window.fill((0, 0, 0))
    window.blit(bg, (0, 0))

    all_sprites.update()
    all_sprites.draw(window)
    pygame.display.update()


pygame.quit()