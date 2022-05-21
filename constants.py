# Declare constants to be used in other programs

#Developer options for debugging
VERBOSITY = 1

#Color RGB
BLACK  = [0, 0, 0]
WHITE  = [255, 255, 255]
GREEN  = [0, 255, 0]
RED    = [255, 60, 0]
PURPLE = [128, 0, 128]
ORANGE = [255, 169, 0]

#Board size
ROW_COUNT = 14
COLUMN_COUNT = 14

#89 is the total no. of squares in all 21 pieces
STARTING_SCORE = 89

#Window size 16:9
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_SIZE = [WINDOW_WIDTH, WINDOW_HEIGHT]

#The empty squares on the board shall be populated by this value
BOARD_FILL_VALUE = 0

#All squares corresponding to player 1 & 2 on the board shall be populated by these values
PLAYER1_VALUE = 1
PLAYER2_VALUE = 2

#Players need to place their initial moves on the following board coordinates
STARTING_PTS = {"player1" : [0,0],
                "player2" : [ROW_COUNT-1,COLUMN_COUNT-1]}

HUMAN_PARAMS = {"default_p1" : {"color" : PURPLE},
                "default_p2" : {"color" : ORANGE}}