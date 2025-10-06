import os
from game import Game

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def play_local_game():
    """Manages a local Tic-Tac-Toe game for two players on the same terminal."""
    game = Game()
    current_player = 'X'

    while not game.check_win() and not game.check_draw():
        clear_screen()
        print("--- Local Tic-Tac-Toe ---\n")
        print(game.get_board_str())
        print(f"Player {current_player}'s turn.")
        
        try:
            move = input(f"Enter your move (1-9), Player {current_player}: ")
            if not move.isdigit() or not game.make_move(int(move), current_player):
                input("\nInvalid move. Press Enter to try again.")
                continue
        except (ValueError, KeyboardInterrupt):
            input("\nInvalid input. Please enter a number. Press Enter to try again.")
            continue

        if game.check_win(current_player):
            clear_screen()
            print(game.get_board_str())
            print(f"🎉 Player {current_player} wins! 🎉")
            break
        elif game.check_draw():
            clear_screen()
            print(game.get_board_str())
            print("🤝 It's a draw! 🤝")
            break
        
        # Switch players
        current_player = 'O' if current_player == 'X' else 'X'

if __name__ == "__main__":
    play_local_game()
