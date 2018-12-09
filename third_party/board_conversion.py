import othello


def convert_to_dhconnelly_board(board):
    assert isinstance(board, othello.Board)

    ret = ['?', '?', '?', '?', '?', '?', '?', '?', '?', '?',
           '?', '.', '.', '.', '.', '.', '.', '.', '.', '?',
           '?', '.', '.', '.', '.', '.', '.', '.', '.', '?',
           '?', '.', '.', '.', '.', '.', '.', '.', '.', '?',
           '?', '.', '.', '.', '.', '.', '.', '.', '.', '?',
           '?', '.', '.', '.', '.', '.', '.', '.', '.', '?',
           '?', '.', '.', '.', '.', '.', '.', '.', '.', '?',
           '?', '.', '.', '.', '.', '.', '.', '.', '.', '?',
           '?', '.', '.', '.', '.', '.', '.', '.', '.', '?',
           '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', ]

    for y in range(8):
        for x in range(8):
            symbol = board.get_symbol((x, y))

            if symbol == '0':
                continue

            assert symbol in ('W', 'B'), symbol
            ret[(y + 1) * 10 + (x + 1)] = 'o' if symbol == 'W' else '@'

    return ret


def convert_to_our_cpp_board(board):
    assert isinstance(board, othello.Board)

    ret = [
        '.', '.', '.', '.', '.', '.', '.', '.',
        '.', '.', '.', '.', '.', '.', '.', '.',
        '.', '.', '.', '.', '.', '.', '.', '.',
        '.', '.', '.', '.', '.', '.', '.', '.',
        '.', '.', '.', '.', '.', '.', '.', '.',
        '.', '.', '.', '.', '.', '.', '.', '.',
        '.', '.', '.', '.', '.', '.', '.', '.',
        '.', '.', '.', '.', '.', '.', '.', '.',
    ]

    for y in range(8):
        for x in range(8):
            symbol = board.get_symbol((x, y))

            if symbol == '0':
                continue

            assert symbol in ('W', 'B'), symbol
            ret[y * 8 + x] = symbol

    return ''.join(ret)
