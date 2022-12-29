
import random
import time
import copy

# move function o duoi cung nha thay :D, em so code logic bi sai co gi thay cham chuoc em voi :D em he vhvl :D
# git bon em : https://github.com/trung3am/btl2
class Bot:
	history = []
	defensive = 0
	cp = 0
	stuck = 0
	first = False
	def __init__(self) -> None:
		pass
	def randomMove(self,prev_board, board,player):

		pool = []
		root = Node(board, None, player,self,0)
		pool = self.gmove(root,True)
		if pool == []: return None
		res = self.checkMo(prev_board, board)
		if res[0]:
			for i in pool:
				if i.move == res[1]: return i.move
		pick  = random.choice(pool)
		return(pick.move)

	def move(self, prev_board, board, player, remain_time_x, remain_time_o):
		Node.time = time.time()
		root = Node(board, None, player,self,0)
		countPre =  self.countPiece(board, player)
		if prev_board == None: Bot.first = True
		if Bot.first: m = self.minimax(prev_board, root, True,player,3,0,20,1)
		else: m = self.minimax(prev_board, root, True,player,3,0,20,2)
		
		if countPre == Bot.cp: Bot.stuck+= 1
		else:
			Bot.cp = countPre
			Bot.stuck == 0

		if countPre - m[0] == 0 or Bot.stuck >= 2:
			Bot.defensive += 1
		else:
			Bot.defensive = 0
		if Bot.defensive >= 4: Bot.stuck = 0
		Bot.history += [m[1]]
		return m[1]

	def minimax(self,prev_board,node, maxplayer,player,maxDepth,alpha,beta,defensive = 0):

# 		if node.depth == 0: print("check")
		if maxDepth <= node.depth or time.time() - Node.time > 5 or self.countPiece(node.board, player) == 0: return(self.countPiece(node.board, player),node.move)

		if maxplayer:
			bestVal = 0
			pool = self.gmove(node,player)
			if len(pool) == 0:
				if node.depth != 0: return (-99,node.move)
				Bot.history = []
				pool = self.gmove(node,player)
			res = pool[0].move
