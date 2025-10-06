# 🎮 Multiplayer Terminal Tic-Tac-Toe 🎮

A classic Tic-Tac-Toe game that you can play with a friend over the internet, right from your terminal! This project showcases networking, concurrency, and game logic implementation in Python.

## ✨ Features

-   **🌐 Multiplayer over Network**: Play against another person on a different computer using TCP sockets.
-   **🖥️ Terminal-Based Interface**: A simple and clean command-line interface.
-   **🔄 Concurrent Game Sessions**: The server can handle multiple games at once.
-   **Synchronized Game State**: Ensures both players see the same board and game status.

## 🛠️ Tech Stack

-   **🐍 Language**: Python 3
-   **📦 Libraries**: `socket`, `threading` (standard libraries)

## 🚀 Getting Started

### Prerequisites

-   Python 3.x

### 1. Clone the Repository

```bash
git clone https://github.com/adired27/multiplayer-terminal-game.git
cd multiplayer-terminal-game
```

### 2. Run the Server SERVER

First, start the server on one machine. It will wait for two players to connect.

```bash
python server.py
```

The server will print its IP address. You'll need this for the clients to connect.

### 3. Connect the Players 🧑‍🤝‍🧑

On two separate terminals (or machines), run the client script to connect to the server.

-   **Player 1 (X)**:
    ```bash
    python client.py <server_ip_address>
    ```

-   **Player 2 (O)**:
    ```bash
    python client.py <server_ip_address>
    ```
    Replace `<server_ip_address>` with the actual IP address printed by the server.

### 4. Play the Game! 🎲

The game will start once both players are connected. The terminal will display the board, and players will be prompted to enter their moves (a number from 1 to 9).

```
Player X's turn
 1 | 2 | 3 
-----------
 4 | 5 | 6 
-----------
 7 | 8 | 9 
Enter your move (1-9):
```

The game ends when one player wins or it's a draw.

## 🔧 How It Works

-   **Server (`server.py`)**: Listens for incoming TCP connections. When two clients connect, it pairs them in a new game thread.
-   **Client (`client.py`)**: Connects to the server and enters a loop to send moves and receive game state updates.
-   **Game Logic (`game.py`)**: Manages the board, checks for wins/draws, and keeps track of the current player.
-   **Concurrency**: The server uses `threading` to handle multiple game sessions simultaneously without blocking. Each game is isolated in its own thread.

Enjoy the game!