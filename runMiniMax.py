import othello
import copy
import math
class MiniMax(object):

    # TODO: Actual minimax implementation. Minimize the opponents score
    @staticmethod
    def minimax_new_play(initial_board, player, depth):
        if depth == 0:
            b_s, w_s = initial_board.heuristic_weighted()
            if player == 'B':
                return b_s, None
            else:
                return w_s, None

        legal_moves = initial_board.get_legal_moves(player)

        minimax_move = None
        minimax_score = -math.inf

        board = copy.deepcopy(initial_board)

        if not legal_moves:
            if not board.get_legal_moves(board.get_opponent(player)):
                b_s, w_s = board.heuristic_weighted()
                if player == 'B':
                    diff = b_s - w_s
                else:
                    diff = w_s - b_s

                if diff > 0:
                    return 1000, None
                else:
                    return -1000, None

            sc, _ = MiniMax.minimax_new_play(board, board.get_opponent(player), depth-1)
            return -sc, None

        for move in legal_moves:
            board = copy.deepcopy(initial_board)
            board.make_move(move, player, play_test=False)

            sc , _ = MiniMax.minimax_new_play(board, board.get_opponent(player), depth-1)
            sc = -1*sc
            if sc > minimax_score:
                minimax_score = sc
                minimax_move = move

        return minimax_score, minimax_move


    # TODO: Not actual minimax. Maximize given players score (greedy)
    @staticmethod
    def minimax_play(board, player, depth):
        if depth == 0:
            b_s, w_s = board.heuristic_weighted()
            return b_s, w_s, None

        legal_moves = board.get_legal_moves(player)

        minimax_move = None
        minimax_score = 0

        initial_board = copy.deepcopy(board)
        b_temp, w_temp = board.heuristic_weighted()
        for move in legal_moves:
            temp_score = 0
            board = copy.deepcopy(initial_board)
            board.make_move(move, player, play_test=False)

            if player == 'B':
                temp_score = b_temp
            else:
                temp_score = w_temp

            b_score, w_score, _ = MiniMax.minimax_play(board, board.get_opponent(player), depth - 1)
            if player == 'B':
                if b_score + temp_score > minimax_score:
                    minimax_score = b_score + temp_score
                    minimax_move = move
            else:
                if w_score + temp_score > minimax_score:
                    minimax_score = w_score + temp_score
                    minimax_move = move

        if player == 'B':
            return minimax_score, w_temp, minimax_move
        else:
            return b_temp, minimax_score, minimax_move

    @staticmethod
    def minimax_search(board, player, depth):
        assert player in ('W', 'B')

        return MiniMax.minimax_play(board, player, depth)[2]
        #return MiniMax.minimax_new_play(board, player, depth)[1]
