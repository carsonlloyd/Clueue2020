from Board import Board
from Player import Player
import time, os, random, argparse, socket, selectors

#Globals
mainBoard = None
players = None
validInputs = ['up','down','left','right','secret','suggest','accuse']
playerNames = ['Col. Mustard','Miss Scarlet','Prof. Plum','Mrs. Peacock','Mr. Green','Mrs. White']
ADDR = 'localhost'
PORT = 65432
selector = selectors.DefaultSelector()


def initNetwork():
    global HOST, ADDR, PORT, selector
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if HOST:
            s.bind((ADDR, PORT))
            s.listen()
            print('listening on ', (ADDR,PORT))
            s.setblocking(False)
            sel.register(s,selectors.EVENT_READ, data=None)
            conn, addr = s.accept
            print('server started, waiting for clients...')
        else:
            s.connect((ADDR, PORT))



def initPlayers(numPlayers):
    players = [Player(playerNames[i]) for i in random.sample(range(6),numPlayers)]
    for playerIdx,roomIdx in enumerate(random.sample(range(9),numPlayers)):
        mainBoard.rooms[roomIdx].addPlayer(players[playerIdx]) #kinda bad encapsulation but thats pythons fault

def initialize():
    '''
    Initialize game board
    @suggest Connect players?

    @return a new, game board and state
    '''
    print('initializing')
    initNetwork()
    global mainBoard, players
    mainBoard = Board()

    #randomly place players
    initPlayers(4)
    mainBoard.updatePlayerLocationsOnBoard()

    

    #render inital gameboard
    render()

def getInput():
    '''
    Gather inputs and either send them as messages to the host
    or process the messages given to you as the host and arrange
    them into their sequence and relevance.
    Input messages from players whose turn it is not will be ignored
    '''
    global validInputs
    action = ''
    while action not in validInputs:
        action = input('please select an action (up, down, left, right, secret, accuse, suggest): ')

    #Host network code to accept player input messages
    if HOST:
        events = selector.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)




def update():
    '''
    Processing inputs and updates game state according to the rules
    of the game.

    For clients they will receive the master game state update message
    and update their state accordingly
    '''
    pass

def render():
    '''
    Using the state of the game, this function will handle all drawing
    and graphical output to the screen.

    The host logic will disregard this function
    '''
    os.system('clear')
    mainBoard.draw()
    


def main():
    '''
    Main loop of the game.
    getInput will take user inputs (or process the input messages as host)
    Update will change the game state (or process state update message as client)
    Render will draw all graphical items based on that state (no render for host)
    '''
    initialize()

    while True: #TODO: Change to while game not won
        getInput()
        update()
        render()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-host', action='store_true', dest='host', default=False,
                        help='Determines whether this instance is the network host')
    results = parser.parse_args()
    global HOST
    HOST = results.host
    print('HOST:' + str(HOST))

    main()
