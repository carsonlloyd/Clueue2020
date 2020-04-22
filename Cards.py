from enum import IntEnum
from random import randint, shuffle

class CardType(IntEnum):
    #rooms
    STUDY = 0
    HALL = 1
    LOUNGE = 2
    LIBRARY = 3
    BILLARD_ROOM = 4
    DINING_ROOM = 5
    CONSERVATORY = 6
    BALL_ROOM = 7
    KITCHEN = 8

    #SUSPECTS
    MUSTARD = 9
    SCARLET = 10
    PLUM = 11
    GREEN = 12
    WHITE = 13
    PEACOCK = 14

    #WEAPONS
    ROPE = 15
    LEAD_PIPE = 16
    KNIFE = 17
    WRENCH = 18
    CANDLESTICK = 19
    REVOLVER = 20

class Cards():
    def __init__(self):
        allcards = []
        for i in range(21):
            allcards.append(i)
        self.deck = allcards
    
    def CaseFile(self):
        roomnum = randint(0,8)
        suspectnum = randint(9,14)
        weaponnum = randint(15,20)
        self.case_file = {'room': CardType(roomnum).name, 'suspect': CardType(suspectnum).name, 'weapon': CardType(weaponnum).name}
        self.deck.remove(roomnum)
        self.deck.remove(suspectnum)
        self.deck.remove(weaponnum)
        
    def shufflecards(self):
        shuffle(self.deck)
        
    def deal(self, numPlayers):
        self.hands = []
        for i in range(0,numPlayers):
            temphand = self.deck[i::numPlayers]
            hand = []
            for j in temphand:
                hand.append(CardType(j).value)
            self.hands.append(hand)