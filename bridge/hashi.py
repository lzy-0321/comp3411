#!/usr/bin/env python3
import numpy as np
import sys

# define a island symbol type can be 1-9 or a-c, signal symbol for the island
ISLAND_SYMBOLS = "123456789abc"

# A bridge is a tuple (start, end, count, direction)
# assume all brigde is from left to right or from top to bottom
class Bridge:
    def __init__(self, start, end, count, direction):
        self.start = start  # Tuple (row, col), the starting point of the bridge
        self.end = end      # Tuple (row, col), the ending point of the bridge
        self.count = count  # The number of bridges connecting the islands
        self.direction = direction  # 'horizontal' or 'vertical'

    def __repr__(self):
        return f"Bridge(start={self.start}, end={self.end}, count={self.count}, direction='{self.direction}')"

# A island is a tuple (row, col, count)
class Island:
    def __init__(self, row, col, count):
        self.row = row
        self.col = col
        self.count = count
    def __repr__(self):
        return f"Island(row={self.row}, col={self.col}, count={self.count})"

# goable variable
bridges = []
islands = []

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


def add_bridges_to_map(nrow, ncol, original_map):
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
def print_map_with_bridges(nrow, ncol, original_map):
    visual_map = add_bridges_to_map(nrow, ncol, original_map)
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

# get_list_of_islands
def get_list_of_islands(nrow, ncol, map):
    for r in range(nrow):
        for c in range(ncol):
            symbol = str(map[r, c])
            if symbol in ISLAND_SYMBOLS:
                island_number = convert_char_to_num(symbol)
                islands.append(Island(r, c, island_number))

# add bridges to islands
def add_island_bridges(r1, c1, r2, c2):
    # minis count to the island in island list
    for island in islands:
        if island.row == r1 and island.col == c1:
            island.count -= 1
        if island.row == r2 and island.col == c2:
            island.count -= 1

# minis bridges to islands
def minis_island_bridges(r1, c1, r2, c2):
    # add count to the island in island list
    for island in islands:
        if island.row == r1 and island.col == c1:
            island.count += 1
        if island.row == r2 and island.col == c2:
            island.count += 1

# add a bridge to the bridges list, input is the island location, add the bridge location
def add_bridge(r1, c1, r2, c2, count):
    # all brigde is from left to right or from top to bottom
    if r1 == r2:
        # if c1 > c2, then swap c1 and c2
        if c1 > c2:
            c1, c2 = c2, c1
        if check_cross(Bridge((r1, c1), (r2, c2), count, 'horizontal')):
            return False
        bridges.append(Bridge((r1, c1+1), (r2, c2-1), count, 'horizontal'))
    else:
        if r1 > r2:
            r1, r2 = r2, r1
        if check_cross(Bridge((r1, c1), (r2, c2), count, 'vertical')):
            return False
        bridges.append(Bridge((r1+1, c1), (r2-1, c2), count, 'vertical'))
    add_island_bridges(r1, c1, r2, c2)
    return True

def remove_bridge(r1, c1, r2, c2, count):
    if r1 == r2:
        if c1 > c2:
            c1, c2 = c2, c1
        for b in bridges:
            if b.start == (r1, c1+1) and b.end == (r2, c2-1):
                if b.count == count:
                    bridges.remove(b)
                elif b.count > count:
                    b.count -= count
                else:
                    return False
    else:
        if r1 > r2:
            r1, r2 = r2, r1
        for b in bridges:
            if b.start == (r1+1, c1) and b.end == (r2-1, c2):
                if b.count == count:
                    bridges.remove(b)
                elif b.count > count:
                    b.count -= count
                else:
                    return False
    minis_island_bridges(r1, c1, r2, c2)
    return True

# check is a bridge crosses another bridge (A parallel bridge cannot pass through the same point as a vertical bridge)
def check_cross(bridge):
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

# return the number of bridges connected to a island
def count_island_bridges(r, c):
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
    return count

# return the number can be connected to a island
def get_island_connectable_bridges(r, c, map):
    count = count_island_bridges(r, c)
    needed = int(map[r, c])
    return needed - count

# for a given island, check if the number of bridges connected to it is equal to the number on the island, if is cannot add more bridges.
def check_island_bridges(r, c, n):
    count = count_island_bridges(r, c)
    print(r, c, n, count)
    return n == count

# check is all islands are connected, going through all the islands and check_island_bridges for each one
def all_islands_connected(nrow, ncol, map):
    for r in range(nrow):
        for c in range(ncol):
            symbol = str(map[r, c])
            # if is a island, check if the number of bridges connected to it is equal to the number on the island
            if symbol in ISLAND_SYMBOLS:
                island_number = convert_char_to_num(symbol)
                if not check_island_bridges(r, c, island_number):
                    return False
    return True

