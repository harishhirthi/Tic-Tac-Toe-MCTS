import math
import random
import time

class TreeNode:
    
    def __init__(self, board, parent):
        """
        To create Root nodes(states or moves) and child nodes(states or moves).

        Args:
        board -> Current board state
        parent -> Parent board state

        """
        self.board = board
        self.parent = parent
        self.visits, self.score = 0, 0
        self.children = dict()
        # Check for board terminal state
        if self.board.is_win() or self.board.is_draw():
            self.is_terminal = True
        else:
            self.is_terminal = False
        # To check whether branch is fully expanded
        self.is_fully_expanded = self.is_terminal

"""_________________________________________________________________________________________________________________________________________________________"""

class mcts():

    def __init__(self, exploration_constant: float = 2, iteration_limit: int = 1000, time_limit: int = None) -> None:
        """
        To create Monte-Carlo Tree Search Algorithm

        Args:
        exploration_constant -> Constant to favour the Exploration in UCT.
        iteration_limit -> Maximum count limit for iterations to take place.
        time_limit -> Maximum time limit for iterations to take place.

        """
        self.exploration_constant = exploration_constant
        self.iteration_limit = iteration_limit
        self.time_limit = time_limit
        # Make sure any one limit is used
        if self.iteration_limit != None and self.time_limit != None:
            raise ValueError("Use any one of the limit. Either Iteration Limit or Time Limit.")

    def search(self, initial_state) -> TreeNode:
        # Search for the best node in the current position.(best move)
        self.root = TreeNode(initial_state, None)
        # Based on count limit
        if self.iteration_limit:
            for _ in range(self.iteration_limit):
                self.execute_step() # Explores for all possible states that it can have to select optimal move
        # Based on time limit
        if self.time_limit:
            timelimit = time.time() + self.time_limit / 1000
            while time.time() < timelimit:
                self.execute_step() # Explores for all possible states that it can have to select optimal move
        # Returns the best root node in the current position by exploitation    
        try:
            return self.get_best_child_move(self.root, exploration_constant = 0)
        except:
            pass
    
    def execute_step(self):
        """
        Phases of MCTS

        """
        # Selection phase
        node = self.select(self.root)
        # Rollout(Simulation) phase
        score = self.rollout(node.board)
        # Backpropagation phase
        self.backpropagate(node, score)
    
    def get_best_child_move(self, node: TreeNode, exploration_constant: float) -> TreeNode:
        # Select the best child node that maximizes the UCT(UCB1) formula.
        """
        UCT(Upper Confidence Bound applied to trees) based on UCB1 algorithm.
        
        UCT = Wi/ni + c * sqrt(ln(Ni)/ni) ................[1]

        Wi -> Total score of the Child node
        ni -> Visits of Child node
        Ni -> Visits of Child's Parent node
        c  -> Exploration constant
        
        Wi/ni -> Exploitation term
        sqrt(ln(Ni)/ni) -> Exploration term

        In actual implementation, a constant is multiplied with Exploitation term which is Negamax search,
        a variant of Minimax search.

        """
        best_score = float('-inf')
        best_nodes = []

        for child_node in node.children.values():
            # Initializing the constant to be multiplied with Exploitation term
            if child_node.board.player_2 == 'X': 
                current_player = 1 # Tries to maximize the user move
            elif child_node.board.player_2 == 'O':
                current_player = -1 # Tries to negate the system move 
            # Calculates the UCT score
            move_score = current_player * child_node.score / child_node.visits + \
                         exploration_constant * math.sqrt(math.log(node.visits) / child_node.visits)
            if move_score > best_score: # Selects the child node with maximum UCT score
                best_score = move_score
                best_nodes = [child_node]
            
            elif move_score == best_score: # Adds the child node whose score is same as best score
                best_nodes.append(child_node)
        # Return one random best node
        return random.choice(best_nodes)
    
    def select(self, node: TreeNode) -> TreeNode:
        # Select the non-terminal fully expanded best node using UCT score
        while not node.is_terminal:
            
            if node.is_fully_expanded:
                node = self.get_best_child_move(node, self.exploration_constant)
            else:
                return self.expand(node) # Expands the tree when the node is not fully expanded
            
        return node
    
    def expand(self, node: TreeNode) -> TreeNode:
        # Expand the nodes for the generated legal states
        states = node.board.generate_states()

        for state in states:
            # Make sure that current state is not in child nodes
            if str(state.positions) not in node.children:

                new_node = TreeNode(state, node)
                node.children[str(state.positions)] = new_node
                # Whether that particular node is fully expanded
                if len(states) == len(node.children):
                    node.is_fully_expanded = True

                return new_node
            
        raise Exception("Should never reach here....")

    def rollout(self, board) -> float:
        # Simulates the game by making random moves until it reaches terminal state and return the score for the players
        while not board.is_win():
            try:
                board = random.choice(board.generate_states())
            except:
                return 0 # score for draw
        # These scores are assigned in the perspective of "X"(User)
        if board.player_2 == 'X': 
            return 1
        elif board.player_2 == 'O':
            return -1

    def backpropagate(self, node: TreeNode, score: float) -> None:
        # Backpropagates the score obtained from rollout and visits of nodes way through it's root node(parent node)
        while node is not None:

            node.visits += 1
            node.score += score
            node = node.parent


"""
References:
1. https://en.wikipedia.org/wiki/Monte_Carlo_tree_search
2. https://github.com/maksimKorzh/tictactoe-mtcs
3. https://github.com/pbsinclair42/MCTS
"""
