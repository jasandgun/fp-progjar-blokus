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
        self.board = np.array([[empty for _ in range(rows)] for _ in range(cols)])
        self.turn_number = 1
        self.pickle_identifier = constants.BOARD_ID

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
            if is_within_starting_pos and self.check_1st_move(piece["arr"], player, piece["place_on_board_at"]):
                for i, x in zip(piece_x_rng, board_x_rng):
                    for j, y in zip(piece_y_rng, board_y_rng):
                        if piece["arr"][i][j] == 1 and self.board[x][y] == empty:
                            self.board[x][y] = player.number * piece["arr"][i][j]
            else:
                if constants.ENABLE_VERBOSE > 0:
                    print("Piece %s placed at %s wasn't fit in the 1st turn"
                          % (piece["piece"], piece["place_on_board_at"]))
                return False
            if mode == "player":
                player.is_1st_move = False
        else:
            if self.check_is_move_valid(piece["arr"], player, piece["place_on_board_at"]):
                for i, x in zip(piece_x_rng, board_x_rng):
                    for j, y in zip(piece_y_rng, board_y_rng):
                        if piece["arr"][i][j] == 1:
                            self.board[x][y] = player.number * piece["arr"][i][j]
            else:
                if constants.ENABLE_VERBOSE > 0:
                    print("In fit_piece, a move with piece %s turned out to be invalid" % piece)
                return False
        if constants.ENABLE_VERBOSE > 0 and not player.is_1st_move:
            print("Piece that was successfully fit:", piece)
        player.discard_piece(piece)
        player.empty_current_piece()
        self.turn_number += 1
        player.turn_number += 1
        player.update_score()
        if constants.ENABLE_VERBOSE > 0:
            print("After turn number %s board is:\n %s" % (self.turn_number - 1, self.board))
            print("Current player's (Player %s) score is: %s and opponent's (Player %s) score is: %s" %
                  (player.number, player.score, opponent_player.number, opponent_player.score))
        # self.update_board_corners(player, opponent_player)
        # self.optimised_update_board_corners(piece, player, opponent_player)
        return True

    def check_is_move_valid(self, piece_arr, player, piece_on_board_at):
        piece_x_rng = range(piece_arr.shape[0])
        piece_y_rng = range(piece_arr.shape[1])
        board_x_rng = range(piece_on_board_at[0], rows)
        board_y_rng = range(piece_on_board_at[1], cols)
        piece_block = 0
        piece_count = 0
        for i in piece_x_rng:
            for j in piece_y_rng:
                if piece_arr[i][j] == 1:
                    piece_block += 1
        for i, x in zip(piece_x_rng, board_x_rng):
            for j, y in zip(piece_y_rng, board_y_rng):
                if piece_arr[i][j] == 1:
                    piece_count += 1
                    if self.board[x][y] != constants.BOARD_FILL_VALUE:
                        return False
                    if x - 1 >= 0:
                        if self.board[x - 1][y] == player.number:
                            return False
                    if x + 1 < rows:
                        if self.board[x + 1][y] == player.number:
                            return False
                    if y - 1 >= 0:
                        if self.board[x][y - 1] == player.number:
                            return False
                    if y + 1 < cols:
                        if self.board[x][y + 1] == player.number:
                            return False
        if piece_count != piece_block:
            return False
        # print(f"\nactual : %d\nturn out: %d" % (piece_block, piece_count))
        for i, x in zip(piece_x_rng, board_x_rng):
            for j, y in zip(piece_y_rng, board_y_rng):
                if piece_arr[i][j] == 1:
                    if x - 1 >= 0:
                        if y - 1 >= 0:
                            if self.board[x - 1][y - 1] == player.number:
                                return True
                        if y + 1 < cols:
                            if self.board[x - 1][y + 1] == player.number:
                                return True
                    if x + 1 < rows:
                        if y - 1 >= 0:
                            if self.board[x + 1][y - 1] == player.number:
                                return True
                        if y + 1 < cols:
                            if self.board[x + 1][y + 1] == player.number:
                                return True
        return False

    def check_1st_move(self, piece_arr, player, piece_on_board_at):
        piece_x_rng = range(piece_arr.shape[0])
        piece_y_rng = range(piece_arr.shape[1])
        board_x_rng = range(piece_on_board_at[0], rows)
        board_y_rng = range(piece_on_board_at[1], cols)
        piece_block = 0
        piece_count = 0
        for i in piece_x_rng:
            for j in piece_y_rng:
                if piece_arr[i][j] == 1:
                    piece_block += 1
        for i, x in zip(piece_x_rng, board_x_rng):
            for j, y in zip(piece_y_rng, board_y_rng):
                if piece_arr[i][j] == 1:
                    piece_count += 1
                    if self.board[x][y] != constants.BOARD_FILL_VALUE:
                        return False
                    if x - 1 >= 0:
                        if self.board[x - 1][y] == player.number:
                            return False
                    if x + 1 < rows:
                        if self.board[x + 1][y] == player.number:
                            return False
                    if y - 1 >= 0:
                        if self.board[x][y - 1] == player.number:
                            return False
                    if y + 1 < cols:
                        if self.board[x][y + 1] == player.number:
                            return False
        if piece_count != piece_block:
            return False
        # print(f"\nactual : %d\nturn out: %d" % (piece_block, piece_count))
        return True

    def is_no_more_move(self, player):
        remaining_piece = player.remaining_pieces
        piece = {"piece": "", "arr": [], "rotated": 0, "flipped": 0, "rects": [], "place_on_board_at": []}
        for key, val in remaining_piece.items():
            for x in range(rows):
                for y in range(cols):
                    #normal state
                    piece["arr"] = player.remaining_pieces[key]["arr"]
                    board_arr_coords = [x, y]
                    j = 0
                    while not piece["arr"][0][j] == 1:
                        j += 1
                    board_arr_coords[1] -= j
                    piece["place_on_board_at"] = board_arr_coords
                    if self.check_is_move_valid(piece['arr'], player, piece['place_on_board_at']):
                        print(f"\nValid move %s at %d,%d" % (key, x, y))
                        return False
                    #rotated state
                    for z in range(player.remaining_pieces[key]["rots"]-1):
                        piece["arr"] = np.rot90(piece["arr"], k=1)
                        board_arr_coords = [x, y]
                        j = 0
                        while not piece["arr"][0][j] == 1:
                            j += 1
                        board_arr_coords[1] -= j
                        piece["place_on_board_at"] = board_arr_coords
                        if self.check_is_move_valid(piece['arr'], player, piece['place_on_board_at']):
                            print(f"\nValid move %s at %d,%d" % (key, x, y))
                            return False
                    piece["arr"] = np.rot90(piece["arr"], k=1)
                    for z in range(player.remaining_pieces[key]["flips"]-1):
                        piece["arr"] = np.flipud(piece["arr"], k=1)
                        board_arr_coords = [x, y]
                        j = 0
                        while not piece["arr"][0][j] == 1:
                            j += 1
                        board_arr_coords[1] -= j
                        piece["place_on_board_at"] = board_arr_coords
                        if self.check_is_move_valid(piece['arr'], player, piece['place_on_board_at']):
                            print(f"\nValid move %s at %d,%d" % (key, x, y))
                            return False
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
