"""
Manage player
"""

import board
import constants
import pieces
import numpy as np


class Player:
    players = [constants.PLAYER1_VALUE, constants.PLAYER2_VALUE]

    def __init__(self, player_number: int, color: list):
        self.number = player_number
        self.remaining_pieces = pieces.get_pieces()
        self.discarded_pieces = []
        self.current_piece = {"piece": "", "arr": [], "rotated": 0, "flipped": 0, "rects": [], "place_on_board_at": []}
        self.color = color
        self.score = board.scoring_fn(self.remaining_pieces)
        self.turn_number = 1

        # tl = top left, bl = bottom left, tr = top right, br = bottom right
        self.board_corners = {"bl": [], "br": [], "tl": [], "tr": []}
        self.is_1st_move = True

    # for rotating player's piece
    def rotate_current_piece(self, clockwise=True):
        max_rots = pieces.get_pieces()[self.current_piece["piece"]]["rots"]
        current_state = self.current_piece["rotated"]

        if clockwise:
            if current_state == max_rots - 1:
                current_state = 0
            else:
                current_state += 1
            self.current_piece["rotated"] = current_state
            self.current_piece["arr"] = np.rot90(self.current_piece["arr"], k=1)
        else:
            if current_state == 0:
                current_state = max_rots - 1
            else:
                current_state -= 1
            self.current_piece["rotated"] = current_state
            self.current_piece["arr"] = np.rot90(self.current_piece["arr"], k=-1)

    # flip current piece
    def flip_current_piece(self):
        if not pieces.get_pieces()[self.current_piece["piece"]]["flips"] == 1:
            if self.current_piece["flipped"] == 1:
                self.current_piece["flipped"] = 0
            else:
                self.current_piece["flipped"] = 1
            self.current_piece["arr"] = np.flipud(self.current_piece["arr"])
