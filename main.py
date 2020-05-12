from Globals import *
from Board import Board
from Player import Player
import Room, Cards
import time, os, random, argparse, socket, selectors, types, json, sys
from typing import List, Dict
import message_drivers as Message
import pygame
from pygame.locals import *

#########################################################################
# This is all networking garbage, you probably dont want this
##########################################################################
def initNetwork(numPlayers):
    global HOST, ADDR, PORT, selector, server_socket, casefile, hands, cards
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
        print(str(cards.getCaseFile())) # FOR DEBUGGING/TESTING
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
    global playerAddresses, hands, characters
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
            Message.send_card_set(playerAddresses[i], players[i].getHand())

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
            # print('received ' + repr(recv_data))
            pass
        else:
            pass
            #print('no data received')
            #print('closing connection to: ', data.addr)
            #selector.unregister(sock)
            #sock.close()
    if mask & selectors.EVENT_WRITE:
        if messages[data.connid]:
            data.outb = messages[data.connid].pop(0)
            # print('sending ', repr(data.outb), ' to ', data.connid)
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
players = []

def initPlayers(numPlayers):
    global players
    players = [Player(playerNames[i]) for i in random.sample(range(6),numPlayers)]
    if HOST:
        for playerIdx,roomIdx in enumerate(random.sample(range(9),numPlayers)):
            mainBoard.rooms[roomIdx].addPlayer(players[playerIdx]) #kinda bad encapsulation but thats pythons fault

    mainBoard.updatePlayerLocationsOnBoard()
    # pygame.display.update()

