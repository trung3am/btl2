import pygame
from game import Game
from bot import Bot
import time
import copy
import os
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
  init = copy.deepcopy(game.board)
  bot = Bot(botside,game)
  select = False
  sRow = 0
  sCol = 0
  t = time.time()
  count = 0
  os.remove('output.txt')
  while True:
    if count == 10:
      pygame.quit()
      break
    clock.tick(FPS)
    print("a")
    w = bot.countPiece(game.board,1)
    if  w == 0 or w == 16 :
      print("win" , str(w))
      count+= 1
      f = open('output.txt', 'a')
      f.write("time: "+ str(time.time()-t))
      f.write("win: " + str(w))
      f.close()
      t = time.time()
      game.board = copy.deepcopy(init)
    bot.move(game.board,game.board,-1,0,0,3)
    nPrint(game)
    game.draw()
    bot.move(game.board,game.board,1,0,0,4)
    nPrint(game)
    game.draw()
  

      

main()