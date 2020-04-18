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
        spacer = '|          |'
        for i in range(3):
            idx = 2 + 8*i
            self.board[idx] = '|'
            for j in range(3):
                playerString = ' '
                for player in self.rooms[3*i+j].getPlayers():
                    playerString += str(player) + ' '
                self.board[idx] += str.center(playerString,12)
                self.board[idx] += spacer
            self.board[idx] += '\n'

    def getPlayerRoom(self, player):
        for room in self.rooms:
            if player in room.getPlayers():
                return room
        print('ERROR: Player was in none of the rooms')
        exit()

    def movePlayer(self, player, action):
        room = self.getPlayerRoom(player) #need to write this still
        global allowedMoves, roomAdjacencies
        print(room.getRoomType())
        if action in Room.allowedMoves[room.getRoomType()]:
            room.removePlayer(player)
            newRoomType = Room.roomAdjacencies[room.getRoomType()][action]
            for room in self.rooms:
                if room.getRoomType() == newRoomType:
                    room.addPlayer(player)
                    break
        else:
            print("invalid move") # invalid move message - integrate with other messaging