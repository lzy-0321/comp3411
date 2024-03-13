#!/usr/bin/env python3
import numpy as np
import sys

# define a island symbol type can be 1-9 or a-c, signal symbol for the island
ISLAND_SYMBOLS = "123456789abc"

# def island_symbol_to_number(symbol):
#     if symbol in '123456789':
#         return int(symbol)
#     elif symbol == 'a':
#         return 10
#     elif symbol == 'b':
#         return 11
#     elif symbol == 'c':
#         return 12
#     else:
#         return None  # 非岛屿字符返回None

# A bridge is a tuple (start, end, count, direction)
class Bridge:
    def __init__(self, start, end, count, direction):
        self.start = start  # Tuple (row, col), the starting point of the bridge
        self.end = end      # Tuple (row, col), the ending point of the bridge
        self.count = count  # The number of bridges connecting the islands
        self.direction = direction  # 'horizontal' or 'vertical'

    def __repr__(self):
        return f"Bridge(start={self.start}, end={self.end}, count={self.count}, direction='{self.direction}')"

# A island is a tuple (row, col, count)
# class Island:
#     def __init__(self, row, col, count):
#         self.row = row
#         self.col = col
#         self.count = count
#     def __repr__(self):
#         return f"Island(row={self.row}, col={self.col}, count={self.count})"

def get_bridge_symbol(count, direction):
    symbols = {
        (1, 'horizontal'): '-',
        (1, 'vertical'): '|',
        (2, 'horizontal'): '=',
        (2, 'vertical'): '"',
        (3, 'horizontal'): 'E',
        (3, 'vertical'): '#',
    }
    return symbols.get((count, direction), ' ')


def add_bridges_to_map(nrow, ncol, original_map, bridges):
    #if is a island, then is the island, if is a bridge, add the bridge, overwise is a space
    visual_map = [[' ' for _ in range(ncol)] for _ in range(nrow)]
    for r in range(nrow):
        for c in range(ncol):
            if original_map[r, c] != 0:
                visual_map[r][c] = original_map[r, c]
    for b in bridges:
        if b.direction == 'horizontal':
            for c in range(b.start[1], b.end[1] + 1):
                visual_map[b.start[0]][c] = get_bridge_symbol(b.count, b.direction)
        else:
            for r in range(b.start[0], b.end[0] + 1):
                visual_map[r][b.start[1]] = get_bridge_symbol(b.count, b.direction)
    return visual_map

# if is a island, print the island, if is a bridge, print the bridge, overwise print a space
def print_map_with_bridges(nrow, ncol, original_map, bridges):
    visual_map = add_bridges_to_map(nrow, ncol, original_map, bridges)
    for r in range(nrow):
        for c in range(ncol):
            # if is 10, 11, 12, then print a, b, c
            if visual_map[r][c] in range(9, 13):
                print(chr(visual_map[r][c] + 87), end="")
            else:
                print(visual_map[r][c], end="")
        print()

def scan_map():
    """
    Reads the puzzle map from stdin, converts it to a numerical representation,
    and returns it along with its dimensions.
    """
    text = []
    for line in sys.stdin:
        row = [convert_char_to_num(ch) for ch in line.strip() if ch.isnumeric() or ch in '.abcdefghi']
        if row:  # Ensure the row is not empty
            text.append(row)

    nrow = len(text)
    ncol = len(text[0]) if text else 0

    map = np.zeros((nrow, ncol), dtype=np.int32)
    for r in range(nrow):
        for c in range(ncol):
            map[r, c] = text[r][c]

    return nrow, ncol, map

def convert_char_to_num(ch):
    """
    Converts a character to the corresponding number. '.' to 0, '1'-'9' to their numeric values,
    'a'-'i' to 10-18 (to support puzzles with numbers higher than 9).
    """
    if ch == '.':
        return 0
    elif ch.isnumeric():
        return int(ch)
    else:
        return ord(ch) - 87  # Convert 'a'-'i' to 10-18

def print_map(nrow, ncol, map):
    """
    Prints the puzzle map using the numerical representation.
    """
    code = ".123456789abc"
    for r in range(nrow):
        for c in range(ncol):
            print(code[map[r, c]], end="")
        print()

# all bridges must run horizontally or vertically
# bridges are not allowed to cross each other, or other islands
# there can be no more than three bridges connecting any pair of islands
# the total number of bridges connected to each island must be equal to the number on the island

# check is a bridge crosses another bridge (A parallel bridge cannot pass through the same point as a vertical bridge)
def check_cross(bridge, bridges):
    for b in bridges:
        # One is horizontal and the other is vertical
        if bridge.direction == 'horizontal':
            # Check if the vertical bridge crosses the horizontal one
            if (b.start[1] >= bridge.start[1] and b.start[1] <= bridge.end[1]) and \
                (bridge.start[0] >= b.start[0] and bridge.start[0] <= b.end[0]):
                return True
        else:  # bridge is vertical and b is horizontal
            if (bridge.start[1] >= b.start[1] and bridge.start[1] <= b.end[1]) and \
                (b.start[0] >= bridge.start[0] and b.start[0] <= bridge.end[0]):
                return True
    return False

