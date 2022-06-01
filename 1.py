import pygame 

pygame.init()
still = 0
jumping = 1
falling = 2
WIDTH = 1000
HEIGHT = 880
gravity = 5
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('ats')
game = True

bg = pygame.image.load('assets/grass.png').convert_alpha()
bg = pygame.transform.scale(bg, (800,700 ))
ball = pygame.image.load('assets/imagensDK/run-right.png').convert_alpha()
ball = pygame.transform.scale(ball, (40, 40))
escada = pygame.image.load('assets/imagensDK/escada.png').convert_alpha()
parede = pygame.image.load('assets/imagensDK/plataforma.png').convert_alpha()
barrel = pygame.image.load("assets/imagensDK/barrel1.png").convert_alpha()
vel_barril = -4

class Tile(pygame.sprite.Sprite):

    def __init__(self, tile_img, i, n, incl):
        pygame.sprite.Sprite.__init__(self)
        tile_img = pygame.transform.scale(tile_img, (40, 40))
        self.image = tile_img
        self.rect = self.image.get_rect()
        if i%2 ==0 :
            self.rect.x = 40 * n
            self.rect.y = 40 * i + incl
        elif i == 20:
            self.rect.x = 40 * n
            self.rect.y = 40 * i - incl
        else:
            self.rect.x = 40 * n
            self.rect.y = 40 * i - incl

class ladder(pygame.sprite.Sprite):
    def __init__(self, tile_img):
        pygame.sprite.Sprite.__init__(self)
        tile_img = pygame.transform.scale(tile_img, (40, 40))
        self.image = tile_img
        self.rect = self.image.get_rect()

class barril(pygame.sprite.Sprite):
    def __init__(self, img, row, column, blocks):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.bottom = 0
        self.blocks = blocks
        self.speedx = vel_barril
        self.speedy = 0
    def update(self):
        self.speedy += gravity
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        hits = pygame.sprite.spritecollide(self, self.blocks, False)
        if self.speedy > 0:
            self.state = falling
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right >= WIDTH:
            self.rect.right = WIDTH - 1
        for i in hits:
            if self.speedy > 0:
                self.rect.bottom = i.rect.top
                self.speedy = 0
                
            if self.speedy < 0:
                self.rect.top = i.rect.bottom
                self.speedy = 0
        if self.rect.x <= 0:
            self.speedx = - vel_barril 
        if self.rect.x >= WIDTH-39:
            self.speedx = vel_barril 

class bola(pygame.sprite.Sprite):
    def __init__(self, img, row, column, blocks):
    
        pygame.sprite.Sprite.__init__(self)
        self.state = still

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = column * 40
        self.rect.bottom = 350
        self.blocks = blocks
        self.speedx = 0
        self.speedy = 0
    def update(self):
        self.speedy += gravity
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        hits = pygame.sprite.spritecollide(self, self.blocks, False)
        if self.speedy > 0:
            self.state = falling
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right >= WIDTH:
            self.rect.right = WIDTH - 1
        for i in hits:
            if self.speedy < 0 :
                self.rect.top = i.rect.bottom
                self.speedy = 0
                self.state = still
            if self.speedy > 0 and self.rect.bottom :
                self.rect.bottom = i.rect.top
                self.speedy = 0
                self.state = still
            
    def jump(self):
        if self.state == still:
            self.speedy -= 40
            self.state = jumping
all_barril = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
blocks = pygame.sprite.Group()


MAP = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]    
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
                tile1 = Tile(escada, i, n, incl)
                all_sprites.add(tile1)
                blocks.add(tile1)
            incl-=1


ball = bola(ball, 12, 4, blocks)
barrel = barril(barrel, 12, 4, blocks)
all_sprites.add(ball)
all_sprites.add(barrel)
all_barril.add(barrel)
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
                    ball.jump()


            if event.type == pygame.KEYUP:

                if event.key == pygame.K_LEFT:
                    ball.speedx += 5
                elif event.key == pygame.K_RIGHT:
                    ball.speedx -= 5

    morreu = pygame.sprite.spritecollide(ball, all_barril, False)
    if morreu != []:
        pygame.quit()

    window.fill((0, 0, 0))
    #window.blit(bg, (0, 0))

    all_sprites.update()
    all_sprites.draw(window)
    pygame.display.update()

pygame.quit()