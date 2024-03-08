#!/usr/bin/env python3
import numpy as np
import sys

class Bridge:
    def __init__(self, start, end, count, direction):
        self.start = start
        self.end = end
        self.count = count
        self.direction = direction

    def __repr__(self):
        return f"Bridge(start={self.start}, end={self.end}, count={self.count}, direction='{self.direction}')"


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

def add_bridges_to_map(original_map, bridges):
    # Create a visual representation of the map based on the original map
    nrow, ncol = original_map.shape
    visual_map = [[' ' if original_map[r, c] == 0 else '.' for c in range(ncol)] for r in range(nrow)]

    for bridge in bridges:
        start, end, count, direction = bridge
        symbol = get_bridge_symbol(count, direction)

        if direction == 'horizontal':
            row = start[0]
            for col in range(start[1], end[1] + 1):  # Ensure correct range for bridge placement
                visual_map[row][col] = symbol
        else:  # direction == 'vertical'
            col = start[1]
            for row in range(start[0], end[0] + 1):  # Ensure correct range for bridge placement
                visual_map[row][col] = symbol

    return visual_map

def print_map_with_bridges(original_map, bridges):
    # Adjust map dimensions as necessary
    nrow, ncol = original_map.shape

    # Add bridges to the visual map based on the original map
    visual_map = add_bridges_to_map(original_map, bridges)

    # Print the map
    for row in visual_map:
        print(''.join(row))

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

def solve_puzzle(map, bridges=[], x=0, y=0):
    if all_islands_connected(map, bridges):
        print_map_with_bridges(map, bridges)
        return True

    for bridge in generate_possible_bridges(map, bridges, x, y):
        if is_bridge_valid(map, bridges, bridge):
            bridges.append(bridge)
            next_x, next_y = get_next_island(map, x, y)
            if solve_puzzle(map, bridges, next_x, next_y):
                return True  # Propagate the success back up the recursion
            bridges.pop()  # Backtrack

    return False  # If no configuration works, backtrack

def all_islands_connected(map, bridges):
    # Create a dictionary to keep track of the number of bridges connected to each island.
    # The key will be the island's coordinates (row, col), and the value will be the count of bridges.
    bridge_count = {(r, c): 0 for r in range(map.shape[0]) for c in range(map.shape[1]) if map[r, c] > 0}

    # Iterate over all bridges and increment the bridge count for both the start and end islands.
    for bridge in bridges:
        # Update the count for the start and end islands of each bridge.
        # Note that the count is incremented by the bridge's count since it can represent 1 to 3 bridges.
        bridge_count[bridge.start] += bridge.count
        bridge_count[bridge.end] += bridge.count

    # Check if the number of bridges connected to each island matches the number on the island.
    for (r, c), count in bridge_count.items():
        if map[r, c] != count:
            return False  # Found an island with incorrect number of bridges.

    return True  # All islands have the correct number of bridges.

def generate_possible_bridges(map, existing_bridges, x, y):
    potential_bridges = []

    # Directions to look for potential bridges: (dx, dy)
    directions = {'right': (0, 1), 'left': (0, -1), 'up': (-1, 0), 'down': (1, 0)}

    for direction, (dx, dy) in directions.items():
        nx, ny = x + dx, y + dy  # Start from the next cell in the direction

        # Look in the direction until hitting another island or the edge of the map
        while 0 <= nx < map.shape[0] and 0 <= ny < map.shape[1]:
            if map[nx, ny] > 0:  # Found a potential end island
                # Check if a bridge can be placed between (x, y) and (nx, ny)
                if can_place_bridge(existing_bridges, (x, y), (nx, ny)):
                    # For each possible bridge count (1-3), create a Bridge object
                    for count in range(1, 4):  # 1 to 3 bridges
                        if is_bridge_placement_valid(existing_bridges, x, y, nx, ny, count):
                            potential_bridges.append(Bridge((x, y), (nx, ny), count, 'horizontal' if dx == 0 else 'vertical'))
                break  # Stop looking in this direction after finding the first island
            nx += dx
            ny += dy

    return potential_bridges

def can_place_bridge(existing_bridges, start, end):
    # This function checks if there's already a bridge between start and end
    # It should also check if adding another bridge would exceed the maximum of 3
    # Implementation depends on how existing_bridges is structured
    # For simplicity, let's assume it's a list of Bridge objects
    for bridge in existing_bridges:
        if (bridge.start == start and bridge.end == end) or (bridge.start == end and bridge.end == start):
            if bridge.count == 3:  # Already have the max number of bridges
                return False
    return True

def is_bridge_valid(map, existing_bridges, new_bridge):
    # Assuming bridges can only be straight lines, check if the path between
    # the start and end points crosses any islands or other bridges.
    start, end = new_bridge.start, new_bridge.end
    direction = new_bridge.direction

    if direction == 'horizontal':
        fixed_row = start[0]
        for col in range(min(start[1], end[1]) + 1, max(start[1], end[1])):
            # Check for any island in the path
            if map[fixed_row, col] > 0:
                return False
            # Check for crossing bridges
            for bridge in existing_bridges:
                if bridge.direction == 'vertical' and bridge.start[1] <= col <= bridge.end[1] and bridge.start[0] <= fixed_row <= bridge.end[0]:
                    return False
    else:  # direction == 'vertical'
        fixed_col = start[1]
        for row in range(min(start[0], end[0]) + 1, max(start[0], end[0])):
            # Check for any island in the path
            if map[row, fixed_col] > 0:
                return False
            # Check for crossing bridges
            for bridge in existing_bridges:
                if bridge.direction == 'horizontal' and bridge.start[0] <= row <= bridge.end[0] and bridge.start[1] <= fixed_col <= bridge.end[1]:
                    return False

    return True


def get_next_island(map, x, y):
    # Scan the map from the current position to find the next island.
    for nx in range(x, map.shape[0]):
        start_col = y if nx == x else 0  # Start from the next column if on the same row, else start from the first column
        for ny in range(start_col, map.shape[1]):
            if map[nx, ny] > 0:
                return nx, ny
    return None, None  # Return None if no more islands are found


def main():
    nrow, ncol, map = scan_map()
    print("Scanned Puzzle Map:")
    print_map(nrow, ncol, map)

    # Placeholder for solving the puzzle
    # solve_puzzle(map)

    # For now, just reprint the original map
    # print("Solved Puzzle Map (placeholder):")
    # print_map(nrow, ncol, map)

if __name__ == '__main__':
    main()

