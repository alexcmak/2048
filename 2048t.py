# No pygame, just the game
import random

DIM = 4
WIN_SCORE = 32  # should be power of 2

def print_board(board):
    print('---------')
    for row in board:
        print(*row)

def two_or_four():
    num_list = [2,4]
    return random.choice(num_list)

def add_new_tile(board):
    empty_tiles = [(r, c) for r in range(DIM) for c in range(DIM) if board[r][c] == 0]
    if empty_tiles:
        row, col = random.choice(empty_tiles)
        board[row][col] = two_or_four()

# this function shove tiles to the left and combine tiles where applicable
def merge_row(row):
    row_len = len(row)
    new_row = [i for i in row if i != 0]
    new_row += [0] * (row_len - len(new_row))
    for i in range(row_len - 1):
        if new_row[i] == new_row[i + 1] and new_row[i] != 0:
            new_row[i] *= 2
            new_row[i + 1] = 0
    new_row = [i for i in new_row if i != 0]
    new_row += [0] * (row_len - len(new_row))
    return new_row

def move_left(board):
    new_board = []
    for row in board:
        new_board.append(merge_row(row))
    return new_board

def move_right(board):
    new_board = []
    for row in board:
        new_board.append(merge_row(row[::-1])[::-1])
    return new_board

def move_up(board):
    new_board = list(zip(*board))
    new_board = move_left(new_board)
    return [list(row) for row in zip(*new_board)]

def move_down(board):
    # the paramater 'board' is a 2D array
    # list(zip()) make pairs into lists; essentially carving out each column into elements
    new_board = list(zip(*board))

    #  A, B, C, D
    #  E, F, G, H
    #  I, J, K, L
    #  M, N, O, P

    # new_board becomes [(A,E,I,M),(B,F,J,N),(C,G,K,O),(D,H,L,P)]

    new_board = move_right(new_board) # shift each element to the right, merge where applicable

    # this expression reconstitute the list back to 2D array
    return [list(row) for row in zip(*new_board)] 

def check_win(board):
    for row in board:
        if WIN_SCORE in row:
            return True
    return False

def check_moves_available(board):
    for row in range(DIM):
        if 0 in board[row]:
            return True
        for col in range(DIM - 1):
            if board[row][col] == board[row][col + 1]:
                return True
    for col in range(DIM):
        for row in range(DIM - 1):
            if board[row][col] == board[row + 1][col]:
                return True
    return False

def main():
    # list comprehension way to initialize a 2D array
    board = [[0] * DIM  for _ in range(DIM)]
    #add_new_tile(board)
    #add_new_tile(board)

    board[0][0] = 4
    board[0][1] = 2
    board[1][0] = 4
    board[2][3] = 16
    board[3][3] = 8

    print_board(board)

    # down arrow
    board = move_down(board)
    print_board(board)

   # board[0][0] = 2

  


if __name__ == "__main__":
	main()