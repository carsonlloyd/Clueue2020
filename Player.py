
class Player():
    def __init__(self, name = None):
        self.location = None
        self.name = name

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

    def setRoom(self, room):
        '''
        Sets the players location to the room/hallway they are in
        @suggest Should move logic go here?
        @param room  The room the player is moving to
        @return N/A
        '''


