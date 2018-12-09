import ctypes
import time
from os import path
from sys import platform
from ctypes import cdll

ctypes_lib_dirname = path.realpath(path.join(path.dirname(__file__), 'othello-cpp/cmake-build-release/'))

lib = None
if platform == "linux" or platform == "linux2":
    lib_filename = path.join(ctypes_lib_dirname, 'libothello.so')
    assert path.isfile(lib_filename), 'file does not exist: {}'.format(lib_filename)
    lib = cdll.LoadLibrary(lib_filename)
else:
    raise NotImplemented(platform)

if lib:
    c_func = getattr(lib, 'best_move')
    c_func.restype = None
    c_func.argtypes = [
        ctypes.c_char_p,  # board string
        ctypes.c_uint8,  # player index
        ctypes.c_uint8,  # strategy index
        ctypes.c_uint8,  # search depth
        ctypes.POINTER(ctypes.c_uint8),
        ctypes.POINTER(ctypes.c_uint8),
    ]


def best_move(board, player, strategy, depth):
    c_func_name = 'best_move'
    c_func = getattr(lib, c_func_name)

    player_indices = {
        'B': 0,
        'W': 1,
    }
    strategy_indices = {
        'minimax': 0,
    }

    assert player in player_indices
    assert strategy in strategy_indices
    assert 0 < depth < 64, depth

    arg_board = ctypes.c_char_p(board.encode('utf-8'))

    arg_player = ctypes.c_uint8(player_indices[player])
    arg_strategy = ctypes.c_uint8(strategy_indices[strategy])
    arg_depth = ctypes.c_uint8(depth)

    arg_x = ctypes.c_uint8(255)
    arg_y = ctypes.c_uint8(255)

    start_time = time.time()
    c_func(
        arg_board, arg_player, arg_strategy, arg_depth, arg_x, arg_y
    )
    elapsed = time.time() - start_time

    x, y = arg_x.value, arg_y.value

    if x == 255 or y == 255:
        return None, elapsed
    return (x, y), elapsed
