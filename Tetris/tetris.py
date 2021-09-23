# !TODO: Scoreboard
# !TODO: Better Frame Refresher
# !TODO: Clear line when it's full

import time
import numpy as np
from pynput import keyboard
import random

screen = [24, 12]  # Board 20x10 + borders
board_height = int(screen[0])
board_width = int(screen[1])
start_coo = [0, 4]  # Start at the middle

pieces = [[[[0, 0, 0, 0], [0, 0, 0, 0], [2, 2, 2, 2], [0, 0, 0, 0]],
           [[0, 0, 2, 0], [0, 0, 2, 0], [0, 0, 2, 0], [0, 0, 2, 0]]],
          [[[0, 0, 0, 0], [0, 0, 2, 0], [2, 2, 2, 0], [0, 0, 0, 0]],
           [[0, 0, 0, 0], [0, 2, 2, 0], [0, 0, 2, 0], [0, 0, 2, 0]],
           [[0, 0, 0, 0], [0, 0, 0, 0], [2, 2, 2, 0], [2, 0, 0, 0]],
           [[0, 0, 0, 0], [0, 2, 0, 0], [0, 2, 0, 0], [0, 2, 2, 0]]],
          [[[0, 0, 0, 0], [2, 0, 0, 0], [2, 2, 2, 0], [0, 0, 0, 0]],
           [[0, 0, 0, 0], [0, 2, 0, 0], [0, 2, 0, 0], [2, 2, 0, 0]],
           [[0, 0, 0, 0], [0, 0, 0, 0], [2, 2, 2, 0], [0, 0, 2, 0]],
           [[0, 0, 0, 0], [0, 2, 2, 0], [0, 2, 0, 0], [0, 2, 0, 0]]],
          [[[0, 0, 0, 0], [0, 2, 0, 0], [2, 2, 2, 0], [0, 0, 0, 0]],
           [[0, 0, 0, 0], [0, 2, 0, 0], [2, 2, 0, 0], [0, 2, 0, 0]],
           [[0, 0, 0, 0], [0, 0, 0, 0], [2, 2, 2, 0], [0, 2, 0, 0]],
           [[0, 0, 0, 0], [0, 2, 0, 0], [0, 2, 2, 0], [0, 2, 0, 0]]],
          [[0, 0, 0, 0], [0, 2, 2, 0], [0, 2, 2, 0], [0, 0, 0, 0]],
          [[[0, 0, 0, 0], [0, 2, 2, 0], [2, 2, 0, 0], [0, 0, 0, 0]],
           [[0, 0, 0, 0], [0, 2, 0, 0], [0, 2, 2, 0], [0, 0, 2, 0]]],
          [[[0, 0, 0, 0], [2, 2, 0, 0], [0, 2, 2, 0], [0, 0, 0, 0]],
           [[0, 0, 0, 0], [0, 0, 2, 0], [0, 2, 2, 0], [0, 2, 0, 0]]]]

board = []


# Simple Clear Screen
# !TODO Create a better way to refresh the frame
def clear_screen():
    # Clear the screen "ctrl + l"
    print(chr(27) + '[2j')
    print('\033c')
    print('\x1bc')


# 1 = fixed piece, 2 = moving piece, 0 = empity cell
def create_board():
    for x in range(board_height):
        board.append([])
        for y in range(board_width):
            if (y == 0 or y == board_width - 1 or x == board_height - 1):
                board[x].append(1)
            else:
                board[x].append(0)


def print_board():
    for y in range(board_height):
        for x in range(board_width):
            if board[y][x] == 1:
                print("[■]", end='')
            if board[y][x] == 0:
                print("   ", end='')
            if board[y][x] == 2:
                print("[x]", end='')
        print()


