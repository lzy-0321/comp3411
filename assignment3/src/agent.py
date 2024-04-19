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

max_depth = 0
round = 0
output_file = open("game_output.txt", "w")

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

corners = [1, 3, 7, 9]
center = [5]

sub_board_values = {}
board_values = {}

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

################################################################################
#print board to txt file

def print_board_row(bd, a, b, c, i, j, k, output_file):
    print(" "+s[bd[a][i]]+" "+s[bd[a][j]]+" "+s[bd[a][k]]+" | " \
             +s[bd[b][i]]+" "+s[bd[b][j]]+" "+s[bd[b][k]]+" | " \
             +s[bd[c][i]]+" "+s[bd[c][j]]+" "+s[bd[c][k]], file=output_file)

def print_board_txt(board, output_file):
    print_board_row(board, 1,2,3,1,2,3, output_file)
    print_board_row(board, 1,2,3,4,5,6, output_file)
    print_board_row(board, 1,2,3,7,8,9, output_file)
    print(" ------+-------+------", file=output_file)
    print_board_row(board, 4,5,6,1,2,3, output_file)
    print_board_row(board, 4,5,6,4,5,6, output_file)
    print_board_row(board, 4,5,6,7,8,9, output_file)
    print(" ------+-------+------", file=output_file)
    print_board_row(board, 7,8,9,1,2,3, output_file)
    print_board_row(board, 7,8,9,4,5,6, output_file)
    print_board_row(board, 7,8,9,7,8,9, output_file)
    print("", file=output_file)

#########################################
# the structure for the game tree

class GameNode:
    # the structure of the game tree node
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

    def cal_value_condition(self, sub_board, condition):
        point_1 = sub_board[condition[0]]
        point_2 = sub_board[condition[1]]
        point_3 = sub_board[condition[2]]
        win, lose = 0, 0
        rate = 1
        for point in [point_1, point_2, point_3]:
            if point == 1:
                win += 1
            elif point == 2:
                lose += 1

        if point_1 != 0 and point_1 in corners:
            rate *= 2
        if point_2 != 0 and point_2 in center:
            rate *= 5
        if point_3 != 0 and point_3 in corners:
            rate *= 2

        if lose == 3:
            return -1000*rate
        elif win == 3:
            return 10000*rate
        elif win == 2 and lose == 0:
            return 30*rate
        elif win == 1 and lose == 0:
            return 1*rate
        elif win == 0 and lose == 2:
            return -30*rate
        elif win == 0 and lose == 1:
            return -1*rate
        else:
            return 0

    def cal_value(self, sub_board):
        index = hash(tuple(sub_board))
        if index in sub_board_values:
            return sub_board_values[index]

        value = 0
        for condition in win_conditions:
            value += self.cal_value_condition(sub_board, condition)
        sub_board_values[index] = value
        return value

    def cal_board_value(self, board):
        index = tuple(map(tuple, board))
        if index in board_values:
            return board_values[index]

        value = 0
        for i in range(1, 10):
            value += self.cal_value(board[i])
        board_values[index] = value
        return value

    def is_finished(self):
        return self.finished

    def check_finished(self):
        # check if the board is finished
        # check the board is win or not
        # The game is won by getting three-in-a row either horizontally, vertically or diagonally in one of the nine boards.
        # we check the small board one by one
        # Define win conditions (patterns) for a 3x3 board

        # Check each small board one by one
        for i in range(1, 10):  # Assuming 9 small boards, indexed from 1 to 9
            for condition in win_conditions:
                if all(self.board[i][pos] == self.player for pos in condition):
                    self.finished = True
                    return

