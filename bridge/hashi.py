#!/usr/bin/env python3
import numpy as np
import sys

# define a island symbol type can be 1-9 or a-c, signal symbol for the island
ISLAND_SYMBOLS = "123456789abc"

# gable variable
bridges = []
islands = []

# A bridge is a tuple (start, end, count, direction)
# assume all brigde is from left to right or from top to bottom
class Bridge:
    def __init__(self, start, end, weight, direction):
        self.start = start  # Tuple (row, col), the starting point of the bridge
        self.end = end      # Tuple (row, col), the ending point of the bridge
        self.weight = weight  # The number of bridges connecting the islands
        self.direction = direction  # 'horizontal' or 'vertical'

    def __repr__(self):
        return f"Bridge(start={self.start}, end={self.end}, weight={self.weight}, direction={self.direction})"

    def get_bridges():
        return bridges

    # add a bridge to the bridges list
    def add_bridge(r1, c1, r2, c2, weight):
        if r1 == r2:
            if c1 > c2:
                c1, c2 = c2, c1
            bridges.append(Bridge((r1, c1+1), (r2, c2-1), weight, 'horizontal'))
        else:
            if r1 > r2:
                r1, r2 = r2, r1
            bridges.append(Bridge((r1+1, c1), (r2-1, c2), weight, 'vertical'))

    # remove the bridge
    def remove_bridge(r1, c1, r2, c2, weight):
        if r1 == r2:
            if c1 > c2:
                c1, c2 = c2, c1
            for b in bridges:
                if b.start == (r1, c1+1) and b.end == (r2, c2-1):
                    if b.weight == weight:
                        bridges.remove(b)
                    elif b.weight > weight:
                        b.weight -= weight
                    else:
                        return False
        else:
            if r1 > r2:
                r1, r2 = r2, r1
            for b in bridges:
                if b.start == (r1+1, c1) and b.end == (r2-1, c2):
                    if b.weight == weight:
                        bridges.remove(b)
                    elif b.weight > weight:
                        b.weight -= weight
                    else:
                        return False

# A island is a tuple (row, col, count)
class Island:
    island_id = 0
    max_single_edges = 3
    def __init__(self, location, weight):
        self.id = Island.island_id
        Island.island_id += 1
        self.loc = location
        self.weight_left = weight
        self.max_degree = weight
        self.neighbors = []

    def __repr__(self):
        return f"Island(id={self.id}, loc={self.loc}, weight_left={self.weight_left}, neighbors={self.neighbors})"

    # add a island to the islands list
    def add_island(location, weight):
        islands.append(Island(location, weight))

    # get island
    def get_island_by_id(id):
        for island in islands:
            if island.id == id:
                return island
        return None

    # get island by location
    def get_island_by_loc(r, c):
        for island in islands:
            if island.loc == (r, c):
                return island
        return None

    # get the list of islands
    def get_list_of_islands():
        if len(islands) == 0:
            return 'No islands found.'
        return islands

    # check if the island is full
    def is_full(self):
        return self.weight_left == 0

    # is all full?
    def all_full():
        for island in islands:
            if not island.is_full():
                return False
        return True

    # get the neighbors of the island
    def get_neighbors(self):
        return self.neighbors

    # get number of neighbors
    def get_number_of_neighbors(self):
        return len(self.neighbors)

    # add a neighbor to the island, neighbor is a island
    def add_neighbor(self, neighbor, weight):
        self.neighbors.append(neighbor)
        self.weight_left -= weight

    # remove a neighbor from the island, neighbor is a island
    def remove_neighbor(self, neighbor, weight):
        self.neighbors.remove(neighbor)
        self.weight_left += weight

    def get_island_neighbors(self, nrow, ncol, map):
        r = self.loc[0]
        c = self.loc[1]
        for i in reversed(range(0, r-1)):
            if map[i, c] != 0:
                neighbor = Island.get_island_by_loc(i, c)
                self.neighbors.append(neighbor.id)
                break
        for i in range(r+1, nrow):
            if map[i, c] != 0:
                neighbor = Island.get_island_by_loc(i, c)
                self.neighbors.append(neighbor.id)
                break
        for j in reversed(range(0, c-1)):
            if map[r, j] != 0:
                neighbor = Island.get_island_by_loc(r, j)
                self.neighbors.append(neighbor.id)
                break
        for j in range(c+1, ncol):
            if map[r, j] != 0:
                neighbor = Island.get_island_by_loc(r, j)
                self.neighbors.append(neighbor.id)
                break

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
                visual_map[b.start[0]][c] = get_bridge_symbol(b.weight, b.direction)
        else:
            for r in range(b.start[0], b.end[0] + 1):
                visual_map[r][b.start[1]] = get_bridge_symbol(b.weight, b.direction)
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
            # Add islands to the islands list
            if text[r][c] in range(1, 13):
                Island.add_island((r, c), text[r][c])

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

