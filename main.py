from Globals import *
from Board import Board
from Player import Player
import Room, Cards
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
    global playerAddresses, hands
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
        #send out knowledge cards
        for i in range(numPlayers):
            players[i].setHand(hands[i])
            Message.send_card_set(playerAddresses[i], players[i].hand)

        #set up weapons
        for weapon in mainBoard.getWeapons():
            rooms = mainBoard.getRooms()
            room = random.choice(rooms)
            room.addWeapon(weapon)

        #send game start message
        sendAll(Message.send_start_game, {})
        global turn
        #send first turn message
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

def getPlayerFromName(name):
    for player in players:
        if name == player.getName():
            return player

def cardToString(card):
        #translate
    val = -1
    if card == 0:
        val = "Study"
    if card == 1:
        val = "Hall"
    if card == 2:
        val = "Lounge"
    if card == 3:
        val = "Library"
    if card == 4:
        val = "Billiard Room"
    if card == 5:
        val = "Dining Room"
    if card == 6:
        val = "Conservatory"
    if card == 7:
        val = "Ball Room"
    elif card == 8:
        val = "Kitchen"
    elif card == 9:
        val = 'Col. Mustard'
    elif card == 10:
        val = 'Miss Scarlet'
    elif card == 11:
        val = 'Prof. Plum' 
    elif card == 12:
        val = 'Mr. Green'
    elif card == 13:
        val = 'Mrs. White'
    elif card == 14:
        val = 'Mrs. Peacock'
    elif card == 15:
        val = "Rope"
    elif card == 16:
        val = "Lead pipe"
    elif card == 17:
        val = "Knife"
    elif card == 18:
        val = "Wrench"
    elif card == 19:
        val = "Candlestick"
    elif card == 20:
        val = "Revolver"
    return val

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
    elif message_type == 'card_set':
        players[0].setHand([Cards.CardType(c) for c in message['cards']])
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
    elif message_type == 'update_player_pos': #and not HOST:
        updated = True
        player = getPlayerBySymbol(message['player'])
        mainBoard.updatePlayerPos(player, message['pos'])
        # print(str(mainBoard.getPlayerRoom(player).getRoomType()) + " : ")
        if mainBoard.getPlayerRoom(player).getRoomType() > Room.RoomType.MAX_ROOM: # if into hallway, end turn
            # print(str(players[0]) + " : " + str(message['player']))
            if str(players[0]) == message['player']:
                Message.send_end_turn((ADDR,PORT), str(player))
    elif message_type == 'make_suggestion':
        available_suspects = message['suspects']
        available_weapons = message['weapons']
        # TODO present gui for player to make suggestion
        # suspect,weapon = suggestion details from player
        suspect = weapon = None
        while suspect == None:
            string = "Choose a suspect (" + str(available_suspects) + "): "
            input_val = input(string)
            if input_val in available_suspects:
                suspect = input_val
        while weapon == None:
            string = "Choose a weapon (" + str(available_weapons) + "): "
            input_val = input(string)
            try:
                input_val = int(input_val)
                if input_val in available_weapons:
                    weapon = input_val
            except ValueError:
                pass
            
        Message.send_suggestion((ADDR,PORT), str(players[turn]), suspect, weapon) # this is for sending to host server right?
    elif message_type == 'suggestion':
        # receive suggestion from client
        client = message['client_id']
        suspect = message['suspect']
        weapon = message['weapon']
        room = mainBoard.getPlayerRoom(players[turn])
        
        # move suspect and weapon to this room
        player2 = getPlayerFromName(suspect)
        weapon_old_room = mainBoard.getWeaponRoom(weapon)
        weapon_old_room.removeWeapon(weapon)
        room.addWeapon(weapon)
        mainBoard.updatePlayerPos(player2, room.getRoomType())
        sendAll(Message.send_update_player_pos, {'player':str(player2), 'pos':room.getRoomType()})

        # disproves will be done automatically by server ***
        print("STARTING DISPROVE")
        done_disprove = False
        disproved = False
        d_card = None
        for p in players:
            matches = []
            if p is not players[turn]:
                for card in p.getHand():
                    #translate
                    if card < 9:
                        val = card
                    elif card == 9:
                        val = 'Col. Mustard'
                    elif card == 10:
                        val = 'Miss Scarlet'
                    elif card == 11:
                        val = 'Prof. Plum' 
                    elif card == 12:
                        val = 'Mr. Green'
                    elif card == 13:
                        val = 'Mrs. White'
                    elif card == 14:
                        val = 'Mrs. Peacock'
                    elif card == 15:
                        val = 0
                    elif card == 16:
                        val = 1
                    elif card == 17:
                        val = 2
                    elif card == 18:
                        val = 3
                    elif card == 19:
                        val = 4
                    elif card == 20:
                        val = 5
                    # if more than one matches, the player disproving should be allowed to choose the card to show
                    # need to add back and forth messaging and client prompts:
                    if val == suspect:
                        matches.append(cardToString(card))
                    elif val == weapon:
                        matches.append(cardToString(card))
                    elif val == room.getRoomType():
                        matches.append(cardToString(card))

            if matches:
                print("DISPROVE MATCH MADE: " + str(matches) + " by player index " + str(players.index(p)))
                # server send info to suggesting-player
                Message.send_make_disprove(playerAddresses[players.index(p)], str(players[turn]), matches)
                
                done_disprove = True
                disproved = True
            else:
                pass # move on to next player
            
            if done_disprove:
                break
        # end suggestion and disproves
        # TODO do we need to indicate end turn here?
        if not disproved:
            print("NOT DISPROVED")
            # allow accusation
            available_suspects = [p.name for p in players if p != players[turn]] # remove current player
            available_weapons = mainBoard.getWeapons()
            available_rooms = [r.getRoomType() for r in mainBoard.getRooms() if r.getPlayers()] # list rooms, from board's rooms if room has player(s)
            Message.send_make_accusation(playerAddresses[turn], available_suspects, available_weapons, available_rooms)

    elif message_type == 'cannot_suggest':
        pass #TODO
    elif message_type == 'make_disprove':
        matches = message['matches']
        # allow player to choose which match to send back
        choice = None
        while choice == None:
            string = "Choose a card (" + str(matches) + "): "
            input_val = input(string)
            if input_val in matches:
                choice = input_val
        Message.send_disprove_made((ADDR,PORT), message['client_id'], choice)
    elif message_type == 'disprove_made':
        # TELL CLIENT
        Message.send_disprove_notify(playerAddresses[turn], message['pick'])
        pass
    elif message_type == 'disprove_notify':
        # show suggester what disproved them
        print("DISPROVED: " + message['pick'])
        Message.send_end_turn((ADDR,PORT), str(players[0]))
    elif message_type == 'make_accusation':
        print("IN MAKE ACCUSATION")
        available_suspects = message['suspects']
        available_weapons = message['weapons']
        available_rooms = message['rooms']
        # allow player to choose
        suspect = weapon = room = None
        while suspect == None:
            string = "Choose a suspect (" + str(available_suspects) + "): "
            input_val = input(string)
            if input_val in available_suspects:
                suspect = input_val
        while weapon == None:
            string = "Choose a weapon (" + str(available_weapons) + "): "
            input_val = input(string)
            try:
                input_val = int(input_val)
                if input_val in available_weapons:
                    weapon = input_val
            except ValueError:
                pass
        while room == None:
            string = "Choose a room (" + str(available_rooms) + "): "
            input_val = input(string)
            if input_val in available_rooms:
                room = input_val
        Message.send_accusation_made((ADDR,PORT), str(players[0]), suspect, weapon, room)
    elif message_type == 'accusation_made' and HOST:
        global case_file
        client = message['client_id']
        suspect = message['suspect']
        weapon = message['weapon']
        room = message['room']
        # confirm accusation is correct
        case_file = cards.getCaseFile()
        if suspect == case_file['suspect'] and weapon == case_file['weapon'] and room == case_file['room']:
            sendAll(Message.send_game_win_accusation, {'client':client, 'suspect':suspect, 'weapon':weapon, 'room':room})
            game_won = True
            # go on to display message to clients
        else:
            Message.send_false_accusation(playerAddresses[turn], suspect, weapon, room)
            # go on to display message to client
    elif message_type == 'game_win_accusation':
        print("Game has been won: ") # TODO FILL OUT
    elif message_type == 'false_accusation':
        print("Accusation was false.")
        Message.send_end_turn((ADDR,PORT), str(players[0]))
    elif message_type == 'end_turn' and HOST and message['client_id'] == str(players[turn]):
        incrementTurn()
        Message.send_ready_for_turn(playerAddresses[turn])
        

def parseAction(action):
    if action in ['up','down','left','right','secret']:
        Message.send_player_move((ADDR,PORT), str(players[0]), action)
    elif action == 'help':
        print('\nThis is the game of Clue. You are playing as ' + str(players[0]) + '. Please either make a move by typing ' + \
              'up, down, left, right, secret, or make a suggestion or accusation by typing suggest/accuse [PLAYER_SYMBOL] [ROOM_NAME] [WEAPON].')
        print('Keep in mind that only one player can occupy a hallway at a time and suggestions for a room must be made with you in that room\n')
        print('When you move into a room, you must make a suggestion, and one player will show you one card to disprove a part of your suggestion')
        print('On a players turn, if they correctly accuse the right person/room/weapon then they win the game!\n')
        global isTurn
        isTurn = True
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
        action = input('Please select an action (up, down, left, right, secret, accuse, suggest, help): ')

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
