import Room
import os

class Board:

    def __init__(self):
        # Creates a brand new, blank board data structure.
        self.rooms = [Room.Room(roomType) for roomType in Room.RoomType]
        self.board = []

        self.room_empty =    '|            |----------|            |----------|            |\n'
        self.room_r1 = '|    Study   |----------|    Hall    |----------|   Lounge   |\n'
        self.room_r2 = '|   Library  |----------|  Billiard  |----------|   Dining   |\n'
        self.room_r3 = '|Conservatory|----------|  Ballroom  |----------|   Kitchen  |\n'
        self.room_tb = '|            |          |            |          |            |\n'
        self.room_secret = '|           >|          |            |          |<           |\n'
        self.hallway = '      | |                     | |                     | |    \n'

        self.board.append(self.room_tb)
        self.board.append(self.room_r1)
        self.board.append(self.room_tb)#2
        self.board.append(self.room_empty)
        self.board.append(self.room_secret)
        self.board.append(self.hallway)
        self.board.append(self.hallway)
        self.board.append(self.hallway)
        self.board.append(self.room_tb)
        self.board.append(self.room_r2)
        self.board.append(self.room_tb) #10
        self.board.append(self.room_empty)
        self.board.append(self.room_tb)
        self.board.append(self.hallway)
        self.board.append(self.hallway)
        self.board.append(self.hallway)
        self.board.append(self.room_secret)
        self.board.append(self.room_r3)
        self.board.append(self.room_tb) #18
        self.board.append(self.room_empty)
        self.board.append(self.room_tb)

    def draw(self):
        fullboard = ''
        print(fullboard)
        for item in self.board:
            #print(item)
            fullboard += item
        print(fullboard)

    def updatePlayerLocationsOnBoard(self):
        '''
        updates the game board to properly display where the
        players currently are
        Works by making a list of the characters symbols and then padding to the desired size
        #TODO: make this work for hallways as well
        '''
        spacer = '|'
        for i in range(3):
            idx = 2 + 8*i
            self.board[idx] = '|'
            for j in range(3):
                playerString = ' '
                for player in self.rooms[3*i+j].getPlayers():
                    playerString += str(player) + ' '
                self.board[idx] += str.center(playerString,12)
                self.board[idx] += spacer
                if (j<2):
                    playerString = ' '
                    for player in self.rooms[5*i+10+j].getPlayers():
                        playerString += str(player) + ' '
                    self.board[idx] += str.center(playerString,10)
                    self.board[idx] += spacer
            self.board[idx] += '\n'

        spacer = '|                     |'
        for i in range(2):
            idx = 6 + 8*i
            self.board[idx] = '      |'
            for j in range(3):
                playerString = ''
                playerInHallway = False
                for player in self.rooms[5*i+12+j].getPlayers():
                    playerString += str(player)
                    playerInHallway = True
                if (playerInHallway):
                    self.board[idx] += playerString
                else:
                    self.board[idx] += ' '
                if(j<2):
                    self.board[idx] += spacer
                else:
                    self.board[idx] += '|'
            self.board[idx] += '\n'

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
        room = self.getPlayerRoom(player) #need to write this still
        roomTemp = room
        global allowedMoves, roomAdjacencies
        print(room.getRoomType())
        if action in Room.allowedMoves[room.getRoomType()]:
            newRoomType = Room.roomAdjacencies[room.getRoomType()][action]
            for room in self.rooms:
                if room.getRoomType() == newRoomType:
                    if(newRoomType>=10) and (room.getPlayers() != []) :
                        print("invalid move")
                        return False
                    else:
                        room.addPlayer(player)
                        roomTemp.removePlayer(player)                                 
                        return True
        else:
            print("invalid move") # invalid move message - integrate with other messaging
            return False