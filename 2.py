from tkinter.ttk import Widget
import pygame 
vidas = 3
pygame.init()
still = 0
jumping = 1
falling = 2
climbing = 3
WIDTH = 1000
HEIGHT = 800
gravity = 1
level = True
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('ats')
game = True
dk = pygame.image.load('assets/imagensDK/dkForward.png').convert_alpha()
dk = pygame.transform.scale(dk, (100,100))
bg = pygame.image.load('assets/grass.png').convert_alpha()
bg = pygame.transform.scale(bg, (800,700))
ball = pygame.image.load('assets/imagensDK/run-right.png').convert_alpha()
ball = pygame.transform.scale(ball, (40, 40))
escada = pygame.image.load('assets/imagensDK/escada.png').convert_alpha()
parede = pygame.image.load('assets/imagensDK/plataforma.png').convert_alpha()
barrel_img = pygame.image.load("assets/imagensDK/barrel1.png").convert_alpha()
barrel_img = pygame.transform.scale(barrel_img, (15, 15))
vida_img = pygame.font.Font('assets/PressStart2P.ttf', 28)
menu =  pygame.image.load("assets/imagensDK/title-screen.png").convert_alpha()
menu_width = 0.75 * WIDTH
menu_height = menu_width
menu = pygame.transform.scale(menu, (menu_height, menu_width))
over =  pygame.image.load("assets/DonkeyKong-master/game-over-screen.png").convert_alpha()
over = pygame.transform.scale(over, (menu_height, menu_width))
win =  pygame.image.load("assets/DonkeyKong-master/win-screen.png").convert_alpha()
win = pygame.transform.scale(win, (menu_height, menu_width))
climbing = pygame.image.load("assets/DonkeyKong-master/marioClimb1.png").convert_alpha()
climbing = pygame.transform.scale(climbing, (40, 40))

#sons
deathsound = pygame.mixer.Sound("assets/DonkeyKong-master/death/death.wav")
bacmusic = pygame.mixer.Sound("assets/DonkeyKong-master/bacmusic/bacmusic.wav")
introsound = pygame.mixer.Sound("assets/elevator.wav")
jumpsound = pygame.mixer.Sound("assets/DonkeyKong-master/jump/jump.wav")
walkingsound = pygame.mixer.Sound("assets/DonkeyKong-master/walking/walking.wav")
winsound = pygame.mixer.Sound("assets/fortnitewin.wav")
loosesound = pygame.mixer.Sound("assets/taketheL.wav")
bruh = pygame.mixer.Sound("assets/bruh.wav")
boom = pygame.mixer.Sound("assets/vineboom.wav")

vel_barril = -7
tmp = 0

pontuacao=0
pontosx = 10
pontosy = 10
fonte = pygame.font.Font("freesansbold.ttf", 32)
highscore = 0
def scoreboard(x,y):
    score = fonte.render("Score: " + str(pontuacao), True, (255, 255, 255))
    window.blit(score, (x,y))
def highscoreboard(x,y):
    score = fonte.render(str(highscore), True, (255, 255, 255))
    window.blit(score, (x,y))
def finalscore(x,y):
    score = fonte.render( str(pontuacao), True, (255, 255, 255))
    window.blit(score, (x,y))

    

class Tile(pygame.sprite.Sprite):

    def __init__(self, tile_img, i, n, incl):
        pygame.sprite.Sprite.__init__(self)
        tile_img = pygame.transform.scale(tile_img, (40, 20))
        self.image = tile_img
        self.rect = self.image.get_rect()
        if i%2 ==0 :
            self.rect.x = 40 * n
            self.rect.y = 40 * i 
        elif i == 20:
            self.rect.x = 40 * n
            self.rect.y = 40 * i 
        else:
            self.rect.x = 40 * n
            self.rect.y = 40 * i

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
        self.rect.bottom = 120
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
        if self.rect.right >= WIDTH-1:
            self.speedx = vel_barril 

class bola(pygame.sprite.Sprite):
    def __init__(self, img, row, column, blocks):
    
        pygame.sprite.Sprite.__init__(self)
        self.state = still

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = 700
        self.rect.bottom = 700
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
            
            self.speedy -= 20
            self.state = jumping


