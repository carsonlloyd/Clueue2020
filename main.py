from Board import Board
from Player import Player
import time, os, random, argparse, socket, selectors, types

#Globals
mainBoard = None
players = None
validInputs = ['up','down','left','right','secret','suggest','accuse']
playerNames = ['Col. Mustard','Miss Scarlet','Prof. Plum','Mrs. Peacock','Mr. Green','Mrs. White']
ADDR = 'localhost'
PORT = 65432
server_socket = None
selector = selectors.DefaultSelector()


def initNetwork():
    global HOST, ADDR, PORT, selector, server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if HOST:
        server_socket.bind((ADDR, PORT))
        server_socket.listen()
        print('listening on ', (ADDR,PORT))
        server_socket.setblocking(False)
        selector.register(server_socket,selectors.EVENT_READ, data=None)
        print('server started, waiting for clients...')
    else:
        start_connections(ADDR,PORT)

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

def accept_wrapper(sock):
    conn, addr = sock.accept() #should be ready to read
    print('accepted connection from: ', addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(connid=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    selector.register(conn, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            print('received' + repr(recv_data))
            data.outb += recv_data
        else:
            print('closing connection to: ', data.addr)
            selector.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if not HOST and not data.outb and data.messages:
            data.outb = data.messages.pop(0)
        if data.outb:
            print('sending', repr(data.outb), 'to', data.connid)
            sent = sock.send(data.outb) # Should be ready to write
            data.outb = data.outb[sent:]
    else:
        print('no mask')

def start_connections(host, port, num_conns=1):
    messages = [b'message 1', b'message 2']
    server_addr = ('localhost', 65432)
    for i in range(0, num_conns):
        connid = i+1
        print('starting connection,' + str(connid) + 'to' + str(server_addr))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(connid=connid,
                                     msg_total = sum(len(m) for m in messages),
                                     recv_total=0,
                                     messages=list(messages),
                                     outb=b'')
        selector.register(sock, events, data=data)

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

    events = selector.select(timeout=1)
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
