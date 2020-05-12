import Player
from enum import IntEnum

class WeaponType(IntEnum):
    #Weapons
    ROPE = 0
    LEAD_PIPE = 1
    KNIFE = 2
    WRENCH = 3
    CANDLESTICK = 4
    REVOLVER = 5
    # MAX_WEAPON = 6

class RoomType(IntEnum):
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
    H_HALL_LOUNGE = 11
    H_LOUNGE_HALL = 11
    H_STUDY_LIBRARY = 12
    H_LIBRARY_STUDY = 12
    H_HALL_BILLIARD_ROOM = 13
    H_BILLIARD_ROOM_HALL = 13
    H_LOUNGE_DINING_ROOM = 14
    H_DINING_ROOM_LOUNGE = 14
    H_LIBRARY_BILLIARD_ROOM = 15
    H_BILLIARD_ROOM_LIBRARY = 15
    H_BILLIARD_ROOM_DINING_ROOM = 16
    H_DINING_ROOM_BILLIARD_ROOM = 16
    H_LIBRARY_CONSERVATORY = 17
    H_CONSERVATORY_LIBRARY = 17
    H_BILLIARD_ROOM_BALL_ROOM = 18
    H_BALL_ROOM_BILLIARD_ROOM = 18
    H_DINING_ROOM_KITCHEN = 19
    H_KITCHEN_DINING_ROOM = 19
    H_CONSERVATORY_BALL_ROOM = 20
    H_BALL_ROOM_CONSERVATORY = 20
    H_BALL_ROOM_KITCHEN = 21
    H_KITCHEN_BALL_ROOM = 21

    #HOMESQUARES
    MIN_START = 22
    GREEN_HS = 23
    MUSTARD_HS = 24
    SCARLET_HS = 25
    PLUM_HS = 26
    WHITE_HS = 27
    PEACOCK_HS = 28

roomAdjacencies = {
    22: {},
    23: {'up':RoomType.H_CONSERVATORY_BALL_ROOM },
    24: {'left':RoomType.H_DINING_ROOM_LOUNGE },
    25: {'down':RoomType.H_HALL_LOUNGE},
    26: {'right':RoomType.H_STUDY_LIBRARY },
    27: {'up':RoomType.H_BALL_ROOM_KITCHEN },
    28: {'right':RoomType.H_LIBRARY_CONSERVATORY },
    
    0: {'right':RoomType.H_STUDY_HALL, 'down':RoomType.H_STUDY_LIBRARY, 'secret':RoomType.KITCHEN},
    1: {'down': RoomType.H_HALL_BILLIARD_ROOM, 'right': RoomType.H_HALL_LOUNGE, 'left': RoomType.H_HALL_STUDY,},
    2: {'down': RoomType.H_LOUNGE_DINING_ROOM, 'left': RoomType.H_LOUNGE_HALL, 'secret': RoomType.CONSERVATORY },
    3: {'up': RoomType.H_LIBRARY_STUDY, 'down': RoomType.H_LIBRARY_CONSERVATORY, 'right': RoomType.H_LIBRARY_BILLIARD_ROOM },
    4: {'down': RoomType.H_BILLIARD_ROOM_BALL_ROOM, 'right': RoomType.H_BILLIARD_ROOM_DINING_ROOM, 'up': RoomType.H_BILLIARD_ROOM_HALL, 'left': RoomType.H_BILLIARD_ROOM_LIBRARY },
    5: {'left': RoomType.H_DINING_ROOM_BILLIARD_ROOM, 'down': RoomType.H_DINING_ROOM_KITCHEN, 'up': RoomType.H_DINING_ROOM_LOUNGE },
    6: {'right': RoomType.H_CONSERVATORY_BALL_ROOM, 'up': RoomType.H_CONSERVATORY_LIBRARY, 'secret': RoomType.LOUNGE },
    7: {'left': RoomType.H_BALL_ROOM_CONSERVATORY, 'right': RoomType.H_BALL_ROOM_KITCHEN, 'up': RoomType.H_BALL_ROOM_BILLIARD_ROOM },
    8: {'left': RoomType.H_KITCHEN_BALL_ROOM, 'up': RoomType.H_KITCHEN_DINING_ROOM, 'secret': RoomType.STUDY },
    9: {},

    #HALLWAYS
    10: {'left': RoomType.STUDY, 'right': RoomType.HALL },
    11: {'right': RoomType.LOUNGE, 'left': RoomType.HALL },
    12: {'up': RoomType.STUDY, 'down': RoomType.LIBRARY },
    13: {'up': RoomType.HALL, 'down': RoomType.BILLIARD_ROOM },
    14: {'up': RoomType.LOUNGE, 'down': RoomType.DINING_ROOM },
    15: {'left': RoomType.LIBRARY, 'right': RoomType.BILLIARD_ROOM },
    16: {'left': RoomType.BILLIARD_ROOM, 'right': RoomType.DINING_ROOM },
    17: {'up': RoomType.LIBRARY, 'down': RoomType.CONSERVATORY },
    18: {'up': RoomType.BILLIARD_ROOM, 'down': RoomType.BALL_ROOM },
    19: {'up': RoomType.DINING_ROOM, 'down': RoomType.KITCHEN },
    20: {'left': RoomType.CONSERVATORY, 'right': RoomType.BALL_ROOM },
    21: {'left': RoomType.BALL_ROOM, 'right': RoomType.KITCHEN}
       
}

