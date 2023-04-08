from game import Game
import socket, threading, json, uuid,time

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

lobby = []
game_state = []
def tcpRequest(type, body):
  req = {"type": type, "body": body}
  return json.dumps(req).encode('utf-8')
def sendState(conn,state):
  try:
    conn.sendall(tcpRequest("state",state))
  except:pass

def sendGameState(conn,game):
  try:
    conn.sendall(tcpRequest("game",game))
  except:pass


def getNewConnect():
  print("start")
  while True:
    conn, addr = s.accept()
    lobby.append([conn, addr, "init","","",0,0])

  
def processConnection(conn, addr):
  print(addr)
  start = time.time()
  while True:

    try:
      data = conn.recv(1024)
      if data:
        data = json.loads(data)
        if data["type"] =='init':
          for i in lobby:
            if i[1] == addr: 
              i[4] = data["body"]
              break
        if data["type"] == "ack":
          for i in lobby:
            if i[1] == addr: 
              for j in game_state:
                if j['id'] == i[3]:
                  try:j[i[5]] = time.time() + 5
                  except:pass
        if data["type"] == "move":
          move = ((data["body"][0][0],data["body"][0][1]),(data["body"][1][0],data["body"][1][1]))
          print(move)
          
          for i in lobby:
            if i[1] == addr: 
              for j in game_state:
                if j['id'] == i[3]:
                  if j['game'].makeMove(move,i[5]):
                    print(j['game'].board)
                    j[-1] = 0
                    j[1] = 0
                    break
    except:
      print("dis")
      for i in lobby:
        if i[1] == addr: 
          lobby.remove(i)
          if i[2] == 'ingame' and i[3] != "":
            for j in game_state:
              if j["id"] == i[3]:
                j["state"] = "disconnected"
                break
          break
      break
def pair(addr1, addr2,name1,name2):
  game = Game(None)
  id = str(uuid.uuid4())
  instance = {"id":id,"game": game, str(addr1):1, str(addr2):-1, "state": "running",
   1:time.time(), -1:time.time(), "wl":0, "name1":name2, "name2":name1, "delay":0, "score1": 0, "score2": 0}
  game_state.append(instance)
  return id
def removeInstance(uuid):
  for i in game_state:
    if i["id"]==uuid:
      game_state.remove(i)
      return
  
def resetGame(instance):
  if instance['wl'] == 1:
    instance['score1'] += 1
  if instance['wl'] == -1:
    instance['score2'] += 1
  
  instance['game'] = Game(None)
  instance['wl'] = 0
  instance['delay'] = 0

def gameProcess():
  for i in game_state:
    if i["state"]== "disconnected":
      for j in lobby:
        if j[3] == i["id"]:
          j[5] = 0
          j[3] = ""
          j[2] ='listen'
          sendState(j[0],(j[2],j[5]))
    if i["state"] == "running":
      a = i['game'].checkWinSide(1)
      i["wl"] = a
      if a != 0:
        if i['delay'] == 0:
          i['delay'] = time.time()
        elif time.time() - i['delay'] > 3:
          resetGame(i)
      for j in lobby:
        try:
          if j[3] == i["id"] and time.time() - i[j[5]] > 0.5:
            i[j[5]] = time.time()
            sendGameState(j[0],[i["game"].board,i["game"].turn,i["wl"],i["name1"],i['name2'], i["score1"],i["score2"]])
        except:pass

def main():
  threading.Thread(target=getNewConnect).start()
  while True:

    for i in lobby:
      if i[2] == "init":
        i[2]="listen"
        threading.Thread(target=processConnection,args=[i[0],i[1]]).start()
      if i[2] == 'listen':
        for j in lobby:
          if j[2] == 'listen' and j[1] != i[1]:
            i[2] = 'ingame'
            j[2] = 'ingame'
            print(i)
            print(j)
            id = pair(j[1],i[1],j[4],i[4])
            i[3] = id
            j[3] = id
            i[5] = 1
            j[5] = -1
            break
      if i[2] == 'listen' or i[2] == 'ingame':
        try:
          if(time.time() - i[6] > 3 ): 
            sendState(i[0],(i[2],i[5]))
            i[6] = time.time()
        except:
          pass
    gameProcess()
            

main()