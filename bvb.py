import pygame
from game import Game
from bot import Bot
import time
import copy
import os
import random
import numpy as np
from agent import Agent


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
display = pygame.display
win = display.set_mode((WIDTH, HEIGHT))
display.set_caption('Checkers')
font = pygame.font.SysFont(None, 50)

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
  record = 0
  delay = .04
  s=0
  run = True
  clock = pygame.time.Clock()
  game = Game(win)
  game.draw()
  init = copy.deepcopy(game.board)
  bot = Bot()
  t = time.time()
  count = 0
  prev_board = copy.deepcopy(init)
  flag = False
  try:
    os.remove('output.txt')
  except:
    print("cannot find output.txt")

  agent = Agent(game,-1)
  botside = 1
  agentfirst = False
  # agent = Agent(game,1)
  # botside = -1
  # agentfirst = True
  
  prev_rand = None
  while True:
    if count == 30:
      pygame.quit()
      break
    clock.tick(FPS)
    w = agent.countPiece(game.board, agent.player)
    if  w == 0 or w == 16 or flag == True:
      print("win" , flag)
      print(w == 0 or w == 16 )
      print(game.board)
      flag = False
      if w <= 8: 
        p = agent.player
        
      else: 
        p = agent.player*-1
      if p == 1:
        color = " BLUE "
        show_color = BLUE
      else:
        color = " RED "
        show_color = RED
      # train long memory when game is end
      agent.train_long_memory()
      # save model when RL win.
      if p == -1:
        agent.model.save()
        

      count+= 1
      f = open('output.txt', 'a')
      f.write("time: "+ str(time.time()-t))
      f.write("win: " + str(p) +color + "RL Piece(s)" +str(w) +" step: " + str(s) + '\n')
      f.close()
      t = time.time()
      game.board = copy.deepcopy(init)
      game.turn = True
      prev_board = None
      prev_rand = None
      s=0
      img = font.render(  str(color) + ' Win !!!', True, show_color )
      win.blit(img, (300, 20))
      display.update()
      
      time.sleep(.7)
    # random move bot
    time.sleep(delay)
    if not agentfirst:
      prev_rand = copy.deepcopy(game.board)
      board = copy.deepcopy(game.board)
      rand = bot.move(prev_board,board,botside)
      if rand != None: randm =  game.makeMove(rand,botside)
      if rand == None or not randm: 
        print(game.turn)
        flag = True
        continue
      print("Random move: " + str(rand))
      
      s+=1
    
    # nPrint(game)
    game.draw()
    img = font.render(  str(s) + ' step', True, WHITE )
    win.blit(img, (100, 20))
    pieces = font.render(  str(game.countPiece(game.board,agent.player)) + ' pieces', True, BLUE )
    win.blit(pieces, (50, 630))
    display.update()
    time.sleep(delay)
    # RL move with agent
    move = agent.get_action(game.board, prev_rand)
    print("RL move: " + str(move))
    if move != None and move[1] != None: 
      prev_board = copy.deepcopy(game.board)
      movem =  game.makeMove(move[1],agent.player)
    if move == None or not movem: 
      flag = True
      continue
    

    reward = agent.countPiece(prev_board,agent.player) -  agent.countPiece(prev_rand,agent.player)  
    agent.train_short_memory(np.array(prev_rand).flatten(), move[0],reward , np.array(prev_rand).flatten(), flag)

    agent.remember(np.array(prev_rand).flatten(), move[0],reward , np.array(prev_rand).flatten(), flag)
    
    s+=1
    
    # nPrint(game)
    game.draw()
    img = font.render(  str(s) + ' step', True, WHITE )
    win.blit(img, (100, 20))
    pieces = font.render(  str(game.countPiece(game.board,agent.player)) + ' pieces', True, BLUE )
    win.blit(pieces, (50, 630))
    agentfirst = False
    display.update()

      

main()