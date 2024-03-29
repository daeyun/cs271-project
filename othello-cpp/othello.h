#pragma once

#include <iostream>
#include <string>
#include <array>
#include <vector>
#include <functional>
#include <limits>
#include <random>
#include <algorithm>
#include <map>
#include <unordered_map>
#include <omp.h>

using std::array;
using std::vector;
using std::map;
using std::string;
using std::unordered_map;

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

enum class TTFlag {
  UPPERBOUND, LOWERBOUND, EXACT
};

struct TTEntry {
  float value;
  TTFlag flag;
  uint8_t depth;
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
        if (moves) {
          moves->push_back(pos);
        }
      }
    }
  }
  return num_found;
}

void order_moves(vector<Position> *moves) {
  // Same weights as:
  // https://github.com/dhconnelly/paip-python/blob/master/paip/othello.py
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

  std::sort(moves->begin(), moves->end(), [](const Position &a, const Position &b) {
    return weights[a.x + a.y * 8] > weights[b.x + b.y * 8];
  });

//  std::shuffle(moves->begin(), moves->end(), RandomEngine());
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

float weighted_parity_heuristic_1(const array<uint8_t, 64> &board, uint8_t player) {
  // Same weights as:
  // https://github.com/dhconnelly/paip-python/blob/master/paip/othello.py
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

float weighted_parity_heuristic_2(const array<uint8_t, 64> &board, uint8_t player) {
  // Same weights as:
  // https://github.com/dhconnelly/paip-python/blob/master/paip/othello.py
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

  int player_sum = 0;
  int opponent_sum = 0;
  auto opponent = get_opponent(player);
  for (int i = 0; i < 64; ++i) {
    const auto value = board[i];
    if (value == player) {
      player_sum += weights[i];
    } else if (value == opponent) {
      opponent_sum += weights[i];
    }
  }

//  float ret = static_cast<float>(player_sum - opponent_sum + 1) / (player_sum + opponent_sum + 1);
  float ret = static_cast<float>(player_sum - opponent_sum + 1) / (std::abs(player_sum) + std::abs(opponent_sum) + 1);
  return ret;
}

float weighted_parity_heuristic_3(const array<uint8_t, 64> &board, uint8_t player) {
  // https://courses.cs.washington.edu/courses/cse573/04au/Project/mini1/RUSSIA/Final_Paper.pdf
  static int weights[] = {
      4, -3, 2, 2, 2, 2, -3, 4,
      -3, -4, -1, -1, -1, -1, -4, -3,
      2, -1, 1, 0, 0, 1, -1, 2,
      2, -1, 0, 1, 1, 0, -1, 2,
      2, -1, 0, 1, 1, 0, -1, 2,
      2, -1, 1, 0, 0, 1, -1, 2,
      -3, -4, -1, -1, -1, -1, -4, -3,
      4, -3, 2, 2, 2, 2, -3, 4
  };

  int player_sum = 0;
  int opponent_sum = 0;
  auto opponent = get_opponent(player);
  for (int i = 0; i < 64; ++i) {
    const auto value = board[i];
    if (value == player) {
      player_sum += weights[i];
    } else if (value == opponent) {
      opponent_sum += weights[i];
    }
  }

  float ret = static_cast<float>(player_sum - opponent_sum + 1) / (std::abs(player_sum) + std::abs(opponent_sum) + 1);
  return ret;
}

float parity_heuristic(const array<uint8_t, 64> &board, uint8_t player) {
  int ret = 0;
  auto opponent = get_opponent(player);
  for (int i = 0; i < 64; ++i) {
    const auto value = board[i];
    if (value == player) {
      ret += 1;
    } else if (value == opponent) {
      ret -= 1;
    }
  }
  return ret;
}

float mobility_heuristic(const array<uint8_t, 64> &board, uint8_t player) {
  // Number of possible moves.
  int num_valid_moves_player = find_valid_moves(board, player, nullptr);
  int num_valid_moves_opponent = find_valid_moves(board, get_opponent(player), nullptr);
  return static_cast<float>(num_valid_moves_player - num_valid_moves_opponent + 1)
      / (num_valid_moves_player + num_valid_moves_opponent + 1);
}

float permanent_disk_heuristic(const array<uint8_t, 64> &board, uint8_t player) {
  std::function<bool(const array<uint8_t, 64> &board, int x, int y, Direction direction)> touches_border;
  touches_border = [&](const array<uint8_t, 64> &board, int x, int y, Direction direction) -> bool {
    int dx = 0, dy = 0;
    direction_delta(direction, &dx, &dy);

    uint8_t ref_value = board[x + y * 8];
    int search_x = x;
    int search_y = y;

    bool ret = true;
    while (true) {
      search_x += dx;
      search_y += dy;
      if (search_x < 0 or search_x >= 8 or search_y < 0 or search_y >= 8) {
        break;  // Out of range.
      }
      auto value = board[search_x + search_y * 8];
      if (value != ref_value) {
        // If we encounter another symbol before going out of range, it does not touch the border.
        ret = false;
        break;
      }
    };
    return ret;
  };

  const auto is_definitely_permanent = [&](const array<uint8_t, 64> &board, int x, int y) {
    Direction direction_pairs[][2] = {
        {Direction::DOWN_LEFT, Direction::UP_RIGHT},
        {Direction::DOWN_RIGHT, Direction::UP_LEFT},
        {Direction::UP, Direction::DOWN},
        {Direction::LEFT, Direction::RIGHT},
    };

    for (const auto &pair : direction_pairs) {
      // If we see any pairs not touching the border in at least one direction, this disk may not be permanent.
      if (!touches_border(board, x, y, pair[0]) and !touches_border(board, x, y, pair[1])) {
        return false;
      }
    }
    return true;
  };

  int player_permanent_count = 0;
  int opponent_permanent_count = 0;

  uint8_t opponent = get_opponent(player);

  for (int y = 0; y < 8; ++y) {
    for (int x = 0; x < 8; ++x) {
      auto value = board[x + y * 8];
      if (value == EMPTY) {
        continue;
      }
      if (is_definitely_permanent(board, x, y)) {
        if (value == player) {
          ++player_permanent_count;
        } else if (value == opponent) {
          ++opponent_permanent_count;
        }
      }
    }
  }

  return static_cast<float>(player_permanent_count - opponent_permanent_count + 1)
      / (player_permanent_count + player_permanent_count + 1);
}

float heuristic(const array<uint8_t, 64> &board, uint8_t player, int heuristic_type) {
  switch (heuristic_type) {
    case 0: return weighted_parity_heuristic_1(board, player);
    case 1: return weighted_parity_heuristic_2(board, player);
    case 2: return weighted_parity_heuristic_3(board, player);
    case 3: return parity_heuristic(board, player);
    case 4: return mobility_heuristic(board, player);
    case 5: return permanent_disk_heuristic(board, player);
    case 6: return weighted_parity_heuristic_2(board, player) + mobility_heuristic(board, player);
    case 7: return weighted_parity_heuristic_2(board, player) + 0.5f * mobility_heuristic(board, player);
    case 8:
      return weighted_parity_heuristic_2(board, player) * 4 + mobility_heuristic(board, player) * 5
          + permanent_disk_heuristic(board, player) * 6;
//      return weighted_parity_heuristic_1(board, player) * 0.5 + mobility_heuristic(board, player) * 4
//          + permanent_disk_heuristic(board, player) * 4;
    default: return 0; // random
  }
}

// https://en.wikipedia.org/wiki/Negamax#Negamax_base_algorithm
float minimax(const array<uint8_t, 64> &board, uint8_t player, int depth, int heuristic_type) {
  if (depth <= 0) {
    return heuristic(board, player, heuristic_type);
  }
  vector<Position> moves;
  find_valid_moves(board, player, &moves);
  auto opponent = get_opponent(player);
  if (moves.empty() and !any_valid_move(board, opponent)) {
    // Terminal node. Game ending condition.
//    return heuristic(board, player, heuristic_type);
    return static_cast<float>((parity_heuristic(board, player) > 0) ? 1 : -1) * 10000;
  }

  float best = -kInfinity;
  for (const auto &move_pos : moves) {
    array<uint8_t, 64> next_board = board;
    apply_move(&next_board, player, move_pos);
    best = std::max(best, -minimax(next_board, opponent, depth - 1, heuristic_type));
  }
  if (best == -kInfinity) {
    best = -minimax(board, opponent, depth - 1, heuristic_type);
  }

  return best;
}

// https://en.wikipedia.org/wiki/Negamax#Negamax_with_alpha_beta_pruning
float minimax_ab(const array<uint8_t, 64> &board, uint8_t player, int depth,
                 float alpha, float beta, int heuristic_type) {
  if (depth <= 0) {
    return heuristic(board, player, heuristic_type);
  }
  vector<Position> moves;
  find_valid_moves(board, player, &moves);
  auto opponent = get_opponent(player);
  if (moves.empty() and !any_valid_move(board, opponent)) {
    // Terminal node. Game ending condition.
//    return heuristic(board, player, heuristic_type);
    return static_cast<float>((parity_heuristic(board, player) > 0) ? 1 : -1) * 10000;
  }

  order_moves(&moves);

  float best = -kInfinity;
  for (const auto &move_pos : moves) {
    array<uint8_t, 64> next_board = board;
    apply_move(&next_board, player, move_pos);
    best = std::max(best, -minimax_ab(next_board, opponent, depth - 1, -beta, -alpha, heuristic_type));
    alpha = std::max(alpha, best);
    if (alpha >= beta) {
      break;
    }
  }
  if (best == -kInfinity) {
    best = -minimax_ab(board, opponent, depth - 1, -beta, -alpha, heuristic_type);
  }
  return best;
}

// https://en.wikipedia.org/wiki/Negamax#Negamax_with_alpha_beta_pruning_and_transposition_tables
float minimax_ab_transposition(const array<uint8_t, 64> &board,
                               uint8_t player,
                               int depth,
                               float alpha,
                               float beta,
                               int heuristic_type,
                               unordered_map<string, TTEntry> *table) {
  if (depth <= 0) {
    return heuristic(board, player, heuristic_type);
  }

  float alpha_orig = alpha;

  const string board_str(reinterpret_cast<const char *>(board.data()), 64);
  auto it = table->find(board_str);
  bool is_valid_lookup = it != table->end();
  if (is_valid_lookup) {
    auto tt_entry = it->second;
    if (tt_entry.depth >= depth) {
      if (tt_entry.flag == TTFlag::EXACT) {
        return tt_entry.value;
      } else if (tt_entry.flag == TTFlag::LOWERBOUND) {
        alpha = std::max(alpha, tt_entry.value);
      } else {  // UPPERBOUND
        beta = std::min(beta, tt_entry.value);
      }

      if (alpha >= beta) {
        return tt_entry.value;
      }
    }
  }

  vector<Position> moves;
  find_valid_moves(board, player, &moves);
  auto opponent = get_opponent(player);
  if (moves.empty() and !any_valid_move(board, opponent)) {
    // Terminal node. Game ending condition.
//    return heuristic(board, player, heuristic_type);
    return static_cast<float>((parity_heuristic(board, player) > 0) ? 1 : -1) * 10000;
  }

  order_moves(&moves);

  float best = -kInfinity;
  for (const auto &move_pos : moves) {
    array<uint8_t, 64> next_board = board;
    apply_move(&next_board, player, move_pos);
    best = std::max(best,
                    -minimax_ab_transposition(next_board, opponent, depth - 1, -beta, -alpha, heuristic_type, table));
    alpha = std::max(alpha, best);
    if (alpha >= beta) {
      break;
    }
  }
  if (best == -kInfinity) {
    best = -minimax_ab_transposition(board, opponent, depth - 1, -beta, -alpha, heuristic_type, table);
  }

  // Add new entry.
  auto &tt_entry = (*table)[board_str];
  tt_entry.value = best;
  if (best <= alpha_orig) {
    tt_entry.flag = TTFlag::UPPERBOUND;
  } else if (best >= beta) {
    tt_entry.flag = TTFlag::LOWERBOUND;
  } else {
    tt_entry.flag = TTFlag::EXACT;
  }
  tt_entry.depth = static_cast<uint8_t>(depth);  // Assume depth < 256.

  return best;
}

bool search_next_move(const array<uint8_t, 64> &board, uint8_t player, int depth,
                      const std::function<float(const array<uint8_t, 64> &board, uint8_t player,
                                                int depth)> &searcher, Position *next_move) {
  vector<Position> moves;
  float best = -kInfinity;
  auto opponent = get_opponent(player);
  if (find_valid_moves(board, player, &moves) > 0) {
    vector<float> values(moves.size());

#pragma omp parallel for schedule(auto)
    for (int j = 0; j < moves.size(); ++j) {
      const auto &move_pos = moves[j];
      array<uint8_t, 64> next_board = board;
      apply_move(&next_board, player, move_pos);
      auto value = searcher(next_board, opponent, depth - 1);

#pragma omp critical
      {
        if (value > best) {
          best = value;
        }
      };
      values[j] = value;
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