def button(msg,x,y,w,h,ac, action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(DISPLAYSURF, ac,(x,y,w,h))
        if click[0] == 1 and action !=None:
                action()
    else:
        pygame.draw.rect(DISPLAYSURF, ac,(x,y,w,h))

    smallText = pygame.font.Font("freesansbold.ttf",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    DISPLAYSURF.blit(textSurf, textRect)

def text_objects(text, font):
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()

def game_intro(DISPLAYSURF, clock):

    scarlett = (200,0,0)
    white = (255,255,255)
    green = (0,200,0)
    peacock = (65,85,150)
    mustard = (255, 219, 88)
    plum = (221,160,221)

    intro = True
    while intro:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        largeText = pygame.font.Font('freesansbold.ttf',50)
        TextSurf, TextRect = text_objects("Clueless: Pick your character", largeText)
        TextRect.center = ((960/2),(720/3))
        DISPLAYSURF.blit(TextSurf, TextRect)

        mouse = pygame.mouse.get_pos()

        button ("Mr. Green", 150, 350, 150, 50, green, initPlayers('G'))
        button ("Col. Mustard", 150, 450, 150, 50, mustard, initPlayers('M'))
        button ("Miss Scarlett", 150, 550, 150, 50, scarlett, initPlayers('S'))
        button ("Prof. Plum", 450, 350, 150, 50, plum, initPlayers('P'))
        button ("Mrs. Peacock", 450, 450, 150, 50, peacock, initPlayers('C'))
        button ("Mrs. White", 450, 550, 150, 50, white, initPlayers('W'))

        pygame.display.update()
        clock.tick(15)

def initialize(DISPLAYSURF, PLAYERIMAGES, clock):
    '''
    Initialize game board
    '''
    global mainBoard
    print('initializing')

    mainBoard = Board(DISPLAYSURF, PLAYERIMAGES)
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

def cardToString(cards):
    '''
    Translate card int enum into a display string
    '''
    temp = []
    for card in cards:
        if card == 0:
            val = 'Study'
        elif card == 1:
            val = 'Hall'
        elif card == 2:
            val = 'Lounge'
        elif card == 3:
            val = 'Library'
        elif card == 4:
            val = 'Billiard room'
        elif card == 5:
            val = 'Dining room'
        elif card == 6:
            val = 'Conservatory'
        elif card == 7:
            val = 'Ballroom'
        elif card == 8:
            val = 'Kitchen'
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
            val = 'Rope'
        elif card == 16:
            val = 'Lead pipe'
        elif card == 17:
            val = 'Knife'
        elif card == 18:
            val = 'Wrench'
        elif card == 19:
            val = 'Candlestick'
        elif card == 20:
            val = 'Revolver'
        temp.append(val)
    return temp

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
    global isTurn, gameStarted, updated, turn, HOST, playerNames, game_won
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
        mainBoard.updatePlayerLocationsOnBoard()
    elif message_type == 'ready_for_turn':
        isTurn = True
    elif message_type == 'card_set':
        players[0].setHand([Cards.CardType(c) for c in message['cards']])
        print('Your cards are: ' + str([card.name for card in players[0].getHand()]))
    elif message_type == 'player_move' and HOST:
        player = getPlayerBySymbol(message['player'])
        if mainBoard.movePlayer(player, message['direction']):
            updated = True
            sendAll(Message.send_update_player_pos, {'player':str(player), 'pos':mainBoard.getPlayerRoom(player).getRoomType()}) 

            # is this where make_suggestion would be sent to the client?
            if mainBoard.getPlayerRoom(player).getRoomType() < Room.RoomType.MAX_ROOM:
                global playerNames
                available_suspects = playerNames
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
        mainBoard.updatePlayerLocationsOnBoard()
    elif message_type == 'make_suggestion':
        print("Make suggestion: ")
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
            string = "Choose a weapon (" + str([Room.WeaponType(x).name for x in available_weapons]) + "): "
            input_val = input(string)
            try:
                input_val = Room.WeaponType[input_val].value
                if input_val in available_weapons:
                    weapon = input_val
            except KeyError:
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
        if player2 in players:
            mainBoard.updatePlayerPos(player2, room.getRoomType())
            sendAll(Message.send_update_player_pos, {'player':str(player2), 'pos':room.getRoomType()})

        # disproves will be done automatically by server ***
        #print("STARTING DISPROVE")
        done_disprove = False
        disproved = False
        d_card = None
        for p in players:
            matches = []
            if p is not players[turn]:
                for card in p.getHand():
                    #translate card enum so that we can match other data types
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
                        val = 'ROPE'
                    elif card == 16:
                        val = 'LEAD_PIPE'
                    elif card == 17:
                        val = 'KNIFE'
                    elif card == 18:
                        val = 'WRENCH'
                    elif card == 19:
                        val = 'CANDLESTICK'
                    elif card == 20:
                        val = 'REVOLVER'

                    # if more than one matches, the player disproving should be allowed to choose the card to show
                    # need to add back and forth messaging and client prompts:
                    if val == suspect:
                        #print(str(val) + " : " + suspect)
                        matches.append(card)
                    elif val == Room.WeaponType(weapon).name:
                        #print(str(val) + " : " + str(Room.WeaponType(weapon).name))
                        matches.append(card)
                    elif val == room.getRoomType():
                        #print(str(val) + " : " + str(room.getRoomType()))
                        matches.append(card)

            if matches:
                #print("DISPROVE MATCH MADE: " + str(cardToString(matches)) + " by player index " + str(players.index(p)))
                # server send info to suggesting-player
                Message.send_make_disprove(playerAddresses[players.index(p)], str(players[turn]), matches)
                
                done_disprove = True
                disproved = True
            else:
                pass # move on to next player
            
            if done_disprove:
                break
        # end suggestion and disproves
        if not disproved:
            #print("NOT DISPROVED")
            # allow accusation
            available_suspects = playerNames
            available_weapons = mainBoard.getWeapons()
            available_rooms = [r.getRoomType() for r in mainBoard.getRooms() if r.getPlayers() and r.getRoomType() < Room.RoomType.MAX_ROOM] # list rooms, from board's rooms if room has player(s)
            Message.send_make_accusation(playerAddresses[turn], available_suspects, available_weapons, available_rooms)

    elif message_type == 'cannot_suggest':
        pass #TODO
    elif message_type == 'make_disprove':
        print("Make disprove: ")
        matches = message['matches'] # these are CardType enums
        # allow player to choose which match to send back
        matches = cardToString(matches)

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
        print("Make accusation: ")
        available_suspects = message['suspects']
        available_weapons = message['weapons']
        available_rooms = message['rooms']
        # convert rooms for usability
        for i in range(len(available_rooms)):
            available_rooms[i] = Room.RoomType(available_rooms[i]).name
        # allow player to choose
        suspect = weapon = room = None
        while suspect == None:
            string = "Choose a suspect (" + str(available_suspects) + "): "
            input_val = input(string)
            if input_val in available_suspects:
                suspect = input_val
        while weapon == None:
            string = "Choose a weapon (" + str([Room.WeaponType(x).name for x in available_weapons]) + "): "
            input_val = input(string)
            try:
                input_val = Room.WeaponType[input_val].value
                if input_val in available_weapons:
                    weapon = input_val
            except KeyError:
                pass
        while room == None:
            string = "Choose a room (" + str(available_rooms) + "): "
            input_val = input(string)
            if input_val in available_rooms:
                room = input_val
        Message.send_accusation_made((ADDR,PORT), str(players[0]), suspect, weapon, room)
    elif message_type == 'accusation_made' and HOST:
        global cards, game_won
        client = message['client_id']
        suspect = message['suspect']
        weapon = message['weapon']
        room = message['room']
        # confirm accusation is correct
        case_file = cards.getCaseFile()

        # translate case file to match user strings
        cf_suspect = cf_weapon = None
        for c in Cards.CardType:
            if c.name == case_file['suspect']:
                cf_suspect = cardToString([c])[0]

        if suspect == cf_suspect and Room.WeaponType(weapon).name == case_file['weapon'] and room == case_file['room']:
            sendAll(Message.send_game_win_accusation, {'client_id':client, 'suspect':suspect, 'weapon':case_file['weapon'], 'room':room})
            #game_won = True # HAVE TO COMMENT THIS OUT - race condition?
            # go on to display message to clients
        else:
            Message.send_false_accusation(playerAddresses[turn])

            p = players[turn] # PLAYER WHO WAS WRONG
            p.setFailed()

            # if there are NO players left, just END
            isEnd = True
            for x in players:
                if not x.isFailed():
                    isEnd = False

            if isEnd:   # end game, end false message and game_won
                sendAll(Message.send_game_win_accusation, {'client_id':client, 'suspect':False, 'weapon':False, 'room':False})
                game_won = True
            else:       # otherwise, continue on like normal
                if mainBoard.getPlayerRoom(p).getRoomType() > Room.RoomType.MAX_ROOM:
                    in_hallway = True # if in hallway, move them
                else:
                    in_hallway = False # otherwise no need to move them

                if p in players and in_hallway:    # move player into a room so they are out of the hallway
                    # for now just go random, TODO move them to their starting room?
                    room = random.randint(0,8)
                    mainBoard.updatePlayerPos(p, room)
                    sendAll(Message.send_update_player_pos, {'player':str(p), 'pos':room})
    elif message_type == 'game_win_accusation':
        culprit = str(message['suspect'])
        weapon = str(message['weapon'])
        room = str(message['room'])

        if culprit == 'False' and weapon == 'False' and room == 'False':
            print("All players lost! Too bad!")
            # TODO display gui window with this information
        else:
            print("Game has been won: " + culprit + " in the " + room + " with the " + weapon)
            # TODO display gui window with this information

        game_won = True
    elif message_type == 'false_accusation':
        print("Accusation was false.")
        p = players[0]
        p.setFailed()
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
    global isTurn, players
    if not isTurn:
        return
    if players[0].isFailed(): # if failed, don't give a turn
        print("SKIPPING TURN")
        isTurn = False

        Message.send_end_turn((ADDR,PORT), str(players[0]))

        return

    global validInputs
    action = ''
    while action not in validInputs: 
        action = input('Please select an action (up, down, left, right, secret, help): ')

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

    # attempt to only update board is action is real?
    if action:
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
    # os.system('cls' if os.name == 'nt' else 'clear') # comment out to stop clearing screen
    # mainBoard.draw() # not needed any more? used to be for console printing?
    updated = False
    


def main():
    '''
    Main loop of the game.
    getInput will take user inputs (or process the input messages as host)
    Update will change the game state (or process state update message as client)
    Render will draw all graphical items based on that state (no render for host)
    '''
    global clock, DISPLAYSURF, black, white, IMAGESDICT
    pygame.init()
    clock = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((960, 720))
    pygame.display.set_caption('Clueless')
    black = (0,0,0)
    white = (255,255,255)
    DISPLAYSURF.fill(white)

    IMAGESDICT = {'gameboard': pygame.image.load('gameboard.png'),
                  'greenplayer': pygame.image.load('green.png'),
                  'mustardplayer': pygame.image.load('mustard.png'),
                  'scarletplayer': pygame.image.load('scarlett.png'),
                  'whiteplayer': pygame.image.load('white.png'),
                  'plumplayer': pygame.image.load('plum.png'),
                  'peacockplayer': pygame.image.load('peacock.png')}

    currentImage = 0
    PLAYERIMAGES = [IMAGESDICT['greenplayer'],
                    IMAGESDICT['mustardplayer'],
                    IMAGESDICT['scarletplayer'],
                    IMAGESDICT['whiteplayer'],
                    IMAGESDICT['plumplayer'],
                    IMAGESDICT['peacockplayer']]

    # game_intro(DISPLAYSURF, clock) # not taking player input any more, to simplify and get this working, skip this

    initialize(DISPLAYSURF, PLAYERIMAGES, clock)

    global game_won
    while not game_won:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                game_won = True
        action = getInput()
        update(action)
        render()
        pygame.display.update()

    # game_won = True, what else? cleanup? TODO
    # FIX HERE - game just closes when won - would be okay if just running command line
    print("GAME_WON = True")

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
