#!/usr/bin/python3
#  agent.py
#  Nine-Board Tic-Tac-Toe Agent starter code
#  COMP3411/9814 Artificial Intelligence
#  CSE, UNSW

import socket
import sys
import numpy as np

# a board cell can hold:
#   0 - Empty
#   1 - We played here
#   2 - Opponent played here

# the boards are of size 10 because index 0 isn't used
boards = np.zeros((10, 10), dtype="int8")
s = [".","X","O"]
curr = 0 # this is the current board to play in

first_move_b = 0 # the first move board
first_move_c = 0 # the first move cell

# print a row
def print_board_row(bd, a, b, c, i, j, k):
    print(" "+s[bd[a][i]]+" "+s[bd[a][j]]+" "+s[bd[a][k]]+" | " \
             +s[bd[b][i]]+" "+s[bd[b][j]]+" "+s[bd[b][k]]+" | " \
             +s[bd[c][i]]+" "+s[bd[c][j]]+" "+s[bd[c][k]])

# Print the entire board
def print_board(board):
    print_board_row(board, 1,2,3,1,2,3)
    print_board_row(board, 1,2,3,4,5,6)
    print_board_row(board, 1,2,3,7,8,9)
    print(" ------+-------+------")
    print_board_row(board, 4,5,6,1,2,3)
    print_board_row(board, 4,5,6,4,5,6)
    print_board_row(board, 4,5,6,7,8,9)
    print(" ------+-------+------")
    print_board_row(board, 7,8,9,1,2,3)
    print_board_row(board, 7,8,9,4,5,6)
    print_board_row(board, 7,8,9,7,8,9)
    print()


#########################################
# use minmax tree to choice next step

class GameNode:
    # the sturcture of the game tree node
    # board: the current board
    # move: the move to get to this board
    # value: the value of this node
    # children: the children of this node
    def __init__(self, board, k, L, player, parent):
        self.board = board
        self.k = k # the sub-board to play in
        self.L = L # the cell to play in
        self.player = player
        self.parent = parent
        self.children = []
        self.value = 0
        self.finished = False
    
    def add_value(self, value):
        self.value = value
    
    def is_finished(self):
        return self.finished
    
    def check_finished(self):
        # check if the board is finished
        # check the board is win or not
        # The game is won by getting three-in-a row either horizontally, vertically or diagonally in one of the nine boards.
        # we check the small board one by one
        # Define win conditions (patterns) for a 3x3 board
        win_conditions = [
            (1, 2, 3),  # Rows
            (4, 5, 6),
            (7, 8, 9),
            (1, 4, 7),  # Columns
            (2, 5, 8),
            (3, 6, 9),
            (1, 5, 9),  # Diagonals
            (3, 5, 7)
        ]

        # Check each small board one by one
        for i in range(1, 10):  # Assuming 9 small boards, indexed from 1 to 9
            for condition in win_conditions:
                if all(self.board[i][pos] == self.player for pos in condition):
                    self.finished = True
                    if self.player == 1:
                        self.value = 1
                    else:
                        self.value = -1
                    return
        
