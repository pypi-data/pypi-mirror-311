def a_star():
    code = '''
    1. A* Search Algorithm (a_star)
Overview:
A* is an informed search algorithm used for pathfinding and graph traversal. It combines the benefits of Dijkstra's algorithm (optimality) and Greedy Best-First Search (speed), using a heuristic function to guide the search.

Key Elements:

Cost function: f(n) = g(n) + h(n)
g(n): Cost to reach node n from the start.
h(n): Heuristic estimate of the cost from n to the goal.
f(n): Total estimated cost of the cheapest solution through n.
Priority Queue: Maintains nodes to be explored based on f(n).
Steps:

Start with the initial node and calculate f(n) for all neighbors.
Add neighbors to the priority queue and pick the node with the smallest f(n).
Expand the node, updating g(n) and f(n) for its neighbors.
Repeat until the goal node is reached.
Reconstruct the path from the goal node to the start using a parent map.
Mathematics:

If the heuristic function h(n) is admissible (never overestimates the true cost) and consistent (satisfies the triangle inequality), A* is guaranteed to find the optimal solution.
The runtime complexity depends on the branching factor b and the depth d of the solution: O(b^d) in the worst case, but often better in practice with a good heuristic.
Applications:
Used in robotics, video game AI, and route planning systems.
    
    import heapq

class Node:
    def __init__(self, name, heuristic):
        self.name = name
        self.heuristic = heuristic
        self.neighbors = []

    def add_neighbor(self, neighbor, weight):
        self.neighbors.append((neighbor, weight))

def a_star_search(start, goal):
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: start.heuristic}

    while open_list:
        current_f, current = heapq.heappop(open_list)
        if current == goal:
            path = []
            while current in came_from:
                path.append(current.name)
                current = came_from[current]
            path.append(start.name)
            return path[::-1], g_score[goal]

        for neighbor, weight in current.neighbors:
            tentative_g_score = g_score[current] + weight
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + neighbor.heuristic
                heapq.heappush(open_list, (f_score[neighbor], neighbor))

    return None, float('inf')

nodes = {}
node_data = input("Enter nodes with their heuristic values (e.g., 'A 1 B 2 C 3'): ").split()
for i in range(0, len(node_data), 2):
    name = node_data[i]
    heuristic = float(node_data[i+1])
    nodes[name] = Node(name, heuristic)

edge_data = input("Enter edges with weights (e.g., 'A B 1 B C 2'): ").split()
for i in range(0, len(edge_data), 3):
    node1 = edge_data[i]
    node2 = edge_data[i+1]
    weight = float(edge_data[i+2])
    nodes[node1].add_neighbor(nodes[node2], weight)
    nodes[node2].add_neighbor(nodes[node1], weight)

start_node = nodes[input("Enter the start node: ")]
goal_node = nodes[input("Enter the goal node: ")]

path, cost = a_star_search(start_node, goal_node)
if path:
    print("Path found:", " -> ".join(path))
    print("Total cost:", cost)
else:
    print("No path found")

    
    
  inputs: = Enter nodes with their heuristic values (e.g., 'A 1 B 2 C 3'): S 11.5 A 10.1 B 5.8 C 3.4 D 9.2 E 7.1 F 3.5 G 0
Enter edges with weights (e.g., 'A B 1 B C 2'): S A 3 S D 4 A B 4 A D 5 D E 2 B E 5 B C 4 E F 4 F G 3.5
Enter the start node: S
Enter the goal node: G
Path found: S -> D -> E -> F -> G
Total cost: 13.5
    
    '''
    print(code)


