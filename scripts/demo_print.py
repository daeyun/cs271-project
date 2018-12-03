import othello


def main():
    board = othello.Board()
    board.force_place_symbol((0, 0), 'W')
    board.force_place_symbol((1, 1), 'B')
    board.force_place_symbol((3, 1), 'W')
    board.print()


if __name__ == '__main__':
    main()
