"""
Constants for Blokus
"""

# enable debugging (print to console)
ENABLE_VERBOSE = 1

# colors that are used
DICT_COLORS = {
    0: [0, 0, 0],  # BLACK
    1: [255, 255, 255],  # WHITE
    2: [255, 0, 0],  # RED
    3: [0, 255, 0],  # GREEN
    4: [0, 0, 255],  # BLUE
    5: [128, 0, 128],  # PURPLE
    6: [255, 128, 0],  # ORANGE
    7: [0, 128, 128],  # NAVY
}
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GREEN = [0, 255, 0]
RED = [255, 60, 0]
PURPLE = [128, 0, 128]
ORANGE = [255, 169, 0]

# board size (rows x columns)
ROW_COUNT = 14
COLUMN_COUNT = 14

# window properties
CLIENT_CAPTION = "Blokus Client"
SERVER_CAPTION = "Blokus Server"
WINDOW_ICON = "../static/assets/blokus-icon.png"

# total number of squares in all pieces
STARTING_SCORE = 89

# game window specification
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_SIZE = [WINDOW_WIDTH, WINDOW_HEIGHT]

# value for empty squares
BOARD_FILL_VALUE = 0

# value for player-populated squares
PLAYER1_VALUE = 1
PLAYER2_VALUE = 2

# starting points for players
STARTING_PTS = {"player1": [0, 0],
                "player2": [ROW_COUNT - 1, COLUMN_COUNT - 1]}

# colors for players
HUMAN_PARAMS = {"default_p1": {"color": DICT_COLORS[5]},
                "default_p2": {"color": DICT_COLORS[6]}}

# pickle identifiers
BOARD_ID = "board-pickle"
PLAYER_ID = "player-pickle"
