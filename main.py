from Board import Board
from Player import Player
import time, os, random

#Globals
mainBoard = None
players = None
validInputs = ['up','down','left','right','secret','suggest','accuse']
playerNames = ['Col. Mustard','Miss Scarlet','Prof. Plum','Mrs. Peacock','Mr. Green','Mrs. White']

def initPlayers(numPlayers):
    players = [Player(playerNames[i]) for i in random.sample(range(6),numPlayers)]
    for playerIdx,roomIdx in enumerate(random.sample(range(9),numPlayers)):
        mainBoard.rooms[roomIdx].addPlayer(players[playerIdx]) #kinda bad encapsulation but thats pythons fault

def initialize():
    '''
    Initialize game board
    @suggest Connect players?

    @return a new, game board and state
    '''
    print('initializing')
    global mainBoard, players
    mainBoard = Board()

    #randomly place players
    initPlayers(4)
    mainBoard.updatePlayerLocationsOnBoard()

    

    #render inital gameboard
    render()

def getInput():
    '''
    Gather inputs and either send them as messages to the host
    or process the messages given to you as the host and arrange
    them into their sequence and relevance.
    Input messages from players whose turn it is not will be ignored
    '''
    global validInputs
    action = ''
    while action not in validInputs:
        action = input('please select an action (up, down, left, right, secret, accuse, suggest): ')



def update():
    '''
    Processing inputs and updates game state according to the rules
    of the game.

    For clients they will receive the master game state update message
    and update their state accordingly
    '''
    pass

def render():
    '''
    Using the state of the game, this function will handle all drawing
    and graphical output to the screen.

    The host logic will disregard this function
    '''
    os.system('clear')
    mainBoard.draw()
    


def main():
    '''
    Main loop of the game.
    getInput will take user inputs (or process the input messages as host)
    Update will change the game state (or process state update message as client)
    Render will draw all graphical items based on that state (no render for host)
    '''
    initialize()

    while True: #TODO: Change to while game not won
        getInput()
        update()
        render()

if __name__ == "__main__":
    main()
