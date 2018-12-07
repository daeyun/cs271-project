import othello


def main():
    board = othello.Board()
    for i in range(8):
        for j in range(8):
            board.force_place_symbol((i, j), '0')

    board.force_place_symbol((4, 4), 'B')
    board.force_place_symbol((5, 5), 'B')

    board.force_place_symbol((4, 5), 'W')
    board.force_place_symbol((5, 4), 'W')

    # board.force_place_symbol((0, 0), 'W')
    # board.force_place_symbol((7, 7), 'W')
    # board.force_place_symbol((0, 7), 'W')
    # board.force_place_symbol((7, 0), 'W')
    # board.force_place_symbol((5, 5), '0')
    # board.force_place_symbol((5, 0), 'W')
    # board.force_place_symbol((0, 5), 'W')
    # board.force_place_symbol((5, 7), 'W')
    # board.force_place_symbol((7, 5), 'W')
    #
    # board.force_place_symbol((1, 3), '0')
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