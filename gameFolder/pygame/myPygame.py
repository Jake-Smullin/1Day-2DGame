import sys
import random
from random import randint
import pygame
from pygame.locals import *
import os

SCREENRECT = Rect(0, 0, 640, 480)
enemies = pygame.sprite.Group()
MAX_SHOTS = 3

main_dir = os.path.split(os.path.abspath(__file__))[0]

def imgcolorkey(image, colorkey):
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image

def load_image(filename, colorkey = None):
    filename = os.path.join('data', filename)
    image = pygame.image.load(filename).convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return imgcolorkey(image, colorkey)

class SpriteSheet:
    def __init__(self, filename):
        self.sheet = load_image(filename)
    def imgat(self, rect, colorkey = None):
        rect = Rect(rect)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        return imgcolorkey(image, colorkey)
    def imgsat(self, rects, colorkey = None):
        imgs = []
        for rect in rects:
            imgs.append(self.imgat(rect, colorkey))
        return imgs

class Arena:
    speed = 2
    def __init__(self):
        w = SCREENRECT.width
        h = SCREENRECT.height
        self.tileside = self.myBackgroundTile.get_height()
        self.counter = 0
        self.surface = pygame.Surface((w, h + self.tileside)).convert()
        for x in range(w/self.tileside):
            for y in range(h/self.tileside + 1):
                self.surface.blit(self.myBackgroundTile, (x*self.tileside, y*self.tileside))
    def increment(self):
        self.counter = (self.counter - self.speed) % self.tileside

class dummysound:
    def play(self): pass

def load_sound(file):
    if not pygame.mixer: return dummysound()
    file = os.path.join(main_dir, 'data', file)
    try:
        sound = pygame.mixer.Sound(file)
        return sound
    except pygame.error:
        print ('Warning, unable to load, %s' % file)
    return dummysound()

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
        self.Xwhere = 320
        self.Ywhere = 460

    def handleKeys(self):
        key = pygame.key.get_pressed()
        dist = 5 # distance moved in 1 frame, try changing it to 5
        if  self.Xwhere < 615 and  self.Xwhere > 25 and self.Ywhere < 480 and self.Ywhere > 0:
            if key[pygame.K_RIGHT]: # right key
                self.rect.move_ip((dist, 0))
                self.Xwhere += dist
            elif key[pygame.K_LEFT]: # left key
                self.rect.move_ip((-dist, 0))
                self.Xwhere -= dist
            if key[pygame.K_UP]: # up key
                self.rect.move_ip((0, -dist))
                self.Ywhere -= dist
            elif key[pygame.K_DOWN]: # down key
                self.rect.move_ip((0, dist))
                self.Ywhere += dist
        elif not self.Xwhere < 615:
            if key[pygame.K_LEFT]: # left key
                self.rect.move_ip((-dist, 0))
                self.Xwhere -= dist
        elif not self.Xwhere > 25:
            if key[pygame.K_RIGHT]: # right key
                self.rect.move_ip((dist, 0))
                self.Xwhere += dist
        elif not self.Ywhere < 455:
            if key[pygame.K_UP]: # left key
                self.rect.move_ip((-dist, 0))
                self.Ywhere -= dist
        elif not self.Ywhere > 25:
            if key[pygame.K_DOWN]: # right key
                self.rect.move_ip((dist, 0))
                self.Ywhere += dist

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Explosion(pygame.sprite.Sprite):
    defaultlife = 12
    animcycle = 3
    def __init__(self, actor, surface):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('explosion1.gif', -1)
        self.rect = self.image.get_rect()
        surface.blit(self.image,actor.rect)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen, speed):
        self.speed = speed
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("meteor.png", -1)
        self.rect = self.image.get_rect()
        self.rect.move_ip(randint(25, 615), 0)

    def update(self):
        self.rect.move_ip(0, self.speed)

class Score(pygame.sprite.Sprite):
    def __init__(self, surface):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 20)
        self.font.set_italic(1)
        self.color = Color('white')
        self.lastscore = -1
        msg = "Score: %d" % 0
        self.image = self.font.render(msg, 0, self.color)
        self.surface = surface
        self.rect = self.image.get_rect().move(10, 450)
   
    def draw(self, score):
        msg = "Score: %d" % score
        self.image = self.font.render(msg, 0, self.color)
        self.surface.blit(self.image, self.rect)

def run(difficulty):
    pygame.init()
    if pygame.mixer and not pygame.mixer.get_init():
        print ('Warning, no sound')
        pygame.mixer = None
    keystate = pygame.key.get_pressed()
    winstyle = 0
    clock = pygame.time.Clock()
    bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pygame.display.set_mode((640, 480), winstyle, bestdepth)
    spritesheet = SpriteSheet('background2.gif')
    Arena.myBackgroundTile = spritesheet.imgat((0, 0, 32, 32))
    arena = Arena()
    player = Player()
    score = Score(screen)

    if pygame.mixer:
        music = os.path.join(main_dir, 'data', 'thegame.mp3')
        pygame.mixer.music.load(music)
        pygame.mixer.music.play(-1)

    SCORE = 0
    while True:
        firing = keystate[K_SPACE]
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            elif event.type == KEYDOWN:
                if event.key == K_q:
                    return
        if randint(0,30) == 5:
            enemies.add(Enemy(screen, difficulty))
            SCORE = SCORE + 1
        arena.increment()
        screen.blit(arena.surface, (0, 0), (0, arena.counter, SCREENRECT.width, SCREENRECT.height))
        enemies.update()
        enemies.draw(screen)
        player.handleKeys()
        player.draw(screen)
        score.draw(SCORE)

        for player in pygame.sprite.spritecollide(player, enemies, 1):
            player.kill()
            Explosion(player, screen)
        pygame.display.update()
        clock.tick(30)
    if pygame.mixer:
        pygame.mixer.music.fadeout(1000)
    pygame.time.wait(1000)
    pygame.quit()


if __name__ == "__main__":
    driverProgram()
