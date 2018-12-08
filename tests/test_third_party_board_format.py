import othello
from third_party import board_conversion
from third_party import dhconnelly


def test_board_conversion_dhconnelly():
    board = othello.Board()  # empty board
    board.force_place_symbol((0, 0), 'W')
    board.force_place_symbol((1, 1), 'B')
    board.force_place_symbol((3, 1), 'B')
    board.force_place_symbol((4, 2), 'W')
    board.print()

    converted_board = board_conversion.convert_to_dhconnelly_board(board)

    print()
    print(dhconnelly.print_board(converted_board))

    assert len(converted_board) == 100

    target = ['?', '?', '?', '?', '?', '?', '?', '?', '?', '?',
              '?', 'o', '.', '.', '.', '.', '.', '.', '.', '?',
              '?', '.', '@', '.', '@', '.', '.', '.', '.', '?',
              '?', '.', '.', '.', '.', 'o', '.', '.', '.', '?',
              '?', '.', '.', '.', '.', '.', '.', '.', '.', '?',
              '?', '.', '.', '.', '.', '.', '.', '.', '.', '?',
              '?', '.', '.', '.', '.', '.', '.', '.', '.', '?',
              '?', '.', '.', '.', '.', '.', '.', '.', '.', '?',
              '?', '.', '.', '.', '.', '.', '.', '.', '.', '?',
              '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', ]

    assert converted_board == target
