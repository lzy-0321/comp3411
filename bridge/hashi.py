#!/usr/bin/env python3
import numpy as np
import sys

# 增加递归深度限制
sys.setrecursionlimit(10000000)
# define a island symbol type can be 1-9 or a-c, signal symbol for the island
ISLAND_SYMBOLS = "123456789abc"

# gable variable
bridges = []
islands = []
island_path = []

# A bridge is a tuple (start, end, count, direction)
# assume all brigde is from left to right or from top to bottom
class Bridge:
    def __init__(self, id1, id2, start, end, weight, direction):
        self.island1_id = id1
        self.island2_id = id2
        self.start = start  # Tuple (row, col), the starting point of the bridge
        self.end = end      # Tuple (row, col), the ending point of the bridge
        self.weight = weight  # The number of bridges connecting the islands
        self.direction = direction  # 'horizontal' or 'vertical'

    def __repr__(self):
        return f"Bridge(island1_id={self.island1_id}, island2_id={self.island2_id}, start={self.start}, end={self.end}, weight={self.weight}, direction={self.direction})"

    def get_bridges():
        return bridges

    # add a bridge to the bridges list
    def add_bridge(id1, id2, r1, c1, r2, c2, weight):
        if r1 == r2:
            if c1 > c2:
                c1, c2 = c2, c1
            bridges.append(Bridge(id1, id2, (r1, c1+1), (r2, c2-1), weight, 'horizontal'))
        else:
            if r1 > r2:
                r1, r2 = r2, r1
            bridges.append(Bridge(id1, id2, (r1+1, c1), (r2-1, c2), weight, 'vertical'))

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
        self.connect_list = []

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
        id = self.neighbors
        return [Island.get_island_by_id(i) for i in id]

    # get number of unconnected neighbors
    def get_unconnected_neighbors(id):
        island = Island.get_island_by_id(id)
        # print("island", island, id)
        # print("neighbors", island.neighbors)
        # print("connect_list", island.connect_list)
        id_list = list(set(island.neighbors) - set(island.connect_list))
        return id_list

    # get number of neighbors
    def get_number_of_neighbors(self):
        return len(self.neighbors)

    # add a neighbor to the island, neighbor is a island
    def add_connection(self, neighbor, weight):
        self.connect_list.append(neighbor.id)
        self.weight_left -= weight
        neighbor.connect_list.append(self.id)
        neighbor.weight_left -= weight
        # print("add_connection", self, neighbor)

    # remove a neighbor from the island, neighbor is a island
    def remove_connection(self, neighbor, weight):
        self.connect_list.remove(neighbor.id)
        self.weight_left += weight
        neighbor.connect_list.remove(self.id)
        neighbor.weight_left += weight

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
            if visual_map[r][c] in range(10, 13):
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
    if island is None or neighbor is None or weight < 1 or weight > 3:
        return False
    r1, c1 = island.loc
    r2, c2 = neighbor.loc
    # avoid the bridge cross another bridge
    if check_cross(r1, c1, r2, c2):
        return False
    Bridge.add_bridge(island.id, neighbor.id, r1, c1, r2, c2, weight)
    Island.add_connection(island, neighbor, weight)
    return True

def remove_bridge(brigde):
    island1 = Island.get_island_by_id(brigde.island1_id)
    island2 = Island.get_island_by_id(brigde.island2_id)
    if island1 is None or island2 is None:
        return False
    r1, c1 = island1.loc
    r2, c2 = island2.loc
    Bridge.remove_bridge(r1, c1, r2, c2, brigde.weight)
    Island.remove_connection(island1, island2, brigde.weight)
    return True

# check is a bridge crosses another bridge (A parallel bridge cannot pass through the same point as a vertical bridge)
# before try to add a bridge between (r1, c1) and (r2, c2), check if there is a bridge between (r1, c1) and (r2, c2)
# if cross, return True, else return False
def check_cross(r1, c1, r2, c2):
    for b in bridges:
        if r1 == r2: # horizontal
            # Check if the vertical bridge crosses the horizontal one
            c1, c2 = min(c1, c2) + 1, max(c1, c2) - 1
            if (b.start[1] >= c1 and b.start[1] <= c2) and \
                (r1 >= b.start[0] and r1 <= b.end[0]):
                return True
        else:  # bridge is vertical and b is horizontal
            r1, r2 = min(r1, r2) + 1, max(r1, r2) - 1
            # Check if the horizontal bridge crosses the vertical one
            if (b.start[0] >= r1 and b.start[0] <= r2) and \
                (c1 >= b.start[1] and c1 <= b.end[1]):
                return True
    return False

