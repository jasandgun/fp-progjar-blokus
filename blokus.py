# Main program

import pygame, os
import constants, drawElements, player
from board import Board

#Handles where the window position is drawn on the os so it drawn centered
os.environ['SDL_VIDEO_CENTERED'] = '1'

class PygameClass:
    def __init__(self, player_init_params = None, render = True):
        if render:
            self.screen, self.background, self.piece_surface, self.clock = self.init_pygame()
        self.game_over = False
        self.selected = None
        self.gameboard = Board()
        self.board_rects = drawElements.init_gameboard(self.gameboard.board)

        if player_init_params is None:
            player_init_params = {"p1" : constants.HUMAN_PARAMS["default_p1"],
                                  "p2" : constants.HUMAN_PARAMS["default_p2"]}
        self.player1, self.player2 = self.init_players(player_init_params)
        
    def init_pygame(self):
        pygame.init()
        window = pygame.display.set_mode(constants.WINDOW_SIZE)
        background = pygame.Surface(constants.WINDOW_SIZE)
        piece_surface = pygame.Surface([50,50]).set_alpha(180)
        clock = pygame.time.Clock()
        pygame.display.set_caption("Blokus on Pygame")
        return window, background, piece_surface, clock
    
    def init_players(self, player_init_params):
        player1 = player.Player(constants.PLAYER1_VALUE, player_init_params["p1"]["color"])
        player2 = player.Player(constants.PLAYER2_VALUE, player_init_params["p2"]["color"])
        return player1, player2
    
    def event_handler(self, active_player, opponent):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
                IS_QUIT = True
        return active_player, opponent

#The main game loop
def game_loop():
    pgc = PygameClass()
    active_player, opponent = pgc.player1, pgc.player2
    drawElements.init_piece_rects(pgc.player1.remaining_pieces, pgc.player2.remaining_pieces)
    
    while not pgc.game_over:
        #Player's turn, listen for input. We use that as our basis for checking and making turn based moves.
        active_player, opponent = pgc.event_handler(active_player, opponent)
        
        #Set the screen background
        pgc.background.fill(constants.BLACK)
        
        #Draw the necessary components
        drawElements.draw_gameboard(pgc.background, pgc.board_rects, pgc.gameboard, active_player.current_piece, active_player, opponent)

        drawElements.draw_pieces(pgc.background, pgc.player1, pgc.player2, active_player, pgc.selected)
        
        pgc.screen.blit(pgc.background, (0,0))
        
        # Limit to 60 frames per second
        pgc.clock.tick(60)
 
        # Update the screen with what is drawn.
        pygame.display.update()

if __name__ == "__main__":
    IS_QUIT = False

    game_loop()

    if IS_QUIT:
        pygame.quit()