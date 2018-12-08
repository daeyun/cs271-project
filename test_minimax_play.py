import othello
import runMiniMax
import copy


def main():
    board = othello.Board()
    minimax = runMiniMax.MiniMax()

    for i in range(8):
        for j in range(8):
            board.force_place_symbol((i, j), '0')

    board.force_place_symbol((3, 3), 'B')
    board.force_place_symbol((4, 4), 'B')

    board.force_place_symbol((3, 4), 'W')
    board.force_place_symbol((4, 3), 'W')

    board.print()
    print("--------------")

    i = 10

    while True:
        i = i-1
        if i == 0:
            break

        temp_board = copy.deepcopy(board)

        move_b = minimax.minimax_search(temp_board, 'B')
        if move_b is not None:
            board.make_move(move_b, 'B', play_test=False)
        board.print()
        print()

        temp_board = copy.deepcopy(board)

        move_w = minimax.minimax_search(temp_board, 'W')
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