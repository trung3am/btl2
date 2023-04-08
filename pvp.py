import pygame
from game import Game
import socket ,json, uuid, copy, threading

# if event.type == pygame.KEYDOWN:
#   if active:
#       if event.key == pygame.K_RETURN:
#           print(text)
#           text = ''
#       elif event.key == pygame.K_BACKSPACE:
#           text = text[:-1]
#       else:
#           text += event.unicode
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
# HOST = "127.0.0.1"
# PORT = 65432 
HOST = "0.tcp.ap.ngrok.io"
PORT = 18857

def pvp():
  def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col
 
  userName = "Linee"
  matchId = str(uuid.uuid4())
  def tcpRequest(s,type, body):
    req = {"type": type, "body": body}
    s.sendall(json.dumps(req).encode('utf-8'))
  def move(s,move):
    tcpRequest(s,"move",move)
  def initRequest(s,n):
    tcpRequest(s,"init",n)
  def reconnectRequest(s):
    tcpRequest(s,"reconnect",(userName, matchId))
  s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  def sendAck(s):
    tcpRequest(s,"ack","ack")

  color = pygame.Color('lightskyblue3')
  exit = pygame.Rect(10, 10, 80, 50)
  txtExit = font.render("Quit",True, color)
  def nameInput():
    input_box = pygame.Rect(100, 100, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    inputTag = font.render(' Please input your username:', True, RED)
    run = True
    name = ""
    while run:
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              return False
          if event.type == pygame.MOUSEBUTTONDOWN:
              if exit.collidepoint(event.pos):
                return False
              if input_box.collidepoint(event.pos):
                  # Toggle the active variable.
                  active = not active
              else:
                  active = False
              # Change the current color of the input box.
              color = color_active if active else color_inactive
          if event.type == pygame.KEYDOWN:
              if active:
                  if event.key == pygame.K_RETURN:
                      if name =="": name = "Linee"
                      return name
                  elif event.key == pygame.K_BACKSPACE:
                      name = name[:-1]
                  else:
                      name += event.unicode

      win.fill((30, 30, 30))
      txt_surface = font.render(name, True, color)
      width = max(200, txt_surface.get_width()+10)
      input_box.w = width
      win.blit(txt_surface, (input_box.x+5, input_box.y+5))
      win.blit(inputTag,(input_box.x-20, input_box.y-30))
      pygame.draw.rect(win, color, input_box, 2)
      win.blit(txtExit,(exit.x +5, exit.y +5))
      pygame.draw.rect(win, color, exit, 2)
      pygame.display.flip()
      clock.tick(60)

  
  side = 0
  recv = False
  clock = pygame.time.Clock()
  game = Game(win)
  select = False
  sRow = 0
  sCol = 0
  win_lose = 0
  r = True

  waitforgame = pygame.Rect(200, 350, 300, 50)
  txtWait = font.render("Waiting for Game",True, color)
  state = {"side":0,"recv":False, "wl": 0, 1:"", -1:"","score1":0,"score2": 0}
  def recvData():
    while r:
      data = s.recv(1024)
      if data:
        data = json.loads(data)
        if data['type'] == "game":

          game.board = data['body'][0]
          game.turn = data['body'][1]
          state["wl"] = data['body'][2]
          state[1] = data['body'][3]
          state[-1] = data['body'][4]
          state["score1"] = data['body'][5]
          state["score2"] = data['body'][6]
          state["recv"] = True

        if data['type'] == "state":
          state["side"] = data['body'][1]
        print(data)

  userName = nameInput()
  print(userName)
  if userName== False:
    r = False
  else:
    s.connect((HOST,PORT))
    initRequest(s,userName)
  threading.Thread(target=recvData).start()

  load = False
  p1 = (200,40)
  p2 = (200,620)
  turn = (450,10)
  while r:
    c = RED if game.turn == True else BLUE
    t = "RED TURN" if game.turn == True else "BLUE TURN"
    displayTurn = font.render(t,True,c)
    if  state["wl"] !=0:
      wl = "Win" if state["wl"] == state["side"] else "Lose"
      img = font.render(state[state["wl"]] + "Win" + ' !!!', True, (255,242,0))
      win.blit(img, (250, 300))
    s1 = (p1[0]+21*len(state[1]),p1[1])
    s2 = (p2[0]+21*len(state[-1]),p2[1])
    player1 = font.render(state[1],True, RED)
    player2 = font.render(state[-1],True, BLUE)
    score1 = font.render(": " +str(state['score1']),True, RED)
    score2 = font.render(": "+str(state['score2']),True, BLUE)
    
    if state["side"]==0:
      win.fill((30,30,30))
      win.blit(txtWait,(waitforgame.x +5, waitforgame.y +5))
      pygame.draw.rect(win, color, waitforgame, 2)
      pygame.display.flip()
      load = True
    elif load:
      load = False
      game.draw()
      win.blit(player1,p1)
      win.blit(player2,p2)
      win.blit(score1,s1)
      win.blit(score2,s2)
      win.blit(displayTurn,turn)
    win.blit(txtExit,(exit.x +5, exit.y +5))
    pygame.draw.rect(win, color, exit, 2)
    pygame.display.flip()
    if state["recv"]: 
      try:sendAck(s)
      except:pass
      game.draw()
      select = False
      state["recv"] = False
    clock.tick(15)
    if  state["wl"] !=0:
      img = font.render(state[state["wl"]] + "Win" + ' !!!', True, (255,242,0))
      win.blit(img, (250, 300))
    win.blit(txtExit,(exit.x +5, exit.y +5))
    pygame.draw.rect(win, color, exit, 2)
    if state["side"] != 0:
      win.blit(player1,p1)
      win.blit(player2,p2)
      win.blit(score1,s1)
      win.blit(score2,s2)
      win.blit(displayTurn,turn)
    pygame.display.flip()
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        print("esc")
        r = False
      
      if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        if exit.collidepoint(pos):
          r = False
        row, col = get_row_col_from_mouse(pos)

        if select and (game.turn == (state['side'] ==1)):
          print(state["side"])
          if game.board[row][col] == 0:
            if game.checkMove(((sRow,sCol),(row,col)),state["side"]):
              print("move")
              move(s,((sRow,sCol),(row,col)))
              game.draw()
              continue
              # if game.checkWin():
              #   print("win2" , game.board)
              #   wl = "Win" if game.board[game.lastMoveIdx[0]][game.lastMoveIdx[1]] ==1 else "Lose"
              #   img = font.render('You ' + wl + ' !!!', True, RED)
              #   win.blit(img, (300, 20))
              
              
          game.deSelect(sRow,sCol)
          select = False
        elif game.turn == (state['side'] ==1): 
          if game.board[row][col] != state["side"]: continue
          # print(game.turn)
          game.select(row,col)
          sRow = row
          sCol = col
          select = True


# pvp()