class Game:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None

    def get_board_str(self):
        board_str = ""
        for i in range(3):
            row = self.board[i*3:(i+1)*3]
            board_str += ' | '.join(row) + '\n'
            if i < 2:
                board_str += '----------\n'
        
        # Add number guide for players
        guide = "\nReference:\n 1 | 2 | 3 \n----------\n 4 | 5 | 6 \n----------\n 7 | 8 | 9 \n"
        return board_str + guide

    def make_move(self, square, letter):
        square -= 1 # Adjust for 0-based index
        if 0 <= square < 9 and self.board[square] == ' ':
            self.board[square] = letter
            if self.check_win(letter):
                self.current_winner = letter
            return True
        return False

    def check_win(self, letter=None):
        # Check rows
        for i in range(0, 9, 3):
            if self.board[i] == self.board[i+1] == self.board[i+2] != ' ':
                self.current_winner = self.board[i]
                return True
        # Check columns
        for i in range(3):
            if self.board[i] == self.board[i+3] == self.board[i+6] != ' ':
                self.current_winner = self.board[i]
                return True
        # Check diagonals
        if self.board[0] == self.board[4] == self.board[8] != ' ':
            self.current_winner = self.board[0]
            return True
        if self.board[2] == self.board[4] == self.board[6] != ' ':
            self.current_winner = self.board[2]
            return True
            
        if letter and self.current_winner == letter:
            return True

        return False

    def check_draw(self):
        return ' ' not in self.board and not self.check_win()