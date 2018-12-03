import re


class Board(object):
    def __init__(self, symbols=None):
        """
        :param symbols: List of 64 symbols {0, W, B} defining the starting board.
        """
        self.board_size = 8
        self.data = [['0' for _ in range(self.board_size)] for _ in range(self.board_size)]

        if symbols is not None:
            assert len(symbols) == self.board_size ** 2
            for i, item in enumerate(symbols):
                xy = self.subscripts_from_linear_index(i)
                self.force_place_symbol(xy, item)

    def subscripts_from_linear_index(self, i):
        """
        Similar to Matlab function ind2sub, except this is in row-major order.
        Only used for initializing the board.
        """
        assert i >= 0
        assert i < self.board_size ** 2
        x = i % self.board_size
        y = i // self.board_size
        return x, y

    def force_place_symbol(self, xy, symbol):
        assert symbol in ['0', 'W', 'B']
        assert isinstance(xy, (tuple, list)) and len(xy) == 2
        x, y = xy
        self.data[y][x] = symbol

    def print(self):
        for row in self.data:
            for item in row:
                if item == '0':
                    printed_character = '.'
                else:
                    printed_character = item
                print('{} '.format(printed_character), end='')
            print('')

    def get_symbol(self, xy):
        x, y = xy
        return self.data[y][x]

    def is_valid_move(self, xy, player) -> bool:
        assert isinstance(xy, (tuple, list)) and len(xy) == 2
        assert player in ('W', 'B')

        if self.get_symbol(xy) != '0':
            return False

        # TODO
        raise NotImplemented()

    def move(self, xy, player):
        assert isinstance(xy, (tuple, list)) and len(xy) == 2
        assert player in ('W', 'B')

        if not self.is_valid_move(xy, player):
            raise RuntimeError('Invalid move: {}, {}'.format(xy, player))

        self.force_place_symbol(xy, symbol=player)

        # TODO: Flip existing symbols.
        raise NotImplemented()


class Game(object):
    def __init__(self, board: Board):
        self.board = board

    def get_user_input_string(self) -> str:
        input_string = input('Make move (x, y): ')
        return input_string

    def parse_user_input_string(self, input_string) -> tuple:
        m = re.search(r'\(?(\d)[, ]+(\d)\)?', input_string)
        if m is None:
            raise ValueError('Invalid user input: {}'.format(input_string))
        x = int(m.group(1))
        y = int(m.group(2))
        if x < 0 or y < 0 or x >= self.board.board_size or y >= self.board.board_size:
            raise ValueError('Out of range: ({}, {})'.format(x, y))
        return x, y
