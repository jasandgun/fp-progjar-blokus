"""
Constants for Blokus
"""

# enable debugging (print to console)
ENABLE_VERBOSE = 1

# enable audio (false for mute)
ENABLE_AUDIO = False
MUSIC_MENU = './static/assets/audio/music-game.mp3'
SOUND_NEGATIVE = './static/assets/audio/sound-negative.wav'

# colors that are used
COLORS = {
    "BLACK": [0, 0, 0],
    "WHITE": [255, 255, 255],
    "RED": [255, 0, 0],
    "GREEN": [0, 255, 0],
    "BLUE": [0, 0, 255],
    "PURPLE": [128, 0, 128],
    "ORANGE": [255, 128, 0],
    "NAVY": [0, 128, 128],
}

# board size (rows x columns)
ROW_COUNT = 14
COLUMN_COUNT = 14

# window properties
CLIENT_CAPTION = "Blokus Client"
SERVER_CAPTION = "Blokus Server"
WINDOW_ICON = "./static/assets/img/blokus-icon.png"

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
HUMAN_PARAMS = {"default_p1": {"color": COLORS["PURPLE"]},
                "default_p2": {"color": COLORS["ORANGE"]}}

# pickle identifiers
BOARD_ID = "board-pickle"
PLAYER_ID = "player-pickle"