# check does two islands are already conneted
# return True mean already be connected
def is_island_connected(island, neighbors):
    if island is None or neighbors is None:
        return False
    return neighbors.id in island.connect_list

# 刚好足够的邻居技巧（Just Enough Neighbor Technique）：当一个岛屿周围的邻居数量与岛屿上的数字相匹配时，这个技巧会用来确定所有的桥梁。这意味着如果一个岛屿标记为“4”，并且它有四个邻居，则应该与每个邻居建立一座桥。
# 单一未解决的邻居技巧（One Unsolved Neighbor Technique）：如果一个岛屿只有一个尚未连接的邻居，并且该岛屿还需要一座桥来完成其桥梁数量，那么这座桥必须建在这两个岛屿之间。
def apply_just_enough_neighbor_technique(nrow, ncol, map):
    for r in range(nrow):
        for c in range(ncol):
            symbol = str(map[r, c])
            if symbol in ISLAND_SYMBOLS:
                island_temp = Island.get_island_by_loc(r, c)
                neighbors = Island.get_neighbors(island_temp)  # Assuming this returns a list of IDs or coordinates

                if len(neighbors) == 1:
                    neighbor = neighbors[0]
                    if neighbor.weight_left < island_temp.weight_left:
                        return False
                    add_bridge(island_temp, neighbor, island_temp.weight_left)

                # if len(neighbor_ids) == island_temp.weight_left == 4:
                #     for neighbor in neighbors:
                #         if neighbor.weight_left < 1:
                #             return False
                #         add_bridge(island_temp, neighbor, 1)

                if sum([neighbor.weight_left for neighbor in neighbors]) == island_temp.weight_left:
                    for neighbor in neighbors:
                        add_bridge(island_temp, neighbor, neighbor.weight_left)
    return True

# 少数邻居技巧（Few Neighbors Technique）：这个技巧基于桥梁数量的限制规则，如果一个岛屿仅能与有限的几个岛屿建立桥梁，那么会使用此技巧来确定桥梁的分配。

# 剩余技巧（Leftovers Technique）：当一个岛屿的剩余桥数等于其剩余未连接邻居数时使用。这意味着这些桥必须以某种方式分布于剩余的邻居之间。

# 隔离技巧（Isolation Technique）：这是一个关键技巧，它利用了每个岛屿都必须相互连接的规则。如果不连接某些桥梁会导致某个岛屿或岛屿群隔离，那么这些连接就必须建立。
def apply_hashi_techniques(nrow, ncol, map):
    if not apply_just_enough_neighbor_technique(nrow, ncol, map):
        return False
    return True

# Find the starting island which is the island has minium neighbors which has minimum weight_left
def find_next_island(islandsID_list):
    # get the list of islands
    islands_list = [Island.get_island_by_id(id) for id in islandsID_list]

    # 收集符合条件的岛屿
    valid_islands = [island for island in islands_list if island.get_number_of_neighbors() > 0 and island.weight_left > 0]

    # 根据邻居数和 weight_left 排序
    # 注意：这里先按照 weight_left 排序，然后按照邻居数排序，因为Python的排序是稳定的，这样可以确保邻居数优先级更高
    sorted_islands = sorted(valid_islands, key=lambda island: (island.get_number_of_neighbors(), island.weight_left))

    # return the list of id
    return [island.id for island in sorted_islands]

def solve_puzzle(nrow, ncol, map):
    # 先尝试使用Hashi解题技巧
    # add neighbors to the islands
    for island in islands:
        Island.get_island_neighbors(island, nrow, ncol, map)
    apply_hashi_techniques(nrow, ncol, map)
    if Island.all_full():
            return True
    # print_map_with_bridges(nrow, ncol, map)
    starting_islandIDs = find_next_island([island.id for island in islands])
    starting_islandID = starting_islandIDs[0]
    # print("starting_island", starting_islandID)
    not_connected_island = Island.get_unconnected_neighbors(starting_islandID)
    next_islandID_list = find_next_island(not_connected_island)
    # print("next_island_list", next_islandID_list)
    island_path.append([starting_islandID, next_islandID_list, 3])
    if dfs(starting_islandID, next_islandID_list, nrow, ncol, map):
        return True
    else:
        return False

#================================================================================================
# debug print
def print_map_with_bridges_to_string(nrow, ncol, original_map):
    visual_map = add_bridges_to_map(nrow, ncol, original_map)
    map_str = ""
    for r in range(nrow):
        for c in range(ncol):
            if visual_map[r][c] in range(10, 13):
                map_str += chr(visual_map[r][c] + 87)
            else:
                map_str += str(visual_map[r][c])
        map_str += "\n"
    return map_str

