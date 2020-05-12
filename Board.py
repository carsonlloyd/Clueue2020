import Room
import os, pygame

class Board:

    def __init__(self, DISPLAYSURF, PLAYERIMAGES):
        # Creates a brand new, blank board data structure

        global boardimg, images
        boardimg = pygame.image.load('gameboard.png')
 
        images = {'G': PLAYERIMAGES[0], 'M': PLAYERIMAGES[1], 'S': PLAYERIMAGES[2],'W': PLAYERIMAGES[3], 'P': PLAYERIMAGES[4], 'C': PLAYERIMAGES[5]}
        
        DISPLAYSURF.blit(boardimg, (0,0))
        DISPLAYSURF.blit(PLAYERIMAGES[0], (295,650))
        gstartx = 295
        gstarty = 650
        DISPLAYSURF.blit(PLAYERIMAGES[3], (605,650))
        wstartx = 605
        wstarty = 650
        DISPLAYSURF.blit(PLAYERIMAGES[5], (20,450))
        cstartx = 20
        cstarty = 450
        DISPLAYSURF.blit(PLAYERIMAGES[4], (20,230))
        pstartx = 20
        pstarty = 230
        DISPLAYSURF.blit(PLAYERIMAGES[2], (605,20))
        sstartx = 605
        sstarty = 20
        DISPLAYSURF.blit(PLAYERIMAGES[1], (900,230))
        mstartx = 900
        mstarty = 230

        self.board = DISPLAYSURF
        self.rooms = [Room.Room(roomType) for roomType in Room.RoomType]
        self.weapons = [w.value for w in Room.WeaponType]
        self.avatarposx = {'G': gstartx, 'W': wstartx, 'C': cstartx, 'P': pstartx, 'M': mstartx, 'S':sstartx}
        self.avatarposy = {'G': gstarty, 'W': wstarty, 'C': cstarty, 'P': pstarty, 'M': mstarty, 'S':sstarty}

        # MINUS 6 HERE - index 0 = -6 room type number enum
        self.abs_pos = [
                {'x': 125, 'y':130}, #STUDY = 0
                {'x': 435, 'y':130}, #HALL = 1
                {'x': 745, 'y':130}, #LOUNGE = 2
                {'x': 125, 'y':332}, #LIBRARY = 3
                {'x': 435, 'y':332}, #BILLIARD_ROOM = 4
                {'x': 745, 'y':332}, #DINING_ROOM = 5
                {'x': 125, 'y':542}, #CONSERVATORY = 6
                {'x': 435, 'y':542}, #BALL_ROOM = 7
                {'x': 745, 'y':542}, #KITCHEN = 8
                {'x': 0, 'y':0}, #MAX_ROOM = 9

                {'x': 300, 'y':125}, #H_STUDY_HALL = 10
                {'x': 600, 'y':125}, #H_HALL_LOUNGE = 11
                {'x': 150, 'y':230}, #H_STUDY_LIBRARY = 12
                {'x': 450, 'y':230}, #H_HALL_BILLIARD_ROOM = 13
                {'x': 750, 'y':230}, #H_LOUNGE_DINING_ROOM = 14
                {'x': 300, 'y':335}, #H_LIBRARY_BILLIARD_ROOM = 15
                {'x': 600, 'y':335}, #H_BILLIARD_ROOM_DINING_ROOM = 16
                {'x': 150, 'y':440}, #H_LIBRARY_CONSERVATORY = 17
                {'x': 450, 'y':440}, #H_BILLIARD_ROOM_BALL_ROOM = 18
                {'x': 750, 'y':440}, #H_DINING_ROOM_KITCHEN = 19
                {'x': 300, 'y':545}, #H_CONSERVATORY_BALL_ROOM = 20
                {'x': 600, 'y':545}  #H_BALL_ROOM_KITCHEN = 21
            ]

    def draw(self, img, x,y):
        self.board.blit(img, (x,y))

    def updatePlayerLocationsOnBoard(self):
        '''
        updates the game board to properly display where the
        players currently are
        Works by making a list of the characters symbols and then padding to the desired size
        '''

        self.board.blit(boardimg,(0,0))

        for room in self.rooms:
            layer = 30
            coords = self.abs_pos[room.getRoomType()]
            x = coords['x'] - layer
            y = coords['y'] 


            players_inside = room.getPlayers()
            for player in players_inside:
                self.avatarposx[str(player)] = x
                self.avatarposy[str(player)] = y
                x += layer

                self.board.blit(images[str(player)], (self.avatarposx[str(player)] + 15, self.avatarposy[str(player)] + 40))

    def getPlayerRoom(self, player):
        for room in self.rooms:
            if player in room.getPlayers():
                return room
        print('ERROR: Player was in none of the rooms')
        exit()

    def updatePlayerPos(self, player, room):
        '''
        This function simply puts the player in a new place without checking,
        having assumed that the host checked before sending the message that
        triggers this update
        '''
        curRoom = self.getPlayerRoom(player)
        curRoom.removePlayer(player)
        room = self.rooms[room]
        room.addPlayer(player)

    def movePlayer(self, player, action):
        '''
        This function validates a move and is generally only used by the host
        '''
        oldRoom = self.getPlayerRoom(player)
        global allowedMoves, roomAdjacencies
        # print(oldRoom.getRoomType())
        
        canMove = True
        newRoom = None # scope this
        # move validation
        if action not in Room.allowedMoves[oldRoom.getRoomType()]: # move is a valid direction?
            canMove = False
        else: # if it is valid direction
            newRoom = self.rooms[Room.roomAdjacencies[oldRoom.getRoomType()][action]] #lol kinda disgusting but whatever
            if newRoom.getRoomType() > Room.RoomType.MAX_ROOM and newRoom.getPlayers(): # is the hallway already occupied?
                canMove = False
        
        if canMove:
            newRoom.addPlayer(player)
            oldRoom.removePlayer(player)
            return True
        else:
            # prints on server
            # print("invalid move") # invalid move message - real message sent in Main.py
            return False

    def getWeapons(self):
        '''
        This function just returns a list of all weapons held by the Board instance.
        '''
        return self.weapons

    def getRooms(self):
        '''
        This function just returns a list of all rooms held by the Board instance.
        '''
        return self.rooms

    def getWeaponRoom(self, weapon):
        for room in self.rooms:
            #print(str(weapon) + " : " + str(room.getWeapons()))
            if weapon in room.getWeapons():
                return room
        print('ERROR: Weapon was in none of the rooms')
        exit()