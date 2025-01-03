#!/usr/bin/python3
#  agent.py
#  Nine-Board Tic-Tac-Toe Agent starter code
#  COMP3411/9814 Artificial Intelligence
#  CSE, UNSW

"""
Ziyao Lu z5340468 
Hanxi Ma z5365221

Question: Briefly describe how your program works, including any algorithms and data structures employed, and explain 
any design decisions you made along the way.

Initially, we used a minimax tree to analyze the possible moves on the board and determine the next move based on the calculated 
board values, which represent the potential number of ways that the agent can form a line of three nodes.However, due to the 
inefficiency of the minimax algorithm causing timeouts, we switched to use alpha-beta pruning tree.

By storing the opponent's last move as the root of the AB tree, we apply alpha-beta pruning recursively to explore all possible moves. 
At each depth of recursion, either when reaching the maximum depth or when one side wins, we read (if the same board state has been 
previously evaluated) or compute a heuristic value. The alpha-beta recursion updates this value and prunes branches accordingly. And 
in all optimal choices (max value), we randomly select one move to avoid always choosing the first optimal solution.

After implementing AB pruning search, we found that calculating the node values directly wasn't good enough. Therefore, we switched 
to use heuristics. This involved counting the number of agent's, opponent's, and empty cells in each row, column, and diagonal of the 
current sub-board. We also considered the positions of these cells to calculate a heuristic value.

In this heuristic approach:
- The node in the center of the board carry have highest weight.
- Midpoints of rows, columns, and diagonals have slightly lower weights compared to the center.
- The node in the four corners of the board carry the lowest weight.

Then we use these weights and the counter of agent's and opponent's nodes in each row, column, and diagonal to calculate the heuristic 
value(e.g there are only one agent in the diagional). 

In our code, we also implemented dynamic depth for the AB tree. The reason why we using dynamic depth is due to that at the beginning 
of the game, we don't need to search very deeply in the tree because the probability of pruning is quite small, and if we search depply 
in the beginning which may lead to timeout.

Therefore, the depth of the AB tree is adjusted dynamically based on the current game round. As the game processing and more moves are
made (the game round increases), we increase the depth of the tree search. 

When max depth is changed to a larger value, which means that there will be a larger tree to search, the time complexity will increase by 
a lots of calculating the heuristic value. But actually, the situation in the sub-board may be as same as one of the previous sub-boards,
so we use a dictionary to store the value of the sub-board to avoid calculating the same sub-board repeatedly. So we can use the hash value
of the sub-board as the key to store the value of the sub-board. And for board value, we also use the hash value of the board to store the
value of the whole board. And we use tuple for the key of the dictionary because the list is unhashable. 

So far, our code can run up to level 8 without timeout, but the win rate is not 100%. We think the next improvement needed is in 
the heuristic value calculation. It may require more detailed analysis of possible board states, but due to ddl is coming we do not 
have much time, so we have not implemented this step yet.

Additionally, we have some other ideas that we have not implemented yet:

- Since our tree doesn't need to go very deep in the early rounds of the game, there are rounds required time is much short. Therefore, 
we can potentially save time for later rounds by pre-computing the values of other boards during the initial rounds.

- Because the board is symmetrical (nodes can appear symmetrically), although node positions are symmetric, their indices are different.
Maybe we can use mathematical methods to align them in dictionaries, which can save time during evaluations.

"""


import random
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
max_size = 3 ** 10
# output_file = open("game_output.txt", "w")

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

center = [5]
corners = [1, 3, 7, 9]
middles = [2, 4, 6, 8]
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

# def print_board_row(bd, a, b, c, i, j, k, output_file):
#     print(" "+s[bd[a][i]]+" "+s[bd[a][j]]+" "+s[bd[a][k]]+" | " \
#              +s[bd[b][i]]+" "+s[bd[b][j]]+" "+s[bd[b][k]]+" | " \
#              +s[bd[c][i]]+" "+s[bd[c][j]]+" "+s[bd[c][k]], file=output_file)

# def print_board_txt(board, output_file):
#     print_board_row(board, 1,2,3,1,2,3, output_file)
#     print_board_row(board, 1,2,3,4,5,6, output_file)
#     print_board_row(board, 1,2,3,7,8,9, output_file)
#     print(" ------+-------+------", file=output_file)
#     print_board_row(board, 4,5,6,1,2,3, output_file)
#     print_board_row(board, 4,5,6,4,5,6, output_file)
#     print_board_row(board, 4,5,6,7,8,9, output_file)
#     print(" ------+-------+------", file=output_file)
#     print_board_row(board, 7,8,9,1,2,3, output_file)
#     print_board_row(board, 7,8,9,4,5,6, output_file)
#     print_board_row(board, 7,8,9,7,8,9, output_file)
#     print("", file=output_file)

#########################################
# the structure for the game tree

