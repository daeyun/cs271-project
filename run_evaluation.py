import othello
import random
import time
from alphaBeta import alphaBeta
import runMiniMax
import numpy as np

from third_party import dhconnelly
from third_party import board_conversion
import othello_ctypes

minimax = runMiniMax.MiniMax()


def find_move_third_party_dhconnelly(board: othello.Board, player_color: str, depth: int):
    """
    Implementation from http://dhconnelly.com/paip-python/docs/paip/othello.html

    :param board: Our board object.
    :param player_color: 'B', or 'W'
    :return: The next move tuple (x, y) computed by their algorithm. 0-indexed.
    Returns None is there is no legal move available.
    """

    assert isinstance(board, othello.Board)
    assert player_color in ('W', 'B')

    strategy = dhconnelly.alphabeta_searcher(depth=depth, evaluate=dhconnelly.weighted_score)

    their_board = board_conversion.convert_to_dhconnelly_board(board)
    their_player = dhconnelly.BLACK if player_color == 'B' else dhconnelly.WHITE

    start_time = time.time()
    if not dhconnelly.any_legal_move(their_player, their_board):
        elapsed = time.time() - start_time
        return None, elapsed
    their_move = dhconnelly.get_move(strategy, their_player, their_board)
    elapsed = time.time() - start_time

    y = (their_move // 10) - 1
    x = (their_move % 10) - 1

    ret = (x, y)

    return ret, elapsed


def find_move_ours(board, player_color, depth):
    # move = alphaBeta(state=board, depth=depth, player=player_color)
    move = minimax.minimax_search(board, player_color, depth=depth)
    return move


def play_against_dhconnelly(our_depth=3, their_depth=3):
    board = othello.Board()

    for i in range(8):
        for j in range(8):
            board.force_place_symbol((i, j), '0')

    board.force_place_symbol((3, 3), 'W')
    board.force_place_symbol((4, 4), 'W')

    board.force_place_symbol((3, 4), 'B')
    board.force_place_symbol((4, 3), 'B')

    while True:
        move_w = find_move_ours(board, 'W', depth=our_depth)
        if move_w is not None:
            board.make_move(move_w, 'W', play_test=False)

        move_b, elapsed_seconds = find_move_third_party_dhconnelly(board, 'B', depth=their_depth)
        if move_b is not None:
            board.make_move(move_b, 'B', play_test=False)

        if move_b is None and move_w is None:
            break

    print(board.get_winner() + ' wins!')
    return board.get_winner()


def play_against_dhconnelly_use_cpp(our_depth=3, their_depth=3):
    board = othello.Board()

    for i in range(8):
        for j in range(8):
            board.force_place_symbol((i, j), '0')

    board.force_place_symbol((3, 3), 'B')
    board.force_place_symbol((4, 4), 'B')

    board.force_place_symbol((3, 4), 'W')
    board.force_place_symbol((4, 3), 'W')

    total_runtime = 0
    total_runtime_theirs = 0

    while True:
        move_b, elapsed_seconds = othello_ctypes.best_move(board_conversion.convert_to_our_cpp_board(board), player='B',
                                                           strategy='all', depth=our_depth)
        total_runtime += elapsed_seconds
        if move_b is not None:
            board.make_move(move_b, 'B', play_test=False)

        move_w, elapsed_seconds = find_move_third_party_dhconnelly(board, 'W', depth=their_depth)
        total_runtime_theirs += elapsed_seconds
        if move_w is not None:
            board.make_move(move_w, 'W', play_test=False)

        if move_b is None and move_w is None:
            break

    print(board.get_winner() + ' wins!')
    return board.get_winner(), total_runtime, total_runtime_theirs


def play_against_our_baseline(our_depth=3, their_depth=3):
    board = othello.Board()

    for i in range(8):
        for j in range(8):
            board.force_place_symbol((i, j), '0')

    board.force_place_symbol((3, 3), 'B')
    board.force_place_symbol((4, 4), 'B')

    board.force_place_symbol((3, 4), 'W')
    board.force_place_symbol((4, 3), 'W')

    total_runtime = 0
    total_runtime_theirs = 0

    while True:
        move_b, elapsed_seconds = othello_ctypes.best_move(board_conversion.convert_to_our_cpp_board(board),
                                                           player='B', strategy='all', depth=our_depth)
        total_runtime += elapsed_seconds
        if move_b is not None:
            board.make_move(move_b, 'B', play_test=False)

        move_w, elapsed_seconds = othello_ctypes.best_move(board_conversion.convert_to_our_cpp_board(board),
                                                           player='W', strategy='weighted_parity_1', depth=their_depth)
        total_runtime_theirs += elapsed_seconds
        if move_w is not None:
            board.make_move(move_w, 'W', play_test=False)

        if move_b is None and move_w is None:
            break

    print(board.get_winner() + ' wins!')
    return board.get_winner(), total_runtime, total_runtime_theirs


def runtime_fixed_board(depth):
    board = othello.Board('..................B..B....BWBW...WWWWW....BBBWW.................'.replace('.', '0'))
    _, elapsed_seconds = othello_ctypes.best_move(board_conversion.convert_to_our_cpp_board(board), player='B',
                                                  strategy='all', depth=depth)
    return elapsed_seconds


def win_rate(result, player):
    assert isinstance(result, (list, tuple))
    assert player in ('W', 'B')

    w_wins = result.count('W')
    b_wins = result.count('B')

    assert w_wins + b_wins == len(result)

    if player == 'W':
        return w_wins / len(result)
    else:
        return b_wins / len(result)


def winrate_benchmark1():
    for our_depth, their_depth in [(2, 2), (3, 2), (4, 2), (5, 2)]:
        winners = [play_against_dhconnelly_use_cpp(our_depth=our_depth, their_depth=their_depth)[0] for _ in range(50)]
        print('our depth: {}, their depth: {}'.format(our_depth, their_depth))
        print(winners)
        rate = win_rate(winners, 'B')
        print('Our win rate was {} out of {} games'.format(rate, len(winners)))


def winrate_benchmark2():
    for our_depth, their_depth in [(3, 7), ]:
        winners = [play_against_our_baseline(our_depth=our_depth, their_depth=their_depth)[0] for _ in range(50)]
        print('our depth: {}, their depth: {}'.format(our_depth, their_depth))
        print(winners)
        rate = win_rate(winners, 'B')
        print('Our win rate was {} out of {} games'.format(rate, len(winners)))


def winrate_benchmark3():
    for our_depth, their_depth in [(2, 2), ]:
        winners = [play_against_dhconnelly_use_cpp(our_depth=our_depth, their_depth=their_depth)[0] for _ in range(100)]
        print('our depth: {}, their depth: {}'.format(our_depth, their_depth))
        print(winners)
        rate = win_rate(winners, 'B')
        print('Our win rate was {} out of {} games'.format(rate, len(winners)))


def runtime_benchmark():
    total_runtimes = [play_against_our_baseline(our_depth=5, their_depth=1)[1:] for _ in range(30)]
    total_runtimes = np.array(total_runtimes)

    print(total_runtimes.shape)

    print('Ours: {:.5f} seconds'.format(np.mean(total_runtimes[:, 0])))
    print('Theirs: {:.5f} seconds'.format(np.mean(total_runtimes[:, 1])))


def runtime_benchmark2():
    depth = 8
    total_runtimes = [runtime_fixed_board(depth=depth) for _ in range(10)]
    print('(depth {}): {:.5f} seconds'.format(depth, np.mean(total_runtimes)))


if __name__ == '__main__':
    runtime_benchmark2()
    # winrate_benchmark2()
