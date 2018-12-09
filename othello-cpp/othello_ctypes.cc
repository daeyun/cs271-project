#include <cstdint>
#include "othello.h"

extern "C" {
void best_move(const char *board_str, uint8_t player, uint8_t strategy, uint8_t depth, uint8_t *out_x, uint8_t *out_y);
}

void best_move(const char *board_str, uint8_t player, uint8_t strategy, uint8_t depth, uint8_t *out_x, uint8_t *out_y) {
  array<uint8_t, 64> board = board_from_string(board_str);

  Position next_move{};
  bool has_next_move = search_next_move(board, player, depth,
                                        [&](const array<uint8_t, 64> &board, uint8_t player, int depth) -> int {
                                          return -minimax(board, player, depth);
                                        }, &next_move);
  if (has_next_move) {
    *out_x = next_move.x;
    *out_y = next_move.y;
  }
}

