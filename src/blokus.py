"""
Main program
"""

import os
import pygame

import constants
import drawElements
import player
from board import Board

# Handles where the window position is drawn on the os so it drawn centered
os.environ['SDL_VIDEO_CENTERED'] = '1'


class PygameClass:
    def __init__(self, player_init_params=None, render=True):
        if render:
            self.screen, self.background, self.piece_surface, self.clock = self.init_pygame()
        self.offset_list = []
        self.game_over = False
        self.selected = None
        self.gameboard = Board()
        self.board_rects = drawElements.init_gameboard(self.gameboard.board)
        self.infobox_msg_time_start = None
        self.infobox_msg = None

        if player_init_params is None:
            player_init_params = {"p1": constants.HUMAN_PARAMS["default_p1"],
                                  "p2": constants.HUMAN_PARAMS["default_p2"]}
        self.player1, self.player2 = self.init_players(player_init_params)

    def init_pygame(self):
        pygame.init()
        window = pygame.display.set_mode(constants.WINDOW_SIZE)
        background = pygame.Surface(constants.WINDOW_SIZE)
        piece_surface = pygame.Surface([50, 50]).set_alpha(180)
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
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if constants.VERBOSITY > 1:
                    print("Mouse pos:", pygame.mouse.get_pos())
                # if a piece is selected by the player, check if it can be placed
                if self.selected is not None:
                    if drawElements.are_squares_within_board(active_player.current_piece, self.board_rects):
                        rect_coords = [active_player.current_piece["rects"][0].centerx,
                                       active_player.current_piece["rects"][0].centery]
                        board_arr_coords = drawElements.grid_to_array_coords(rect_coords)
                        # adjusts the coordinates so the piece's arr coord is chosen at [0,0]
                        j = 0
                        while not active_player.current_piece["arr"][0][j] == 1:
                            j += 1
                        board_arr_coords[1] -= j
                        active_player.current_piece["place_on_board_at"] = board_arr_coords

                        # fitting the piece
                        if self.gameboard.fit_piece(active_player.current_piece, active_player, opponent):
                            self.selected = None
                            active_player, opponent = player.switch_active_player(active_player, opponent)
                        # display error message if it doesn't fit
                        else:
                            self.display_infobox_msg_start("not_valid_move")
                    # clear the selection if clicking outside the board
                    else:
                        self.selected = None
                # else check if there's a need to pick up a piece
                else:
                    self.offset_list, self.selected = drawElements.generate_element_offsets(
                        active_player.remaining_pieces, event)
                    if self.selected is not None:
                        active_player.current_piece["piece"] = self.selected
                        active_player.current_piece["arr"] = active_player.remaining_pieces[self.selected]["arr"]
                        active_player.current_piece["rects"] = active_player.remaining_pieces[self.selected]["rects"]
            elif event.type == pygame.MOUSEBUTTONUP:
                drawElements.init_piece_rects(self.player1.remaining_pieces, self.player2.remaining_pieces)
            elif event.type == pygame.KEYDOWN:
                if self.selected is not None:
                    self.key_controls(event, active_player)
        return active_player, opponent

    def key_controls(self, event, active_player):
        # rotate left
        if event.key == pygame.K_LEFT:
            active_player.rotate_current_piece()
            self.offset_list = drawElements.draw_rotated_flipped_selected_piece(active_player.current_piece)
        # rotate right
        elif event.key == pygame.K_RIGHT:
            active_player.rotate_current_piece(False)
            self.offset_list = drawElements.draw_rotated_flipped_selected_piece(active_player.current_piece)
        # flip diagonally
        elif event.key == pygame.K_UP:
            active_player.flip_current_piece()
            self.offset_list = drawElements.draw_rotated_flipped_selected_piece(active_player.current_piece)

    def display_infobox_msg_start(self, msg_key):
        self.infobox_msg_time_start = pygame.time.get_ticks()
        self.infobox_msg = msg_key

    def display_infobox_msg_end(self, end_now=False):
        if end_now:
            self.infobox_msg_time_start = None
        elif pygame.time.get_ticks() - self.infobox_msg_time_start > self.infobox_msg_timeout:
            self.infobox_msg_time_start = None


# The main game loop
def game_loop():
    pgc = PygameClass()
    active_player, opponent = pgc.player1, pgc.player2
    drawElements.init_piece_rects(pgc.player1.remaining_pieces, pgc.player2.remaining_pieces)

    while not pgc.game_over:
        # Player's turn, listen for input. We use that as our basis for checking and making turn based moves.
        active_player, opponent = pgc.event_handler(active_player, opponent)

        # Set the screen background
        pgc.background.fill(constants.BLACK)

        """
        Draw the necessary components
        """
        # -- infobox insert here --
        drawElements.draw_gameboard(pgc.background, pgc.board_rects, pgc.gameboard, active_player.current_piece,
                                    active_player, opponent)
        drawElements.draw_pieces(pgc.background, pgc.player1, pgc.player2, active_player, pgc.selected)
        pgc.screen.blit(pgc.background, (0, 0))
        if pgc.selected is not None:
            drawElements.draw_selected_piece(pgc.background, pgc.offset_list, pygame.mouse.get_pos(),
                                             active_player.current_piece, active_player.color)
        # Limit to 60 frames per second
        pgc.clock.tick(60)

        # Update the screen with what is drawn.
        pygame.display.update()


if __name__ == "__main__":
    IS_QUIT = False

    game_loop()

    if IS_QUIT:
        pygame.quit()