def write_info_to_file(starting_islandID, next_islandID_list, nrow, ncol, map):
    with open("info.txt", "a") as file:
        file.write("=======start========\n")
        file.write(f"isfull : {Island.all_full()}\n" )
        file.write("Map:\n")
        file.write(print_map_with_bridges_to_string(nrow, ncol, map))
        file.write(f"starting_island: {starting_islandID}\n")
        file.write(f"next_island_list: {next_islandID_list}\n")
        for island in islands:
            file.write(f"island: {island}\n")
        for bridge in bridges:
            file.write(f"bridge: {bridge}\n")
        for path in island_path:
            file.write(f"island_path : {path}\n")
        file.write("=======end========\n")
#================================================================================================

def dfs_back_to_last_island(starting_islandID, nrow, ncol, map):
    island_path.pop()
    starting_islandID = island_path[-1][0]
    return dfs(starting_islandID, island_path[-1][1], nrow, ncol, map)

def dfs_move_to_next_island(next_islandID, nrow, ncol, map):
    not_connected_island = Island.get_unconnected_neighbors(next_islandID)
    next_next_islandID_list = find_next_island(not_connected_island)
    island_path.append([next_islandID, next_next_islandID_list, 3])
    return dfs(next_islandID, next_next_islandID_list, nrow, ncol, map)

def dfs_move_to_next_in_next_island_list(starting_islandID, nrow, ncol, map):
    island_path[-1][1] = island_path[-1][1][1:]
    island_path[-1][2] = 3
    return dfs(starting_islandID, island_path[-1][1], nrow, ncol, map)

def dfs(starting_islandID, next_islandID_list, nrow, ncol, map):
    write_info_to_file(starting_islandID, next_islandID_list, nrow, ncol, map)
    # if all islands are full, then return True
    if Island.all_full():
        return True

    # if the next_island_list is empty, then return False
    if starting_islandID is island_path[0] and next_islandID_list is None:
        return False

    # if the next_island_list is empty, we need to go back to the last starting_island
    if len(next_islandID_list) == 0 or next_islandID_list is None:
        return dfs_back_to_last_island(starting_islandID, nrow, ncol, map)

    # if we try all connections of the current island, then we need to try next island in the next_island_list
    if island_path[-1][2] == 0:
        # means we need to choose another next island in next_island_list
        if len(next_islandID_list) == 1:
            if len(island_path) == 1:
                return False
            remove_bridge(bridges[-1])
            return dfs_back_to_last_island(starting_islandID, nrow, ncol, map)
        else:
            # remove the last bridge
            remove_bridge(bridges[-1])
            dfs_move_to_next_in_next_island_list(starting_islandID, nrow, ncol, map)

    if next_islandID_list is not None or next_islandID_list or len(next_islandID_list) > 0:
        next_islandID = next_islandID_list[0]
        max_weight = island_path[-1][2]
        bridge_weight = 3
        # we set the initialize max_weight for 3, so if is not 3, means we need to change the weight, and remove the last bridge
        if max_weight < 3:
            remove_bridge(bridges[-1])
        starting_island = Island.get_island_by_id(starting_islandID)
        next_island = Island.get_island_by_id(next_islandID)
        # print("starting_island", starting_island)
        # print("next_island", next_island)
        min_weight = min(starting_island.weight_left, next_island.weight_left)
        if (min_weight >= 3 and max_weight == 3):
            bridge_weight = 3
        elif (min_weight >= 2 and max_weight >= 2):
            bridge_weight = 2
        elif (min_weight >= 1, max_weight >= 1):
            bridge_weight = 1

        # add the bridge
        if add_bridge(starting_island, next_island, bridge_weight):
            # means next time we come back here, we need to change the weight - 1
            island_path[-1][2] = bridge_weight - 1
            if next_island.is_full():
                if len(next_islandID_list) == 1:
                    return dfs_back_to_last_island(next_islandID, nrow, ncol, map)
                else:
                    return dfs_move_to_next_in_next_island_list(starting_islandID, nrow, ncol, map)
            return dfs_move_to_next_island(next_islandID, nrow, ncol, map)
        else:
            if len(next_islandID_list) == 1:
                return dfs_back_to_last_island(starting_islandID, nrow, ncol, map)
            else:
                return dfs_move_to_next_in_next_island_list(starting_islandID, nrow, ncol, map)

def main():
    nrow, ncol, map = scan_map()
    visual_map = map
    print("Scanned Puzzle Map:")
    print_map(nrow, ncol, map)
    # Placeholder for solving the puzzle
    solve_puzzle(nrow, ncol, visual_map)
    print("Solved Puzzle Map:")
    print_map_with_bridges(nrow, ncol, map)
if __name__ == '__main__':
    main()