def eight_puzzle():
    code = '''
    . 8-Puzzle Solver (eight_puzzle)
Overview:
The 8-Puzzle involves arranging tiles numbered 1 to 8 on a 3x3 grid in a specific order by sliding them into the empty space. The A* algorithm with the Manhattan Distance heuristic is used to find the optimal solution.

Key Elements:

State Space: Each state is a 3x3 configuration of the puzzle.
Heuristic Function:
h(n) = Sum of the Manhattan distances of each tile from its goal position.
Manhattan Distance = |x1 - x2| + |y1 - y2|.
Steps:

Initialize the priority queue with the initial state and its f(n).
Expand the state with the smallest f(n), generating valid moves (up, down, left, right).
Update g(n) and f(n) for the new states.
Continue until the goal state is reached.
Mathematics:

Total estimated cost: f(n) = g(n) + h(n), where g(n) is the number of moves made so far.
Manhattan Distance guarantees admissibility and optimality since it never overestimates the actual number of moves.
Applications:
Demonstrates state-space search and is a classic example of AI problem-solving.
    
    import heapq

class PuzzleState:
    def __init__(self, board, goal, moves=0, prev=None):
        self.board = board
        self.goal = goal
        self.blank_pos = board.index('*')
        self.moves = moves
        self.prev = prev

    def __lt__(self, other):
        return (self.moves + self.heuristic()) < (other.moves + other.heuristic())

    def heuristic(self):
        """ Calculate Manhattan Distance """
        goal_positions = {i: (i // 3, i % 3) for i in range(1, 9)}
        goal_positions['*'] = (2, 2)  # The goal position for the empty tile
        distance = 0
        
        for i in range(9):
            tile = self.board[i]
            if tile == '*':
                continue
            tile = int(tile)  # Convert tile to integer for comparison
            goal_pos = goal_positions[tile]
            cur_pos = (i // 3, i % 3)
            distance += abs(cur_pos[0] - goal_pos[0]) + abs(cur_pos[1] - goal_pos[1])
        
        return distance

    def get_neighbors(self):
        """ Generate neighboring states by moving the blank tile """
        neighbors = []
        r, c = divmod(self.blank_pos, 3)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 3 and 0 <= nc < 3:
                new_blank_pos = nr * 3 + nc
                new_board = list(self.board)
                new_board[self.blank_pos], new_board[new_blank_pos] = new_board[new_blank_pos], new_board[self.blank_pos]
                neighbors.append(PuzzleState(tuple(new_board), self.goal, self.moves + 1, self))
        
        return neighbors

    def is_goal(self):
        return self.board == self.goal

    def __repr__(self):
        return '\n'.join([' '.join(map(str, self.board[i:i+3])) for i in range(0, 9, 3)])

def a_star(start_state):
    open_set = []
    heapq.heappush(open_set, start_state)
    closed_set = set()

    while open_set:
        current_state = heapq.heappop(open_set)

        if current_state.is_goal():
            return current_state

        closed_set.add(current_state.board)

        for neighbor in current_state.get_neighbors():
            if neighbor.board in closed_set:
                continue
            heapq.heappush(open_set, neighbor)

    return None

def get_user_input(prompt):
    """ Get a state from user input with validation """
    print(prompt)
    input_str = input().strip()
    input_list = input_str.split()
    
    if len(input_list) != 9 or '*' not in input_list or len(set(input_list)) != 9:
        raise ValueError("Invalid input. Make sure you enter exactly 9 values with numbers 1-8 and one '*' for the empty space.")

    return tuple(input_list)

# Main execution
if __name__ == "__main__":
    try:
        start_board = get_user_input("Enter the start state (9 values with numbers 1-8 and '*' for empty space):")
        goal_board = get_user_input("Enter the goal state (9 values with numbers 1-8 and '*' for empty space):")

        if start_board == goal_board:
            raise ValueError("Start state cannot be the same as the goal state.")

        start = PuzzleState(start_board, goal_board)
        solution = a_star(start)

        if solution:
            path = []
            while solution:
                path.append(solution)
                solution = solution.prev
            for state in reversed(path):
                print(state)
                print()
        else:
            print("No solution found.")
    except ValueError as e:
        print(e)

'''
    print(code)



