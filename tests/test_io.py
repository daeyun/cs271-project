import pytest
import othello


def test_input_parser():
    board = othello.Board()  # empty board
    game = othello.Game(board)

    xy = game.parse_user_input_string('(0, 1)')
    assert isinstance(xy, tuple)
    assert len(xy) == 2
    assert xy[0] == 0
    assert xy[1] == 1

    for valid_input_string in ['(1, 0)', '1,0', '1 0', '  1 0  ', '  (1 0)', '(1 0']:
        xy = game.parse_user_input_string(valid_input_string)
        assert isinstance(xy, tuple)
        assert len(xy) == 2
        assert xy[0] == 1
        assert xy[1] == 0

    for invalid_input_string in ['9999, 0', '0, 9999', '0, -1', '(10)', '1', ', 0', '  a, b  ', '(1, a)', 'b, 0']:
        with pytest.raises(ValueError):
            game.parse_user_input_string(invalid_input_string)
