import re


class Board(object):
    def __init__(self, symbols=None):
        """
        :param symbols: List of 64 symbols {0, W, B} defining the starting board.
        """
        self.board_size = 8
        self.data = [['0' for _ in range(self.board_size)] for _ in range(self.board_size)]

        self.num_whites = 0
        self.num_blacks = 0
        self.turns_played = 0

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
        self.turns_played = 0  # Reset turns when artifically placing pieces
        x, y = xy

        if self.data[y][x] == 'W':
            self.num_whites -= 1
        elif self.data[y][x] == 'B':
            self.num_blacks -= 1

        self.data[y][x] = symbol

        if symbol == 'W':
            self.num_whites += 1
        elif symbol == 'B':
            self.num_blacks += 1

    def print(self):
        print('  {}'.format(' '.join([str(item) for item in range(8)])))

        for i_row, row in enumerate(self.data):
            print('{} '.format(i_row), end='')
            for item in row:
                if item == '0':
                    printed_character = '.'
                else:
                    printed_character = item
                print('{} '.format(printed_character), end='')
            print('')

        print('Number of Black Pieces: ', self.num_blacks)
        print('Number of White Pieces: ', self.num_whites)

    def get_opponent(self, player):
        assert player in ('W', 'B')
        if player == 'W':
            return 'B'
        else:
            return 'W'

    def get_symbol(self, xy):
        x, y = xy
        assert self.is_on_board(x, y)

        return self.data[y][x]

    def is_on_board(self, x, y):
        return x >= 0 and x < self.board_size and y >= 0 and y < self.board_size

    def make_move(self, xy, player, play_test=True):
        assert isinstance(xy, (tuple, list)) and len(xy) == 2
        assert player in ('W', 'B')

        if self.get_symbol(xy) != '0':
            return 0

        board = self.data
        opponent = self.get_opponent(player)

        self.turns_played += 1

        x, y = xy
        board[y][x] = player
        flip_tiles = []

        for dx, dy in [[0, 1], [1, 0], [0, -1], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]:
            x_cur, y_cur = x + dx, y + dy
            flip_count = 0;
            while self.is_on_board(x_cur, y_cur) and board[y_cur][x_cur] == opponent:
                flip_count = flip_count + 1
                x_cur, y_cur = x_cur + dx, y_cur + dy
            if self.is_on_board(x_cur, y_cur) and board[y_cur][x_cur] == player and flip_count > 0:
                while [x_cur, y_cur] != [x, y]:
                    x_cur, y_cur = x_cur - dx, y_cur - dy
                    flip_tiles.append([y_cur, x_cur])

        board[y][x] = '0'

        if len(flip_tiles) == 0:
            return 0

        if not play_test:
            for [y_cur, x_cur] in flip_tiles:
                self.data[y_cur][x_cur] = player
            num_tiles_converted = len(flip_tiles) - 1
            if player == 'W':
                self.num_whites += 1  # Increase by 1 for tile placed on board
                self.num_whites += num_tiles_converted  # Increase again for each tile flipped
                self.num_blacks -= num_tiles_converted  # Opponent loses those number of pieces
            else:
                self.num_blacks += 1  # Increase by 1 for tile placed on board
                self.num_blacks += num_tiles_converted  # Increase again for each tile flipped
                self.num_whites -= num_tiles_converted  # Opponent loses those number of pieces

        return len(flip_tiles)

    def is_valid_move(self, xy, player) -> bool:
        assert isinstance(xy, (tuple, list)) and len(xy) == 2
        assert player in ('W', 'B')

        if self.get_symbol(xy) != '0':
            return False

        score = self.make_move(xy, player, play_test=True)
        return score > 0

    def move(self, xy, player):
        assert isinstance(xy, (tuple, list)) and len(xy) == 2
        assert player in ('W', 'B')

        score = self.make_move(xy, player, play_test=False)
        if score <= 0:
            raise RuntimeError('Invalid move: {}, {}'.format(xy, player))

        return score

    def get_legal_moves(self, player):
        linear_range = self.board_size ** 2
        legal_moves = []
        for i in range(linear_range):
            x, y = self.subscripts_from_linear_index(i)
            if self.is_valid_move((x, y), player):
                legal_moves.append((x, y))
        return legal_moves

    def get_scores(self):
        b_count = 0
        w_count = 0

        linear_range = self.board_size ** 2
        for i in range(linear_range):
            x, y = self.subscripts_from_linear_index(i)
            if self.data[y][x] == 'B':
                b_count = b_count + 1
            elif self.data[y][x] == 'W':
                w_count = w_count + 1

        return b_count, w_count

    def get_winner(self):
        b_count, w_count = self.get_scores()
        if b_count >= w_count:
            return 'B'
        else:
            return 'W'

    def get_corner_disk_count(self):
        n = self.board_size - 1
        corner_disks = []
        corner_positions = [(0, 0), (0, n), (n, 0), (n, n)]
        for pos in corner_positions:
            corner_disks.append(self.data[pos[1]][pos[0]])

        return corner_disks.count('B'), corner_disks.count('W')

    def search_different_tile(self, yx, tile, dir):
        y_cur, x_cur = yx
        while self.is_on_board(x_cur, y_cur) and self.data[y_cur][x_cur] == tile:
            y_cur, x_cur = y_cur + dir[0], x_cur + dir[1]

        if not self.is_on_board(x_cur, y_cur):
            return True

        return False

    def get_permanent_disk_count(self):
        b_count = 0
        w_count = 0

        dir_pairs = [[[0, 1], [0, -1]], [[1, 0], [-1, 0]], [[1, 1], [-1, -1]], [[-1, 1], [1, -1]]]
        for i in range(self.board_size):
            for j in range(self.board_size):
                tile = self.data[i][j]

                if tile == '0':
                    continue

                is_permanent = True
                for dir in dir_pairs:
                    is_permanent = self.search_different_tile((i, j), tile, dir[0]) or self.search_different_tile(
                        (i, j), tile, dir[1])
                    if not is_permanent:
                        break

                if is_permanent:
                    if tile == 'B':
                        b_count = b_count + 1
                    else:
                        w_count = w_count + 1

        return b_count, w_count

    def heuristic_count(self):
        b_count, w_count = self.get_scores()
        return b_count, w_count

    def heuristic_numMoves(self):
        b_count = len(self.get_legal_moves('B'))
        w_count = len(self.get_legal_moves('W'))
        return b_count, w_count

    def heuristic_weighted(self):
        b_score, w_score = self.heuristic_count()
        b_perm, w_perm = self.get_permanent_disk_count()
        b_moves, w_moves = self.heuristic_numMoves()
        return b_score + b_perm + b_moves, w_score + w_perm + w_moves


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