def csp():
    code = '''
    Cryptarithmetic Puzzle Solver (csp)
Overview:
Cryptarithmetic puzzles involve solving word addition problems where letters represent digits. For example, SEND + MORE = MONEY, with each letter corresponding to a unique digit.

Key Elements:

Constraint Satisfaction Problem (CSP):
Each letter must map to a unique digit.
The numbers formed by words must satisfy the arithmetic equation.
Steps:

Generate all permutations of digits for the letters involved.
Check constraints for each permutation.
Return the mapping if a solution is found.
Mathematics:

Permutation-based search with constraints:
If there are k unique letters, there are k! permutations of digits.
Constraints:
Words are converted to numbers:
SEND = 1000S + 100E + 10N + D.
Ensure the sum of SEND and MORE equals MONEY.
Applications:
Demonstrates combinatorial problem-solving and constraint propagation.
    
    import itertools

def solve_cryptarithm(words, result):
    unique_letters = ''.join(set(''.join(words) + result))
    
    if len(unique_letters) > 10:
        print("Too many unique letters for a single-digit solution.")
        return
    
    digits = '0123456789'
    
    for perm in itertools.permutations(digits, len(unique_letters)):
        letter_to_digit = dict(zip(unique_letters, perm))
        
        def word_to_number(word):
            return int(''.join(letter_to_digit[letter] for letter in word))
        
        if any(letter_to_digit[word[0]] == '0' for word in words + [result]):
            continue
        
        sum_words = sum(word_to_number(word) for word in words)
        
        if sum_words == word_to_number(result):
            print("Solution found!")
            for word in words:
                print(f"{word} = {word_to_number(word)}")
            print(f"{result} = {word_to_number(result)}")
            print(f"Letter to Digit Mapping: {letter_to_digit}")
            return
    
    print("No solution found.")

input_words = input("Enter the words to sum (space-separated): ").upper().split()
input_result = input("Enter the result word: ").upper()

solve_cryptarithm(input_words, input_result)


'''
    print(code)



def sudoku():
    code = '''
Sudoku Solver (sudoku)
Overview:
The Sudoku solver uses recursive backtracking to fill a 9x9 grid with digits 1-9, ensuring no repetitions in rows, columns, or 3x3 subgrids.

Key Elements:

Systematic Search: Tries each digit in empty cells.
Backtracking: Undoes choices when constraints are violated.
Steps:

Find the first empty cell.
Try placing digits 1-9 in the cell.
If constraints are satisfied, move to the next empty cell.
If no valid digit exists, backtrack to the previous cell and try a different digit.
Repeat until the grid is filled.
Mathematics:

The search space is large but reduced by constraint propagation.
Complexity is exponential in the worst case but manageable for most puzzles due to pruning.
Applications:
Solves puzzles and demonstrates systematic search algorithms.




def is_valid(board, row, col, num):
    for x in range(9):
        if board[row][x] == num or board[x][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def solve_sudoku(board):
    empty = find_empty_location(board)
    if not empty:
        return True
    row, col = empty
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0
    return False

def find_empty_location(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return (row, col)
    return None

def print_board(board):
    for row in board:
        print(" ".join(str(num) if num != 0 else '.' for num in row))

def input_board():
    print("Enter the Sudoku puzzle (9x9 grid). Use 0 for empty cells:")
    board = []
    for i in range(9):
        while True:
            try:
                row = list(map(int, input(f"Row {i+1}: ").strip().split()))
                if len(row) != 9:
                    raise ValueError("Each row must have exactly 9 numbers.")
                if any(num < 0 or num > 9 for num in row):
                    raise ValueError("Numbers must be between 0 and 9.")
                board.append(row)
                break
            except ValueError as e:
                print(f"Invalid input: {e}. Please enter the row again.")
    return board

if __name__ == "__main__":
    board = input_board()
    if solve_sudoku(board):
        print("Solved Sudoku:")
        print_board(board)
    else:
        print("No solution exists")

'''
    print(code)




