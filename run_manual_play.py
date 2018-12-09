import othello
import time
import othello_ctypes
import matplotlib.pyplot as pt
import numpy as np
from third_party import board_conversion
from run_evaluation import find_move_third_party_dhconnelly

gui_x = None
gui_y = None

search_depths = [11] * 2 + [10] * 4 + [9]


def search_depth_at_turn(turn):
    if turn >= len(search_depths):
        ret = search_depths[-1]
    else:
        ret = search_depths[turn]
    print('Search depth: {}'.format(ret))
    return ret


def open_window():
    fig = pt.figure()
    ax = fig.add_subplot(111)

    def onclick(event):
        global gui_x, gui_y
        gui_x, gui_y = int(event.xdata), int(event.ydata)
        print('x = %d, y = %d' % (gui_x, gui_y))

    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    pt.ion()
    pt.show()
    return ax


def get_input_from_gui():
    global gui_x, gui_y
    gui_x, gui_y = None, None
    print('Waiting for GUI input.')
    while gui_x is None or gui_y is None:
        pt.pause(0.3)
    return gui_x, gui_y


def main():
    game = othello.Game(othello.Board())
    game.board.print()  # Print empty board

    turn = 0
    total_elapsed_seconds = 0

    while True:
        computer_xy, elapsed_seconds = othello_ctypes.best_move(
            board_conversion.convert_to_our_cpp_board(game.board), player='B', strategy='all',
            depth=search_depth_at_turn(turn))
        print(computer_xy, elapsed_seconds)
        total_elapsed_seconds += elapsed_seconds
        if computer_xy is not None:
            game.board.make_move(computer_xy, 'B', play_test=False)
            game.board.print()  # Print after placing the W symbol.

        user_can_move = len(game.board.get_legal_moves('W')) > 0
        if user_can_move:
            user_entered_legal_move = False
            while not user_entered_legal_move:
                input_string = game.get_user_input_string()  # Prompts for console input.
                xy = game.parse_user_input_string(input_string)
                if not game.board.is_valid_move(xy, 'W'):
                    print('Invalid move: {}'.format(xy))
                    continue
                game.board.make_move(xy, 'W', play_test=False)
                game.board.print()  # Print after placing the W symbol.
                user_entered_legal_move = True

        turn += 1

        if computer_xy is None and not user_can_move:
            break

    print(game.board.get_winner() + ' wins!')
    print('Total run time: {} seconds'.format(total_elapsed_seconds))
    return game.board.get_winner()


def main_gui():
    game = othello.Game(othello.Board())
    # game.board = othello.Board('............W....BBWWB....WWWWWW..WBWB....BBBB.....B.......B....'.replace('.', '0'))
    # game.board = othello.Board('WWWWWWWWW.BWWBBWWBWBWBBBWWBWWWBBWWBBWWBBWWBW.WBBW.BBBBBB..BBBBBB'.replace('.', '0'))
    # game.board = othello.Board('..................B..B....BWBW...WWWWW....BBBWW.................'.replace('.', '0'))
    game.board.print()  # Print empty board

    ax = open_window()

    turn = 0
    total_elapsed_seconds = 0

    while True:
        computer_xy, elapsed_seconds = othello_ctypes.best_move(
            board_conversion.convert_to_our_cpp_board(game.board), player='B', strategy='all',
            depth=search_depth_at_turn(turn))
        print(computer_xy, elapsed_seconds)
        total_elapsed_seconds += elapsed_seconds
        if computer_xy is not None:
            game.board.make_move(computer_xy, 'B', play_test=False)
            game.board.print()  # Print after placing the W symbol.
            print(board_conversion.convert_to_our_cpp_board(game.board))
            game.board.plot(ax)

        user_can_move = len(game.board.get_legal_moves('W')) > 0
        if user_can_move:
            user_entered_legal_move = False
            while not user_entered_legal_move:
                xy = get_input_from_gui()
                if not game.board.is_valid_move(xy, 'W'):
                    print('Invalid move: {}'.format(xy))
                    continue
                game.board.make_move(xy, 'W', play_test=False)
                game.board.print()  # Print after placing the W symbol.
                print(board_conversion.convert_to_our_cpp_board(game.board))
                game.board.plot(ax)
                pt.pause(1)
                user_entered_legal_move = True
        else:
            pt.pause(1)

        turn += 1

        if computer_xy is None and not user_can_move:
            break

    print(game.board.get_winner() + ' wins!')
    print('Total run time: {} seconds'.format(total_elapsed_seconds))
    return game.board.get_winner()


if __name__ == '__main__':
    main_gui()