allowedMoves = {
    22: [],
    23: ['up'],
    24: ['left'],
    25: ['down'],
    26: ['right'],
    27: ['up'],
    28: ['right'],
    
    0: ['right','down','secret'],
    1: ['right','down','left'],
    2: ['left', 'down', 'secret'],
    3: ['right','down', 'up'],
    4: ['right','down', 'up', 'left'],
    5: ['up', 'left', 'down'],
    6: ['up', 'right', 'secret'],
    7: ['right','left', 'up'],
    8: ['left', 'up', 'secret'],
    9: [],

    #HALLWAYS
    10: ['left', 'right'],
    11: ['left', 'right'],
    12: ['up', 'down'],
    13: ['up', 'down'],
    14: ['up', 'down'],
    15: ['left', 'right'],
    16: ['left', 'right'],
    17: ['up', 'down'],
    18: ['up', 'down'],
    19: ['up', 'down'],
    20: ['left', 'right'],
    21: ['left', 'right'],

    #ROOMS
    'MIN_START': [],
    'GREEN_HS': ['up'],
    'MUSTARD_HS': ['left'],
    'SCARLET_HS':['down'],
    'PLUM_HS':['right'],
    'WHITE_HS':['up'],
    'PEACOCK_HS':['right'],
    
    'STUDY': ['right','down','secret'],
    'HALL': ['right','down','left'],
    'LOUNGE': ['left', 'down', 'secret'],
    'LIBRARY': ['right','down', 'up'],
    'BILLIARD_ROOM': ['right','down', 'up', 'left'],
    'DINING_ROOM': ['up', 'left', 'down'],
    'CONSERVATORY': ['up', 'right', 'secret'],
    'BALL_ROOM': ['right','down', 'up'],
    'KITCHEN': ['left', 'up', 'secret'],
    'MAX_ROOM': [],

    #HALLWAYS
    'H_STUDY_HALL': ['up', 'down'],
    'H_HALL_STUDY': ['up', 'down'],
    'H_STUDY_LIBRARY': ['up', 'down'],
    'H_LIBRARY_STUDY': ['up', 'down'],
    'H_HALL_LOUNGE': ['left', 'right'],
    'H_LOUNGE_HALL': ['left', 'right'],
    'H_HALL_BILLIARD_ROOM': ['up', 'down'],
    'H_BILLIARD_ROOM_HALL': ['up', 'down'],
    'H_LOUNGE_DINING_ROOM': ['up', 'down'],
    'H_DINING_ROOM_LOUNGE': ['up', 'down'],
    'H_LIBRARY_BILLIARD_ROOM': ['left', 'right'],
    'H_BILLIARD_ROOM_LIBRARY': ['left', 'right'],
    'H_LIBRARY_CONSERVATORY': ['up', 'down'],
    'H_CONSERVATORY_LIBRARY': ['up', 'down'],
    'H_BILLIARD_ROOM_BALL_ROOM': ['up', 'down'],
    'H_ROOM_BALL_ROOM_BILLIARD': ['up', 'down'],
    'H_BILLIARD_ROOM_DINING_ROOM': ['left', 'right'],
    'H_DINING_ROOM_BILLIARD_ROOM': ['left', 'right'],
    'H_DINING_ROOM_KITCHEN': ['up', 'down'],
    'H_KITCHEN_DINING_ROOM': ['up', 'down'],
    'H_CONSERVATORY_BALL_ROOM': ['left', 'right'],
    'H_BALL_ROOM_CONSERVATORY': ['left', 'right'],
    'H_BALL_ROOM_KITCHEN': ['left', 'right'],
    'H_KITCHEN_BALL_ROOM': ['left', 'right'],
}


class Room:
    def __init__(self, roomType = None):
        self.roomType = roomType

        if roomType < RoomType.MAX_ROOM or roomType > RoomType.MIN_START:
            self.isRoom = True
        else:
            self.isRoom = False
        self.weapons = []
        self.players = []

    def getRoomType(self):
        return self.roomType

    def getPlayers(self):
        return self.players

    def getWeapons(self):
        return self.weapons

    def addPlayer(self, player):
        # print('adding ' + str(player) + ' to ' + str(self.roomType))
        self.players.append(player)

    def addWeapon(self, weapon):
        self.weapons.append(weapon)

    def removePlayer(self, player):
        self.players.remove(player)

    def removeWeapon(self, weapon):
        self.weapons.remove(weapon)
