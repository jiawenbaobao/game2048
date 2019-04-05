import numpy as np
import numpy.random as npr
from readchar import readchar
import os


def create_chessboard(size=4):
    """create a new chessboard"""

    board = np.zeros((size, size), dtype=np.int32)
    board = initial_each_step(board)
    shown_board = draw_chessboard(board)
    print(shown_board)

    return board


def initial_each_step(board):
    """select a random position with value 0 and set it to 2"""

    board_size = board.shape[0]
    choice_range_list = []
    x_list, y_list = np.where(board == 0)
    for x, y in zip(x_list, y_list):
        choice_range_list.append(x * board_size + y)

    position = npr.choice(choice_range_list)
    position_x = position // board_size
    position_y = position % board_size
    # TODO: initialize with 4 in lower probability
    board[position_x, position_y] = 2

    return board


def next_step(board, direction='up'):
    """step to the next step in the game"""

    board_size = board.shape[0]
    if direction == 'left' or direction == 'right':
        board = board.T

    for i in range(board_size):
        column = board[:, i]
        addition_result = []
        if direction == 'down' or direction == 'right':
            column = column[::-1]

        # remove zeros in a column
        column = np.delete(column, np.where(column == 0))
        j = 0
        while j < len(column)-1:
            if column[j] == column[j+1]:
                addition_result.append(column[j] + column[j+1])
                j += 2
            else:
                addition_result.append(column[j])
                j += 1
        if j == len(column)-1:
            addition_result.append(column[j])

        while len(addition_result) < board_size:
            addition_result.append(0)
        addition_result = np.array(addition_result)
        if direction == 'down' or direction == 'right':
            addition_result = addition_result[::-1]

        board[:, i] = addition_result

    if direction == 'left' or direction == 'right':
        board = board.T

    return board


def draw_chessboard(board):
    """draw the chessboard"""

    size = board.shape[0]
    output = ''

    for i in range(size):
        output += ('+' + '-' * 6) * size
        output += '+\n'
        output += ('|' + ' ' * 6) * size
        output += '|\n'

    output += ('+' + '-' * 6) * size
    output += '+'

    output = list(output)
    x_list, y_list = np.where(board != 0)

    for x, y in zip(x_list, y_list):
        rect_position = (7 * size + 2) * (2 * x + 1) + 7 * y + 5
        num = board[x, y]
        while True:
            last_ch = str(num % 10)
            num //= 10
            output[rect_position] = last_ch
            rect_position -= 1

            if num == 0:
                break

    output = ''.join(output)

    return output


os.system('clear')

chessboard_size = 4
chessboard = create_chessboard(chessboard_size)

# current_score = 0
keys = 'WASDRQwasdrq'
actions = ['up', 'left', 'down', 'right', 'restart', 'exit']
action_dict = dict(zip(keys, actions * 2))

while 2048 not in chessboard:
    reminder_message = 'Press a key: WASD to move, R to restart, Q to quit\n'
    print(reminder_message)
    control_key = readchar()

    if control_key in 'WASDwasd':
        temp = chessboard.copy()  # need a slice rather than reference
        chessboard = next_step(chessboard, action_dict[control_key])
        if not (chessboard == temp).all():  # if the chessboard is changed
            chessboard = initial_each_step(chessboard)
        shown_board = draw_chessboard(chessboard)
        os.system('clear')
        print(shown_board)

    elif control_key in 'Rr':
        chessboard = create_chessboard(chessboard_size)

    elif control_key in 'Qq':
        print('Done')
        break

    else:
        continue

if 2048 in chessboard:
    shown_board = draw_chessboard(chessboard)
    shown_board = '\b' * (len(shown_board) + len(reminder_message)) + \
            shown_board
    print(shown_board)
    print('Congratulations! You win!')