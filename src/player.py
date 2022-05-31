"""
Manage player actions and capabilities
"""

import board
import constants
import pieces
import numpy as np


class Player:
    players = [constants.PLAYER1_VALUE, constants.PLAYER2_VALUE]

    # initialize player
    def __init__(self, player_number: int, color: list):
        self.number = player_number
        self.remaining_pieces = pieces.get_pieces()
        self.discarded_pieces = []
        self.current_piece = {"piece": "", "arr": [], "rotated": 0, "flipped": 0, "rects": [], "place_on_board_at": []}
        self.color = color
        self.score = board.scoring_fn(self.remaining_pieces)
        self.turn_number = 1
        self.cant_move = False
        self.truly_cant_move = False

        # tl = top left, bl = bottom left, tr = top right, br = bottom right
        self.board_corners = {"bl": [], "br": [], "tl": [], "tr": []}
        self.is_1st_move = True if self.number == constants.PLAYER1_VALUE else False
        self.pickle_identifier = constants.PLAYER_ID

    # update player's score
    def update_score(self):
        self.score = board.scoring_fn(self.remaining_pieces)

    def update_turn(self):
        self.is_1st_move = not self.is_1st_move

    """
    Player's piece controls
    - Choose piece
    - Empty piece (change chosen piece)
    - Discard piece (remove piece after placed on board)
    - Retrieve piece (get last piece that has been discarded)
    - Rotate piece (clockwise or counterclockwise)
    - Flip piece
    """

    # Choose piece
    def set_current_piece(self, piece_name):
        self.current_piece = {"piece": piece_name, "arr": pieces.get_pieces()[piece_name]}

    # Empty piece
    def empty_current_piece(self):
        self.current_piece = {"piece": "", "arr": [], "rotated": 0, "flipped": 0, "rects": [], "place_on_board_at": []}

    # Discard piece, delete from dictionary of current pieces on the player's disposal
    def discard_piece(self, piece):
        del self.remaining_pieces[piece["piece"]]
        # append to dictionary of discarded pieces for the player
        self.discarded_pieces.append(piece)

    # Retrieve piece
    def retrieve_last_piece(self):
        piece = self.discarded_pieces[-1]
        self.remaining_pieces[piece["piece"]] = pieces.get_pieces()[piece["piece"]]
        return piece

    # Rotate piece, clockwise or counterclockwise
    def rotate_current_piece(self, clockwise=True):
        max_rots = pieces.get_pieces()[self.current_piece["piece"]]["rots"]
        current_state = self.current_piece["rotated"]
        # clockwise rotation
        if clockwise:
            if current_state == max_rots - 1:
                current_state = 0
            else:
                current_state += 1
            self.current_piece["rotated"] = current_state
            self.current_piece["arr"] = np.rot90(self.current_piece["arr"], k=1)
        # counterclockwise rotation
        else:
            if current_state == 0:
                current_state = max_rots - 1
            else:
                current_state -= 1
            self.current_piece["rotated"] = current_state
            self.current_piece["arr"] = np.rot90(self.current_piece["arr"], k=-1)

    # Flip piece diagonally
    def flip_current_piece(self):
        if not pieces.get_pieces()[self.current_piece["piece"]]["flips"] == 1:
            if self.current_piece["flipped"] == 1:
                self.current_piece["flipped"] = 0
            else:
                self.current_piece["flipped"] = 1
            self.current_piece["arr"] = np.flipud(self.current_piece["arr"])


# Switch players that is currently playing
def switch_active_player(active_player, opponent):
    if constants.ENABLE_VERBOSE > 0:
        print("Player number %d is now active" % opponent.number)
    return opponent, active_player
