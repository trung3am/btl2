import torch
import random
import numpy as np
from collections import deque
from model import Linear_QNet, QTrainer
import copy

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent2:

  def __init__(self, game, player):
    self.prev_board = None
    self.player = player
    self.game = game
    self.n_games = 0
    self.epsilon = 0 # randomness
    self.gamma = 0.9 # discount rate
    self.memory = deque(maxlen=MAX_MEMORY) # popleft()
    self.model = Linear_QNet(25, 256, 3)
    # self.pos_model = Linear_QNet(25,256,25)
    # self.pos_trainer = QTrainer(self.model,lr = LR, gamma=self.gamma)
    self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

  def map_state(self):
    state = self.game.board
    pool =  self.gmove(self.player, state)
    rev_pool = copy.deepcopy(pool)
    opponent_pool = self.gmove(self.player*-1,state)
    strong_pos = []
    offensive_move = []
    mo_move = []
    for i in pool:
      flag = False
      if i[1][0] == 2 and i[1][1] == 2:
        flag = True
        strong_pos += [i]
      if (i[1][0] == 1 or i[1][0] == 3 ) and (i[1][1] == 3 or i[1][1] == 1):
        strong_pos += [i]
        flag = True
      if self.checkGanh(state, i[1],self.player): 
        offensive_move += [i]
        flag = True
      if self.checkGanh(state, i[0],self.player*-1):
        for j in opponent_pool:
          if j[1] == i[0]:
            mo_move += [i]
            flag = True
            break
      if flag: pool[pool.index(i)] = False
    pool = set(pool)
    try:
      pool.remove(False)
    except:
      pass
    pool = list(pool)
    # 0 offense, 1 hold strong point, 2 tao mo, 3 4 remain move for reserve
    return (offensive_move, strong_pos, mo_move, pool,rev_pool)
    
  def checkMo(self, prev_board, board):
    res = (0,0)
    count = 0
    for i in range(5):
      for j in range(5):
        if prev_board[i][j] != board[i][j]:
          if board[i][j] == 0: res = (i,j)
          count +=1
    # if count > 2: return (False, res)
    _res = self.checkGanh(board,res,self.player)
    return (_res, res)
    


    
  
  def checkGanh(self, board, spot,player):
    if spot[0] == 0 and spot[1] == 0: return False
    if spot[0] == 0 and spot[1] == 4: return False
    if spot[0] == 4 and spot[1] == 0: return False
    if spot[0] == 4 and spot[1] == 4: return False
    if spot[0] == 0 or spot[0] == 4:
      if board[spot[0]][spot[1]+1] != 0 and board[spot[0]][spot[1]+1] == player*-1 and board[spot[0]][spot[1]+1] == board[spot[0]][spot[1]-1] and board[spot[0]][spot[1]-1] !=0:
        return True
      return False
    if spot[1] == 0 or spot[1] == 4:
      if board[spot[0]+1][spot[1]] != 0 and board[spot[0]+1][spot[1]] == player*-1 and board[spot[0]+1][spot[1]] == board[spot[0]-1][spot[1]] and board[spot[0]-1][spot[1]] != 0:
        return True
      return False
    if board[spot[0]+1][spot[1]] !=0 and board[spot[0]+1][spot[1]] == player*-1 and board[spot[0]+1][spot[1]] == board[spot[0]-1][spot[1]] and board[spot[0]-1][spot[1]] != 0:
      return True
    if board[spot[0]][spot[1]+1] != 0 and board[spot[0]][spot[1]+1] == player*-1 and board[spot[0]][spot[1]+1] == board[spot[0]][spot[1]-1] and board[spot[0]][spot[1]-1] != 0:
      return True
    if board[spot[0]-1][spot[1]-1] !=0 and board[spot[0]-1][spot[1]-1] == player*-1 and board[spot[0]-1][spot[1]-1] == board[spot[0]+1][spot[1]+1] and board[spot[0]+1][spot[1]+1] != 0:
      return True
    if board[spot[0]-1][spot[1]+1] !=0 and board[spot[0]-1][spot[1]+1] == player*-1 and board[spot[0]-1][spot[1]+1] == board[spot[0]+1][spot[1]-1] and board[spot[0]+1][spot[1]-1] != 0:
      return True
    return False

  def gmove(self,player,board):
    
    pool = []
    for i in range(5):
      for j in range(5):
        
        if board[i][j]==player: pool+= self.generateMove((i,j),board,player)
    # pool.sort()

    return pool

  def generateMove(self, spot,board,player):
    res = []
    i = spot[0]
    j = spot[1]
    if  self.testMove(board, (spot,(i+1,j)),player): res += [(spot,(i+1,j))]
    if  self.testMove(board, (spot,(i-1,j)),player): res += [(spot,(i-1,j))]
    if  self.testMove(board, (spot,(i,j+1)),player): res += [(spot,(i,j+1))]
    if  self.testMove(board, (spot,(i,j-1)),player): res += [(spot,(i,j-1))]
    if  self.testMove(board, (spot,(i+1,j+1)),player): res += [(spot,(i+1,j+1))]
    if  self.testMove(board, (spot,(i-1,j+1)),player): res += [(spot,(i-1,j+1))]
    if  self.testMove(board, (spot,(i-1,j-1)),player): res += [(spot,(i-1,j-1))]
    if  self.testMove(board, (spot,(i+1,j-1)),player): res += [(spot,(i+1,j-1))]
    return res

  def checkWin(self,board):
    pnum = self.countPiece(board,1)
    if pnum == 16 or pnum == 0: return True
    return False

  def countPiece(self, board, player):
    count = 0
    for i in board:
      for j in i:
        if j == player: count+=1

    return count


  def testMove(self, board, move, player):
    if move[1][0] < 0 or move[1][1] < 0:
      return False 
    if self.checkWin(board): return False
    if move[0] == move[1]:
      return False
    if board[move[0][0]][move[0][1]] != player:
      return False
    if move[0][0] > 4 or move[0][1] > 4 or move[1][0] > 4 or move[1][1] > 4:
      return False
    if abs(move[0][0] - move[1][0]) > 1 or abs(move[0][1] - move[1][1]) > 1:
      return False
    if board[move[1][0]][move[1][1]] != 0:
      return False
    if abs(move[0][0] - move[1][0]) == 1 and abs(move[0][1] - move[1][1]) == 1:
      if move[0][0] % 2 == 0 and move[0][1] % 2 == 0 and move[1][0] % 2 == 1 and move[1][1] % 2 == 1:
        return True
      if move[1][0] % 2 == 0 and move[1][1] % 2 == 0 and move[0][0] % 2 == 1 and move[0][1] % 2 == 1:
        return True
      return False
    return True


  def remember(self, state, action, reward, next_state, done):
    self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

  def train_long_memory(self):
    if len(self.memory) > BATCH_SIZE:
      mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
    else:
      mini_sample = self.memory

    states, actions, rewards, next_states, dones = zip(*mini_sample)
    self.trainer.train_step(states, actions, rewards, next_states, dones)


  def train_short_memory(self, state, action, reward, next_state, done):
    self.trainer.train_step(state, action, reward, next_state, done)

  def get_action(self, state, prev_board):
    move = None
    self.epsilon = self.n_games - 20
    # 3 behaviour offense, hold strong point, tao mo
    final_move = [0,0,0]
    map_move =  self.map_state()
    # print(map_move)
    if len(map_move[4]) == 0: return None
    if prev_board != None:
      res = self.checkMo(prev_board, self.game.board)
      if res[0] == True:
        for i in map_move[4]:
          if i[1] == res[1]:

            return ([1,0,0],i)
            
    if random.randint(0, 200) < self.epsilon:
      strat = random.randint(0, 2)
      final_move[strat] = 1
      if len(map_move[strat]) > 0: 
        move = random.choice(map_move[strat])
      else:
        for i in range(4):
          if len(map_move[i]) > 0:
            move = random.choice(map_move[i])
            break
        
    else:
      state0 = torch.tensor(np.array(state).flatten(), dtype=torch.float)
      prediction = self.model(state0)
      # strat = behavior 0-2 choose max number index
      strat = torch.argmax(prediction).item()
      print(strat)
      final_move[strat] = 1
      if len(map_move[strat]) > 0: 
        move = random.choice(map_move[strat])
      else:
        for i in range(4):
          if len(map_move[i]) > 0:
            move = random.choice(map_move[i])
            break
    # print("RL move: " + str(move))
    return (final_move,move)

