import pygame
from game import Game
from bot import Bot
import time
import copy
import os
import random
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

def randomMove(game,board,player):

  pool = []
  for i in range(5):
    for j in range(5):	
      if board[i][j]==player: pool+= [(i,j)]
  if pool == []: return
  while True:


    pick  = random.choice(pool)
    move = (random.randint(max(0,pick[0]-1),min(4,pick[0]+1)),random.randint(max(0,pick[1]-1),min(4,pick[1]+1)))
    if game.makeMove((pick,move),player): break

def main():
  s=0
  run = True
  clock = pygame.time.Clock()
  game = Game(win)
  game.draw()
  init = copy.deepcopy(game.board)
  bot = Bot()
  select = False
  sRow = 0
  sCol = 0
  t = time.time()
  count = 0
  prev_board = copy.deepcopy(init)
  try:
    os.remove('output.txt')
  except:
    print("cannot find output.txt")
  while True:
    if count == 20:
      pygame.quit()
      break
    clock.tick(FPS)
    w = bot.countPiece(game.board,1)
    if  w == 0 or w == 16 :
      print("win" , str(w))
      count+= 1
      f = open('output.txt', 'a')
      f.write("time: "+ str(time.time()-t))
      f.write("win: " + str(w) + "step: " + str(s) + '\n')
      f.close()
      t = time.time()
      game.board = copy.deepcopy(init)
      s=0
    game.makeMove(bot.randomMove(prev_board,game.board,1),1)
    prev_board = copy.deepcopy(game.board)
    s+=1
    nPrint(game)
    game.draw()
    game.makeMove(bot.move(prev_board,game.board,-1,0,0),-1)
    prev_board = copy.deepcopy(game.board)
    s+=1
    nPrint(game)
    game.draw()
  

      

main()