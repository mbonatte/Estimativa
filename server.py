import socket
import pickle
import threading
import time
from Game import Game
from Player import Player

PORT = 5000
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDRESS)

clients = set()
games = {} #To have more than one game.

####################################################################

def getClient():
    conn, addr = server.accept()
    print(f"[NEW CONNECTION] {conn.getpeername()}")
    with threading.Lock():
        clients.add(conn)
    return conn

def removeClient(conn):
    with threading.Lock():
        clients.remove(conn)
    print(f"[REMOVE CONNECTION] {conn.getpeername()}")
    conn.close()

def handleClient(conn):
    while True:
        try:
            msg = conn.recv(1024)
            msg = pickle.loads(msg)
            handMessage(conn,msg)
        except Exception as e:
            print(e)
            break
    removeClient(conn)
     

def startServer(server):
    server.listen()
    while True:
        try:
            conn = getClient()
            thread = threading.Thread(target = handleClient,
                                      args = (conn, ))
            thread.start()
        except Exception as e:
            print(e)
            break
    server.close()
 
def handMessage(conn,msg):
    for key, value in msg.items():
        if key == 'NEW_GAME':
            newGame(conn,value)
        elif key == 'JOIN_GAME':
            addClientToGame(conn,value)
        #elif key == 'N_PLAYERS':
            #game.numberOfPlayers = value
        elif key == 'CHAT':
            broadcastMessage(value)
        elif key == 'BET':
            for game in games:
                if conn in games[game]:
                    game.setBetViaConn(conn,value)
        elif key == 'PICK':
            for game in games:
                if conn in games[game]:
                    game.setPickViaConn(conn,value)
        elif key == 'NAME':
            for game in games:
                if conn in games[game]:
                    game.setName(conn,value)
        else:
            print(key, value)

##################################################################

def sendMsg(conn, msg):
    conn.sendall(pickle.dumps(msg))

def broadcastMessage(message):
    message = {'CHAT': message}
    with threading.Lock():
        for client in clients:
            sendMsg(client,message)


################################################################3

def addClientToGame(conn,globalID):
    for game in games:
        if globalID == game.globalID:
            player = Player(conn)
            game.addPlayer(player)
            games[game].add(conn)
            print(f"[NEW PLAYER] on {globalID}")
    broadcastMessage("{name} has joined the game!")

def newGame(conn,nPlayers):
    from uuid import uuid4
    #globalID = uuid4().hex[:6]
    globalID = 'ANDRESSA'
    game = Game(globalID,nPlayers)
    print(f"[NEW GAME] {globalID}")
    with threading.Lock(): # I think I don't need this line
        games[game] = set()
    addClientToGame(conn,globalID)
    thread = threading.Thread(target = handleGame,
                                       args = (game,))
    thread.start()


def handleGame(game):
    while game.numberOfPlayers != len(game.playersActived):
        broadcastMessage('Waiting players')
        time.sleep(5)
    game.run()
    with threading.Lock():
        for client in games[game]:
            removeClient(client)
        games.remove(game)
        
        
#############################################################3
print("Server is working on ", ADDRESS)
startServer(server)
