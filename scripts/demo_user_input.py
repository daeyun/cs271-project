import othello


def main():
    game = othello.Game(othello.Board())
    game.board.print()  # Print empty board
    input_string = game.get_user_input_string()  # Prompts for console input.
    xy = game.parse_user_input_string(input_string)
    game.board.force_place_symbol(xy, 'W')
    game.board.print()  # Print after placing the W symbol.


if __name__ == '__main__':
    main()