# for a given island, check if the number of bridges connected to it is equal to the number on the island, if is cannot add more bridges.
def check_island_bridges(r, c, n, bridges):
    count = 0
    for b in bridges:
        # for horizontal bridge
        if b.start[0] == b.end[0] and b.start[0] == r:
            if (b.start[1] == c + 1  and b.end[1] >= c) or (b.end[1] == c - 1 and b.start[1] <= c):
                count += b.count
        # for vertical bridge
        elif b.start[1] == b.end[1] and b.start[1] == c:
            if (b.start[0] == r + 1 and b.end[0] >= r) or (b.end[0] == r - 1 and b.start[0] <= r):
                count += b.count
    print(r, c, n, count)
    return n == count

# check is all islands are connected, going through all the islands and check_island_bridges for each one
def check_islands_connected(nrow, ncol, map, bridges):
    for r in range(nrow):
        for c in range(ncol):
            symbol = str(map[r, c])
            # if is a island, check if the number of bridges connected to it is equal to the number on the island
            if symbol in ISLAND_SYMBOLS:
                island_number = convert_char_to_num(symbol)
                if not check_island_bridges(r, c, island_number, bridges):
                    return False
    return True

# # 检查桥两端的island增加的最大桥数
# def check_max_bridges(start, end, bridges, map):
#     # 检查桥两端的island增加的最大桥数
#     if start[0] == end[0]:  # 横向桥
#         # 横向桥的两端的island的最大桥数
#         max_bridges = island_symbol_to_number(map[start[0], start[1]]) - 1
#         # 横向桥的两端的island的已有桥数
#         for b in bridges:
#             if b.start[0] == start[0] and b.start[1] < end[1] and b.end[1] > start[1]:
#                 max_bridges -= b.count
#         return max_bridges
#     else:  # 纵向桥
#         # 纵向桥的两端的island的最大桥数
#         max_bridges = island_symbol_to_number(map[start[0], start[1]]) - 1
#         # 纵向桥的两端的island的已有桥数
#         for b in bridges:
#             if b.start[1] == start[1] and b.start[0] < end[0] and b.end[0] > start[0]:
#                 max_bridges -= b.count
#         return max_bridges

# # add bridge
# def add_bridge(start, end, count, direction, bridges, map):
#     # check if the bridge crosses another bridge
#     if check_cross(Bridge(start, end, count, direction), bridges):
#         return False
#     # check if the bridge is already in the list
#     for b in bridges:
#         if b.start == start and b.end == end and b.direction == direction:
#             # add the count to the bridge
#             b.count += count
#             return True
#     # add the bridge to the list
#     bridges.append(Bridge(start, end, count, direction))


def solve_puzzle(map, bridges):
    # loop through all the islands

    #test2.txt
    #..1..
    #.....
    #1...1
    #.....
    #1.2.2
    #add a bridge from between 1...1

    # # test for print_map_with_bridges
    # bridges.append(Bridge((2, 1), (2, 3), 1, 'horizontal'))
    # #test for check_cross
    # print(check_cross(Bridge((1, 2), (3, 2), 1, 'vertical'), bridges))

    # # test for check_islands_connected
    # bridges.append(Bridge((1, 2), (3, 2), 1, 'vertical'))
    # bridges.append(Bridge((3, 0), (3, 0), 1, 'vertical'))
    # bridges.append(Bridge((3, 4), (3, 4), 1, 'vertical'))
    # bridges.append(Bridge((4, 1), (4, 1), 1, 'horizontal'))
    # bridges.append(Bridge((4, 3), (4, 3), 1, 'horizontal'))
    # print(bridges)
    # print(check_islands_connected(5, 5, map, bridges))


    # test for 12
    #test3.txt
    # ..3..
    # .....
    # 3.c.3
    # .....
    # ..3..
    # bridges.append(Bridge((1, 2), (1, 2), 3, 'vertical'))
    # bridges.append(Bridge((3, 2), (3, 2), 3, 'vertical'))
    # bridges.append(Bridge((2, 1), (2, 1), 3, 'horizontal'))
    # bridges.append(Bridge((2, 3), (2, 3), 3, 'horizontal'))
    # print(check_islands_connected(5, 5, map, bridges))
    return False  # If no configuration works, backtrack

def main():
    nrow, ncol, map = scan_map()
    print("Scanned Puzzle Map:")
    print_map(nrow, ncol, map)
    Bridges = []
    # Placeholder for solving the puzzle
    solve_puzzle(map, Bridges)

    # For now, just reprint the original map
    print("Solved Puzzle Map (placeholder):")
    print_map_with_bridges(nrow, ncol, map, Bridges)

if __name__ == '__main__':
    main()

