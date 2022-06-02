"""
Handle the rendering of UI elements
"""

import math
import pygame

import constants

# This file handles generation of all the sizes of the elements
# The values have been optimised for 1280*720 window area
MARGIN = 2

board_width = 620
board_box_width = 42
piece_box_width = (constants.WINDOW_WIDTH - board_width) / 2  # 330
one_piece_box_width = piece_box_width / 2  # 165
single_piece_width = 9
info_box_width = constants.WINDOW_WIDTH  # 1280

board_height = board_width  # 620
board_box_height = board_box_width
piece_box_height = board_height
one_piece_box_height = math.floor(board_height / 11)  # 56
single_piece_height = single_piece_width  # 9
info_box_height = constants.WINDOW_HEIGHT - board_height  # 100

board_origin = [piece_box_width, info_box_height]  # [330, 100]


def draw_title_window():
    pass


def array_to_grid_coords():
    pass


def grid_to_array_coords(pos):
    col = int((pos[0] - (piece_box_width + MARGIN)) // (MARGIN + board_box_width))
    row = int((pos[1] - (info_box_height + MARGIN)) // (MARGIN + board_box_height))
    return [row, col]


def init_gameboard(board_arr):
    rects = []
    for row in range(board_arr.shape[0]):
        for column in range(board_arr.shape[1]):
            box_width = piece_box_width + MARGIN + ((MARGIN + board_box_width) * column)
            box_height = info_box_height + MARGIN + ((MARGIN + board_box_height) * row)
            dims = [box_width, box_height, board_box_width, board_box_height]
            rects.append(pygame.Rect(dims))
    return rects


def draw_gameboard(canvas, board_rects, gameboard, current_piece, player):
    counter = 0
    board_arr = gameboard.board
    is_valid_move = False

    # generate green margin when showing a valid spot
    if len(current_piece["rects"]) > 0:
        if player.is_1st_move:
            for rect in current_piece["rects"]:
                if grid_to_array_coords([rect.centerx, rect.centery]) == \
                        constants.STARTING_PTS["player%s" % player.number]:
                    is_valid_move = True
        else:
            rect_coords = [current_piece["rects"][0].centerx,
                           current_piece["rects"][0].centery]
            board_arr_coords = grid_to_array_coords(rect_coords)
            j = 0
            while not current_piece["arr"][0][j] == 1:
                j += 1
            board_arr_coords[1] -= j
            if gameboard.check_is_move_valid(current_piece["arr"], player, board_arr_coords):
                is_valid_move = True
    for row in range(board_arr.shape[0]):
        for column in range(board_arr.shape[1]):
            rect = board_rects[counter]
            # Draw the green board box margin if the move is valid
            for piece_rect in current_piece["rects"]:
                if piece_rect.collidepoint(rect.centerx, rect.centery) and board_arr[row][
                    column] == constants.BOARD_FILL_VALUE \
                        and is_valid_move:
                    rect.x -= MARGIN
                    rect.y -= MARGIN
                    rect.h += 2 * MARGIN
                    rect.w += 2 * MARGIN
                    pygame.draw.rect(canvas, constants.COLORS["GREEN"], rect)
                    rect.x += MARGIN
                    rect.y += MARGIN
                    rect.h -= 2 * MARGIN
                    rect.w -= 2 * MARGIN
            # Board fill color
            if board_arr[row][column] == constants.BOARD_FILL_VALUE:
                pygame.draw.rect(canvas, constants.COLORS["WHITE"], rect)
            elif board_arr[row][column] == constants.PLAYER1_VALUE:
                pygame.draw.rect(canvas, constants.HUMAN_PARAMS["default_p1"]["color"], rect)
            elif board_arr[row][column] == constants.PLAYER2_VALUE:
                pygame.draw.rect(canvas, constants.HUMAN_PARAMS["default_p2"]["color"], rect)
            # Blit the text to mark the starting points
            if [row, column] == constants.STARTING_PTS["player1"]:
                text = pygame.font.SysFont(None, 15).render("Player 1", True, constants.COLORS["BLACK"])
                canvas.blit(text, [rect.x, rect.centery - 2])
            elif [row, column] == constants.STARTING_PTS["player2"]:
                text = pygame.font.SysFont(None, 15).render("Player 2", True, constants.COLORS["BLACK"])
                canvas.blit(text, [rect.x, rect.centery - 2])
            else:
                # WARNING: This rendering within the loop slows down the game
                if constants.ENABLE_VERBOSE > 1:
                    text = pygame.font.SysFont(None, 15).render("(%s, %s)" % (row, column), True,
                                                                constants.COLORS["BLACK"])
                    canvas.blit(text, [rect.x + 2, rect.centery - 2])
            counter += 1


def init_piece_rects(p1_remaining_pieces):
    row, column = 0, 0
    for piece in p1_remaining_pieces.keys():
        piece_rects = []
        for i in range(p1_remaining_pieces[piece]["arr"].shape[0]):
            for j in range(p1_remaining_pieces[piece]["arr"].shape[1]):
                if p1_remaining_pieces[piece]["arr"][i][j] == 1:
                    x = (one_piece_box_width * column) + ((MARGIN + single_piece_width) * j) + MARGIN
                    y = info_box_height + (one_piece_box_height * row) + ((MARGIN + single_piece_height) * i)
                    piece_rects.append(pygame.Rect([x, y, single_piece_width, single_piece_height]))
        p1_remaining_pieces[piece]["rects"] = piece_rects
        column += 1
        if column == 2:
            row += 1
            column = 0


def draw_pieces(canvas, player1, player2, active_player, selected):
    p1_pieces, p2_pieces = player1.remaining_pieces, player2.remaining_pieces
    p1_color, p2_color = player1.color, player2.color
    for key, val in p1_pieces.items():
        if not (key == selected and player1.number == active_player.number):
            for unit_sq in val["rects"]:
                pygame.draw.rect(canvas, p1_color, unit_sq)
                unit_sq.x -= MARGIN
                unit_sq.y -= MARGIN
                pygame.draw.rect(canvas, constants.COLORS["WHITE"], unit_sq, MARGIN)
                unit_sq.x += MARGIN
                unit_sq.y += MARGIN
    for key, val in p2_pieces.items():
        if not (key == selected and player2.number == active_player.number):
            for unit_sq in val["rects"]:
                pygame.draw.rect(canvas, p2_color, unit_sq)
                unit_sq.x -= MARGIN
                unit_sq.y -= MARGIN
                pygame.draw.rect(canvas, constants.COLORS["WHITE"], unit_sq, MARGIN)
                unit_sq.x += MARGIN
                unit_sq.y += MARGIN


def draw_selected_piece(canvas, offset_list, mouse_pos, current_piece, player_color):
    counter = 0
    rects = current_piece["rects"]
    # ref_x, ref_y = rects[0].x, rects[0].y
    for i in range(current_piece["arr"].shape[0]):
        for j in range(current_piece["arr"].shape[1]):
            if current_piece["arr"][i][j] == 1:
                rects[counter].x = mouse_pos[0] + offset_list[counter][0] + \
                                   (board_box_width - single_piece_width) * j - MARGIN
                rects[counter].y = mouse_pos[1] + offset_list[counter][1] + \
                                   (board_box_height - single_piece_height) * i - MARGIN
                rects[counter].h = board_box_height + (2 * MARGIN)
                rects[counter].w = board_box_width + (2 * MARGIN)
                pygame.draw.rect(canvas, constants.COLORS["WHITE"], rects[counter], MARGIN)
                rects[counter].x += MARGIN
                rects[counter].y += MARGIN
                rects[counter].h -= 2 * MARGIN
                rects[counter].w -= 2 * MARGIN
                pygame.draw.rect(canvas, player_color, rects[counter])
                counter += 1


def draw_rotated_flipped_selected_piece(current_piece):
    ref_x, ref_y = current_piece["rects"][0].x, current_piece["rects"][0].y
    current_piece["rects"], offset_list = [], []
    mouse_pos = pygame.mouse.get_pos()
    counter = 0
    for i in range(current_piece["arr"].shape[0]):
        for j in range(current_piece["arr"].shape[1]):
            if current_piece["arr"][i][j] == 1:
                x = ref_x + ((board_box_width - single_piece_width) * j) - MARGIN
                y = ref_y + ((board_box_height - single_piece_height) * i) - MARGIN
                h = board_box_height
                w = board_box_width
                current_piece["rects"].append(pygame.Rect(x, y, h, w))
                selected_offset_x = x - ((board_box_width / 2) * j) - mouse_pos[0] - MARGIN
                selected_offset_y = y - ((board_box_height / 2) * i) - mouse_pos[1] - MARGIN
                offset_list.append([selected_offset_x, selected_offset_y])
                counter += 1
    return offset_list


# Checks if all the squares of the current selected piece lie within the board
def are_squares_within_board(current_piece, board_rects):
    is_within_board = False
    for piece_rect in current_piece["rects"]:
        for board_rect in board_rects:
            if piece_rect.collidepoint(board_rect.centerx, board_rect.centery):
                is_within_board = True
        if not is_within_board:
            return False
        else:
            is_within_board = False
    return True


def draw_infobox(canvas, player1, player2, active_player):
    text_dict = {"p1_score": "Player 1 Score: %s" % player1.score,
                 "p2_score": "Player 2 Score: %s" % player2.score,
                 "title": "Blokus on Pygame"}

    font = pygame.font.SysFont("Trebuchet MS", 30)
    if active_player.number == 1:
        current_player_rect = pygame.Rect(
            (20, 20, piece_box_width - 40, info_box_height - 40))  # x=20, y=20, w=290, h=60
    else:
        current_player_rect = pygame.Rect((piece_box_width + board_width + 20, 20, piece_box_width - 40,
                                           info_box_height - 40))  # x=1010, y=20, w=290, h=60
    pygame.draw.rect(canvas, constants.COLORS["GREEN"], current_player_rect)

    font_dict = {"p1_score": font.render(text_dict["p1_score"], False, constants.COLORS["WHITE"]),
                 "p2_score": font.render(text_dict["p2_score"], False, constants.COLORS["WHITE"]),
                 "title": font.render(text_dict["title"], False, constants.COLORS["WHITE"])}

    pos_rect_dict = {"p1_score": pygame.Rect((0, 0, piece_box_width, info_box_height)),  # x=0, y=0, w=330, h=100
                     "p2_score": pygame.Rect((piece_box_width + board_width, 0, piece_box_width, info_box_height)),
                     # x=990, y=0, w=330, h=100
                     "title": pygame.Rect((0, 0, info_box_width, info_box_height))}  # x=0, y=0, w=1280, h=100

    pos_dict = {"p1_score": pos_rect_dict["p1_score"].center,
                "p2_score": pos_rect_dict["p2_score"].center,
                "title": (pos_rect_dict["title"].midtop[0] + 13, pos_rect_dict["title"].midtop[1] + 13)}

    for key, val in font_dict.items():
        canvas.blit(val, val.get_rect(center=pos_dict[key]))


def generate_element_offsets(remaining_pieces, event):
    offset_list = []
    selected = None
    for key, val in remaining_pieces.items():
        for r in val["rects"]:
            r.x -= MARGIN
            r.y -= MARGIN
            if r.collidepoint(event.pos):
                selected = key
                r.x += MARGIN
                r.y += MARGIN
                break
            r.x += MARGIN
            r.y += MARGIN
        if selected is not None:
            break
    if selected is not None:
        for chosen_piece in remaining_pieces[selected]["rects"]:
            selected_offset_x = chosen_piece.x - event.pos[0]
            selected_offset_y = chosen_piece.y - event.pos[1]
            offset_list.append([selected_offset_x, selected_offset_y])
    return offset_list, selected


def draw_infobox_msg(canvas, player1, player2, msg_key):
    game_over_text = ""
    if msg_key == "game_over":
        if player1.score > player2.score:
            game_over_text = "Game over. Player %s wins!" % player1.number
        elif player1.score < player2.score:
            game_over_text = "Game over. Player %s wins!" % player2.number
        else:
            game_over_text = "Game over. It's a tie!"
    text_dict = {"not_valid_move": "Invalid move. This piece cannot be placed there",
                 "game_over": game_over_text}

    font = pygame.font.SysFont("Trebuchet MS", 25)

    font_dict = {"not_valid_move": font.render(text_dict["not_valid_move"], False, constants.COLORS["RED"]),
                 "game_over": font.render(text_dict["game_over"], False, constants.COLORS["GREEN"])}

    pos_rect_dict = {"not_valid_move": pygame.Rect((0, 0, info_box_width, info_box_height)),  # x=0, y=0, w=1280, h=100
                     "game_over": pygame.Rect((0, 0, info_box_width, info_box_height))}  # x=0, y=0, w=1280, h=100

    pos_dict = {"not_valid_move": pos_rect_dict["not_valid_move"].center,
                "game_over": pos_rect_dict["game_over"].center, }

    canvas.blit(font_dict[msg_key], font_dict[msg_key].get_rect(center=pos_dict[msg_key]))
