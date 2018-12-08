import othello
import random
from alphaBeta import alphaBeta
import runMiniMax

from third_party import dhconnelly
from third_party import board_conversion

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

    if not dhconnelly.any_legal_move(their_player, their_board):
        return None

    their_move = dhconnelly.get_move(strategy, their_player, their_board)

    y = (their_move // 10) - 1
    x = (their_move % 10) - 1

    ret = (x, y)

    return ret


def find_move_ours(board, player_color, depth):
    #move = alphaBeta(state=board, depth=depth, player=player_color)
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

        move_b = find_move_third_party_dhconnelly(board, 'B', depth=their_depth)
        if move_b is not None:
            board.make_move(move_b, 'B', play_test=False)

        if move_b is None and move_w is None:
            break

    print(board.get_winner() + ' wins!')
    return board.get_winner()


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


if __name__ == '__main__':
    for our_depth, their_depth in [(2, 2), (3, 2), (4, 2)]:
        random.seed(42)  # To make this reproducible, set random seed.
        winners = [play_against_dhconnelly(our_depth=our_depth, their_depth=their_depth) for _ in range(3)]
        print('our depth: {}, their depth: {}'.format(our_depth, their_depth))
        print(winners)
        rate = win_rate(winners, 'W')
        print('Our win rate was {} out of {} games'.format(rate, len(winners)))