def ttt():
    code = '''
Tic-Tac-Toe with Minimax AI (ttt)
Overview:
Minimax is a decision-making algorithm for two-player games. It aims to minimize the possible loss for a worst-case scenario by simulating all possible moves.

Key Elements:

Game Tree: Represents all possible game states.
Minimax Value: Each node has a value indicating the outcome of the game if both players play optimally.
Terminal States: Win, lose, or draw conditions.
Steps:

Generate the game tree from the current state.
Assign values to terminal states (+1 for AI win, -1 for AI loss, 0 for draw).
Propagate values back up the tree, choosing the maximum for the AI and minimum for the opponent.
Choose the move with the best value.
Mathematics:

Value at node n:
Maximize: v(n) = max(value of children).
Minimize: v(n) = min(value of children).
Complexity: O(b^d), where b is the branching factor and d is the depth of the game tree.
Applications:
Used in games like chess, checkers, and Tic-Tac-Toe to create strong AI opponents.


import itertools

def print_board(board):
    print('\n'.join(' '.join(row) for row in board), end='\n\n')

def check_win(board, player):
    win = [player] * 3
    return (any(all(cell == player for cell in row) for row in board) or        # Check rows
            any(all(board[i][j] == player for i in range(3)) for j in range(3)) or  # Check columns
            all(board[i][i] == player for i in range(3)) or                # Check main diagonal
            all(board[i][2 - i] == player for i in range(3)))              # Check anti-diagonal

def is_board_full(board):
    return all(cell != ' ' for row in board for cell in row)

def minimax(board, depth, is_maximizing):
    if check_win(board, 'X'): return 10 - depth
    if check_win(board, 'O'): return depth - 10
    if is_board_full(board): return 0

    best_score = float('-inf') if is_maximizing else float('inf')
    for i, j in itertools.product(range(3), repeat=2):
        if board[i][j] == ' ':
            board[i][j] = 'X' if is_maximizing else 'O'
            score = minimax(board, depth + 1, not is_maximizing)
            board[i][j] = ' '
            best_score = max(score, best_score) if is_maximizing else min(score, best_score)
    return best_score

def find_best_move(board):
    best_move = None
    best_score = float('-inf')
    for i, j in itertools.product(range(3), repeat=2):
        if board[i][j] == ' ':
            board[i][j] = 'X'
            score = minimax(board, 0, False)
            board[i][j] = ' '
            if score > best_score:
                best_score = score
                best_move = (i, j)
    return best_move

def convert_to_indices(position):
    return (position - 1) // 3, (position - 1) % 3

board = [[' ' for _ in range(3)] for _ in range(3)]
print_board(board)

while True:
    try:
        pos = int(input("Enter position for O (1-9): "))
        row, col = convert_to_indices(pos)
        if board[row][col] == ' ':
            board[row][col] = 'O'
            print("O moves:")
            print_board(board)
            if check_win(board, 'O'):
                print("O wins!")
                break
            if is_board_full(board):
                print("It's a tie!")
                break
        else:
            print("Cell already taken. Try again.")
    except (ValueError, IndexError):
        print("Invalid input. Enter a number between 1 and 9.")

    move = find_best_move(board)
    if move:
        board[move[0]][move[1]] = 'X'
        print("X moves:")
        print_board(board)
        if check_win(board, 'X'):
            print("X wins!")
            break
        if is_board_full(board):
            print("It's a tie!")
            break


'''
    print(code)




def lr():
    code = '''Linear Regression
Overview:
Linear regression is a supervised learning algorithm used to predict a continuous output based on one or more input features. It assumes a linear relationship between the input variables and the target variable.

Key Elements:

Hypothesis function: h(x) = w₀ + w₁x₁ + w₂x₂ + ... + wₙxₙ, where w₀ is the intercept and w₁, w₂, ..., wₙ are the feature weights.
Cost function: Mean Squared Error (MSE) = (1/2m) Σ (yᵢ - h(xᵢ))², where m is the number of training examples.
Optimization: Weights are optimized using techniques like Gradient Descent.
Steps:

Initialize weights randomly or to zero.
Compute the hypothesis for all training samples.
Calculate the cost using MSE.
Update weights to minimize the cost using Gradient Descent:
wⱼ = wⱼ - α ∂J/∂wⱼ, where α is the learning rate.
Repeat until convergence or for a set number of iterations.
Mathematics:

Normal Equation: w = (XᵀX)⁻¹Xᵀy provides a closed-form solution for the weights when the dataset is small.
Assumes linearity, no multicollinearity, homoscedasticity, and normally distributed errors.
Applications:
Used in predictive modeling, stock price prediction, and estimating relationships between variables.'''


