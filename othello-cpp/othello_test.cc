#define CATCH_CONFIG_MAIN
#include <catch/catch.hpp>
#include "othello.h"

TEST_CASE("IsValidMove", "invalid move") {
  array<uint8_t, 64> board = board_from_string("..........W.......W.BW....WWBB....WWW.....WB.W..................");
  Position pos{};
  pos.x = 1;
  pos.y = 0;
  REQUIRE_FALSE(is_valid_move(board, BLACK, pos));
}

TEST_CASE("Heuristics", "weighted sum") {
  array<uint8_t, 64> board = board_from_string("..................WBBW....WBWB....WBB.....WWWW.....BW.....WB.W..");
  REQUIRE(-92 == weighted_parity_heuristic_1(board, BLACK));
  REQUIRE(92 == weighted_parity_heuristic_1(board, WHITE));
}

TEST_CASE("ApplyMove", "flip") {
  array<uint8_t, 64> board = board_from_string("..................WBBW....WBWB....WBB.....WWWW.....BW.....WB.W..");
  Position pos{.x = 2, .y=6};
  apply_move(&board, BLACK, pos);
  REQUIRE(board[8 * 6 + 2] == BLACK);
  REQUIRE(board[8 * 5 + 2] == WHITE);
  REQUIRE(board[8 * 5 + 3] == BLACK);
  REQUIRE(board[8 * 4 + 4] == BLACK);
  REQUIRE(board[8 * 6 + 3] == BLACK);
  REQUIRE(board[8 * 7 + 2] == WHITE);
}

// https://stackoverflow.com/questions/17074324/how-can-i-sort-two-vectors-in-the-same-way-with-criteria-that-uses-only-one-of
template<typename T, typename Compare>
std::vector<std::size_t> sort_permutation(
    const std::vector<T> &vec,
    Compare compare) {
  std::vector<std::size_t> p(vec.size());
  std::iota(p.begin(), p.end(), 0);
  std::sort(p.begin(), p.end(),
            [&](std::size_t i, std::size_t j) { return compare(vec[i], vec[j]); });
  return p;
}

template<typename T>
std::vector<T> apply_permutation(
    const std::vector<T> &vec,
    const std::vector<std::size_t> &p) {
  std::vector<T> sorted_vec(vec.size());
  std::transform(p.begin(), p.end(), sorted_vec.begin(),
                 [&](std::size_t i) { return vec[i]; });
  return sorted_vec;
}

TEST_CASE("Minimax Depth 1", "check sorted costs") {
  auto searcher = [&](const array<uint8_t, 64> &board, uint8_t player, int depth) -> float {
    return -minimax(board, player, depth, 0);
  };

  uint8_t player = BLACK;
  array<uint8_t, 64> board = board_from_string("..................WBBW....WBWB....WBB.....WWWW.....BW.....WB.W..");
  int depth = 1;

  vector<Position> moves;
  vector<float> values;
  float best = -kInfinity;
  auto opponent = get_opponent(player);
  if (find_valid_moves(board, player, &moves) > 0) {
    for (const auto &move_pos : moves) {
      array<uint8_t, 64> next_board = board;
      apply_move(&next_board, player, move_pos);
      auto value = searcher(next_board, opponent, depth - 1);

      if (value > best) {
        best = value;
      }
      values.push_back(value);
    }
  }

  auto p = sort_permutation(values, [](int const &a, int const &b) { return a > b; });

  values = apply_permutation(values, p);
  moves = apply_permutation(moves, p);

  REQUIRE(values.size() == 16);
  REQUIRE(moves.size() == 16);

  REQUIRE(values[0] == -55);
  REQUIRE(values[1] == -61);
  REQUIRE(values[2] == -67);
  REQUIRE(values[3] == -67);
  REQUIRE(values[15] == -102);

  REQUIRE(moves[0].x == 1);
  REQUIRE(moves[0].y == 4);
  REQUIRE(moves[1].x == 1);
  REQUIRE(moves[1].y == 2);
  REQUIRE(moves[2].x == 5);
  REQUIRE(moves[2].y == 1);

}

TEST_CASE("Minimax Depth 2", "check sorted costs") {
  auto searcher = [&](const array<uint8_t, 64> &board, uint8_t player, int depth) -> float {
    return -minimax(board, player, depth, 0);
  };

  uint8_t player = BLACK;
  array<uint8_t, 64> board = board_from_string("..................WBBW....WBWB....WBB.....WWWW.....BW.....WB.W..");
  int depth = 2;

  vector<Position> moves;
  vector<float> values;
  float best = -kInfinity;
  auto opponent = get_opponent(player);
  if (find_valid_moves(board, player, &moves) > 0) {
    for (const auto &move_pos : moves) {
      array<uint8_t, 64> next_board = board;
      apply_move(&next_board, player, move_pos);
      auto value = searcher(next_board, opponent, depth - 1);

      if (value > best) {
        best = value;
      }
      values.push_back(value);
    }
  }

  auto p = sort_permutation(values, [](int const &a, int const &b) { return a > b; });

  values = apply_permutation(values, p);
  moves = apply_permutation(moves, p);

  REQUIRE(values.size() == 16);
  REQUIRE(moves.size() == 16);

  REQUIRE(values[0] == -82);
  REQUIRE(values[1] == -93);
  REQUIRE(values[2] == -102);
  REQUIRE(values[3] == -102);
  REQUIRE(values[4] == -104);
  REQUIRE(values[5] == -108);
  REQUIRE(values[15] == -184);

  REQUIRE(moves[0].x == 1);
  REQUIRE(moves[0].y == 4);
  REQUIRE(moves[1].x == 1);
  REQUIRE(moves[1].y == 7);
  REQUIRE(moves[4].x == 1);
  REQUIRE(moves[4].y == 5);
}

