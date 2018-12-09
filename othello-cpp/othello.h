#pragma once

#include <iostream>
#include <string>
#include <array>
#include <vector>
#include <functional>
#include <limits>
#include <random>
#include <algorithm>

using std::array;
using std::vector;

#define EMPTY 255
#define BLACK 0
#define WHITE 1

constexpr float kInfinity = std::numeric_limits<float>::infinity();

enum class Direction {
  UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT
};

struct Position {
  uint8_t x, y;
};

static std::mt19937 &RandomEngine() {
  thread_local static std::mt19937 engine{std::random_device{}()};
  return engine;
}

void print_board(const array<uint8_t, 64> &board) {
  for (int i = 0; i < 64; ++i) {
    if (board[i] == EMPTY) {
      std::cout << ".";
    } else if (board[i] == BLACK) {
      std::cout << "@";
    } else if (board[i] == WHITE) {
      std::cout << "O";
    }
    if (i % 8 == 7 && i > 0) {
      std::cout << std::endl;
    }
  }
}

array<uint8_t, 64> board_from_string(const char *board_str) {
  array<uint8_t, 64> board{};
  for (int i = 0; i < 64; ++i) {
    if (board_str[i] == '.') {
      board[i] = EMPTY;
    } else if (board_str[i] == 'B') {
      board[i] = BLACK;
    } else if (board_str[i] == 'W') {
      board[i] = WHITE;
    } else {
      throw std::runtime_error("Invalid value found in board.");
    }
  }
  return board;
}

inline uint8_t get_opponent(uint8_t player) {
  return static_cast<uint8_t>((player == BLACK) ? WHITE : BLACK);
}

inline void direction_delta(Direction direction, int *dx, int *dy) {
  if (direction == Direction::UP) {
    *dx = 0;
    *dy = -1;
  } else if (direction == Direction::UP_RIGHT) {
    *dx = 1;
    *dy = -1;
  } else if (direction == Direction::RIGHT) {
    *dx = 1;
    *dy = 0;
  } else if (direction == Direction::DOWN_RIGHT) {
    *dx = 1;
    *dy = 1;
  } else if (direction == Direction::DOWN) {
    *dx = 0;
    *dy = 1;
  } else if (direction == Direction::DOWN_LEFT) {
    *dx = -1;
    *dy = 1;
  } else if (direction == Direction::LEFT) {
    *dx = -1;
    *dy = 0;
  } else if (direction == Direction::UP_LEFT) {
    *dx = -1;
    *dy = -1;
  } else {
    throw std::runtime_error("Unexpected direction");
  }
}

bool find_line_ending(const array<uint8_t, 64> &board, uint8_t player, Position pos, Direction direction,
                      uint8_t *out_x, uint8_t *out_y) {
  int search_x = pos.x;
  int search_y = pos.y;

  // Query position must be empty.
  if (search_x < 0 or search_x >= 8 or search_y < 0 or search_y >= 8 or board[search_x + search_y * 8] != EMPTY) {
    return false;
  }

  int dx = 0, dy = 0;
  direction_delta(direction, &dx, &dy);

  const uint8_t opponent = get_opponent(player);

  search_x += dx;
  search_y += dy;
  // Adjacent piece must be opponent's.
  if (search_x < 0 or search_x >= 8 or search_y < 0 or search_y >= 8 or board[search_x + search_y * 8] != opponent) {
    return false;
  }

  // Now search for ours.
  while (true) {
    search_x += dx;
    search_y += dy;
    if (search_x < 0 or search_x >= 8 or search_y < 0 or search_y >= 8) {
      break;  // Out of range.
    }
    auto value = board[search_x + search_y * 8];
    if (value == player) {
      if (out_x) {
        *out_x = static_cast<uint8_t>(search_x);
      }
      if (out_y) {
        *out_y = static_cast<uint8_t>(search_y);
      }
      return true;
    } else if (value == EMPTY) {
      break;
    }
    // Otherwise opponent's piece.
  };
  return false;
}

bool is_valid_move(const array<uint8_t, 64> &board, uint8_t player, Position pos) {
  Direction directions[] = {
      Direction::UP, Direction::UP_RIGHT, Direction::RIGHT, Direction::DOWN_RIGHT,
      Direction::DOWN, Direction::DOWN_LEFT, Direction::LEFT, Direction::UP_LEFT,
  };

  for (const auto &direction : directions) {
    if (find_line_ending(board, player, pos, direction, nullptr, nullptr)) {
      return true;
    };
  }
  return false;
}

int find_valid_moves(const array<uint8_t, 64> &board, uint8_t player, vector<Position> *moves) {
  int num_found = 0;
  for (int y = 0; y < 8; ++y) {
    for (int x = 0; x < 8; ++x) {
      // Valid move position must be empty.
      if (board[x + y * 8] != EMPTY) {
        continue;
      }
      Position pos{
          .x = static_cast<uint8_t>(x),
          .y = static_cast<uint8_t>(y),
      };
      if (is_valid_move(board, player, pos)) {
        ++num_found;
        moves->push_back(pos);
      }
    }
  }
  return num_found;
}

