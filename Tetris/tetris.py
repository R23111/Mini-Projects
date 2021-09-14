board_height = 21
board_width = 12

board = []


def clear_screen():
    # Clear the screen "ctrl + l"
    print(chr(27) + '[2j')
    print('\033c')
    print('\x1bc')


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
        print()


clear_screen()
create_board()
print_board()