class GameTree:
    # the structure of the game tree
    def __init__(self):
        self.tree = {}

    def final_value(self, agent_counter, opponent_counter):
        if agent_counter == 3:
            return 100000
        elif agent_counter == 2 and opponent_counter == 0:
            return 1000
        elif agent_counter == 1 and opponent_counter == 0:
            return 10
        elif opponent_counter == 3:
            return -100000
        elif opponent_counter == 2 and agent_counter == 0:
            return -1000
        elif opponent_counter == 1 and agent_counter == 0:
            return -10
        else:
            return 0

    def cal_value_condition(self, sub_board, condition):
        agent_value = 0
        agent_counter = 0
        opponent_counter = 0
        center_value = 6
        middle_value = 4
        corner_value = 2
        point_1 = sub_board[condition[0]]
        point_2 = sub_board[condition[1]]
        point_3 = sub_board[condition[2]]

        for point in [point_1, point_2, point_3]:
            if point == 1:
                agent_counter += 1
            elif point == 2:
                opponent_counter += 1

        if point_2 in center and point_2 != 0:
            agent_value += center_value
        elif point_2 in middles and point_2 != 0:
            agent_value += middle_value
        if point_1 in corners and point_1 != 0:
            agent_value += corner_value
        if point_3 in corners and point_3 != 0:
            agent_value += corner_value

        return self.final_value(agent_counter, opponent_counter) + agent_value

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
        index = hash(tuple(tuple(sub) for sub in board))
        if index in board_values:
            return board_values[index]

        value = 0
        for i in range(1, 10):
            value += self.cal_value(board[i])
        board_values[index] = value
        return value

    def check_finished(self, board):
        # check if the board is finished
        # check the board is win or not
        # The game is won by getting three-in-a row either horizontally, vertically or diagonally in one of the nine boards.
        # we check the small board one by one
        # Define win conditions (patterns) for a 3x3 board

        # Check each small board one by one
        for i in range(1, 10):  # Assuming 9 small boards, indexed from 1 to 9
            for condition in win_conditions:
                if all(board[i][pos] == 1 for pos in condition) or all(board[i][pos] == 2 for pos in condition):
                    return True
        return False

    def generate_tree(self, board, first_move):
        deep = 1
        pre_move = first_move[1]
        best_moves, best_move_score = [], -np.inf
        for i in range(1, 10):
            if board[pre_move][i] == 0:
                move = i
                board[first_move[1]][move] = 1 # place the move
                move_value = self.alpha_beta_generate(board, curr, move, 2, -np.inf, np.inf, deep)
                board[first_move[1]][move] = 0 # remove the move
                if move_value > best_move_score:
                    best_moves = [move]
                    best_move_score = move_value
                elif move_value == best_move_score:
                    best_moves.append(move)
        return random.choice(best_moves)

    def alpha_beta_generate(self, board, k, L, player, alpha, beta, deep):
        moves = []
        for i in range(1, 10):
            if board[L][i] == 0:
                moves.append(i)
        if moves == []:
            return 1000

        if self.check_finished(board):
            if player == 2:
                return 1000000*(max_depth+1 - deep)
            else:
                return -1000000*(max_depth+1 - deep)

        if deep == max_depth:
            # we need to calculate the value of the node
            value = self.cal_board_value(board)
            return value

        # we assume that we are the player 1
        if player == 1:
            return self.max_value(board, k, L, player, alpha, beta, deep, moves)
        else:
            return self.min_value(board, k, L, player, alpha, beta, deep, moves)

    def max_value(self, board, k, L, player, alpha, beta, deep, moves):
        value = -np.inf
        for move in moves:
            board[L][move] = player
            value = max(value, self.alpha_beta_generate(board, L, move, 2, alpha, beta, deep + 1))
            board[L][move] = 0
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    def min_value(self, board, k, L, player, alpha, beta, deep, moves):
        value = np.inf
        for move in moves:
            board[L][move] = player
            value = min(value, self.alpha_beta_generate(board, L, move, 1, alpha, beta, deep + 1))
            board[L][move] = 0
            if value <= alpha:
                return value
            beta = min(beta, value)
        return value

# update the max depth of the minmax tree
def update_depth(round):
    if round < 3:
        return 3
    elif round < 11:
        return 5
    elif round < 15:
        return 6
    elif round < 17:
        return 7
    elif round < 20:
        return 8
    elif round < 29:
        return 9
    elif round < 40:
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
    # print("round", round, "=====================", file=output_file)
    max_depth = update_depth(round)
    # print_board_txt(boards, output_file)
    tree = GameTree()
    n = tree.generate_tree(boards, first_move)
    print("playing", n)
    # print("our move", curr, n, file=output_file)
    place(curr, n, 1)
    # print_board_txt(boards, output_file)
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
        # print("our move", int(args[0]), int(args[1]), file=output_file)
        # place the second move (chosen by opponent)
        first_move = [curr, int(args[2])]
        # print("enemy move", curr, int(args[2]), file=output_file)
        place(curr, int(args[2]), 2)
        return play(first_move) # choose and return the third move

    # nex_move(M) means that the previous move was into
    # square M of the designated sub-board,
    # and we are expected to return the next move.
    elif command == "next_move":
        # place the previous move (chosen by opponent)
        first_move = [curr, int(args[0])]
        # print("enemy move", curr, int(args[0]), file=output_file)
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

if __name__ == "__main__":
    main()
    # output_file.close()
