from game import Game
import random
import time
import copy

class Bot:
	def __init__(self,side, game: Game) -> None:
		self.game = game
		self.side = side

	def randomMove(self):

		pool = []
		for i in range(5):
			for j in range(5):
				if self.game.board[i][j]==-1: pool+= [(i,j)]
		if pool == []: return
		while True:


			pick  = random.choice(pool)
			move = (random.randint(max(0,pick[0]-1),min(4,pick[0]+1)),random.randint(max(0,pick[1]-1),min(4,pick[1]+1)))
			if self.game.makeMove((pick,move),self.side): break

	def move(self, preboard, board, player, remain_time_x, remain_time_o):
		Node.time = time.time()
		root = Node(board, None, player,self,0,[],[])

		m = self.minimax(root, False,player,5,0,16)
		
		print(m[1])
		self.game.makeMove(m[1],player)
		print(str(time.time()-Node.time))


	def minimax(self,node,maxplayer,player,maxDepth,alpha,beta):
		
		if maxDepth <= node.depth : return(self.countPiece(node.board, player),node.move)

		if maxplayer:
			bestVal = 0
			pool = self.gmove(node)
			if len(pool) == 0: return (self.countPiece(node.board, player),node.move)
			res = pool[0].move
			for i in pool:
				v = self.minimax(i,not maxplayer, player,maxDepth,alpha,beta)
				bestVal = max(bestVal,v[0])
				if node.depth == 0 and bestVal < v[0]:
					res = i.move
				alpha = max(alpha,bestVal)
				if beta <= alpha or bestVal ==16: break
		else:
			bestVal = 16
			pool = self.gmove(node)
			if len(pool) == 0: return (self.countPiece(node.board, player),node.move)
			res = pool[0].move
			for i in pool:
				v = self.minimax(i,not maxplayer, player,maxDepth,alpha,beta)
				bestVal = min(bestVal,v[0])
				if node.depth == 0 and bestVal > v[0]:
					res = i.move
				beta = min(beta,bestVal)
				if beta <= alpha or bestVal == 0: break
		return (bestVal,res)


	def countPiece(self, board, player):
		count = 0
		for i in board:
			for j in i:
				if j == player: count+=1

		return count

	
	def gmove(self, node):
		pool = []
		for i in range(5):
			for j in range(5):
				
				if node.board[i][j]==node.player: pool+= self.generateMove((i,j),node.board,node.player,node.depth+1,node.pmove1,node.pmove2)
		# pool.sort()

		return pool

	def generateMove(self, spot,board,player,depth,pmove1,pmove2):
		
		res = []
		i = spot[0]
		j = spot[1]
		if self.checkRepeat(player,pmove1,pmove2,(spot,(i+1,j))) and self.testMove(board, (spot,(i+1,j)),player): res += [Node(board,(spot,(i+1,j)),player*-1,self,depth,pmove1,pmove2)]
		if self.checkRepeat(player,pmove1,pmove2,(spot,(i-1,j))) and self.testMove(board, (spot,(i-1,j)),player): res += [Node(board,(spot,(i-1,j)),player*-1,self,depth,pmove1,pmove2)]
		if self.checkRepeat(player,pmove1,pmove2,(spot,(i,j+1))) and self.testMove(board, (spot,(i,j+1)),player): res += [Node(board,(spot,(i,j+1)),player*-1,self,depth,pmove1,pmove2)]
		if self.checkRepeat(player,pmove1,pmove2,(spot,(i,j-1))) and self.testMove(board, (spot,(i,j-1)),player): res += [Node(board,(spot,(i,j-1)),player*-1,self,depth,pmove1,pmove2)]
		if self.checkRepeat(player,pmove1,pmove2,(spot,(i+1,j+1))) and self.testMove(board, (spot,(i+1,j+1)),player): res += [Node(board,(spot,(i+1,j+1)),player*-1,self,depth,pmove1,pmove2)]
		if self.checkRepeat(player,pmove1,pmove2,(spot,(i-1,j+1))) and self.testMove(board, (spot,(i-1,j+1)),player): res += [Node(board,(spot,(i-1,j+1)),player*-1,self,depth,pmove1,pmove2)]
		if self.checkRepeat(player,pmove1,pmove2,(spot,(i-1,j-1))) and self.testMove(board, (spot,(i-1,j-1)),player): res += [Node(board,(spot,(i-1,j-1)),player*-1,self,depth,pmove1,pmove2)]
		if self.checkRepeat(player,pmove1,pmove2,(spot,(i+1,j-1))) and self.testMove(board, (spot,(i+1,j-1)),player): res += [Node(board,(spot,(i+1,j-1)),player*-1,self,depth,pmove1,pmove2)]
		return res
	
	def checkRepeat(self, player, pmove1,pmove2,move): 
		if player == -1:
			if pmove1[-1:] == [move]: return False
		else:
			if pmove2[-1:] == [move]: return False
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
				self.chet(board,move[1])
				return True
			if move[1][0] % 2 == 0 and move[1][1] % 2 == 0 and move[0][0] % 2 == 1 and move[0][1] % 2 == 1:
				board[move[0][0]][move[0][1]] = 0
				board[move[1][0]][move[1][1]] = player
				# print("player: " + str(player) + " moved")
				self.ganh(board,move[1])
				self.chet(board,move[1])
				return True
			print("invalid move")
			return False
		board[move[0][0]][move[0][1]] = 0
		board[move[1][0]][move[1][1]] = player
		self.ganh(board,move[1])
		self.chet(board,move[1])
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
		if board[spot[0]][spot[1]+1] != 0 and board[spot[0]][spot[1]+1] == board[spot[0]][spot[1]-1] and board[spot[0]][spot[1]-1] != 0:
			board[spot[0]][spot[1]-1] = board[spot[0]][spot[1]]
			board[spot[0]][spot[1]+1] = board[spot[0]][spot[1]]
		if board[spot[0]-1][spot[1]-1] !=0 and board[spot[0]-1][spot[1]-1] == board[spot[0]+1][spot[1]+1] and board[spot[0]+1][spot[1]+1] != 0:
			board[spot[0]-1][spot[1]-1] = board[spot[0]][spot[1]]
			board[spot[0]+1][spot[1]+1] = board[spot[0]][spot[1]]
		if board[spot[0]-1][spot[1]+1] !=0 and board[spot[0]-1][spot[1]+1] == board[spot[0]+1][spot[1]-1] and board[spot[0]+1][spot[1]-1] != 0:
			board[spot[0]-1][spot[1]+1] = board[spot[0]][spot[1]]
			board[spot[0]+1][spot[1]-1] = board[spot[0]][spot[1]]
		return

	def checkChet(self, cBoard, spot, player):
		if cBoard[spot[0]][spot[1]] == 0 or cBoard[spot[0]][spot[1]] == player: return True
		if cBoard[spot[0]][spot[1]]*player < 0 or cBoard[spot[0]][spot[1]] % 4 == 0: return False
		cBoard[spot[0]][spot[1]]*=2
		if spot[0] % 2 == 0 and spot[1] % 2 == 0 or spot[0] % 2 == 1 and spot[1] % 2 == 1:
			if spot[0]-1 >= 0 and spot[1]-1 >= 0:
				if self.checkChet(cBoard,(spot[0]-1,spot[1]-1),player): return self.retdiv(cBoard,spot)
			if spot[0]-1 >= 0 and spot[1]+1 <= 4:
				if self.checkChet(cBoard,(spot[0]-1,spot[1]+1),player): return self.retdiv(cBoard,spot)
			if spot[0]+1 <= 4 and spot[1]-1 >= 0:
				if self.checkChet(cBoard,(spot[0]+1,spot[1]-1),player): return self.retdiv(cBoard,spot)
			if spot[0]+1 <= 4 and spot[1]+1 <= 4:
				if self.checkChet(cBoard,(spot[0]+1,spot[1]+1),player): return self.retdiv(cBoard,spot)
		if spot[0]-1 >= 0:
			if self.checkChet(cBoard, (spot[0]-1,spot[1]),player): return self.retdiv(cBoard,spot)
		if spot[0]+1 <= 4:
			if self.checkChet(cBoard, (spot[0]+1,spot[1]),player): return self.retdiv(cBoard,spot)
		if spot[1]-1 >= 0:
			if self.checkChet(cBoard, (spot[0],spot[1]-1),player): return self.retdiv(cBoard,spot)
		if spot[1]+1 <= 4:
			if self.checkChet(cBoard, (spot[0],spot[1]+1),player): return self.retdiv(cBoard,spot)
		return False


	def retdiv(self, cBoard,spot):
		cBoard[spot[0]][spot[1]]/=2
		return True

	def checkStuck(self, cBoard, spot, player):
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

	def chet(self, board, spot):
		player = board[spot[0]][spot[1]]*-1
		cBoard = copy.deepcopy(board)
		for i in range(len(board)):
			for j in range(len(board[i])):
				self.checkStuck(cBoard,(i,j),player)
		for i in range(len(board)):
			for j in range(len(board[i])):
				if cBoard[i][j]*player <=0: continue
				tBoard = copy.deepcopy(cBoard)
				if not self.checkChet(cBoard,(i,j),player):
					tBoard[i][j] = player*-1
					board[i][j] = player*-1
					cBoard = tBoard
				
		return


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
	def __init__(self, board, move, player, bot:Bot,depth,pmove1,pmove2) -> None:
		self.depth = depth
		
		if player == -1: 
			self.pmove1 = [move]
			self.pmove2 = pmove2

		else: 
			self.pmove2 =[move]
			self.pmove1 = pmove1

		self.player = player
		self.board = copy.deepcopy(board)
		self.move = move
		if move != None: bot.makeMove(self.board,self.move,player*-1)

		# self.children = []

	# def __lt__(self,other):
	# 	self.count < other.count

	# def __str__(self) -> str:
	# 	return self.count

	# def __gt__(self,other):
	# 	self.count > other.count
	
	def isDetour(self,range):
		if range <= 0 or self.move == None or self.parent == None or self.parent.parent == None or self.parent.move == None or self.parent.parent.move == None: return False
		# print(self.move,"??", self.parent.parent.move, self.move == self.parent.parent.move)
		if self.move[1] == self.parent.parent.move[0] and self.move[0] == self.parent.parent.move[1]: return True
		self.parent.parent.isDetour(range-2)

