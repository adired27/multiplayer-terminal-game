import socket
import threading
from game import Game

class GameServer:
    def __init__(self, host='0.0.0.0', port=12345):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.clients = []
        print(f"[*] Server listening on {host}:{port}")
        try:
            print(f"[*] Server IP for local network is {socket.gethostbyname(socket.gethostname())}")
        except socket.gaierror:
            print("[!] Could not determine local network IP. Use '127.0.0.1' for local connections.")


    def start(self):
        print("[*] Waiting for players to connect...")
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
            self.clients.append(client_socket)
            if len(self.clients) >= 2:
                player1_socket, player2_socket = self.clients.pop(0), self.clients.pop(0)
                print("[*] Two players connected. Starting a new game thread.")
                game_thread = threading.Thread(target=self.handle_game, args=(player1_socket, player2_socket))
                game_thread.start()

    def handle_game(self, player1_socket, player2_socket):
        game = Game()
        players = {player1_socket: 'X', player2_socket: 'O'}

        player1_socket.sendall(b"Welcome! You are Player X. The game is starting...")
        player2_socket.sendall(b"Welcome! You are Player O. Waiting for Player X to move...")

        current_player_socket = player1_socket

        while not game.check_win() and not game.check_draw():
            other_player_socket = player2_socket if current_player_socket == player1_socket else player1_socket
            
            board_str = game.get_board_str()
            turn_message = f"\n{board_str}\nPlayer {players[current_player_socket]}'s turn. Enter your move (1-9): ".encode()
            wait_message = f"\n{board_str}\nWaiting for Player {players[current_player_socket]}'s move...".encode()

            try:
                current_player_socket.sendall(turn_message)
                other_player_socket.sendall(wait_message)

                move_data = current_player_socket.recv(1024)
                if not move_data:
                    print("[!] Player disconnected. Ending game.")
                    other_player_socket.sendall(b"\nThe other player disconnected. Game over.")
                    break
                
                move = int(move_data.decode().strip())
                
                if game.make_move(move, players[current_player_socket]):
                    if game.check_win(players[current_player_socket]):
                        win_message = f"\n{game.get_board_str()}\n🎉 Player {players[current_player_socket]} wins! 🎉".encode()
                        current_player_socket.sendall(win_message)
                        other_player_socket.sendall(win_message)
                        break
                    elif game.check_draw():
                        draw_message = f"\n{game.get_board_str()}\n🤝 It's a draw! 🤝".encode()
                        current_player_socket.sendall(draw_message)
                        other_player_socket.sendall(draw_message)
                        break
                    current_player_socket, other_player_socket = other_player_socket, current_player_socket
                else:
                    current_player_socket.sendall(b"Invalid move. Press Enter to try again.")

            except (ValueError, ConnectionResetError, BrokenPipeError):
                print("[!] A player disconnected or an error occurred. Ending game.")
                error_message = b"\nA player disconnected or an error occurred. Game over."
                if not other_player_socket._closed:
                    other_player_socket.sendall(error_message)
                break
        
        player1_socket.close()
        player2_socket.close()
        print("[*] Game finished. Sockets closed.")


if __name__ == "__main__":
    server = GameServer()
    server.start()