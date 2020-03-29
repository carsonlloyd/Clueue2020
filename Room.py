import Player
from enum import IntEnum

class RoomName(IntEnum):
    #ROOMS
    STUDY = 0
    HALL = 1
    LOUNGE = 2
    LIBRARY = 3
    BILLIARD_ROOM = 4
    DINING_ROOM = 5
    CONSERVATORY = 6
    BALL_ROOM = 7
    KITCHEN = 8
    MAX_ROOM = 9 #ignore this value, just happened to be a nice thing to compare with

    #HALLWAYS
    H_STUDY_HALL = 10
    H_HALL_STUDY = 10
    H_STUDY_LIBRARY = 11
    H_LIBRARY_STUDY = 11
    H_HALL_LOUNGE = 12
    H_LOUNGE_HALL = 12
    H_HALL_BILLIARD_ROOM = 13
    H_BILLIARD_ROOM_HALL = 13
    H_LOUNGE_DINING_ROOM = 14
    H_DINING_ROOM_LOUNGE = 14
    H_LIBRARY_BILLIARD_ROOM = 15
    H_BILLIARD_ROOM_LIBRARY = 15
    H_LIBRARY_CONSERVATORY = 16
    H_CONSERVATORY_LIBRARY = 16
    H_BILLIARD_ROOM_BALL_ROOM = 17
    H_ROOM_BALL_ROOM_BILLIARD = 17
    H_BILLIARD_ROOM_DINING_ROOM = 18
    H_DINING_ROOM_BILLIARD_ROOM = 18
    H_DINING_ROOM_KITCHEN = 19
    H_KITCHEN_DINING_ROOM = 19
    H_CONSERVATORY_BALL_ROOM = 20
    H_BALL_ROOM_CONSERVATORY = 20
    H_BALL_ROOM_KITCHEN = 21
    H_KITCHEN_BALL_ROOM = 21



class Room:
    def __init__(self, roomName = None):
        self.roomName = roomName
        if roomName < RoomName.MAX_ROOM:
            self.isRoom = True
        else:
            self.isRoom = False
        self.weapons = []
        self.players = []

    def getPlayers(self):
        return self.players

    def getWeapons(self):
        return self.weapons

    def addPlayer(self, player):
        print('adding ' + str(player) + ' to ' + str(self.roomName))
        self.players.append(player)

    def addWeapon(self, weapon):
        self.weapons.append(player)

    def removePlayer(self, player):
        self.players.remove(player)

    def removeWeapon(self, weapon):
        self.weapons.remove(player)

    def draw(self):
        '''
        In the GUI, each element will draw itself to the game board.
        #TODO: For the time being, this will be non-functional as it
                is easier to draw things monolithically in the terminal
        '''
        pass