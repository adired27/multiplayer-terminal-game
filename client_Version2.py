import socket
import sys
import threading

def receive_messages(sock):
    """Continuously receive messages from the server and print them."""
    try:
        while True:
            response = sock.recv(1024).decode()
            if not response:
                print("\n[*] Server closed the connection.")
                break
            
            # Clear the line and print the new message
            sys.stdout.write('\r' + ' ' * 50 + '\r')
            print(response)
            
            if "turn" in response:
                sys.stdout.write("> ")
                sys.stdout.flush()
            elif "wins" in response or "draw" in response or "disconnected" in response or "over" in response:
                break
    except ConnectionAbortedError:
        print("\n[*] You have been disconnected from the server.")
    except OSError: # Handle socket closing while in recv
        pass

def game_client(server_ip, port=12345):
    """Manages the client-side connection and user input."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_ip, port))
        print("[*] Connected to the game server.")
    except ConnectionRefusedError:
        print("[!] Connection failed. Is the server running at that IP?")
        sys.exit(1)
    except socket.gaierror:
        print("[!] Hostname could not be resolved. Is the IP address correct?")
        sys.exit(1)

    # Start a thread to listen for server messages
    receiver_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receiver_thread.daemon = True
    receiver_thread.start()

    try:
        while receiver_thread.is_alive():
            move = input()
            if move:
                client_socket.sendall(move.encode())
    except KeyboardInterrupt:
        print("\n[*] Closing connection. Goodbye!")
    finally:
        client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python client.py <server_ip_address>")
        sys.exit(1)
    
    server_ip = sys.argv[1]
    game_client(server_ip)