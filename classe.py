import pygame
still = 0
jumping = 1
falling = 2
WIDTH = 1000
HEIGHT = 880
gravity = 5
vel_barril = -4
climbing = 3
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



class DK(pygame.sprite.Sprite):
    def __init__(self, img):
    
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = 440
        self.rect.bottom = 128

class stair(pygame.sprite.Sprite):
    def __init__(self, tile_img, i, n):
        pygame.sprite.Sprite.__init__(self)
        tile_img = pygame.transform.scale(tile_img, (40, 40))
        self.image = tile_img
        self.rect = self.image.get_rect()
        self.rect.x = 40 * n
        self.rect.y = 40 * i