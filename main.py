import time

def getInput(elapsedTime):
    '''
    Gather inputs and either send them as messages to the host
    or process the messages given to you as the host and arrange
    them into their sequence and relevance.
    Input messages from players whose turn it is not will be ignored
    '''
    pass

def update(elapsedTime):
    '''
    Processing inputs and updates game state according to the rules
    of the game.

    For clients they will receive the master game state update message
    and update their state accordingly
    '''
    pass

def render(elapsedTime):
    '''
    Using the state of the game, this function will handle all drawing
    and graphical output to the screen.

    The host logic will disregard this function
    '''
    pass


def main():
    '''
    Main loop of the game.
    getInput will take user inputs (or process the input messages as host)
    Update will change the game state (or process state update message as client)
    Render will draw all graphical items based on that state (no render for host)
    '''
    prevTime = time.time()
    while True:
        curTime = time.time()
        elapsedTime = curTime - prevTime
        prevTime = curTime
        getInput(elapsedTime)
        update(elapsedTime)
        render(elapsedTime)

if __name__ == "__main__":
    main()
