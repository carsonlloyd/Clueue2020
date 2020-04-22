#This file exists to avoid redefinition of globals should we import anything from 
# main into the other files
import selectors
from typing import List, Dict
mainBoard = None
players: List = []
playerAddresses: Dict = {}
numPlayers = 3 #TODO: parse this as argument to host
validInputs = ['up','down','left','right','secret','suggest','accuse', 'help']
playerNames = ['Col. Mustard','Miss Scarlet','Prof. Plum','Mrs. Peacock','Mr. Green','Mrs. White']
ADDR = 'localhost' #make socket.gethostname() to make it visible to non-local clients
PORT = 65432
server_socket = None
selector = selectors.DefaultSelector()
messages: Dict = {}
turn = 0

isTurn = False
gameStarted = False
updated = True

game_won = False