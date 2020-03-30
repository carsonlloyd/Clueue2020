import Room
import os

class Board:

    def __init__(self):
        # Creates a brand new, blank board data structure.
        self.rooms = [Room.Room(roomName) for roomName in Room.RoomName]
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

    def move_player(self, board, player, movement):
        x,y = getPlayerPosition(player) #need to write this still
        board[y][x] = ' '
        if (movement == 'north') and (y > 2):
            board[y - 4][x] = player
        elif (movement == 'south') and (y < 18):
            board[y + 4][x] = player
        elif (movement == 'east') and (x < 55):
            board[y][x+12] = player
        elif (movement == 'west') and (x >7):
            board[y][x-12] = player
        elif (movement == 'northeast') and ((y >2) and (x < 55)):
            board[y-8][x + 24] = player
        elif (movement == 'northwest') and ((y >2) and (x > 7)):
            board[y-8][x - 24] = player
        elif (movement == 'southeast') and ((y < 18) and (x < 55)):
            board[y+8][x + 24] = player
        elif (movement == 'southwest') and ((y < 18) and (x > 7)):
            board[y+8][x - 24] = player
        else:
            print("invalid move") # invalid move message - integrate with other messaging
        return board