# add a bridge to the bridges list, input is the island location, add the bridge location
def add_bridge(island, neighbor, weight):
    # all bridges are from left to right or from top to bottom
    if island is None or neighbor is None:
        return False
    r1, c1 = island.loc
    r2, c2 = neighbor.loc
    Bridge.add_bridge(r1, c1, r2, c2, weight)
    Island.add_neighbor(island, neighbor, weight)
    return True

def remove_bridge(island, neighbor, weight):
    if island is None or neighbor is None:
        return False
    r1, c1 = island.loc
    r2, c2 = neighbor.loc
    Bridge.remove_bridge(r1, c1, r2, c2, weight)
    Island.remove_neighbor(island, neighbor, weight)
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

# 刚好足够的邻居技巧（Just Enough Neighbor Technique）：当一个岛屿周围的邻居数量与岛屿上的数字相匹配时，这个技巧会用来确定所有的桥梁。这意味着如果一个岛屿标记为“4”，并且它有四个邻居，则应该与每个邻居建立一座桥。
# 单一未解决的邻居技巧（One Unsolved Neighbor Technique）：如果一个岛屿只有一个尚未连接的邻居，并且该岛屿还需要一座桥来完成其桥梁数量，那么这座桥必须建在这两个岛屿之间。
def apply_just_enough_neighbor_technique(nrow, ncol, map):
    for r in range(nrow):
        for c in range(ncol):
            symbol = str(map[r, c])
            if symbol in ISLAND_SYMBOLS:
                island_temp = Island.get_island_by_loc(r, c)
                neighbor_ids = Island.get_neighbors(island_temp)  # Assuming this returns a list of IDs or coordinates

                # Convert neighbor IDs or coordinates to Island objects
                neighbors = [Island.get_island_by_id(id) for id in neighbor_ids]

                if len(neighbor_ids) == island_temp.weight_left or sum([neighbor.weight_left for neighbor in neighbors]) == island_temp.weight_left:
                    for neighbor in neighbors:
                        print("add bridge: ", island_temp, neighbor)
                        add_bridge(island_temp, neighbor, neighbor.weight_left)

                if len(neighbor_ids) == 1:
                    neighbor = neighbors[0]
                    print("add bridge: ", island_temp, neighbor)
                    add_bridge(island_temp, neighbor, island_temp.weight_left)

# 少数邻居技巧（Few Neighbors Technique）：这个技巧基于桥梁数量的限制规则，如果一个岛屿仅能与有限的几个岛屿建立桥梁，那么会使用此技巧来确定桥梁的分配。

# 剩余技巧（Leftovers Technique）：当一个岛屿的剩余桥数等于其剩余未连接邻居数时使用。这意味着这些桥必须以某种方式分布于剩余的邻居之间。

# 隔离技巧（Isolation Technique）：这是一个关键技巧，它利用了每个岛屿都必须相互连接的规则。如果不连接某些桥梁会导致某个岛屿或岛屿群隔离，那么这些连接就必须建立。
def apply_hashi_techniques(nrow, ncol, map):
    apply_just_enough_neighbor_technique(nrow, ncol, map)

def dfs_solve(nrow, ncol, map):
    # 如果所有岛屿都正确连接，则返回成功
    if Island.all_full():
        return True

    return False

def solve_puzzle(nrow, ncol, map):
    # 先尝试使用Hashi解题技巧
    apply_hashi_techniques(nrow, ncol, map)

    # # 检查是否所有岛屿都已经连接
    # if not Island.all_full():
    #     # 使用DFS尝试解决未解决的部分
    #     if not dfs_solve(nrow, ncol, map):
    #         return False  # 如果DFS失败，则谜题无解
    return True

def main():
    nrow, ncol, map = scan_map()
    visual_map = map
    print("Scanned Puzzle Map:")
    print_map(nrow, ncol, map)
    # Placeholder for solving the puzzle

    # add neighbors to the islands
    for island in islands:
        Island.get_island_neighbors(island, nrow, ncol, map)
    print(Island.get_list_of_islands())
    solve_puzzle(nrow, ncol, visual_map)
    print("Solved Puzzle Map:")
    print_map_with_bridges(nrow, ncol, map)
if __name__ == '__main__':
    main()

