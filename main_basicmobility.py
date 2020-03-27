print('Welcome to Clueless! \n')

# Insert player choices here

from BasicMobility import drawBoard
#while True:
# Reset the board and game.
mainBoard = BasicMobility.getNewBoard()

#This list changes based on user input
players = ['Col. Mustard', 'Miss Scarlet', 'Prof. Plum', 'Mrs. Peacock',
          'Mr. Green', 'Mrs. White', 'Test']
if len(players) >0:
    homeboard =  BasicMobility.homestate(players,mainBoard)
    drawBoard(homeboard)
else:
    drawBoard(mainBoard)

#duplicate homeboard to board that will change with each turn
playboard = homeboard
    
#while turns are in motion  -- while statement here
# variable 'move' is from player input based on cardinal directions north, south, east, west, northeast, northwest, southeast, southwest
move = 'northeast'
turnMade = BasicMobility.move_player(playboard, 'M', move)
drawBoard(playboard)