class GameTree:
    # the structure of the game tree
    def __init__(self):
        self.root = None

    def generate_tree(self, board, first_move):
        self.root = GameNode(board, first_move[0], first_move[1], 2, None) # the root is the first move of the opponent
        self._generate_tree_recursive(self.root, 1, 1)  # Start with depth 1, and player 1 (us)

    def _generate_tree_recursive(self, current_node, current_depth, player):
        # Define the maximum depth as a constant, for example, 3 layers deep

        if current_depth > max_depth:
            return

        current_node.check_finished()
        if current_node.is_finished():
            if current_node.player == 1:
                current_node.value = 1000000 * (max_depth + 1 - current_depth)
            else:
                current_node.value = -1000000 * (max_depth + 1 - current_depth)
            return

        # we check in the current board's sub-board(parent's L)
        for i in range(1, 10):  # Assuming board indices go from 1 to 9
            if current_node.board[current_node.L][i] == 0:
                new_board = current_node.board.copy()
                new_board[current_node.L][i] = player
                new_node = GameNode(new_board, current_node.L, i, player, current_node)
                if current_depth == max_depth:
                    new_node_value = new_node.cal_board_value(new_board)
                    new_node.value = new_node_value
                current_node.children.append(new_node)
                self._generate_tree_recursive(new_node, current_depth + 1, 3 - player)

    def print_tree(self, file):
        self._print_tree_recursive(self.root, 0, file)

    def _print_tree_recursive(self, node, depth, file):
        if node is not None:
            print("  " * depth + f"{node.L} {node.player} {node.value}", file=file)
            for child in node.children:
                self._print_tree_recursive(child, depth + 1, file)

    # alpha-beta pruning
    def alpha_beta(self, depth):
        choice = []
        max_value = -np.inf
        for child in self.root.children:
            value = self.min_value(child, -np.inf, np.inf, depth)
            if value > max_value:
                max_value = value
                choice =[child.L]
            elif value == max_value:
                choice.append(child.L)
        # if multiple moves have the same value, choose the random one
        return np.random.choice(choice)

    def max_value(self, node, alpha, beta, depth):
        if depth == 0 or self.isTerminal(node):
            return self.get_value(node)
        clf = -np.inf
        for child in node.children:
            temp_value = self.min_value(child, alpha, beta, depth - 1)
            clf = max(clf, temp_value)
            if clf >= beta:
                return clf
            alpha = max(alpha, clf)
        node.value = clf
        return clf

    def min_value(self, node, alpha, beta, depth):
        if depth == 0 or self.isTerminal(node):
            return self.get_value(node)
        clf = np.inf
        for child in node.children:
            temp_value = self.max_value(child, alpha, beta, depth - 1)
            clf = min(clf, temp_value)
            if clf <= alpha:
                return clf
            beta = min(beta, clf)
        node.value = clf
        return clf

    def get_value(self, node):
        return node.value

    def isTerminal(self, node):
        # no children
        if node.children == []:
            return True
        return False

# update the max depth of the minmax tree
def update_depth(round):
    if round < 3:
        return 3
    elif round < 10:
        return 5
    elif round < 20:
        return 6
    elif round < 25:
        return 7
    elif round < 50:
        return 10
    else:
        return 11

# choose a move to play
def play(first_move):
    # print_board(boards)

    # just play a random move for now
    # n = np.random.randint(1,9)
    # while boards[curr][n] != 0:
    #     n = np.random.randint(1,9)

    # use minmax tree to choice next step
    # generate the game tree if the root is None
    global round
    global max_depth
    global output_file
    round += 1
    print("round", round, "=====================", file=output_file)
    max_depth = update_depth(round)
    print_board_txt(boards, output_file)
    tree = GameTree()
    tree.generate_tree(boards, first_move)
    # print("minmax tree=================================", file=output_file)
    # tree.print_tree(output_file)
    # n equals to the move that has the value is value
    n = tree.alpha_beta(max_depth)
    print("alpha beta cut tree=========================", file=output_file)
    tree.print_tree(output_file)
    print("playing", n)
    print("our move", curr, n, file=output_file)
    place(curr, n, 1)
    print_board_txt(boards, output_file)
    return n

# place a move in the global boards
def place(board, num, player):
    global curr
    curr = num
    boards[board][num] = player

# read what the server sent us and
# parse only the strings that are necessary
def parse(string):
    first_move = []
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
        # place the first move (randomly generated for opponent)
        # print("second move", args)
        first_move = [int(args[0]), int(args[1])]
        place(int(args[0]), int(args[1]), 2)
        return play(first_move)  # choose and return the second move

    # third_move(K,L,M) means that the first and second move were
    # in square L of sub-board K, and square M of sub-board L,
    # and we are expected to return the third move.
    elif command == "third_move":
        # print("third move", args)
        # place the first move (randomly generated for us)
        place(int(args[0]), int(args[1]), 1)
        print("our move", int(args[0]), int(args[1]), file=output_file)
        # place the second move (chosen by opponent)
        first_move = [curr, int(args[2])]
        print("enemy move", curr, int(args[2]), file=output_file)
        place(curr, int(args[2]), 2)
        return play(first_move) # choose and return the third move

    # nex_move(M) means that the previous move was into
    # square M of the designated sub-board,
    # and we are expected to return the next move.
    elif command == "next_move":
        # place the previous move (chosen by opponent)
        first_move = [curr, int(args[0])]
        print("enemy move", curr, int(args[0]), file=output_file)
        place(curr, int(args[0]), 2)
        return play(first_move) # choose and return our next move

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

def close_output():
    global output_file
    output_file.close()

if __name__ == "__main__":
    main()
    output_file.close()