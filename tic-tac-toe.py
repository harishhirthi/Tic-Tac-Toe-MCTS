from copy import deepcopy
from mcts import mcts

class Board:
    """
    To create a layout, players, moves and states for Tic-Tac-Toe Game (Cross and Noughts).  

    """
    def __init__(self, board = None):

        self.player_1 = 'X'
        self.player_2 = 'O'
        self.empty_box = '.'
        self.positions = dict()

        self.init_board()
        if board is not None:
            self.__dict__ = deepcopy(board.__dict__)
        
    def init_board(self) -> None:
        # Initialising board cells with dots to represent it as empty cells
        for row in range(3):
            for col in range(3):
                self.positions[row, col] = self.empty_box

    def make_move(self, row: int, col: int):
        # Filling the cells with respective player's mark
        board = Board(self)
        board.positions[row, col] = self.player_1
        # Swap players for next move
        board.player_1, board.player_2 = board.player_2, board.player_1

        return board
    
    def is_draw(self):
        # Checking condition for Draw state
        for row, col in self.positions:
            if self.positions[row, col] == self.empty_box: # No empty cell indicates Draw state
                return False
        return True
    
    def is_win(self):
        """
        Checking condition for Win state (All 3 "X" or "O" are same). The possibilities are
        1. Vertical axes (Columns 1 or 2 or 3)
        2. Horizontal axes (Rows 1 or 2 or 3)
        3. Diagonals (Left or Right)
        
        """
        # Vertical Axes
        for col in range(3):
            count_v = 0
            for row in range(3):
                if self.positions[row, col] == self.player_2: # player_2 is since player_1 will be swapped to player_2
                    count_v += 1
                
            if count_v == 3:
                return True
            
        # Horizontal Axes
        for row in range(3):
            count_h = 0
            for col in range(3):
                if self.positions[row, col] == self.player_2:
                    count_h += 1
                
            if count_h == 3:
                return True
            
        # Right Diagonal
        count_rd = 0
        for row in range(3):
            col = row
            if self.positions[row, col] == self.player_2:
                count_rd += 1
        if count_rd == 3:
            return True
        
        # Left Diagonal
        count_ld = 0
        for row in range(3):
            col = 2 - row
            if self.positions[row, col] == self.player_2:
                count_ld += 1
        if count_ld == 3:
            return True

        return False

    def generate_states(self):
        # To Generate possible states or moves for a given current board state and current player
        actions = []
        for row in range(3):
            for col in range(3):
                if self.positions[row, col] == self.empty_box:
                    actions.append(self.make_move(row, col)) 

        return actions
    
    def game_loop(self):
        """
                                    Welcome to Tic-Tac-Toe Game. 
        Cell locations are given as follows. Type numbers (1 - 9) to select the location to make a move.
                                           1 | 2 | 3 
                                           4 | 5 | 6
                                           7 | 8 | 9
        Type "exit" to Exit the game.
        
        """
        print(self)
        # Mapping integers to board positions to make user-friendly 
        self.pos = {1: (0, 0), 2: (0, 1), 3: (0, 2),
                    4: (1, 0), 5: (1, 1), 6: (1, 2),
                    7: (2, 0), 8: (2, 1), 9: (2, 2)
                   }
        # Initiating Monte Carlo Tree Search Instance
        searcher = mcts(exploration_constant = 2, iteration_limit = 1000, time_limit = None) # time_limit is in milliseconds (1000ms = 1sec)

        while True:
            # Getting position from user
            user_in = input('> ') 

            if user_in == 'exit': break
            if user_in == '': continue

            try:

                row = self.pos[int(user_in)][0]
                col = self.pos[int(user_in)][1]
                # To check whether the position is already filled or not
                if self.positions[row, col] != self.empty_box: 
                    print("Illegal Move. Please Try again")
                    continue
                # User's move
                self = self.make_move(row, col)
                print(self)
                # System's move
                best_move = searcher.search(self)

                try:
                    self = best_move.board
                except: pass

                print(self)
                # Win state
                if self.is_win():
                    print("!!! Player '%s' has won the game !!!" % self.player_2)
                    print("!!!! Enjoyed Playing !!!!")
                    break
                # Draw state
                elif self.is_draw():
                    print("Game is Draw.....")
                    print("If you like to Restart, type (y) for 'yes' or (n) for 'no'")
                    u_in = input('> ') 
                    # To restart the game after draw
                    if u_in == 'y':
                        self.player_1 = 'X'
                        self.player_2 = 'O'
                        self.init_board()
                        print(self)
                        continue
                    # To exit the game after draw
                    elif u_in == 'n': 
                        print("!!!! Thank you for Playing !!!!") 
                        break
            # Raise error when user enters other than numbers (1 - 9)
            except Exception as e:
                print("   Error: ", e)
                print("   Invalid Command")

    def __str__(self) -> str:
        # Print Board layout along with "X" and "O"
        board_string = ''

        for row in range(3):
            for col in range(3):
                if col != 2:
                    board_string += ' %s |' % self.positions[row, col]
                else:
                    board_string += ' %s' % self.positions[row, col]

            board_string += '\n'
        
        if self.player_1 == 'X':
            board_string = '\n===============\n "X" to move:\n===============\n\n' + board_string
            
        elif self.player_1 == 'O':
            board_string = '\n===============\n "O" to move:\n===============\n\n' + board_string
            
        return board_string

if __name__ == '__main__':

    # Initiate Board Instance
    board = Board() 
    print(board.game_loop.__doc__) # Print game instructions for the user
    board.game_loop() # Kick-start the game
