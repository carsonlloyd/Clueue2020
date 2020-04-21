from Globals import *
from Board import Board
from Player import Player
import Room
import Cards
import time, os, random, argparse, socket, selectors, types, json
from typing import List, Dict
import message_drivers as Message

#########################################################################
# This is all networking garbage, you probably dont want this
##########################################################################
def initNetwork(numPlayers):
    global HOST, ADDR, PORT, selector, server_socket, casefile, hands
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if HOST:
        server_socket.bind((ADDR, PORT))
        server_socket.listen() #add num_players for max socket count
        print('listening on ', (ADDR,PORT))
        server_socket.setblocking(False)
        selector.register(server_socket,selectors.EVENT_READ, data=None)
        print('server started, waiting for clients...')
        cards = Cards.Cards()
        casefile = cards.CaseFile()
        cards.shufflecards()
        cards.deal(numPlayers)
        hands = cards.hands
    start_connections(ADDR,PORT)

def sendAll(messageFunc, kwargs):
    '''
    Sends a given message to all players through the messageFunc
    ex. sendAll(message_drivers.send_character_unavail, {})
    '''
    for addr in playerAddresses.values():
        messageFunc(addr, **kwargs)

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

    players[len(playerAddresses)-1].addr = addr
    #confirms character as well, currently. #TODO: character choices
    Message.send_player_connected(addr, str(players[len(playerAddresses)-1]))
    
    #set up game.
    if len(playerAddresses) == numPlayers:
        #send initial positions
        sendAll(Message.send_player_positions, {'positions':{str(player):mainBoard.getPlayerRoom(player).getRoomType() for player in players}})
        #determine turn order
        determineOrder()
        determineKnowledges()
        #send game start message
        sendAll(Message.send_start_game, {})
        for i in range(numPlayers):
            players[i].setHand(hands[i])
            Message.send_card_set(playerAddresses[i], players[i].hand)
        #send first turn message
        global turn
        Message.send_ready_for_turn(playerAddresses[turn])

def service_connection(key, mask):
    global messages
    sock = key.fileobj
    data = key.data
    recv_data = None
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(256)
        if recv_data:
            print('received ' + repr(recv_data))
        else:
            pass
            #print('no data received')
            #print('closing connection to: ', data.addr)
            #selector.unregister(sock)
            #sock.close()
    if mask & selectors.EVENT_WRITE:
        if messages[data.connid]:
            data.outb = messages[data.connid].pop(0)
            print('sending ', repr(data.outb), ' to ', data.connid)
            sent = sock.send(data.outb) # Should be ready to write
            data.outb = data.outb[sent:]
    else:
        print('no mask')

    return recv_data

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
#########################################################################
# END OF NETWORKING GARBAGE
##########################################################################

def initPlayers(numPlayers):
    global players
    players = [Player(playerNames[i]) for i in random.sample(range(6),numPlayers)]
    if HOST:
        for playerIdx,roomIdx in enumerate(random.sample(range(9),numPlayers)):
            mainBoard.rooms[roomIdx].addPlayer(players[playerIdx]) #kinda bad encapsulation but thats pythons fault

def initialize():
    '''
    Initialize game board
    '''
    global mainBoard
    print('initializing')

    mainBoard = Board()
    #randomly place players
    initPlayers(numPlayers)
    initNetwork(numPlayers)



def determineOrder():
    '''
    Currently going to be the default connection order for demo purposes
    '''
    pass

def determineKnowledges():
    pass

def setPositions(positions):
    '''
    Takes a dictionary of player positions and places them in the correct places in a client game

    @param positions Dictionary following the form Dict[char: int]
    '''
    global updated
    updated = True
    count = 1
    for key, value in positions.items():
        if key == str(players[0]):
            print('adding myself (' + str(key) + ') to ' + str(Room.RoomType(value)))
            mainBoard.rooms[value].addPlayer(players[0])
        else:
            print('adding ' + str(key) + ' to ' + str(Room.RoomType(value)))
            players[count].setName(key)
            mainBoard.rooms[value].addPlayer(players[count])
            count += 1

def getPlayerBySymbol(char):
    for player in players:
        if char == str(player):
            return player

def incrementTurn():
    global turn, numPlayers
    turn += 1
    turn %= numPlayers

