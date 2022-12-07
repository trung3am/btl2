from game import Game
import random

class Bot:
	def __init__(self, game: Game) -> None:
		self.game = game

	def randomMove(self):

		pool = []
		side = -1
		for i in range(5):
			for j in range(5):
				if Game.board[i][j]==-1: pool+= [(i,j)]
		
		while True:


			pick  = random.choice(pool)
			move = (random.randint(max(0,i-1),min(4,i+1)),random.randint(max(0,j-1),min(4,j+1)))
			if self.game.makeMove((pick,move),side): break


pool = [(1,2)]

pool += [(3,5)]
pool += [(1,5)]
pool += [(7,6)]
pool += [(2,9)]
pool += [(4,0)]

n = 10
while n > 0:
	print(random.choice(pool))
	n-=1