# The piece is inside an 4x4 matrix, that moves inside the board matrix.
def move_on_board(piece, point):
    stop_move = False
    for y in range(board_height):
        for x in range(board_width):
            if y >= point[0] and y < point[0] + 4 and x >= point[
                    1] and x < point[1] + 4:

                if piece[y - point[0]][x - point[1]] == 2 and board[y +
                                                                    1][x] == 1:
                    board[y][x] = piece[y - point[0]][x - point[1]]
                    stop_move = True
                elif board[y][x] != 1:
                    board[y][x] = piece[y - point[0]][x - point[1]]

            elif board[y][x] != 1:
                board[y][x] = 0

    if (stop_move):
        print(np.array(board))
        for y in range(board_height):
            for x in range(board_width):
                if board[y][x] == 2:
                    board[y][x] = 1
        return [start_coo, stop_move]
    return [[point[0] + 1, point[1]], stop_move]


def move_horizontal(dir, piece, point):
    can_move = True

    for y in range(board_height):
        for x in range(board_width):
            if y >= point[0] and y < point[0] + 4 and x >= point[
                    1] and x < point[1] + 4:
                if piece[y - point[0]][x -
                                       point[1]] == 2 and board[y][x +
                                                                   dir] == 1:
                    can_move = False
    if can_move:
        return [point[0], point[1] + dir]

    return point


def try_turn(i, piece_l, point):
    j = (i + 1) % len(piece_l)
    piece = piece_l[j]
    for y in range(board_height):
        for x in range(board_width):
            if y >= point[0] and y < point[0] + 4 and x >= point[
                    1] and x < point[1] + 4:
                if (x - point[1] < 0):
                    pass
                elif (x - point[1] > board_width - 1):
                    pass
                if (x == 0 and piece[y - point[0]][x - point[1]] == 2):
                    pass
                elif (x == board_width - 1
                      and piece[y - point[0]][x - point[1]] == 2):
                    pass
    return j


def refresh_board(piece, point):
    for y in range(board_height):
        for x in range(board_width):
            if y >= point[0] and y < point[0] + 4 and x >= point[
                    1] and x < point[1] + 4:

                while (True):
                    if (x - point[1] < 0):
                        point[1] -= 1
                        continue
                    elif (x - point[1] > board_width - 1):
                        point[1] += 1
                    if (x == 0 and piece[y - point[0]][x - point[1]] == 2):
                        point[1] += 1
                    elif (x == board_width - 1
                          and piece[y - point[0]][x - point[1]] == 2):
                        point[1] -= 1
                    else:
                        break

                if piece[y - point[0]][x - point[1]] == 2:
                    board[y][x] = piece[y - point[0]][x - point[1]]
                elif board[y][x] != 1:
                    board[y][x] = piece[y - point[0]][x - point[1]]
            elif board[y][x] != 1:
                board[y][x] = 0

    return point


create_board()
piece = random.choice(pieces)
point = start_coo
i = 0
clear_screen()
move_on_board(piece[i], point)
while True:
    move = True
    clear_screen()
    print_board()
    with keyboard.Events() as events:
        event = events.get(0.5)
        if event is None:
            move = True
        elif (event.key == keyboard.Key.space or event.key == keyboard.Key.up):
            i = try_turn(i, piece, point)
            move = False
        elif (event.key == keyboard.Key.right):
            point = move_horizontal(dir=1, point=point, piece=piece[i])
            move = False
        elif (event.key == keyboard.Key.left):
            move = False
            point = move_horizontal(dir=-1, point=point, piece=piece[i])
        elif (event.key == keyboard.Key.down):
            temp = move_on_board(point=point, piece=piece[i])
            next_piece = temp[1]
            point = temp[0]
            if (next_piece):
                piece = random.choice(pieces)
                point = start_coo
                i = 0
            continue
        elif (event.key == keyboard.Key.esc):
            break
    if move:
        temp = move_on_board(point=point, piece=piece[i])
        print(temp[1])
        next_piece = temp[1]
        point = temp[0]
        if (next_piece):
            piece = random.choice(pieces)
            point = start_coo
            i = 0
            print(piece)
    else:
        point = refresh_board(piece[i], point)