def parseMessage(jsonMessage):
    '''
    Receives message as bytes from the socket. Must be converted to a readable JSON format
    This is where most of the magic is going to happen
    Feel free to break out anything into functions, I'll probably do that later for most of this
    to make it look less gross
    '''
    global isTurn, gameStarted, updated, turn, HOST
    message = json.loads(jsonMessage)
    message_type = message['message_type']
    if message_type == 'player_connected':
        players[0].setName(message['connected_client'])
        print('You will be playing as ' + message['connected_client'])
    elif message_type == 'player_positions' and not HOST:
        setPositions(message['positions'])
    elif message_type == 'start_game':
        updated = True
        gameStarted = True
        print('game started')
    elif message_type == 'ready_for_turn':
        isTurn = True
    elif message_type == 'player_move' and HOST:
        player = getPlayerBySymbol(message['player'])
        if mainBoard.movePlayer(player, message['direction']):
            updated = True
            sendAll(Message.send_update_player_pos, {'player':str(player), 'pos':mainBoard.getPlayerRoom(player).getRoomType()}) 

            # is this where make_suggestion would be sent to the client?
            if mainBoard.getPlayerRoom(player).getRoomType() < Room.RoomType.MAX_ROOM:
                available_suspects = [p.name for p in players]
                available_weapons = mainBoard.getWeapons()
                Message.send_make_suggestion(playerAddresses[turn], available_suspects, available_weapons)
        else:
            #send failure message so they can resend turn
            Message.send_cannot_move(playerAddresses[turn])
    elif message_type == 'cannot_move':
        # TODO show client message to player
        # TODO request new move from player
        isTurn = True
    elif message_type == 'update_player_pos' and not HOST:
        updated = True
        player = getPlayerBySymbol(message['player'])
        mainBoard.updatePlayerPos(player, message['pos'])
        Message.send_end_turn((ADDR,PORT), str(player))
    elif message_type == 'make_suggestion':
        available_suspects = message['suspects']
        available_weapons = message['weapons']
        # TODO present gui for player to make suggestion
        # suspect,weapon = suggestion details from player
        suspect = available_suspects[0] # HARDCODED FOR NOW
        weapon = available_weapons[0] # HARDCODED FOR NOW
        Message.send_suggestion((ADDR,PORT), player, suspect, weapon) # this is for sending to host server right?
    elif message_type == 'suggestion':
        # receive suggestion from client
        client = message['client_id']
        suspect = message['suspect']
        weapon = message['weapon']
        room = mainBoard.getPlayerRoom(player)
        
        # move suspect and weapon to this room
        player2 = getPlayerBySymbol(suspect)
        player2_oldRoom = mainBoard.getPlayerRoom(player2)
        player2_oldRoom.removeWeapon(weapon)
        room.addWeapon(weapon)
        mainBoard.updatePlayerPos(player2, room)
        sendAll(Message.send_update_player_pos, {'player':str(player2), 'pos':room})

        # disproves will be done automatically by server ***
        done_disprove = False
        disproved = False
        d_card = None
        for p in players[~player]:
            for card in p.getHand():
                # if more than one matches, the player disproving should be allowed to choose the card to show
                # need to add back and forth messaging and client prompts:
                matches = []
                if card == suspect: # TODO check types
                    matches.append(card)
                elif card == weapon: # TODO check types
                    matches.append(card)
                elif card == room: # TODO check types
                    matches.append(card)

            if matches:
                # server send info to suggesting-player
                Message.send_make_disprove(playerAddresses(p), player, matches)
                
                done_disprove = True
                disproved = True
            else:
                pass # move on to next player
            
            if done_disprove:
                break
        # end suggestion and disproves
        # TODO do we need to indicate end turn here?
        if not disproved:
            # allow accusation
            available_suspects = [p.name for p in players if p != player] # remove current player
            available_weapons = mainBoard.getWeapons()
            available_rooms = [r.getRoomType() for r in mainBoard.getRooms() if r.getPlayers()] # list rooms, from board's rooms if room has player(s)
            Message.send_make_accusation(playerAddresses[turn], available_suspects, available_weapons, available_rooms)

    elif message_type == 'cannot_suggest':
        pass #TODO
    elif message_type == 'make_disprove':
        matches = message['matches']
        # TODO allow player to choose which match to send back
        pick = matches[0] # default to 0 for now
        Message.send_disprove_made((ADDR,PORT), pick)
    elif message_type == 'disprove_made':
        # show player the card chosen to disprove them
        pass
    elif message_type == 'make_accusation' and not HOST:
        available_suspects = message['suspects']
        available_weapons = message['weapons']
        available_rooms = message['rooms']
        # TODO allow player to choose
        suspect = available_suspects[0] # DEFAULTING FOR NOW
        weapon = available_weapons[0]
        room = available_rooms[0]
        Message.send_accusation_made((ADDR,PORT), player, suspect, weapon, room)
    elif message_type == 'accusation_made' and HOST:
        global case_file
        client = message['client_id']
        suspect = message['suspect']
        weapon = message['weapon']
        room = message['room']
        # confirm accusation is correct
        case_file = Cards.getCaseFile()
        if suspect == case_file['suspect'] and weapon == case_file['weapon'] and room == case_file['room']:
            sendAll(Message.send_game_win_accusation, {'client':client, 'suspect':suspect, 'weapon':weapon, 'room':room})
            game_won = True
            # go on to display message to clients
        else:
            sendAll(Message.send_false_accusation, {'client':client, 'suspect':suspect, 'weapon':weapon, 'room':room})
            # go on to display message to clients
    elif message_type == 'end_turn' and HOST and message['client_id'] == str(players[turn]):
        incrementTurn()
        Message.send_ready_for_turn(playerAddresses[turn])
        

def parseAction(action):
    if action in ['up','down','left','right','secret']:
        Message.send_player_move((ADDR,PORT), str(players[0]), action)
    elif action in ['suggest', 'accuse']:
        pass
        #do the other things

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

    isTurn = False
    parseAction(action)


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

    events = selector.select(timeout=None)
    #Host network code to accept player input messages
    message = None
    #if HOST:
    for key, mask in events:
        if key.data is None and HOST:
            accept_wrapper(key.fileobj)
        else:
            message = service_connection(key, mask)
            if message:
                parseMessage(message)

    mainBoard.updatePlayerLocationsOnBoard()

def render():
    '''
    Using the state of the game, this function will handle all drawing
    and graphical output to the screen.

    The host logic will disregard this function
    '''
    global updated, gameStarted
    if not updated:
        return
    if not gameStarted:
        print('waiting for game to start...')
        updated = False
        return
    os.system('clear')
    mainBoard.draw()
    updated = False
    


def main():
    '''
    Main loop of the game.
    getInput will take user inputs (or process the input messages as host)
    Update will change the game state (or process state update message as client)
    Render will draw all graphical items based on that state (no render for host)
    '''
    initialize()

    global game_won
    while not game_won:
        action = getInput()
        update(action)
        render()

    # game_won = True, what else? cleanup? TODO

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
