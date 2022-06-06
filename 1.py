import pygame 

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
        self.rect.x = 440
        self.rect.bottom = 70
        self.blocks = blocks
        self.speedx = vel_barril
        self.speedy = 0
    def update(self):
        self.speedy += gravity
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        hits = pygame.sprite.spritecollide(self, self.blocks, False)
        if self.speedy > 0 :
            self.state = falling
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right >= WIDTH:
            self.rect.right = WIDTH - 1
        for i in hits:
            if self.speedy > 0:
                self.rect.bottom = i.rect.top
                self.speedy = 0
                
            elif self.speedy < 0:
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
        if self.state != climbing:
            self.speedy += gravity
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        hits = pygame.sprite.spritecollide(self, self.blocks, False)
        if self.speedy > 0 and self.state != climbing:
            self.state = falling
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right >= WIDTH:
            self.rect.right = WIDTH - 1
        for i in hits:
            if self.speedy < 0 and self.state != climbing:
                self.rect.top = i.rect.bottom
                self.speedy = 0
                self.state = still
            if self.speedy > 0 and self.state != climbing :
                self.rect.bottom = i.rect.top
                self.speedy = 0
                self.state = still
            
    def jump(self):
        if self.state == still:
            self.speedy -= 40
            self.state = jumping
    
    def escada(self):
        if self.state == still or self.state == climbing:
            print(1)
            self.rect.y = cstr[0].rect.y
            self.rect.x = cstr[0].rect.x
            self.state = climbing
            if cstr != [] or cbck != []:
                self.speedy = -5
            else:
                print(1)
                self.state = still
                self.speedy = 0



class DK(pygame.sprite.Sprite):
    def __init__(self, img):
    
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = 440
        self.rect.bottom = 70

class stair(pygame.sprite.Sprite):
    def __init__(self, tile_img, i, n):
        pygame.sprite.Sprite.__init__(self)
        tile_img = pygame.transform.scale(tile_img, (40, 40))
        self.image = tile_img
        self.rect = self.image.get_rect()
        self.rect.x = 40 * n
        self.rect.y = 40 * i

all_barril = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_stairs = pygame.sprite.Group()
blocks = pygame.sprite.Group()


MAP = [
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
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
            incl-=1

dk = DK(dk)
ball = bola(ball, 12, 4, blocks)
barrel = barril(barrel, 12, 4, blocks)
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
    for event in pygame.event.get():
            print (ball.state)

            if event.type == pygame.QUIT:
                game = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT and ball.state != climbing:
                    ball.speedx -= 5
                elif event.key == pygame.K_RIGHT and ball.state != climbing:
                    ball.speedx += 5
                elif event.key == pygame.K_UP and ball.state != climbing:
                    ball.jump()
                elif event.key == pygame.K_SPACE and cstr != [] and ball.state == still:
                    ball.state = climbing
                    ball.speedx = 0
                    


            if event.type == pygame.KEYUP:

                if event.key == pygame.K_LEFT and ball.state != climbing:
                    ball.speedx += 5
                elif event.key == pygame.K_RIGHT and ball.state != climbing:
                    ball.speedx -= 5
    if ball.state == climbing:
        if cstr != []:
            ball.rect.y = cstr[0].rect.y
            ball.rect.x = cstr[0].rect.x
            ball.state = climbing
        if cstr != [] or cbck != []:
            ball.speedy -= 1
        else:
            ball.state = still
            ball.speedy = 0
                


    morreu = pygame.sprite.spritecollide(ball, all_barril, False)
    #if morreu != []:
     #   pygame.quit()

    window.fill((0, 0, 0))
    #window.blit(bg, (0, 0))


    all_sprites.update()
    all_sprites.draw(window)
    pygame.display.update()

pygame.quit()