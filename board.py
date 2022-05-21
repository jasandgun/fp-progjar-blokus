# To do something with board

import numpy as np
import constants, pieces

empty = constants.BOARD_FILL_VALUE
rows  = constants.ROW_COUNT
cols  = constants.COLUMN_COUNT

class Board:
    def __init__(self):
        self.board = np.array([[empty for i in range(rows)] for j in range(cols)])
        self.turn_number = 1

def scoring_fn(remaining_pieces):
    score = constants.STARTING_SCORE
    if len(remaining_pieces) == 0:
        score += 15
    else:
        for _, val in remaining_pieces.items():
            for i in range(val["arr"].shape[0]):
                for j in range(val["arr"].shape[1]):
                    if val["arr"][i][j] == 1: #1 means 1 unit sq of that piece
                        score -= 1
    # If the last pc played is the 1 unit sq pc, we get extra 5 pts
    if len(remaining_pieces) == 1 and "piece1" in remaining_pieces and score == 88:
        score += 5
    return score