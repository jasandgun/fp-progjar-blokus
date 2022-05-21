# To do something with UI

import pygame, math
import constants

#This file handles generation of all the sizes of the elements
#The values have been optimised for 1280*720 window area
MARGIN = 2

board_width = 620
board_box_width = 42
piece_box_width = (constants.WINDOW_WIDTH - board_width) / 2 #330
one_piece_box_width = piece_box_width / 2 #165
single_piece_width = 9
info_box_width = constants.WINDOW_WIDTH #1280

board_height = board_width #620
board_box_height = board_box_width
piece_box_height = board_height
one_piece_box_height = math.floor(board_height / 11) #56
single_piece_height = single_piece_width #9
info_box_height = constants.WINDOW_HEIGHT - board_height #100

board_origin = [piece_box_width, info_box_height] #[330, 100]

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

def draw_gameboard(canvas, board_rects, gameboard, current_piece, player, opponent):
    counter = 0
    board_arr = gameboard.board
    is_valid_move = False
    
    #This section generates the green margin when a valid move is spotted
    if len(current_piece["rects"]) > 0:
        if player.is_1st_move:
            for rect in current_piece["rects"]:
                if grid_to_array_coords([rect.centerx, rect.centery]) == constants.STARTING_PTS["player%s"%(player.number)]:
                    is_valid_move = True
        else:
            if gameboard.check_is_move_valid(current_piece["arr"], player, grid_to_array_coords([current_piece["rects"][0].centerx, current_piece["rects"][0].centery])):
                is_valid_move = True
    for row in range(board_arr.shape[0]):
        for column in range(board_arr.shape[1]):
            rect = board_rects[counter]
            #Draw the green board box margin if the move is valid
            for piece_rect in current_piece["rects"]:
                if piece_rect.collidepoint(rect.centerx, rect.centery) and board_arr[row][column] == constants.BOARD_FILL_VALUE\
                    and is_valid_move:
                    rect.x -= MARGIN
                    rect.y -= MARGIN
                    rect.h += 2 * MARGIN
                    rect.w += 2 * MARGIN
                    pygame.draw.rect(canvas, constants.GREEN, rect)
                    rect.x += MARGIN
                    rect.y += MARGIN
                    rect.h -= 2 * MARGIN
                    rect.w -= 2 * MARGIN
            #Board fill color
            if board_arr[row][column] == constants.BOARD_FILL_VALUE:
                pygame.draw.rect(canvas, constants.WHITE, rect)
            elif board_arr[row][column] == constants.PLAYER1_VALUE:
                pygame.draw.rect(canvas, constants.PURPLE, rect)
            elif board_arr[row][column] == constants.PLAYER2_VALUE:
                pygame.draw.rect(canvas, constants.ORANGE, rect)
            #Blit the text to mark the starting points
            if [row, column] == constants.STARTING_PTS["player1"]:
                text = pygame.font.SysFont(None, 15).render("Player 1", True, constants.BLACK)
                canvas.blit(text, [rect.x, rect.centery - 2])
            elif [row, column] == constants.STARTING_PTS["player2"]:
                text = pygame.font.SysFont(None, 15).render("Player 2", True, constants.BLACK)
                canvas.blit(text, [rect.x, rect.centery - 2])
            else:
                #WARNING: This rendering within the loop slows down the game
                if constants.VERBOSITY > 1:
                    text = pygame.font.SysFont(None, 15).render("(%s, %s)" % (row, column), True, constants.BLACK)
                    canvas.blit(text, [rect.x + 2, rect.centery - 2])
            counter += 1

def init_piece_rects(p1_remaining_pieces, p2_remaining_pieces):
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
    
    row, column = 0, 0
    for piece in p2_remaining_pieces.keys():
        piece_rects = []
        for i in range(p2_remaining_pieces[piece]["arr"].shape[0]):
            for j in range(p2_remaining_pieces[piece]["arr"].shape[1]):
                if p2_remaining_pieces[piece]["arr"][i][j] == 1:
                    x = piece_box_width + board_width + (one_piece_box_width * column) + ((MARGIN + single_piece_width) * j) + MARGIN
                    y = info_box_height + (one_piece_box_height * row) + ((MARGIN + single_piece_height) * i)
                    piece_rects.append(pygame.Rect([x, y, single_piece_width, single_piece_height]))
        p2_remaining_pieces[piece]["rects"] = piece_rects
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
                pygame.draw.rect(canvas, constants.WHITE, unit_sq, MARGIN)
                unit_sq.x += MARGIN
                unit_sq.y += MARGIN
    for key, val in p2_pieces.items():
        if not (key == selected and player2.number == active_player.number):
            for unit_sq in val["rects"]:
                pygame.draw.rect(canvas, p2_color, unit_sq)
                unit_sq.x -= MARGIN
                unit_sq.y -= MARGIN
                pygame.draw.rect(canvas, constants.WHITE, unit_sq, MARGIN)
                unit_sq.x += MARGIN
                unit_sq.y += MARGIN