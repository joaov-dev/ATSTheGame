import pygame
import os
import random
pygame.init()

WIDTH = 1500
HEIGHT = 400
speed = 14
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('dino')
game = True
still = 0
jumping = 1
track = pygame.image.load(os.path.join("assetsdino/Other", "Track.png"))
dino = pygame.image.load(os.path.join("assetsdino/Dino", "DinoRun1.png"))
cactus = [pygame.image.load(os.path.join("assetsdino/Cactus", "SmallCactus1.png")),pygame.image.load(os.path.join("assetsdino/Cactus", "SmallCactus2.png")),pygame.image.load(os.path.join("assetsdino/Cactus", "SmallCactus3.png")),pygame.image.load(os.path.join("assetsdino/Cactus", "LargeCactus1.png")),pygame.image.load(os.path.join("assetsdino/Cactus", "LargeCactus2.png")),pygame.image.load(os.path.join("assetsdino/Cactus", "LargeCactus3.png"))]
ptero = pygame.image.load(os.path.join("assetsdino/Bird", "Bird1.png"))
exist = False
class obs(pygame.sprite.Sprite):
    def __init__(self, img):
    
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.left = 1500
        self.rect.bottom = 370
        self.speedx = 0 
    def update(self):
        self.rect.x += self.speedx
        

class player(pygame.sprite.Sprite):
    def __init__(self, img):
    
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.bottom = 370
        self.speedy = 0 
        self.state = still

    def update(self):
        self.rect.y += self.speedy
        if self.state == jumping:
            self.speedy += 5
        if self.rect.bottom >= 350:
            self.speedy=0
            self.state=still
    def jump(self):
        if self.state == still:
            self.speedy -= 40
            self.state = jumping
all_sprites = pygame.sprite.Group()
all_obs = pygame.sprite.Group()
dino = player(dino)
all_sprites.add(dino)

clock = pygame.time.Clock()
FPS = 60
track_x=0
track_width = track.get_width()
while game:
    type = random.randint(0,8)
    clock.tick(FPS)
    indice=random. randint(0,5)
    if exist == False:
        if type <=5:
            cac = obs(cactus[indice])
        else:
            cac= obs(ptero)
            cac.rect.y -= 60
        exist = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN:   
            if event.key == pygame.K_SPACE:
                player.jump(dino)

    window.fill((255, 255, 255)) 
    window.blit(track,(track_x,360))
    window.blit(track,(track_width+track_x,360))
    if track_x <= -track_width:
             window.blit(track,(track_width+track_x,360))
             track_x = 0
    track_x-=speed
    cac.speedx = -speed
    
    if cac.rect.x < -cac.rect.width:
        cac.kill()
        exist = False
        all_obs
    all_obs. add(cac)
    all_obs.update()
    all_obs.draw(window)
    all_sprites.update()
    all_sprites.draw(window)

    pygame.display.update()  

pygame.quit()

 