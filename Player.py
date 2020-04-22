
class Player():
    def __init__(self, name = None):
        self.location = None
        self.name = name
        self.addr = None
        self.hand = None

    def __str__(self):
        if self.name == 'Col. Mustard':
            return 'M'
        elif self.name == 'Miss Scarlet':
            return 'S'
        elif self.name == 'Prof. Plum' :
            return 'P'
        elif self.name == 'Mrs. Peacock':
            return 'C'
        elif self.name == 'Mr. Green':
            return 'G'
        elif self.name =='Mrs. White':
            return 'W'

    def __repr__(self):
        return str(self)

    def setName(self, char):
        '''
        Sets the players name, generally by  a successful connection to the host
        '''
        if char == 'M':
            self.name = 'Col. Mustard'
        elif char == 'S':
            self.name = 'Miss Scarlet'
        elif char == 'P':
            self.name = 'Prof. Plum' 
        elif char == 'C':
            self.name = 'Mrs. Peacock'
        elif char == 'G':
            self.name = 'Mr. Green'
        elif char == 'W':
            self.name = 'Mrs. White'

    def setHand(self, cards):
        self.hand = cards

    def getHand(self, hand):
        return self.hand

    def getName(self):
        return self.name