bool any_valid_move(const array<uint8_t, 64> &board, uint8_t player) {
  int num_found = 0;
  for (int y = 0; y < 8; ++y) {
    for (int x = 0; x < 8; ++x) {
      // Valid move position must be empty.
      if (board[x + y * 8] != EMPTY) {
        continue;
      }
      Position pos{
          .x = static_cast<uint8_t>(x),
          .y = static_cast<uint8_t>(y),
      };
      if (is_valid_move(board, player, pos)) {
        return true;
      }
    }
  }
  return false;
}

// Assumes `move_pos` is valid.
void apply_move(array<uint8_t, 64> *board, uint8_t player, Position move_pos) {
  Direction directions[] = {
      Direction::UP, Direction::UP_RIGHT, Direction::RIGHT, Direction::DOWN_RIGHT,
      Direction::DOWN, Direction::DOWN_LEFT, Direction::LEFT, Direction::UP_LEFT,
  };

  bool flipped_any = false;
  for (const auto &direction : directions) {
    uint8_t end_x, end_y;
    if (!find_line_ending(*board, player, move_pos, direction, &end_x, &end_y)) {
      continue;
    }
    flipped_any = true;

    int dx = 0, dy = 0;
    direction_delta(direction, &dx, &dy);

    int search_x = move_pos.x + dx;
    int search_y = move_pos.y + dy;

    while (search_x != end_x or search_y != end_y) {
      (*board)[search_x + search_y * 8] = player;
      search_x += dx;
      search_y += dy;
    };
  }

  // `find_line_ending` assumes the query position is empty. So we fill it last.
  if (flipped_any) {
    (*board)[move_pos.x + move_pos.y * 8] = player;
  }

}

int weighted_sum_heuristic(const array<uint8_t, 64> &board, uint8_t player) {
  static int weights[] = {
      120, -20, 20, 5, 5, 20, -20, 120,
      -20, -40, -5, -5, -5, -5, -40, -20,
      20, -5, 15, 3, 3, 15, -5, 20,
      5, -5, 3, 3, 3, 3, -5, 5,
      5, -5, 3, 3, 3, 3, -5, 5,
      20, -5, 15, 3, 3, 15, -5, 20,
      -20, -40, -5, -5, -5, -5, -40, -20,
      120, -20, 20, 5, 5, 20, -20, 120,
  };

  int ret = 0;
  auto opponent = get_opponent(player);
  for (int i = 0; i < 64; ++i) {
    const auto value = board[i];
    if (value == player) {
      ret += weights[i];
    } else if (value == opponent) {
      ret -= weights[i];
    }
  }
  return ret;
}

// https://en.wikipedia.org/wiki/Negamax#Negamax_base_algorithm
float minimax(const array<uint8_t, 64> &board, uint8_t player, int depth) {
  if (depth <= 0) {
    return weighted_sum_heuristic(board, player);
  }
  vector<Position> moves;
  find_valid_moves(board, player, &moves);
  auto opponent = get_opponent(player);
  if (moves.empty() and !any_valid_move(board, opponent)) {
    // Terminal node. Game ending condition.
    return weighted_sum_heuristic(board, player);
  }

  float best = -kInfinity;
  for (const auto &move_pos : moves) {
    array<uint8_t, 64> next_board = board;
    apply_move(&next_board, player, move_pos);
    best = std::max(best, -minimax(next_board, opponent, depth - 1));
  }
  return best;
}

// https://en.wikipedia.org/wiki/Negamax#Negamax_with_alpha_beta_pruning
float minimax_ab(const array<uint8_t, 64> &board, uint8_t player, int depth, float alpha, float beta) {
  if (depth <= 0) {
    return weighted_sum_heuristic(board, player);
  }
  vector<Position> moves;
  find_valid_moves(board, player, &moves);
  auto opponent = get_opponent(player);
  if (moves.empty() and !any_valid_move(board, opponent)) {
    // Terminal node. Game ending condition.
    return weighted_sum_heuristic(board, player);
  }

  // TODO: Move ordering

  float best = -kInfinity;
  for (const auto &move_pos : moves) {
    array<uint8_t, 64> next_board = board;
    apply_move(&next_board, player, move_pos);
    best = std::max(best, -minimax_ab(next_board, opponent, depth - 1, -beta, -alpha));
    alpha = std::max(alpha, best);
    if (alpha >= beta) {
      break;
    }
  }
  return best;
}

bool search_next_move(const array<uint8_t, 64> &board, uint8_t player, int depth,
                      const std::function<float(const array<uint8_t, 64> &board, uint8_t player,
                                                int depth)> &searcher, Position *next_move) {
  vector<Position> moves;
  vector<float> values;
  float best = -kInfinity;
  auto opponent = get_opponent(player);
  if (find_valid_moves(board, player, &moves) > 0) {
    for (const auto &move_pos : moves) {
//      printf("%d, %d\n", static_cast<int>(move_pos.x), static_cast<int>(move_pos.y));
      array<uint8_t, 64> next_board = board;
      apply_move(&next_board, player, move_pos);
      auto value = searcher(next_board, opponent, depth - 1);
      if (value > best) {
        best = value;
      }
      values.push_back(value);
    }

    std::vector<Position> best_moves;
    for (int i = 0; i < values.size(); ++i) {
      if (values[i] == best) {
        best_moves.push_back(moves[i]);
      }
    }
    auto n = static_cast<int>(best_moves.size());
    *next_move = best_moves[std::uniform_int_distribution<decltype(n)>{0, n - 1}(RandomEngine())];
    return true;
  }
  // No valid moves.
  return false;
}
