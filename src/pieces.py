# To keep all game pieces. Each player has 21-piece sets
# Each set contains 21 pieces, each a different shape

import numpy as np


# returns every possible piece
def get_pieces():
    dict_pieces = {
        "piece1": {"arr": np.array([[1]]), "rots": 1, "flips": 1, "rects": []},
        "piece2": {"arr": np.array([[1], [1]]), "rots": 2, "flips": 1, "rects": []},
        "piece3": {"arr": np.array([[1], [1], [1]]), "rots": 2, "flips": 1, "rects": []},
        "piece4": {"arr": np.array([[1, 0], [1, 1]]), "rots": 4, "flips": 1, "rects": []},
        "piece5": {"arr": np.array([[1], [1], [1], [1]]), "rots": 2, "flips": 1, "rects": []},
        "piece6": {"arr": np.array([[0, 1], [0, 1], [1, 1]]), "rots": 4, "flips": 2, "rects": []},
        "piece7": {"arr": np.array([[1, 0], [1, 1], [1, 0]]), "rots": 4, "flips": 1, "rects": []},
        "piece8": {"arr": np.array([[1, 1], [1, 1]]), "rots": 1, "flips": 1, "rects": []},
        "piece9": {"arr": np.array([[1, 1, 0], [0, 1, 1]]), "rots": 2, "flips": 2, "rects": []},
        "piece10": {"arr": np.array([[1], [1], [1], [1], [1]]), "rots": 2, "flips": 1, "rects": []},
        "piece11": {"arr": np.array([[0, 1], [0, 1], [0, 1], [1, 1]]), "rots": 4, "flips": 2, "rects": []},
        "piece12": {"arr": np.array([[0, 1], [0, 1], [1, 1], [1, 0]]), "rots": 4, "flips": 2, "rects": []},
        "piece13": {"arr": np.array([[0, 1], [1, 1], [1, 1]]), "rots": 4, "flips": 2, "rects": []},
        "piece14": {"arr": np.array([[1, 1], [0, 1], [1, 1]]), "rots": 4, "flips": 1, "rects": []},
        "piece15": {"arr": np.array([[1, 0], [1, 1], [1, 0], [1, 0]]), "rots": 4, "flips": 2, "rects": []},
        "piece16": {"arr": np.array([[0, 1, 0], [0, 1, 0], [1, 1, 1]]), "rots": 4, "flips": 1, "rects": []},
        "piece17": {"arr": np.array([[1, 0, 0], [1, 0, 0], [1, 1, 1]]), "rots": 4, "flips": 1, "rects": []},
        "piece18": {"arr": np.array([[1, 1, 0], [0, 1, 1], [0, 0, 1]]), "rots": 4, "flips": 1, "rects": []},
        "piece19": {"arr": np.array([[1, 0, 0], [1, 1, 1], [0, 0, 1]]), "rots": 2, "flips": 2, "rects": []},
        "piece20": {"arr": np.array([[1, 0, 0], [1, 1, 1], [0, 1, 0]]), "rots": 4, "flips": 2, "rects": []},
        "piece21": {"arr": np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]]), "rots": 1, "flips": 1, "rects": []},
    }
    return dict_pieces


# Returns all the possible rotational and flipped states of every piece
def get_all_piece_states(player=None):
    list_pieces = []
    # Take the dictionary of remaining pieces
    if player is None:
        pieces = get_pieces()
    else:
        pieces = player.remaining_pieces
    # Iterate over that dictionary of remaining pieces
    for piece in pieces.keys():
        current_piece = pieces[piece]["arr"]
        # Iterate over number of possible flips for each piece
        for flip in range(pieces[piece]["flips"]):
            if not flip == 0:
                current_piece = np.flipud(current_piece)
            # Iterate over number of possible rotations for each piece
            for rot in range(pieces[piece]["rots"]):
                if not rot == 0:
                    current_piece = np.rot90(current_piece, k=1)
                list_pieces.append({"piece": piece, "arr": current_piece, "flipped": flip, "rotated": rot})
    return list_pieces