class GameTree:
    # the structure of the game tree
    def __init__(self):
        self.root = None
        self.children = []

    def generate_tree(self, board):
        self.root = GameNode(board, first_move_b, first_move_c, 2, None) # the root is the first move of the opponent
        
        self._generate_tree_recursive(self.root, 1, 1)  # Start with depth 1, and player 1 (us)

    def _generate_tree_recursive(self, current_node, current_depth, player):
        # Define the maximum depth as a constant, for example, 3 layers deep
        MAX_DEPTH = 100
        
        if current_depth > MAX_DEPTH:
            return  # Base case: if current depth exceeds MAX_DEPTH, stop recursion
        
        current_node.check_finished()
        if current_node.is_finished():
            # If the current board is finished, check next sub-board
            return
        
        # we check in the current board's sub-board(parent's L)
        for i in range(1, 10):  # Assuming board indices go from 1 to 9
            if current_node.board[current_node.L][i] == 0:
                new_board = current_node.board.copy()
                new_board[current_node.L][i] = player
                new_node = GameNode(new_board, current_node.L, i, player, current_node)
                current_node.children.append(new_node)
                self._generate_tree_recursive(new_node, current_depth + 1, 3 - player)
    
    # update the value of the node by interating the children
    def update_value(self, node):
        if node.children:
            if node.player == 1:
                node.value = max([self.update_value(x) for x in node.children])
            else:
                node.value = min([self.update_value(x) for x in node.children])
        return node.value

    # set node as the root of the tree
    def cut_tree(self, node):
        if node.parent:
            node.parent.children = []
            node.parent.children.append(node)
            self.root = node
    
   # search the best move in the tree for us, and cut the tree
    def search_best_move(self):
        if self.root.children:
            best_move = max(self.root.children, key=lambda x: x.value)
            self.cut_tree(best_move)
            return best_move.L
        return -1

    def print_tree(self):
        self._print_tree_recursive(self.root, 0)
        
    def _print_tree_recursive(self, node, depth):
        print("  " * depth, node.L)
        for child in node.children:
            self._print_tree_recursive(child, depth + 1)

tree = GameTree()
#########################################

# choose a move to play
def play():
    # print_board(boards)

    # just play a random move for now
    # n = np.random.randint(1,9)
    # while boards[curr][n] != 0:
    #     n = np.random.randint(1,9)

    # use minmax tree to choice next step
    # generate the game tree if the root is None
    if not tree.root:
        tree.generate_tree(boards)
        # update the value of the tree
        tree.update_value(tree.root)
        # print the tree
        
    tree.print_tree()
    n = tree.search_best_move()

    print("playing", n)
    place(curr, n, 1)
    return n

# place a move in the global boards
def place( board, num, player ):
    global curr
    curr = num
    boards[board][num] = player

# read what the server sent us and
# parse only the strings that are necessary
def parse(string):
    if "(" in string:
        command, args = string.split("(")
        args = args.split(")")[0]
        args = args.split(",")
    else:
        command, args = string, []
        
    
    # init tells us that a new game is about to begin.
    # start(x) or start(o) tell us whether we will be playing first (x)
    # or second (o); we might be able to ignore start if we internally
    # use 'X' for *our* moves and 'O' for *opponent* moves.

    # second_move(K,L) means that the (randomly generated)
    # first move was into square L of sub-board K,
    # and we are expected to return the second move.
    if command == "second_move":
        first_move_b = int(args[0])
        first_move_c = int(args[1])
        # place the first move (randomly generated for opponent)
        place(int(args[0]), int(args[1]), 2)
        return play()  # choose and return the second move

    # third_move(K,L,M) means that the first and second move were
    # in square L of sub-board K, and square M of sub-board L,
    # and we are expected to return the third move.
    elif command == "third_move":
        # place the first move (randomly generated for us)
        place(int(args[0]), int(args[1]), 1)
        
        first_move_b = curr
        first_move_c = int(args[2])
        
        # place the second move (chosen by opponent)
        place(curr, int(args[2]), 2)
        return play() # choose and return the third move

    # nex_move(M) means that the previous move was into
    # square M of the designated sub-board,
    # and we are expected to return the next move.
    elif command == "next_move":
        # place the previous move (chosen by opponent)
        place(curr, int(args[0]), 2)
        return play() # choose and return our next move

    elif command == "win":
        print("Yay!! We win!! :)")
        return -1

    elif command == "loss":
        print("We lost :(")
        return -1

    return 0

# connect to socket
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = int(sys.argv[2]) # Usage: ./agent.py -p (port)

    s.connect(('localhost', port))
    while True:
        text = s.recv(1024).decode()
        if not text:
            continue
        for line in text.split("\n"):
            response = parse(line)
            if response == -1:
                s.close()
                return
            elif response > 0:
                s.sendall((str(response) + "\n").encode())

if __name__ == "__main__":
    main()
