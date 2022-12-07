import pygame
from game import Game
from bot import Bot
import time
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
img = font.render('You Win !!!', True, RED)
botside = -1
playerside = 1

def get_row_col_from_mouse(pos):
	x, y = pos
	row = y // SQUARE_SIZE
	col = x // SQUARE_SIZE
	return row, col

def main():
	run = True
	clock = pygame.time.Clock()
	game = Game(win)
	game.draw()
	bot = Bot(botside,game)
	select = False
	sRow = 0
	sCol = 0

	while run:
		clock.tick(FPS)
		if  game.checkWin():
			wl = "Win" if game.board[game.lastMoveIdx[0]][game.lastMoveIdx[1]] ==1 else "Lose"
			img = font.render('You ' + wl + ' !!!', True, RED)
			win.blit(img, (300, 20))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			
			if event.type == pygame.MOUSEBUTTONDOWN:
				pos = pygame.mouse.get_pos()
				row, col = get_row_col_from_mouse(pos)

				if select:
					if game.board[row][col] == 0:
						if game.makeMove(((sRow,sCol),(row,col)),playerside):
							select = False
							game.draw()
							bot.move(game.board,game.board,botside,0,0)
							time.sleep(1.5)
							game.draw()
							if game.checkWin():
								wl = "Win" if game.board[game.lastMoveIdx[0]][game.lastMoveIdx[1]] ==1 else "Lose"
								img = font.render('You ' + wl + ' !!!', True, RED)
								win.blit(img, (300, 20))
							game.draw()
							continue
					game.deSelect(sRow,sCol)
					select = False
				else: 
					if game.board[row][col] == 0: continue
					game.select(row,col)
					if game.checkWin():
						wl = "Win" if game.board[game.lastMoveIdx[0]][game.lastMoveIdx[1]] ==1 else "Lose"
						img = font.render('You ' + wl + ' !!!', True, RED)
						win.blit(img, (300, 20))
					sRow = row
					sCol = col
					select = True
	
					


	pygame.quit()

main()