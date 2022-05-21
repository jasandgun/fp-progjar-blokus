# To do something with player

import pieces, constants, board

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
        
        #tl = top left, bl = bottom left, tr = top right, br = bottom right
        self.board_corners = {"bl":[], "br":[], "tl":[], "tr":[]}
        self.is_1st_move = True