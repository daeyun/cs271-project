import othello

class MiniMax(object):

    @staticmethod
    def minimax_play(board, player, depth):
        if depth == 0:
            b_s, w_s = board.heuristic_weighted()
            return b_s, w_s, None

        legal_moves = board.get_legal_moves(player)

        minimax_move = None
        minimax_score = 0

        for move in legal_moves:
            temp_score = 0
            board.make_move(move, player, play_test=False)
            b_temp, w_temp = board.heuristic_weighted()

            if player == 'B':
                temp_score = b_temp
            else:
                temp_score = w_temp

            b_score, w_score, _ = MiniMax.minimax_play(board, board.get_opponent(player), depth-1)
            if player == 'B':
                if b_score + temp_score > minimax_score:
                    minimax_score = b_score + temp_score
                    minimax_move = move
            else:
                if w_score + temp_score > minimax_score:
                    minimax_score = w_score + temp_score
                    minimax_move = move

        if player == 'B':
            return minimax_score, 0, minimax_move
        else:
            return 0, minimax_score, minimax_move

    @staticmethod
    def minimax_search(board, player):
        assert player in ('W', 'B')

        minimax_search_depth = 4
        return MiniMax.minimax_play(board, player, minimax_search_depth)[2]
