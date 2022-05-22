"""
Logic related to board
"""

import numpy as np

import constants

empty = constants.BOARD_FILL_VALUE
rows = constants.ROW_COUNT
cols = constants.COLUMN_COUNT


class Board:
    def __init__(self):
        self.board = np.array([[empty for i in range(rows)] for j in range(cols)])
        self.turn_number = 1

    def fit_piece(self, piece, player, opponent_player, mode="player"):
        piece_x_rng = range(piece["arr"].shape[0])
        piece_y_rng = range(piece["arr"].shape[1])
        board_x_rng = range(piece["place_on_board_at"][0], rows)
        board_y_rng = range(piece["place_on_board_at"][1], cols)

        if player.is_1st_move:
            if player.number == constants.PLAYER1_VALUE:
                pos = constants.STARTING_PTS["player1"]
            elif player.number == constants.PLAYER2_VALUE:
                pos = constants.STARTING_PTS["player2"]

            is_within_starting_pos = False
            for i, x in zip(piece_x_rng, board_x_rng):
                for j, y in zip(piece_y_rng, board_y_rng):
                    if [x, y] == pos and piece["arr"][i][j] == 1:
                        is_within_starting_pos = True
            if is_within_starting_pos:
                for i, x in zip(piece_x_rng, board_x_rng):
                    for j, y in zip(piece_y_rng, board_y_rng):
                        if piece["arr"][i][j] == 1 and self.board[x][y] == empty:
                            self.board[x][y] = player.number * piece["arr"][i][j]
            else:
                if constants.VERBOSITY > 0:
                    print("Piece %s placed at %s wasn't fit in the 1st turn" \
                          % (piece["piece"], piece["place_on_board_at"]))
                return False
            # When an AI like Minimax iterates through all possible moves,send mode="ai"
            # to avoid this parameter being set to False
            if mode == "player":
                player.is_1st_move = False
        else:
            if self.check_is_move_valid(piece["arr"], player, piece["place_on_board_at"]):
                for i, x in zip(piece_x_rng, board_x_rng):
                    for j, y in zip(piece_y_rng, board_y_rng):
                        if piece["arr"][i][j] == 1:
                            self.board[x][y] = player.number * piece["arr"][i][j]
            else:
                if constants.VERBOSITY > 0:
                    print("In fit_piece, a move with piece %s turned out to be invalid" % (piece))
                return False
        if constants.VERBOSITY > 0 and not player.is_ai:
            print("Piece that was successfully fit:", piece)
        player.discard_piece(piece)
        player.empty_current_piece()
        self.turn_number += 1
        player.turn_number += 1
        player.update_score()
        if constants.VERBOSITY > 0:
            print("After turn number %s board is:\n %s" % (self.turn_number - 1, self.board))
            print("Current player's (Player %s) score is: %s and opponent's (Player %s) score is: %s" % \
                  (player.number, player.score, opponent_player.number, opponent_player.score))
        # self.update_board_corners(player, opponent_player)
        self.optimised_update_board_corners(piece, player, opponent_player)
        return True


def scoring_fn(remaining_pieces):
    score = constants.STARTING_SCORE
    if len(remaining_pieces) == 0:
        score += 15
    else:
        for _, val in remaining_pieces.items():
            for i in range(val["arr"].shape[0]):
                for j in range(val["arr"].shape[1]):
                    if val["arr"][i][j] == 1:  # 1 means 1 unit sq of that piece
                        score -= 1
    # If the last pc played is the 1 unit sq pc, we get extra 5 pts
    if len(remaining_pieces) == 1 and "piece1" in remaining_pieces and score == 88:
        score += 5
    return score


