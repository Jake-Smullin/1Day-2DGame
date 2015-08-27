import sys
import random
from random import randint
import pygame
from pygame.locals import *
import os

SCREENRECT = Rect(0, 0, 640, 480)

def load_image(filename, colorkey = None):
    filename = os.path.join('data', filename)
    image = pygame.image.load(filename).convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return imgcolorkey(image, colorkey)

class Player(pygame.sprite.Sprite):
    speed = 10
    gun_offset = -11
    bounce = 20
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('player1.bmp', -1)
        #self.surface = pygame.Surface((64,64)).convert()
        self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
        self.reloading = 0
        self.origtop = self.rect.top
        self.facing = -1
        self.x = 0
        self.where = 320

    def handleKeys(self):
        key = pygame.key.get_pressed()
        dist = 5 # distance moved in 1 frame, try changing it to 5
        if  self.where < 615 and  self.where > 25:
            if key[pygame.K_RIGHT]: # right key
                self.rect.move_ip((dist, 0))
                self.where += dist
            elif key[pygame.K_LEFT]: # left key
                self.rect.move_ip((-dist, 0))
                self.where -= dist
        elif not self.where < 615:
            if key[pygame.K_LEFT]: # left key
                self.rect.move_ip((-dist, 0))
                self.where -= dist
        elif not self.where > 25:
            if key[pygame.K_RIGHT]: # right key
                self.rect.move_ip((dist, 0))
                self.where += dist


    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen):
        self.speed = randint(1,2)
        pygame.sprite.Sprite.__init__(self)
        print "created a new sprite:", id(self)
        self.image = pygame.image.load("meteor.png")
        self.rect = self.image.get_rect()
        self.rect.move_ip(randint(25, 615), 0)

    def update(self):
        self.rect.move_ip(0, self.speed)

def main():
    pygame.init()
    winstyle = 0
    clock = pygame.time.Clock()
    bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pygame.display.set_mode((640, 480), winstyle, bestdepth)
    enemies = pygame.sprite.Group()
    player = Player()

    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                enemies.add(Enemy(screen))
            elif event.type == QUIT:
                sys.exit()
        enemies.update()
        screen.fill(pygame.Color("black"))
        enemies.draw(screen)
        player.draw(screen)
        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    main()