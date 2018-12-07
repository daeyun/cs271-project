import othello


def main():
    board = othello.Board()

    board.force_place_symbol((4, 4), 'W')
    board.force_place_symbol((5, 5), 'W')
    board.force_place_symbol((4, 5), 'B')
    board.force_place_symbol((5, 4), 'B')

    board.print()
    print("--------------")

    while True:
        B_moves = board.get_legal_moves('B')
        if len(B_moves) > 0:
            board.make_move(B_moves[0], 'B', play_test=False)
            board.print()
            print()
        else:
            break

        W_moves = board.get_legal_moves('W')
        if len(W_moves) > 0:
            board.make_move(W_moves[0], 'W', play_test=False)
            board.print()
            print()
        else:
            break

    print(board.get_winner() + ' wins!')
    print(board.print())

if __name__ == '__main__':
    main()