import pygame
import os
import sys
from pygame.locals import *
from random import randint

class Menu(object):

    def __init__(self, screen):
        pygame.init()
        pygame.display.set_caption("Meteor Dodger")
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.screen = screen
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.font = pygame.font.Font("pygame/oneway.ttf", 50)
        self.option = 1


    def loop(self):

        while True: 

            import myPygame

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == K_DOWN:
                        if self.option < 3:
                            self.option += 1
                        else:
                            pass
                    if event.key == K_UP:
                        if self.option > 1:
                            self.option -= 1
                        else:
                            pass
                    if event.key == K_RETURN:
                        if self.option == 1:
                            difficulty = randint(2,3)
                            myPygame.run(difficulty)
                        if self.option == 2:
                            difficulty = randint(4,5)
                            myPygame.run(difficulty)
                        if self.option == 3:
                            pygame.quit()
                            sys.exit()
                                
            ren = self.font.render("Meteor Dodger", 1, (255, 0, 0))
            self.screen.blit(ren, (self.width*0.5-ren.get_width()/2 , 50))
            ren = self.font.render("Start/Beginner", 1, (255, 0, 0))
            self.screen.blit(ren, (self.width*0.5-ren.get_width()/2, 170))
            ren = self.font.render("Start/Pro", 1, (255, 0, 0))
            self.screen.blit(ren, (self.width*0.5-ren.get_width()/2, 300))
            ren = self.font.render("Exit", 1, (255, 0, 0))
            self.screen.blit(ren, (self.width*0.5-ren.get_width()/2, 410))
            if self.option == 1:
                ren = self.font.render("Start/Beginner", 1, (0, 230, 0))
                self.screen.blit(ren, (self.width*0.5-ren.get_width()/2, 170))
            if self.option == 2:
                ren = self.font.render("Start/Pro", 1, (0, 230, 0))
                self.screen.blit(ren, (self.width*0.5-ren.get_width()/2, 300))
            if self.option == 3:
                ren = self.font.render("Exit", 1, (0, 230, 0))
                self.screen.blit(ren, (self.width*0.5-ren.get_width()/2, 410))
            
            pygame.display.flip()
            self.screen.fill((0,0,0))