# 			if node.depth == 0: print(prev_board)
			if prev_board!= None:
				
				mo = self.checkMo(prev_board, node.board)
				# if node.depth == 0: print(mo)
				if mo[0]:
					for i in pool:
				# 		if node.depth == 0:print(i.move)
						if i.move[1] == mo[1]: return (self.countPiece(node.board, player),i.move)
			if node.depth == 0 and Bot.defensive >= defensive:
				_res  =res
				c = 0
				for i in pool:
					temp = self.countPiece(i.board, player) - self.countPiece(node.board,player)
					if temp > c:
						c = temp
						res = i.move
					if self.cmove(i.board, player*-1) < self.cmove(node.board, player*-1):
						_res = i.move
				
				if c > 0: return (c,res)
				return (c,_res)

			for i in pool:
				v = self.minimax(node.board,i,not maxplayer, player,maxDepth,alpha,beta)
				bestVal = max(bestVal,v[0])
				if node.depth == 0 and bestVal == v[0]:
					res = i.move
				alpha = max(alpha,bestVal)
				if self.countPiece(i.board, player) == 16: return (16,res)
				if beta <= alpha: break
		else:
			bestVal = 16
			pool = self.gmove(node,player)
			if len(pool) == 0: return (self.countPiece(node.board, player),node.move)
			res = pool[0].move
			if prev_board!= None:
				mo = self.checkMo(prev_board, node.board)
				if mo[0]:
					for i in pool:
						if i.move == mo[1]: return (self.countPiece(node.board, player),i.move)
			for i in pool:
				v = self.minimax(node.board,i,not maxplayer, player,maxDepth,alpha,beta)
				bestVal = min(bestVal,v[0])
				if node.depth == 0 and bestVal == v[0]:
					res = i.move[1]
				beta = min(beta,bestVal)
				if beta <= alpha: break

		return (bestVal,res)

	def cmove(self, board,player):
		pool = 0
		for i in range(5):
			for j in range(5):
				
				if board[i][j]==player: pool+= self.countMove((i,j),board,player)
		# pool.sort()

		return pool

	def countMove(self, spot,board,player):
		
		res = 0
		i = spot[0]
		j = spot[1]
		if  self.testMove(board, (spot,(i+1,j)),player): res += 1
		if  self.testMove(board, (spot,(i-1,j)),player): res += 1
		if  self.testMove(board, (spot,(i,j+1)),player): res += 1
		if  self.testMove(board, (spot,(i,j-1)),player): res += 1
		if  self.testMove(board, (spot,(i+1,j+1)),player): res += 1
		if  self.testMove(board, (spot,(i-1,j+1)),player): res += 1
		if  self.testMove(board, (spot,(i-1,j-1)),player): res += 1
		if  self.testMove(board, (spot,(i+1,j-1)),player): res += 1
		return res

	def countPiece(self, board, player):
		count = 0
		for i in board:
			for j in i:
				if j == player: count+=1

		return count

	
	def gmove(self, node,player):
		
		pool = []
		for i in range(5):
			for j in range(5):
				
				if node.board[i][j]==node.player: pool+= self.generateMove((i,j),node.board,node.player,node.depth+1,player)
		# pool.sort()

		return pool



	def generateMove(self, spot,board,player,depth,player1):
		
		res = []
		i = spot[0]
		j = spot[1]
		if self.checkRepeat((spot,(i+1,j)),player1==player) and self.testMove(board, (spot,(i+1,j)),player): res += [Node(board,(spot,(i+1,j)),player*-1,self,depth)]
		if self.checkRepeat((spot,(i-1,j)),player1==player) and self.testMove(board, (spot,(i-1,j)),player): res += [Node(board,(spot,(i-1,j)),player*-1,self,depth)]
		if self.checkRepeat((spot,(i,j+1)),player1==player) and self.testMove(board, (spot,(i,j+1)),player): res += [Node(board,(spot,(i,j+1)),player*-1,self,depth)]
		if self.checkRepeat((spot,(i,j-1)),player1==player) and self.testMove(board, (spot,(i,j-1)),player): res += [Node(board,(spot,(i,j-1)),player*-1,self,depth)]
		if self.checkRepeat((spot,(i+1,j+1)),player1==player) and self.testMove(board, (spot,(i+1,j+1)),player): res += [Node(board,(spot,(i+1,j+1)),player*-1,self,depth)]
		if self.checkRepeat((spot,(i-1,j+1)),player1==player) and self.testMove(board, (spot,(i-1,j+1)),player): res += [Node(board,(spot,(i-1,j+1)),player*-1,self,depth)]
		if self.checkRepeat((spot,(i-1,j-1)),player1==player) and self.testMove(board, (spot,(i-1,j-1)),player): res += [Node(board,(spot,(i-1,j-1)),player*-1,self,depth)]
		if self.checkRepeat((spot,(i+1,j-1)),player1==player) and self.testMove(board, (spot,(i+1,j-1)),player): res += [Node(board,(spot,(i+1,j-1)),player*-1,self,depth)]
		return res
	
	def checkRepeat(self,move,flag): 
		# if not flag : return True
		# if len(set(Bot.history[-8:])) == len(set(Bot.history[-8:]+[move])): return False
		return True

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

	def makeMove(self, board, move, player):
		if self.checkWin(board): return False
		if move[1][0] < 0 or move[1][1] < 0: return False
		if move[0] == move[1]:
			print("cannot make move without moving")
			return False
		if board[move[0][0]][move[0][1]] != player:
			print("cannot move others unit/spot doesn't have any unit")
			return False
		if move[0][0] > 4 or move[0][1] > 4 or move[1][0] > 4 or move[1][1] > 4:
			print("out of board move cannot be made")
			return False
		if abs(move[0][0] - move[1][0]) > 1 or abs(move[0][1] - move[1][1]) > 1:
			print("invalid move(too much reach)")
			return False
		if board[move[1][0]][move[1][1]] != 0:
			print("move blocked by other unit")
			return False
		if abs(move[0][0] - move[1][0]) == 1 and abs(move[0][1] - move[1][1]) == 1:
			if move[0][0] % 2 == 0 and move[0][1] % 2 == 0 and move[1][0] % 2 == 1 and move[1][1] % 2 == 1:
				board[move[0][0]][move[0][1]] = 0
				board[move[1][0]][move[1][1]] = player
				# print("player: " + str(player) + " moved")
				self.ganh(board,move[1])
				# self.chet(board,move[1])
				return True
			if move[1][0] % 2 == 0 and move[1][1] % 2 == 0 and move[0][0] % 2 == 1 and move[0][1] % 2 == 1:
				board[move[0][0]][move[0][1]] = 0
				board[move[1][0]][move[1][1]] = player
				# print("player: " + str(player) + " moved")
				self.ganh(board,move[1])
				# self.chet(board,move[1])
				return True
			print("invalid move")
			return False
		board[move[0][0]][move[0][1]] = 0
		board[move[1][0]][move[1][1]] = player
		self.ganh(board,move[1])
		# self.chet(board,move[1])
		# print("player: " + str(player) + " moved")
		return True

	def ganh(self, board, spot):
		if spot[0] == 0 and spot[1] == 0: return 
		if spot[0] == 0 and spot[1] == 4: return 
		if spot[0] == 4 and spot[1] == 0: return 
		if spot[0] == 4 and spot[1] == 4: return 
		if spot[0] == 0 or spot[0] == 4:
			if board[spot[0]][spot[1]+1] != 0 and board[spot[0]][spot[1]+1] == board[spot[0]][spot[1]-1] and board[spot[0]][spot[1]-1] !=0:
				board[spot[0]][spot[1]-1] = board[spot[0]][spot[1]]
				board[spot[0]][spot[1]+1] = board[spot[0]][spot[1]]
			return 
		if spot[1] == 0 or spot[1] == 4:
			if board[spot[0]+1][spot[1]] != 0 and board[spot[0]+1][spot[1]] == board[spot[0]-1][spot[1]] and board[spot[0]-1][spot[1]] != 0:
				board[spot[0]-1][spot[1]] = board[spot[0]][spot[1]]
				board[spot[0]+1][spot[1]] = board[spot[0]][spot[1]]
			return 
		
		if board[spot[0]+1][spot[1]] !=0 and board[spot[0]+1][spot[1]] == board[spot[0]-1][spot[1]] and board[spot[0]-1][spot[1]] != 0:
			board[spot[0]-1][spot[1]] = board[spot[0]][spot[1]]
			board[spot[0]+1][spot[1]] = board[spot[0]][spot[1]]
			return 
		if board[spot[0]][spot[1]+1] != 0 and board[spot[0]][spot[1]+1] == board[spot[0]][spot[1]-1] and board[spot[0]][spot[1]-1] != 0:
			board[spot[0]][spot[1]-1] = board[spot[0]][spot[1]]
			board[spot[0]][spot[1]+1] = board[spot[0]][spot[1]]
			return 
		if board[spot[0]-1][spot[1]-1] !=0 and board[spot[0]-1][spot[1]-1] == board[spot[0]+1][spot[1]+1] and board[spot[0]+1][spot[1]+1] != 0:
			board[spot[0]-1][spot[1]-1] = board[spot[0]][spot[1]]
			board[spot[0]+1][spot[1]+1] = board[spot[0]][spot[1]]
			return 
		if board[spot[0]-1][spot[1]+1] !=0 and board[spot[0]-1][spot[1]+1] == board[spot[0]+1][spot[1]-1] and board[spot[0]+1][spot[1]-1] != 0:
			board[spot[0]-1][spot[1]+1] = board[spot[0]][spot[1]]
			board[spot[0]+1][spot[1]-1] = board[spot[0]][spot[1]]
			return 
		return 

	def checkGanh(self, board, spot):
		if spot[0] == 0 and spot[1] == 0: return False
		if spot[0] == 0 and spot[1] == 4: return False
		if spot[0] == 4 and spot[1] == 0: return False
		if spot[0] == 4 and spot[1] == 4: return False
		if spot[0] == 0 or spot[0] == 4:
			if board[spot[0]][spot[1]+1] != 0 and board[spot[0]][spot[1]+1] == board[spot[0]][spot[1]-1] and board[spot[0]][spot[1]-1] !=0:
				return True
			return False
		if spot[1] == 0 or spot[1] == 4:
			if board[spot[0]+1][spot[1]] != 0 and board[spot[0]+1][spot[1]] == board[spot[0]-1][spot[1]] and board[spot[0]-1][spot[1]] != 0:
				return True
			return False
		if board[spot[0]+1][spot[1]] !=0 and board[spot[0]+1][spot[1]] == board[spot[0]-1][spot[1]] and board[spot[0]-1][spot[1]] != 0:
			return True
		if board[spot[0]][spot[1]+1] != 0 and board[spot[0]][spot[1]+1] == board[spot[0]][spot[1]-1] and board[spot[0]][spot[1]-1] != 0:
			return True
		if board[spot[0]-1][spot[1]-1] !=0 and board[spot[0]-1][spot[1]-1] == board[spot[0]+1][spot[1]+1] and board[spot[0]+1][spot[1]+1] != 0:
			return True
		if board[spot[0]-1][spot[1]+1] !=0 and board[spot[0]-1][spot[1]+1] == board[spot[0]+1][spot[1]-1] and board[spot[0]+1][spot[1]-1] != 0:
			return True
		return False

	def checkMo(self, prev_board, board):

		res = (0,0)
		count = 0
		for i in range(5):
			for j in range(5):
				if prev_board[i][j] != board[i][j]: 
					if board[i][j] == 0: res = (i,j)
					count +=1
		if count > 2: return (False, res)
		_res = self.checkGanh(board,res)
		return (_res, res)

	def checkWin(self,board):
		pnum = self.countPiece(board,1)
		if pnum == 16 or pnum == 0: return True
		return False
	
	def checkWinSide(self, board, side):
		pnum = self.countPiece(board,side)
		if pnum == 16: return 1
		if pnum == 0: return -1
		return 0


		
class Node:

	time = 0
	def __init__(self, board, move, player, bot:Bot,depth) -> None:
		self.depth = depth
		self.player = player
		self.board = copy.deepcopy(board)
		self.move = move
		if move != None: bot.makeMove(self.board,self.move,player*-1)

# move function here ------------------------------------------------------------

bot = Bot()

def move( prev_board, board, player, remain_time_x, remain_time_o):
	# print(board)
	x = bot.move(prev_board, board, player, remain_time_x, remain_time_o)

# 	print("di" +str(x))
	return  x