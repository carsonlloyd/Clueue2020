#This file exists to avoid redefinition of globals should we import anything from 
# main into the other files
import selectors
mainBoard = None
players = []
numPlayers = 4 #TODO: parse this as argument to host
validInputs = ['up','down','left','right','secret','suggest','accuse']
playerNames = ['Col. Mustard','Miss Scarlet','Prof. Plum','Mrs. Peacock','Mr. Green','Mrs. White']
ADDR = 'localhost' #make socket.gethostname() to make it visible to non-local clients
PORT = 65432
server_socket = None
selector = selectors.DefaultSelector()
messages = [[] for _ in range(numPlayers)]
print('real: ' + str(hex(id(messages))))

isTurn = False
gameStarted = False
updated = True