TEST_CASE("Minimax Depth 5", "check sorted costs") {
  auto searcher = [&](const array<uint8_t, 64> &board, uint8_t player, int depth) -> float {
    return -minimax(board, player, depth, 0);
  };

  uint8_t player = BLACK;
  array<uint8_t, 64> board = board_from_string("..................WBBW....WBWB....WBB.....WWWW.....BW.....WB.W..");
  int depth = 5;

  vector<Position> moves;
  vector<float> values;
  float best = -kInfinity;
  auto opponent = get_opponent(player);
  if (find_valid_moves(board, player, &moves) > 0) {
    for (const auto &move_pos : moves) {
      array<uint8_t, 64> next_board = board;
      apply_move(&next_board, player, move_pos);
      auto value = searcher(next_board, opponent, depth - 1);

//      printf("(%d, %d): %d\n", move_pos.x, move_pos.y, value);

      if (value > best) {
        best = value;
      }
      values.push_back(value);
    }
  }

  auto p = sort_permutation(values, [](int const &a, int const &b) { return a > b; });

  values = apply_permutation(values, p);
  moves = apply_permutation(moves, p);

  REQUIRE(values.size() == 16);
  REQUIRE(moves.size() == 16);

  REQUIRE(values[0] == -39);
  REQUIRE(values[1] == -39);
  REQUIRE(values[2] == -42);
  REQUIRE(values[3] == -47);
  REQUIRE(values[4] == -54);
  REQUIRE(values[5] == -55);
  REQUIRE(values[6] == -57);
  REQUIRE(values[15] == -131);

  REQUIRE(moves[2].x == 1);
  REQUIRE(moves[2].y == 7);
  REQUIRE(moves[3].x == 5);
  REQUIRE(moves[3].y == 4);

//  printf("\n\n");
//
//  for (int i = 0; i < values.size(); ++i) {
//    printf("(%d, %d): %d\n", moves[i].x, moves[i].y, values[i]);
//  }

}

TEST_CASE("Minimax with alpha beta pruning. Depth 5", "check sorted costs") {
  auto searcher = [&](const array<uint8_t, 64> &board, uint8_t player, int depth) -> float {
    return -minimax_ab(board, player, depth, -kInfinity, kInfinity, 0);
  };

  uint8_t player = BLACK;
  array<uint8_t, 64> board = board_from_string("..................WBBW....WBWB....WBB.....WWWW.....BW.....WB.W..");
  int depth = 5;

  vector<Position> moves;
  vector<float> values;
  float best = -std::numeric_limits<float>::infinity();
  auto opponent = get_opponent(player);
  if (find_valid_moves(board, player, &moves) > 0) {
    for (const auto &move_pos : moves) {
      array<uint8_t, 64> next_board = board;
      apply_move(&next_board, player, move_pos);
      auto value = searcher(next_board, opponent, depth - 1);

      if (value > best) {
        best = value;
      }
      values.push_back(value);
    }
  }

  auto p = sort_permutation(values, [](int const &a, int const &b) { return a > b; });

  values = apply_permutation(values, p);
  moves = apply_permutation(moves, p);

  REQUIRE(values.size() == 16);
  REQUIRE(moves.size() == 16);

  REQUIRE(values[0] == -39);
  REQUIRE(values[1] == -39);
  REQUIRE(values[2] == -42);
  REQUIRE(values[3] == -47);
  REQUIRE(values[4] == -54);
  REQUIRE(values[5] == -55);
  REQUIRE(values[6] == -57);
  REQUIRE(values[15] == -131);

  REQUIRE(moves[2].x == 1);
  REQUIRE(moves[2].y == 7);
  REQUIRE(moves[3].x == 5);
  REQUIRE(moves[3].y == 4);
}

TEST_CASE("Minimax with alpha beta pruning and lookup table. Depth 5", "check sorted costs") {
  auto searcher = [&](const array<uint8_t, 64> &board, uint8_t player, int depth) -> float {
    unordered_map<string, TTEntry> table;
    return -minimax_ab_transposition(board, player, depth, -kInfinity, kInfinity, 0, &table);
  };

  uint8_t player = BLACK;
  array<uint8_t, 64> board = board_from_string("..................WBBW....WBWB....WBB.....WWWW.....BW.....WB.W..");
  int depth = 5;

  vector<Position> moves;
  vector<float> values;
  float best = -std::numeric_limits<float>::infinity();
  auto opponent = get_opponent(player);
  if (find_valid_moves(board, player, &moves) > 0) {
    for (const auto &move_pos : moves) {
      array<uint8_t, 64> next_board = board;
      apply_move(&next_board, player, move_pos);
      auto value = searcher(next_board, opponent, depth - 1);

      if (value > best) {
        best = value;
      }
      values.push_back(value);
    }
  }

  auto p = sort_permutation(values, [](int const &a, int const &b) { return a > b; });

  values = apply_permutation(values, p);
  moves = apply_permutation(moves, p);

  REQUIRE(values.size() == 16);
  REQUIRE(moves.size() == 16);

  REQUIRE(values[0] == -39);
  REQUIRE(values[1] == -39);
  REQUIRE(values[2] == -42);
  REQUIRE(values[3] == -47);
  REQUIRE(values[4] == -54);
  REQUIRE(values[5] == -55);
  REQUIRE(values[6] == -57);
  REQUIRE(values[15] == -131);

  REQUIRE(moves[2].x == 1);
  REQUIRE(moves[2].y == 7);
  REQUIRE(moves[3].x == 5);
  REQUIRE(moves[3].y == 4);
}
