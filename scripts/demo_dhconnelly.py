from third_party import dhconnelly


def main():
    s1 = dhconnelly.alphabeta_searcher(4, dhconnelly.weighted_score)
    s2 = dhconnelly.alphabeta_searcher(4, dhconnelly.weighted_score)
    board, score = dhconnelly.play(s1, s2)
    print(board)
    print(dhconnelly.print_board(board))
    print(score)

    board = dhconnelly.initial_board()
    print(board)
    print(dhconnelly.print_board(board))


if __name__ == '__main__':
    main()
