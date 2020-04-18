from Globals import *
from Board import Board
from Player import Player
import time, os, random, argparse, socket, selectors, types, json
from typing import List, Dict
import message_drivers as Message

def initNetwork():
    global HOST, ADDR, PORT, selector, server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if HOST:
        server_socket.bind((ADDR, PORT))
        server_socket.listen() #add num_players for max socket count
        print('listening on ', (ADDR,PORT))
        server_socket.setblocking(False)
        selector.register(server_socket,selectors.EVENT_READ, data=None)
        print('server started, waiting for clients...')
    else:
        start_connections(ADDR,PORT)

def initPlayers(numPlayers):
    global players
    players = [Player(playerNames[i]) for i in random.sample(range(6),numPlayers)]
    for playerIdx,roomIdx in enumerate(random.sample(range(9),numPlayers)):
        mainBoard.rooms[roomIdx].addPlayer(players[playerIdx]) #kinda bad encapsulation but thats pythons fault

def initialize():
    '''
    Initialize game board
    @suggest Connect players?

    @return a new, game board and state
    '''
    global mainBoard, players, messages
    print('initializing')

    mainBoard = Board()
    #randomly place players
    initPlayers(numPlayers)
    
    initNetwork()
    #mainBoard.updatePlayerLocationsOnBoard()
    
    #TODO: remove after demo
    print('For the purposes of this demo, you are playing as ' + str(players[0]))

    #render inital gameboard
    #render()

def addMessage(message, connid):
    global messages
    messages[connid].append(message)

def accept_wrapper(sock):
    conn, addr = sock.accept() #should be ready to read
    global playerAddresses
    playerAddresses[len(playerAddresses)] = addr
    messages[addr] = []
    print('accepted connection from: ', addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(connid=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    selector.register(conn, events, data=data)
    Message.send_player_connected(addr, str(players[len(playerAddresses)]))

def service_connection(key, mask):
    global messages
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(256)
        if recv_data:
            print('received ' + repr(recv_data))
            data.outb += recv_data
        else:
            pass
            #print('no data received')
            #print('closing connection to: ', data.addr)
            #selector.unregister(sock)
            #sock.close()
    if mask & selectors.EVENT_WRITE:
        if messages[data.connid]:
            data.outb = messages[data.connid].pop()
            print('sending ', repr(data.outb), ' to ', data.connid)
            sent = sock.send(data.outb) # Should be ready to write
            data.outb = data.outb[sent:]
    else:
        print('no mask')

def start_connections(host, port, num_conns=1):
    global messages
    server_addr = (host,port)
    print('starting connection ' + ' to ' + str(server_addr))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(server_addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    data = types.SimpleNamespace(connid=(host,port),
                                    msg_total = 0,
                                    recv_total=0,
                                    messages=[],
                                    outb=b'')
    messages[server_addr] = []
    selector.register(sock, events, data=data)

def send_message(message):
    pass

def parseAction(action):
    if action in ['up','down','left','right']:
        Messages.send_player_move(0,'M', action)

def getInput():
    '''
    Gather inputs and either send them as messages to the host
    or process the messages given to you as the host and arrange
    them into their sequence and relevance.
    Input messages from players whose turn it is not will be ignored
    '''
    global isTurn
    if not isTurn:
        return
    global validInputs
    action = ''
    while action not in validInputs:
        action = input('please select an action (up, down, left, right, secret, accuse, suggest): ')

    parseAction

    return action

def update(action):
    '''
    Processing inputs and updates game state according to the rules
    of the game.

    For clients they will receive the master game state update message
    and update their state accordingly
    '''
    #TODO: remove after demo
    global players, updated

    events = selector.select(timeout=.1)
    #Host network code to accept player input messages
    if HOST:
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)
    else:
        #Client code
        if events:
            for key, mask in events:
                service_connection(key, mask)
        #check for a socket being monitored to continue
        if not selector.get_map():
            print('something probably broke')

    #mainBoard.movePlayer(players[0], action)
    #mainBoard.updatePlayerLocationsOnBoard()

def render():
    '''
    Using the state of the game, this function will handle all drawing
    and graphical output to the screen.

    The host logic will disregard this function
    '''
    global updated
    if not updated:
        return
    if not gameStarted:
        print('waiting for game to start...')
        updated = False
        return
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
        action = getInput()
        update(action)
        render()

    selector.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-host', action='store_true', dest='host', default=False,
                        help='Determines whether this instance is the network host')
    results = parser.parse_args()
    global HOST
    HOST = results.host
    print('HOST:' + str(HOST))

    main()