class DK(pygame.sprite.Sprite):
    def __init__(self, img):
    
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = 440
        self.rect.bottom = 120
    def joga(self):
        self.image = pygame.image.load('assets/DonkeyKong-master/dkLeft.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (100,100))
    def bate(self):
        self.image =  pygame.image.load('assets/imagensDK/dkForward.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (100,100))

class stair(pygame.sprite.Sprite):
    def __init__(self, tile_img, i, n):
        pygame.sprite.Sprite.__init__(self)
        tile_img = pygame.transform.scale(tile_img, (40, 60))
        self.image = tile_img
        self.rect = self.image.get_rect()
        self.rect.x = 40 * n 
        self.rect.y = 40 * i - 30


all_barril = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_stairs = pygame.sprite.Group()
blocks = pygame.sprite.Group()
final = pygame.sprite.Group()


MAP = [
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [3, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
            if tile_type == 2 or tile_type == 3:
                tile1 = stair(escada, i, n)
                all_sprites.add(tile1)
                all_stairs.add(tile1)
            if tile_type == 3:
                final.add(tile1)
            incl-=0.8
retry = fonte.render('(r)', True, (255, 255, 255))
esc = fonte.render('(esc)', True, (255, 255, 255))
trator = True
dk = DK(dk)
ball = bola(ball, 12, 4, blocks)
barrel = barril(barrel_img, 12, 4, blocks)
all_sprites.add(ball)
all_sprites.add(barrel)
all_sprites.add(dk)
all_barril.add(barrel)
final.add()
clock = pygame.time.Clock()
FPS = 60
game_state = "menu"
while game:
    clock.tick(FPS)
    cstr = pygame.sprite.spritecollide(ball, all_stairs, False)
    cbck = pygame.sprite.spritecollide(ball, ball.blocks, False)
    clear = pygame.sprite.spritecollide(ball, final, False)
    if tmp%120 == 0:
        barrel = barril(barrel_img, 12, 4, blocks)
        all_sprites.add(barrel)
        all_barril.add(barrel)
    for event in pygame.event.get():

            if event.type == pygame.QUIT:
                game = False

            if event.type == pygame.KEYDOWN:
                if game_state == "game over":
                    if event.key == pygame.K_r:
                        introsound.play()
                        game_state = "menu"
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                if game_state == "win":
                    if event.key == pygame.K_r:
                        introsound.play()
                        game_state = "menu"
                        level = True
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()

                if game_state == "menu":
                    vidas = 3
                    if event.key == pygame.K_SPACE:
                        game_state = "jogando"
                if game_state == "jogando":
                    introsound.stop()
                    if event.key == pygame.K_LEFT and ball.state != climbing:
                        ball.speedx -= 6
                        ball.image=pygame.image.load('assets/imagensDK/run-left.png').convert_alpha()
                        ball.image = pygame.transform.scale(ball.image, (40, 40))
                        #walkingsound.play()
                    elif event.key == pygame.K_RIGHT and ball.state != climbing:
                        ball.speedx += 6
                        ball.image=pygame.image.load('assets/imagensDK/run-right.png').convert_alpha()
                        ball.image = pygame.transform.scale(ball.image, (40, 40))
                        #walkingsound.play()
                    elif event.key == pygame.K_UP and ball.state != climbing:
                        jumpsound.play()
                        ball.jump()
                    elif event.key == pygame.K_SPACE and clear !=[] and ball.state == still:
                        walkingsound.play()
                        ball.state = climbing
                        ball.speedx = 0
                        level = False
                        
                    elif event.key == pygame.K_SPACE and cstr != [] and ball.state == still:
                        ball.state = climbing
                        ball.speedx = 0
            if event.type == pygame.KEYUP:
                if game_state == "jogando":
                    if event.key == pygame.K_LEFT and ball.state != climbing: 
                        ball.speedx =0
                    elif event.key == pygame.K_RIGHT and ball.state != climbing:
                        ball.speedx =0
    if game_state == "jogando":
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
        if barrel.rect.y >= 0:
            pontuacao += 1
        tmp +=1
        if level == False and ball.speedy >= 0: 
            game_state = "win"
            winsound.play()
            ball.rect.x = 700
            ball.rect.bottom = 700
        if ball.rect.top >= HEIGHT:
            loosesound.play()
            game_state = "game over"
            ball.rect.x = 700
            ball.rect.bottom = 700
        
        dkb = pygame.sprite.spritecollide(dk, all_barril, False)
        if dkb != []:
            dk.image = pygame.image.load('assets/DonkeyKong-master/dkleft.png').convert_alpha()
            dk.image = pygame.transform.scale(dk.image, (100,100))
        else:
            dk.image = pygame.image.load('assets/imagensDK/dkForward.png').convert_alpha()
            dk.image = pygame.transform.scale(dk.image, (100,100))
        morreu = pygame.sprite.spritecollide(ball, all_barril, False)
        if morreu != []:
            #deathsound.play()
            bruh.play()
            boom.play()
            vidas-=1
            ball.rect.x = 700
            ball.rect.bottom = 700
            for i in all_barril:
                if i.rect.bottom >=HEIGHT-300:
                    i.kill()
        if vidas == 0:
            loosesound.play()
            game_state = "game over"
        all_sprites.update()
        window.fill((0,0,0))
        all_sprites.draw(window)

        
        text_surface = vida_img.render(chr(9829) * vidas, True, (255, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.bottomleft = (10, HEIGHT - 10)
        window.blit(text_surface, text_rect)
        pontosx = WIDTH - 500
        pontosy = 10
        scoreboard(pontosx,pontosy)
    
    if game_state == "menu":
        winsound.stop()
        loosesound.stop()
        pontuacao = 0
        window.fill((0,0,0))
        window.blit(menu,(100, 0))
    if game_state == "game over":
        for barrel in all_barril:
            barrel.kill()
        pontuacao = 0
        window.fill((0,0,0))
        window.blit(over,(100, 0))
        pontosx = WIDTH/2
        pontosy = HEIGHT/2.2 - 10
        if pontuacao > highscore:
            highscore = pontuacao
        finalscore(pontosx,pontosy)
        highy = pontosy + 70
        highx = pontosx + 70
        highscoreboard(highx, highy)
        window.blit(retry,(pontosx +20, highy + 130))
        window.blit(esc,(pontosx , highy + 190))
    if game_state == "win":
        for barrel in all_barril:
            barrel.kill()
        window.fill((0,0,0))
        window.blit(win,(100, 0))
        pontosx = WIDTH/2
        pontosy = HEIGHT/2.2 - 10
        if pontuacao > highscore:
            highscore = pontuacao
        finalscore(pontosx,pontosy)
        highy = pontosy + 70
        highx = pontosx + 70
        highscoreboard(highx, highy)
        window.blit(retry,(pontosx +20, highy + 130))
        window.blit(esc,(pontosx , highy + 190))



    #window.fill((0, 0, 0))
    #window.blit(bg, (0, 0))


    
    pygame.display.update()

pygame.quit()