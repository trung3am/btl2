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
		start = time.time()
		m = self.minimax(board, player, 0)
		self.game.makeMove(m,player)
		print(str(time.time()-start))

	def minimax(self, board, player, depth):
		print(depth)
		heuristic = self.checkWinSide(board, player)
		if heuristic != 0: return (heuristic,None)
		pool =[]
		for i in range(5):
			for j in range(5):
				if board[i][j]==player: pool+= self.generateMove((i,j),board,player)
		for i in pool:
			m =  None
			if depth ==0: m = i
			cBoard = copy.deepcopy(board)
			self.makeMove(cBoard,i,player)
			h = self.checkWinSide(cBoard, player)
			if h == 1: return (h,m)
			if h == 0: 
				h = self.minimax(cBoard, player*-1,depth+1)
				if h[0] == -1: return(h,m)
		return(h[0],m)

	def countPiece(self, board, player):
		count = 0
		for i in board:
			for j in i:
				if j == player: count+=1

		return count



	def generateMove(self, spot,board,player):
		res = []
		i = spot[0]
		j = spot[1]
		if self.testMove(board, (spot,(i+1,j)),player): res += [(spot,(i+1,j))]
		if self.testMove(board, (spot,(i-1,j)),player): res += [(spot,(i-1,j))]
		if self.testMove(board, (spot,(i,j+1)),player): res += [(spot,(i,j+1))]
		if self.testMove(board, (spot,(i,j-1)),player): res += [(spot,(i,j-1))]
		if self.testMove(board, (spot,(i+1,j+1)),player): res += [(spot,(i+1,j+1))]
		if self.testMove(board, (spot,(i-1,j+1)),player): res += [(spot,(i-1,j+1))]
		if self.testMove(board, (spot,(i-1,j-1)),player): res += [(spot,(i-1,j-1))]
		if self.testMove(board, (spot,(i+1,j-1)),player): res += [(spot,(i+1,j-1))]
		return res
	
	def testMove(self, board, move, player):
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
				print("player: " + str(player) + " moved")
				self.ganh(board,move[1])
				self.chet(board,move[1])
				return True
			if move[1][0] % 2 == 0 and move[1][1] % 2 == 0 and move[0][0] % 2 == 1 and move[0][1] % 2 == 1:
				board[move[0][0]][move[0][1]] = 0
				board[move[1][0]][move[1][1]] = player
				print("player: " + str(player) + " moved")
				self.ganh(board,move[1])
				self.chet(board,move[1])
				return True
			print("invalid move")
			return False
		board[move[0][0]][move[0][1]] = 0
		board[move[1][0]][move[1][1]] = player
		self.ganh(board,move[1])
		self.chet(board,move[1])
		print("player: " + str(player) + " moved")
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


	def checkWin(self, board):
		for i in board:
			if len(set(i)) == 3: return False
		return True

	def checkWinSide(self, board, side):
		r = []
		for i in board:
			
			if len(set(i)) == 3: return 0
			if len(set(i)) == 2: r = list(set(i))

		if r[1] != side: return -1
		return 1
			
				


		
			