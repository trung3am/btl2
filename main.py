import pygame
from game import Game
import time
from pvb import playVsBot
from pvp import pvp as PlayOnline
FPS = 60
# rgb
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128,128,128)
WIDTH, HEIGHT = 700, 700
ROWS, COLS = 5, 5
SQUARE_SIZE = WIDTH//COLS
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')
font = pygame.font.SysFont(None, 50)


# playVsBot("RL")

def main():
	run = True
	mode = ""
	ez = pygame.Rect(100, 100, 450, 50)
	medium = pygame.Rect(100, 250, 450, 50)
	pvp = pygame.Rect(100, 400, 450, 50)
	exit = pygame.Rect(100, 550, 450, 50)
	color = pygame.Color('lightskyblue3')
	
	txtEZ = font.render("Play vs Bot Easy(Minimax)",True, color)
	txtMED = font.render("Play vs Bot Medium(RL)",True, color)
	txtPVP = font.render("Play Online",True, color)
	txtExit = font.render("Exit Game",True, color)
	
	while run:
		win.fill((30,30,30))
		if mode == "MINIMAX" or mode == "RL":
			playVsBot(mode)
			mode = ""
		if mode == "PVP":
			PlayOnline()
			mode = ""
		win.blit(txtEZ,(ez.x+5,ez.y+5))
		pygame.draw.rect(win, color, ez, 2)
		win.blit(txtMED,(medium.x+23,medium.y+5))
		pygame.draw.rect(win, color, medium, 2)
		win.blit(txtPVP,(pvp.x+130,pvp.y+5))
		pygame.draw.rect(win, color, pvp, 2)
		win.blit(txtExit,(exit.x+137,exit.y+5))
		pygame.draw.rect(win, color, exit, 2)
		
		pygame.display.flip()
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False
				if event.type == pygame.MOUSEBUTTONDOWN:
					x,y = pygame.mouse.get_pos()
					if x >= 100 and x <= 550:
						if y >=100 and y <= 150:
							mode = "MINIMAX"
						if y >=250 and y <= 300:
							mode = "RL"
						if y >=400 and y <= 450:
							mode = "PVP"
						if y >=550 and y <= 600:
							mode = "Exit"
							run = False

main()