def get_island_neighbors(r, c, nrow, ncol, map):
    # 找到一个岛屿的4个方向存在的最近岛屿
    neighbors = []
    # 向四个方向查找，如果是岛屿，加入neighbors
    for i in reversed(range(0, r-1)):
        if map[i, c] != 0:
            neighbors.append([(i, c), get_island_connectable_bridges(i, c, map)])
            break
    for i in range(r+1, nrow):
        if map[i, c] != 0:
            neighbors.append([(i, c), get_island_connectable_bridges(i, c, map)])
            break
    for j in reversed(range(0, c-1)):
        if map[r, j] != 0:
            neighbors.append([(r, j), get_island_connectable_bridges(r, j, map)])
            break
    for j in range(c+1, ncol):
        if map[r, j] != 0:
            neighbors.append([(r, j), get_island_connectable_bridges(r, j, map)])
            break
    print(neighbors)
    return neighbors

# 刚好足够的邻居技巧（Just Enough Neighbor Technique）：当一个岛屿周围的邻居数量与岛屿上的数字相匹配时，这个技巧会用来确定所有的桥梁。这意味着如果一个岛屿标记为“4”，并且它有四个邻居，则应该与每个邻居建立一座桥。
# 单一未解决的邻居技巧（One Unsolved Neighbor Technique）：如果一个岛屿只有一个尚未连接的邻居，并且该岛屿还需要一座桥来完成其桥梁数量，那么这座桥必须建在这两个岛屿之间。
def apply_just_enough_neighbor_technique(nrow, ncol, map):
    for r in range(nrow):
        for c in range(ncol):
            symbol = str(map[r, c])
            if symbol in ISLAND_SYMBOLS:
                island_number = convert_char_to_num(symbol)
                neighbors = get_island_neighbors(r, c, nrow, ncol, map)
                # 1. 岛屿周围的邻居数量与岛屿上的数字相匹配
                # 2. 岛屿上的桥梁总数量与岛屿周围的邻居需要的总和数量相匹配
                # or
                # 1. 岛屿只有一个尚未连接的邻居
                # 2. 该岛屿还需要一座桥来完成其桥梁数量
                if len(neighbors) == island_number or sum([neighbor[1] for neighbor in neighbors]) == island_number:
                    for neighbor in neighbors:
                        add_bridge(r, c, neighbor[0][0], neighbor[0][1], neighbor[1])
                if len(neighbors) == 1 and island_number - count_island_bridges(r, c) == 1:
                    add_bridge(r, c, neighbors[0][0], neighbors[0][1], 1)

# 少数邻居技巧（Few Neighbors Technique）：这个技巧基于桥梁数量的限制规则，如果一个岛屿仅能与有限的几个岛屿建立桥梁，那么会使用此技巧来确定桥梁的分配。

# 剩余技巧（Leftovers Technique）：当一个岛屿的剩余桥数等于其剩余未连接邻居数时使用。这意味着这些桥必须以某种方式分布于剩余的邻居之间。

# 隔离技巧（Isolation Technique）：这是一个关键技巧，它利用了每个岛屿都必须相互连接的规则。如果不连接某些桥梁会导致某个岛屿或岛屿群隔离，那么这些连接就必须建立。
def apply_hashi_techniques(nrow, ncol, map):
    apply_just_enough_neighbor_technique(nrow, ncol, map)

def dfs_solve(nrow, ncol, map):
    # 如果所有岛屿都正确连接，则返回成功
    if all_islands_connected(map):
        return True

    return False

def solve_puzzle(nrow, ncol, map):
    # 先尝试使用Hashi解题技巧
    apply_hashi_techniques(nrow, ncol, map)

    # 检查是否所有岛屿都已经连接
    if not all_islands_connected(nrow, ncol, map):
        # 使用DFS尝试解决未解决的部分
        if not dfs_solve(nrow, ncol, map):
            return False  # 如果DFS失败，则谜题无解
    return True

def main():
    nrow, ncol, map = scan_map()
    visual_map = map
    print("Scanned Puzzle Map:")
    print_map(nrow, ncol, map)
    get_list_of_islands(nrow, ncol, map)
    # Placeholder for solving the puzzle
    solve_puzzle(nrow, ncol, visual_map)
    print("Solved Puzzle Map:")
    print_map_with_bridges(nrow, ncol, map)
if __name__ == '__main__':
    main()

