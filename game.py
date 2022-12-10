import random
from colorama import init
from termcolor import colored
import time
import copy
init()
import os
import sys
import pygame

WIDTH, HEIGHT = 700, 700
ROWS, COLS = 5, 5
SQUARE_SIZE = WIDTH//COLS

# rgb
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128,128,128)

def clear():
    # type: () -> None
    if sys.platform.startswith('win'):
        os.system('cls')  # For Windows System
    else:
        os.system('clear')  # For Linux System

class Game:


  def __init__(self, win) -> None:
    self.win = win
    self.lastMoveIdx = (0,0)
    self.board = [[1, 1, 1, 1, 1],
                  [1, 0, 0, 0, 1],
                  [1, 0, 0, 0, -1],
                  [-1, 0, 0, 0, -1],
                  [-1, -1, -1, -1, -1]]

  
  def draw(self):
    stepW = WIDTH/6
    stepH = HEIGHT/6
    self.win.fill(BLACK)
    for i in range(5):
      pygame.draw.line(self.win,WHITE,(stepW*(i+1),stepW),(stepW*(i+1),HEIGHT-stepW))
      pygame.draw.line(self.win,WHITE,(stepH,stepH*(i+1)),(WIDTH-stepH,stepH*(i+1)))

    pygame.draw.line(self.win,WHITE,(stepH,stepH),(WIDTH-stepH,HEIGHT-stepH))
    pygame.draw.line(self.win,WHITE,(WIDTH- stepH,stepH),(stepH,HEIGHT-stepH))
    pygame.draw.line(self.win,WHITE,(WIDTH- stepH*3,stepH),(stepH,HEIGHT-stepH*3))
    pygame.draw.line(self.win,WHITE,(WIDTH- stepH*3,stepH),(HEIGHT-stepH,HEIGHT-stepH*3))
    pygame.draw.line(self.win,WHITE,(stepH,HEIGHT-stepH*3),(HEIGHT-stepH*3, HEIGHT-stepH))
    pygame.draw.line(self.win,WHITE,(HEIGHT-stepH,HEIGHT-stepH*3),(HEIGHT-stepH*3,HEIGHT-stepH))

    for i in range(5):
      for j in range(5):
        if self.board[i][j] == 0: continue
        pygame.draw.circle(self.win,RED if self.board[i][j]>0 else BLUE,(stepH*(1+j),stepH*(1+i)),20,200)
    pygame.display.flip()
  
  def select(self,row,col):
    stepH = HEIGHT/6
    pygame.draw.circle(self.win,WHITE,(stepH*(1+col),stepH*(1+row)),20,200)
    pygame.display.flip()
    
  def deSelect(self,row,col):
    stepH = HEIGHT/6
    pygame.draw.circle(self.win,RED if self.board[row][col]>0 else BLUE,(stepH*(1+col),stepH*(1+row)),20,200)
    pygame.display.flip()
    
  def makeMove(self, move, player):
    if self.checkWin(): return False
    if move[1][0] < 0 or move[1][1] < 0: return False
    if move[0] == move[1]:
      print("cannot make move without moving")
      return False
    if self.board[move[0][0]][move[0][1]] != player:
      print("cannot move others unit/spot doesn't have any unit")
      return False
    if move[0][0] > 4 or move[0][1] > 4 or move[1][0] > 4 or move[1][1] > 4:
      print("out of board move cannot be made")
      return False
    if abs(move[0][0] - move[1][0]) > 1 or abs(move[0][1] - move[1][1]) > 1:
      print("invalid move(too much reach)")
      return False
    if self.board[move[1][0]][move[1][1]] != 0:
      print("move blocked by other unit")
      return False
    if abs(move[0][0] - move[1][0]) == 1 and abs(move[0][1] - move[1][1]) == 1:
      if move[0][0] % 2 == 0 and move[0][1] % 2 == 0 and move[1][0] % 2 == 1 and move[1][1] % 2 == 1:
        self.board[move[0][0]][move[0][1]] = 0
        self.board[move[1][0]][move[1][1]] = player
        print("player: " + str(player) + " moved")
        self.ganh(move[1])
        self.chet(move[1])
        self.lastMoveIdx = move[1]
        return True
      if move[1][0] % 2 == 0 and move[1][1] % 2 == 0 and move[0][0] % 2 == 1 and move[0][1] % 2 == 1:
        self.board[move[0][0]][move[0][1]] = 0
        self.board[move[1][0]][move[1][1]] = player
        print("player: " + str(player) + " moved")
        self.ganh(move[1])
        self.chet(move[1])
        self.lastMoveIdx = move[1]
        return True
      print("invalid move")
      return False
    self.board[move[0][0]][move[0][1]] = 0
    self.board[move[1][0]][move[1][1]] = player
    self.ganh(move[1])
    self.chet(move[1])
    self.lastMoveIdx = move[1]
    print("player: " + str(player) + " moved")
    return True

  def ganh(self, spot):
    if spot[0] == 0 and spot[1] == 0: return
    if spot[0] == 0 and spot[1] == 4: return
    if spot[0] == 4 and spot[1] == 0: return
    if spot[0] == 4 and spot[1] == 4: return
    if spot[0] == 0 or spot[0] == 4:
      if self.board[spot[0]][spot[1]+1] != 0 and self.board[spot[0]][spot[1]+1] == self.board[spot[0]][spot[1]-1] and self.board[spot[0]][spot[1]-1] !=0:
        self.board[spot[0]][spot[1]-1] = self.board[spot[0]][spot[1]]
        self.board[spot[0]][spot[1]+1] = self.board[spot[0]][spot[1]]
      return
    if spot[1] == 0 or spot[1] == 4:
      if self.board[spot[0]+1][spot[1]] != 0 and self.board[spot[0]+1][spot[1]] == self.board[spot[0]-1][spot[1]] and self.board[spot[0]-1][spot[1]] != 0:
        self.board[spot[0]-1][spot[1]] = self.board[spot[0]][spot[1]]
        self.board[spot[0]+1][spot[1]] = self.board[spot[0]][spot[1]]
      return
    
    if self.board[spot[0]+1][spot[1]] !=0 and self.board[spot[0]+1][spot[1]] == self.board[spot[0]-1][spot[1]] and self.board[spot[0]-1][spot[1]] != 0:
      self.board[spot[0]-1][spot[1]] = self.board[spot[0]][spot[1]]
      self.board[spot[0]+1][spot[1]] = self.board[spot[0]][spot[1]]
    if self.board[spot[0]][spot[1]+1] != 0 and self.board[spot[0]][spot[1]+1] == self.board[spot[0]][spot[1]-1] and self.board[spot[0]][spot[1]-1] != 0:
      self.board[spot[0]][spot[1]-1] = self.board[spot[0]][spot[1]]
      self.board[spot[0]][spot[1]+1] = self.board[spot[0]][spot[1]]
    if self.board[spot[0]-1][spot[1]-1] !=0 and self.board[spot[0]-1][spot[1]-1] == self.board[spot[0]+1][spot[1]+1] and self.board[spot[0]+1][spot[1]+1] != 0:
      self.board[spot[0]-1][spot[1]-1] = self.board[spot[0]][spot[1]]
      self.board[spot[0]+1][spot[1]+1] = self.board[spot[0]][spot[1]]
    if self.board[spot[0]-1][spot[1]+1] !=0 and self.board[spot[0]-1][spot[1]+1] == self.board[spot[0]+1][spot[1]-1] and self.board[spot[0]+1][spot[1]-1] != 0:
      self.board[spot[0]-1][spot[1]+1] = self.board[spot[0]][spot[1]]
      self.board[spot[0]+1][spot[1]-1] = self.board[spot[0]][spot[1]]
    return
  @staticmethod
  def checkChet(cBoard, spot, player):
    if cBoard[spot[0]][spot[1]] == 0 or cBoard[spot[0]][spot[1]] == player: return True
    if cBoard[spot[0]][spot[1]]*player < 0 or cBoard[spot[0]][spot[1]] % 4 == 0: return False
    cBoard[spot[0]][spot[1]]*=2
    if spot[0] % 2 == 0 and spot[1] % 2 == 0 or spot[0] % 2 == 1 and spot[1] % 2 == 1:
      if spot[0]-1 >= 0 and spot[1]-1 >= 0:
        if Game.checkChet(cBoard,(spot[0]-1,spot[1]-1),player): return Game.retdiv(cBoard,spot)
      if spot[0]-1 >= 0 and spot[1]+1 <= 4:
        if Game.checkChet(cBoard,(spot[0]-1,spot[1]+1),player): return Game.retdiv(cBoard,spot)
      if spot[0]+1 <= 4 and spot[1]-1 >= 0:
        if Game.checkChet(cBoard,(spot[0]+1,spot[1]-1),player): return Game.retdiv(cBoard,spot)
      if spot[0]+1 <= 4 and spot[1]+1 <= 4:
        if Game.checkChet(cBoard,(spot[0]+1,spot[1]+1),player): return Game.retdiv(cBoard,spot)
    if spot[0]-1 >= 0:
      if Game.checkChet(cBoard, (spot[0]-1,spot[1]),player): return Game.retdiv(cBoard,spot)
    if spot[0]+1 <= 4:
      if Game.checkChet(cBoard, (spot[0]+1,spot[1]),player): return Game.retdiv(cBoard,spot)
    if spot[1]-1 >= 0:
      if Game.checkChet(cBoard, (spot[0],spot[1]-1),player): return Game.retdiv(cBoard,spot)
    if spot[1]+1 <= 4:
      if Game.checkChet(cBoard, (spot[0],spot[1]+1),player): return Game.retdiv(cBoard,spot)
    return False
  
  @staticmethod
  def retdiv(cBoard,spot):
    cBoard[spot[0]][spot[1]]/=2
    return True
  @staticmethod
  def checkStuck(cBoard, spot, player):
    if cBoard[spot[0]][spot[1]]*player <= 0:
      return
    if (spot[0] % 2 == 0 and spot[1] % 2 == 0 ) or (spot[0] % 2 == 1 and spot[1] % 2 == 1):
      if spot[0]-1 >= 0 and spot[1]-1 >= 0:
        if cBoard[spot[0]-1][spot[1]-1] == 0: 
          return
      if spot[0]-1 >= 0 and spot[1]+1 <= 4:
        if cBoard[spot[0]-1][spot[1]+1] == 0: 
          return
      if spot[0]+1 <= 4 and spot[1]-1 >= 0:
        if cBoard[spot[0]+1][spot[1]-1] == 0: 
          return
      if spot[0]+1 <= 4 and spot[1]+1 <= 4:
        if cBoard[spot[0]+1][spot[1]+1] == 0: 
          return

    if spot[0]-1 >= 0:
      if cBoard[spot[0]-1][spot[1]] == 0:
        return
    if spot[0]+1  <= 4:
      if cBoard[spot[0]+1][spot[1]] == 0:
        return
    if spot[1]-1 >= 0:
      if cBoard[spot[0]][spot[1]-1] == 0:
        return
    if spot[1]+1 <= 4:
      if cBoard[spot[0]][spot[1]+1] == 0:
        return
    cBoard[spot[0]][spot[1]]*=2
    return

  def chet(self, spot):
    player = self.board[spot[0]][spot[1]]*-1
    cBoard = copy.deepcopy(self.board)
    for i in range(len(self.board)):
      for j in range(len(self.board[i])):
        Game.checkStuck(cBoard,(i,j),player)
    for i in range(len(self.board)):
      for j in range(len(self.board[i])):
        if cBoard[i][j]*player <=0: continue
        tBoard = copy.deepcopy(cBoard)
        if not Game.checkChet(cBoard,(i,j),player):
          tBoard[i][j] = player*-1
          self.board[i][j] = player*-1
          cBoard = tBoard
        
    return

  def countPiece(self, board, player):
    count = 0
    for i in board:
      for j in i:
        if j == player: count+=1

    return count

  def checkWin(self):
    pnum = self.countPiece(self.board,1)
    if pnum == 16 or pnum == 0: return True
    return False
  
  def checkWinSide(self, side):
    pnum = self.countPiece(self.board,side)
    if pnum == 16: return 1
    if pnum == 0: return -1
    return 0


        
# 00 02 04 11 13 20 22 24 31 33 40 42 44

  

