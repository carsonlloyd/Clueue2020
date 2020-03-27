class BasicMobility():
    def drawBoard(board):
        for item in range(len(board)):
            row = ''.join(board[item])
            print(row)


    def getNewBoard():
        # Creates a brand new, blank board data structure.
        board = []
        for i in range(21):
             board.append([' '] * 62)

        room =    '|            |----------|            |----------|            |'
        room_r1 = '|    Study   |          |    Hall    |          |   Lounge   |'
        room_r2 = '|   Library  |          |   Billiard |          |   Dining   |'
        room_r3 = '|Conservatory|          |   Ballroom |          |   Kitchen  |'
        room_tb = '|            |          |            |          |            |'
        room_secret = '|           >|          |            |          |<           |'
        hallway = '      | |                     | |                     | |    ' 

        board[0][0:62] = room_r1
        board[1][0:62] = room
        board[2][0:62] = room_tb
        board[3][0:62] = room
        board[4][0:62] = room_secret
        board[5][0:62] = hallway
        board[6][0:62] = hallway
        board[7][0:62] = hallway
        board[8][0:62] = room_r2
        board[9][0:62] = room
        board[10][0:62] = room_tb
        board[11][0:62] = room
        board[12][0:62] = room_tb
        board[13][0:62] = hallway
        board[14][0:62] = hallway
        board[15][0:62] = hallway
        board[16][0:62] = room_secret
        board[17][0:62] = room
        board[18][0:62] = room_tb
        board[19][0:62] = room
        board[20][0:62] = room_r3

        return board

    def homestate(players, board):
        #Definites the starting state of each player if they are in the game.
        homeboard = board
        if 'Col. Mustard' in players:
            homeboard[6][55] = 'M'
        if 'Miss Scarlet' in players:
            homeboard[2][43] = 'S'
        if 'Prof. Plum' in players:
            homeboard[6][7] = 'P'
        if 'Mrs. Peacock' in players:
            homeboard[14][7] = 'C'
        if 'Mr. Green' in players:
            homeboard[18][19] = 'G'
        if 'Mrs. White' in players:
            homeboard[18][43] = 'W'
        return homeboard

    def getPlayerPosition(player):
        # Used to identify where the player is on the board
        # find based on player image (G,W,C,P,S,M) on the board and return index in array
        return player

    def move_player(board, player, movement):
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