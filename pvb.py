import pygame
from game import Game
import time, copy
from agent import Agent
from bot import Bot
FPS = 60
# rgb
RED = (255, 0, 0)
YELLOW = (255,242,0)
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
select = False
playerside = 1
botside = -1 * playerside
def get_row_col_from_mouse(pos):
  x, y = pos
  row = y // SQUARE_SIZE
  col = x // SQUARE_SIZE
  return row, col

def RL(game, agent, prev_rand):
  if game.turn == (agent.player==1):
    move = agent.get_action(game.board, prev_rand)
    if move != None and move[1] != None:
      select = False
      time.sleep(1.2)
      game.makeMove(move[1],agent.player)
      game.draw()

def minimax(game, bot, prev_rand):
  if game.turn == (botside==1):
    board = copy.deepcopy(game.board)
    move = bot.move(prev_rand,board,botside)
    if move != None:
      game.makeMove(move,botside)
      time.sleep(1.2)
      game.draw()
      select = False


def playVsBot(mode):
  # mode = "RL"
  # mode = "MINIMAX"
  run = True
  clock = pygame.time.Clock()
  game = Game(win)
  game.draw()
  select = False
  sRow = 0
  sCol = 0
  agent = Agent(game,botside)
  bot = Bot()
  agent.player = botside
  prev_rand = game.board
  color = pygame.Color('lightskyblue3')
  exit = pygame.Rect(10, 10, 80, 50)
  txtExit = font.render("Quit",True, color)
  turn = (450,10)
  pause = pygame.Rect(450, 620, 150, 50)
  p1 = (200,40)
  p2 = (200,620)
  s1 = (p1[0]+150),(p1[1])
  s2 = (p2[0]+150),(p2[1])
  pscore = 0
  botscore = 0
  player1 = font.render("Player",True, RED)
  player2 = font.render("Bot",True, BLUE)
  pause_status = False
  pauseScreen = font.render("Game Paused",True, YELLOW)
  while run:
    if not select:
      game.draw()
    if pause_status:
      game.draw()
      win.blit(pauseScreen,(250, 300))
      pauseDisplay = font.render("Unpause",True, YELLOW)
    else:
      pauseDisplay = font.render("Pause",True, YELLOW)
    score1 = font.render(": " +str(pscore),True, RED)
    score2 = font.render(": "+str(botscore),True, BLUE)
    c = RED if game.turn == True else BLUE
    t = "RED TURN" if game.turn == True else "BLUE TURN"
    displayTurn = font.render(t,True,c)
    win.blit(displayTurn,turn)
    win.blit(player1,p1)
    win.blit(player2,p2)
    win.blit(score1,s1)
    win.blit(score2,s2)
    win.blit(pauseDisplay,(pause.x+5,pause.y+5))
    win.blit(txtExit,(exit.x +5, exit.y +5))
    pygame.draw.rect(win, color, exit, 2)
    pygame.draw.rect(win, color, pause, 2)
    pygame.display.flip()
    clock.tick(30)
    if  game.checkWin():
      print("win" , game.board)
      wl = "Win" if game.checkWinSide(1) ==1 else "Lose"
      img = font.render('You ' + wl + ' !!!', True, YELLOW)
      win.blit(img, (250, 300))
      pygame.display.flip()
      time.sleep(3)
      if wl == "Win": pscore +=1
      else: botscore +=1
      game = Game(win)
      game.draw()
      continue
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
      
      if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        if pos[0] >= 0 and pos[0] <= 90 and pos[1] >=0 and pos[1] <=60:
          return
        if pause.collidepoint(pos[0],pos[1]):
          pause_status = not pause_status
        row, col = get_row_col_from_mouse(pos)
        if pause_status: continue
        if select and game.turn == (playerside==1):
          if game.board[row][col] == 0:
            prev_rand = copy.deepcopy(game.board)
            if game.makeMove(((sRow,sCol),(row,col)),playerside):
              if game.checkWin():
                print("win2" , game.board)
                wl = "Win" if game.board[game.lastMoveIdx[0]][game.lastMoveIdx[1]] ==1 else "Lose"
                img = font.render('You ' + wl + ' !!!', True, YELLOW)
                win.blit(img, (250, 300))
              game.draw()
              continue
          game.deSelect(sRow,sCol)
          select = False
        elif game.turn == (playerside==1): 
          if game.board[row][col] != playerside: continue
          if game.turn == (playerside==1): game.select(row,col)
          sRow = row
          sCol = col
          select = True
    win.blit(txtExit,(exit.x +5, exit.y +5))
    win.blit(displayTurn,turn)
    win.blit(player1,p1)
    win.blit(player2,p2)
    win.blit(score1,s1)
    win.blit(score2,s2)
    pygame.draw.rect(win, color, exit, 2)
    pygame.display.flip()
    if mode == "RL":
      RL(game,agent,prev_rand)
    elif mode == "MINIMAX":
      minimax(game,bot,prev_rand)
    # if game.checkWin():
    #   print("win3" , game.board)
    #   wl = "Win" if game.board[game.lastMoveIdx[0]][game.lastMoveIdx[1]] ==1 else "Lose"
    #   img = font.render('You ' + wl + ' !!!', True, RED)
    #   win.blit(img, (300, 20))
          
  pygame.quit()

# playVsBot("RL")