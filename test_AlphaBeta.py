import othello
from alphaBeta import alphaBeta


def main():
    board = othello.Board()

    for i in range(8):
        for j in range(8):
            board.force_place_symbol((i, j), '0')

    board.force_place_symbol((3, 3), 'B')
    board.force_place_symbol((4, 4), 'B')

    board.force_place_symbol((3, 4), 'W')
    board.force_place_symbol((4, 3), 'W')

    board.print()
    print("--------------")

    while True:

        move_b = alphaBeta(state=board, depth=3, player='B')
        if move_b is not None:
            board.make_move(move_b, 'B', play_test=False)
        board.print()
        print()

        move_w = alphaBeta(state=board, depth=3, player='W')
        if move_w is not None:
            board.make_move(move_w, 'W', play_test=False)
        board.print()
        print()

        if move_b is None and move_w is None:
            break

    print(board.get_winner() + ' wins!')
    print(board.print())

if __name__ == '__main__':
    main()