def nb():
    code='''Naive Bayes
Overview:
Naive Bayes is a probabilistic classifier based on Bayes' theorem. It assumes independence between features, which simplifies computation.

Key Elements:

Bayes' theorem: P(C|X) = [P(X|C)P(C)] / P(X), where:
P(C|X): Probability of class C given features X.
P(X|C): Probability of features X given class C.
P(C): Prior probability of class C.
P(X): Probability of features X.
Naive Assumption: Features are conditionally independent given the class.
Steps:

Compute prior probabilities P(C) for all classes.
Calculate likelihoods P(X|C) for all features.
Multiply P(X|C) with P(C) to compute P(C|X) for each class.
Assign the class with the highest probability.
Mathematics:

For feature vector X = (x₁, x₂, ..., xₙ):
P(C|X) ∝ P(C) Π P(xᵢ|C).
Complexity: Linear with respect to the number of samples and features.
Applications:
Spam filtering, sentiment analysis, and text classification.'''


def dt():
    code =''' Decision Trees
Overview:
Decision trees are a supervised learning method used for classification and regression. They split the dataset into subsets based on feature values, creating a tree-like model of decisions.

Key Elements:

Node: Represents a feature.
Branch: Represents a decision rule.
Leaf: Represents the outcome (class or value).
Splitting Criterion: Gini Impurity, Information Gain, or Variance Reduction.
Steps:

Start with the root node containing all data.
Choose the feature that maximizes Information Gain or minimizes Gini Impurity.
Split the dataset based on the feature's values.
Repeat for each branch until stopping criteria are met (e.g., max depth or minimum samples per leaf).
Assign outcomes to leaf nodes.
Mathematics:

Gini Impurity: 1 - Σ(pᵢ²), where pᵢ is the proportion of samples belonging to class i.
Information Gain: IG = H(parent) - Σ(H(children)), where H is the entropy.
Applications:
Used in customer segmentation, credit scoring, and medical diagnosis.'''


def kmeans():
    code='''K-Means
Overview:
K-Means is an unsupervised clustering algorithm that partitions data into k clusters by minimizing the variance within each cluster.

Key Elements:

Centroids: Represent the center of each cluster.
Distance Metric: Often Euclidean distance.
Objective Function: Minimize the sum of squared distances (SSD) between points and their cluster centroids.
Steps:

Initialize k centroids randomly or using a heuristic.
Assign each data point to the nearest centroid.
Recompute centroids as the mean of points in each cluster.
Repeat steps 2 and 3 until centroids converge or a set number of iterations is reached.
Mathematics:

SSD = Σ Σ ||xᵢ - μⱼ||², where xᵢ is a data point and μⱼ is the centroid of cluster j.
Complexity: O(nkdi), where n is the number of points, k is the number of clusters, d is the number of features, and i is the number of iterations.
Applications:
Image segmentation, customer segmentation, and pattern recognition.'''



def svm():
    code='''Support Vector Machine (SVM)
Overview:
SVM is a supervised learning algorithm used for classification and regression. It finds the hyperplane that best separates data into classes with the maximum margin.

Key Elements:

Hyperplane: Decision boundary separating classes.
Margin: Distance between the hyperplane and the nearest points from each class (support vectors).
Kernel Trick: Projects data into higher dimensions to make it linearly separable.
Steps:

Define the optimization problem to maximize the margin while correctly classifying data points.
Solve the optimization problem using techniques like quadratic programming.
For non-linearly separable data, apply a kernel function like RBF, polynomial, or sigmoid.
Mathematics:

Optimization:
Minimize ||w||² subject to yᵢ(w·xᵢ + b) ≥ 1, where yᵢ is the class label.
Dual Form:
Maximize Σαᵢ - 0.5ΣΣαᵢαⱼyᵢyⱼ(xᵢ·xⱼ), where αᵢ are Lagrange multipliers.
Kernel Trick: Replace (xᵢ·xⱼ) with K(xᵢ, xⱼ) for non-linear classification.
Applications:
Image classification, bioinformatics, and text categorization.'''