import os, pygame
from pygame.locals import *
from menu import *

def main():
	pygame.init()
	screen = pygame.display.set_mode((640, 480), 0, 32)
	menu = Menu(screen)
	menu.loop()
