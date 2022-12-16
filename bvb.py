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

def nPrint(game):
  res=""
  print(game.board)
  for i in game.board:
    for j in i:
      res += str(j) + ' '
  print(res)

def main():
  run = True
  clock = pygame.time.Clock()
  game = Game(win)
  game.draw()
  bot = Bot(botside,game)
  select = False
  sRow = 0
  sCol = 0

  while True:
    clock.tick(FPS)
    print("a")
    if  game.checkWin():
      print("win" , game.board)
      wl = "Win" if game.board[game.lastMoveIdx[0]][game.lastMoveIdx[1]] ==1 else "Lose"
      img = font.render('You ' + wl + ' !!!', True, RED)
    bot.randomMove()
    nPrint(game)
    game.draw()
    bot.move(game.board,game.board,1,0,0)
    nPrint(game)
    game.draw()
  

      

        
          


  pygame.quit()

main()