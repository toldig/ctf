#!/usr/bin/python3

import numpy as np
import sys

# Update these for each day
IS_TEST = False
DAY = 14
part1_expected = 24
part2_expected = 93
hole_row = 0
hole_col = 500

if IS_TEST:
    file_name = 'golden_input.txt'
else:
    file_name = 'input.txt'

def load_data(file_name):
    with open(file_name, 'r') as input:
        return input.readlines()

def print_cave(cave):
    for line in cave:
        print(''.join(line[400:]))
    print()

def format_data(lines):
    # Parse walls
    walls = []
    max_col = 0 # y
    max_row = 0 # x
    for line in lines:
        wall = []
        for coord in line.strip().split('->'):
            c = coord.strip().split(',')
            col = int(c[0])
            row = int(c[1])
            max_col = max(col, max_col)
            max_row = max(row, max_row)
            wall.append([row, col])
        walls.append(wall)
    # Init array
    cave = np.full((max_row + 3, max_col + 1000), '.')
    # Add walls
    for wall in walls:
        for index in range(len(wall)-1):
            # Draw wall
            is_fix_row = True
            const = wall[index][0]
            range_min = min(wall[index][1], wall[index+1][1])
            range_max = max(wall[index][1], wall[index+1][1])
            if wall[index][1] == wall[index+1][1]:
                is_fix_row = False
                const = wall[index][1]
                range_min = min(wall[index][0], wall[index+1][0])
                range_max = max(wall[index][0], wall[index+1][0])
            for var in range(range_min, range_max + 1):
                if is_fix_row:
                    cave[const, var] = '#'
                else:
                    cave[var, const] = '#'
    for i in range(len(cave[-1])):
        cave[-1][i] = '_'
    cave[hole_row, hole_col] = '+'
    return cave

def drop_sand(cave, must_abort):
    row = hole_row
    col = hole_col
    while True:
        try:
            if must_abort and cave[row + 1][col] == '_':
                raise IndexError
            # A unit of sand always falls down one step if possible.
            if cave[row + 1][col] == '.':
                row += 1
                # print(f'{row},{col} below')
            # If the tile immediately below is blocked (by rock or sand), the unit of sand attempts to instead move diagonally one step down and to the left.
            elif cave[row + 1][col - 1] == '.':
                row += 1
                col -= 1
                # print(f'{row},{col} below left')
            # If that tile is blocked, the unit of sand attempts to instead move diagonally one step down and to the right.
            elif cave[row + 1][col + 1] == '.':
                row += 1
                col += 1
                # print(f'{row},{col} below right')
            else:
            # If all three possible destinations are blocked, the unit of sand comes to rest
               cave[row, col] = 'o'
               break
        except IndexError:
            return cave, False
    return cave, True

def solve_part1(data):
    ret = 0

    state = True
    while state:
        data, state = drop_sand(data, True)
        ret += 1
    ret -= 1
    if IS_TEST and ret != part1_expected:
        print('Part 1 check failed!')
    return ret
    
def solve_part2(data):
    ret = 0
    
    state = True
    while state:
        data, state = drop_sand(data, False)
        ret += 1
        if data[hole_row, hole_col] == 'o':
            break
    
    if IS_TEST and ret != part2_expected:
        print('Part 2 check failed!')
    return ret
    
lines = load_data(file_name)

print(f'Day{DAY} part 1: {solve_part1(format_data(lines))}')
print(f'Day{DAY} part 2: {solve_part2(format_data(lines))}')
