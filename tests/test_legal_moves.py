import othello


def main():
    board = othello.Board()
    for i in range(8):
        for j in range(8):
            board.force_place_symbol((i, j), 'B')

    board.force_place_symbol((0, 0), 'W')
    board.force_place_symbol((7, 7), 'W')
    board.force_place_symbol((0, 7), 'W')
    board.force_place_symbol((7, 0), 'W')
    board.force_place_symbol((5, 5), '0')
    board.force_place_symbol((5, 0), 'W')
    board.force_place_symbol((0, 5), 'W')
    board.force_place_symbol((5, 7), 'W')
    board.force_place_symbol((7, 5), 'W')

    board.force_place_symbol((1, 3), '0')

    board.print()

    print(board.get_legal_moves('W'))

if __name__ == '__main__':
    main()