#!/usr/bin/python3

import numpy as np

IS_TEST = False
DAY = 1
part1_expected = 21
part2_expected = 8

if IS_TEST:
    file_name = 'golden_input.txt'
else:
    file_name = 'input.txt'


def load_data(file_name):
    with open(file_name, 'r') as input:
        return input.readlines()

def format_data(lines):
    data = np.full((len(lines) + 2, len(lines[0].strip()) + 2), -1)
    for row, line in enumerate(lines):
        for col, tree in enumerate(line.strip()):
            data[row + 1, col + 1] = int(tree)
    return data

def solve_part1(data):
    ret = 0
    
    for row in range(1, len(data) - 1):
        for col in range(1, len(data[row]) - 1):
            tree = data[row,col]
            curr_col = data[:,col]
            curr_row = data[row,:]
            
            if (max(curr_col[:row]) < tree or   # Check top
                max(curr_col[row+1:]) < tree or # Check bot
                max(curr_row[:col]) < tree or   # Check left
                max(curr_row[col+1:]) < tree):  # Check right
                ret += 1
            
    if IS_TEST and ret != part1_expected:
        print('Part 1 check failed!')
    return ret
    
def solve_part2(data):
    max_scenic_score = 0
    
    for row in range(1, len(data) - 1):
        for col in range(1, len(data[row]) - 1):
            tmp_scenic_score = 1
            tree = data[row,col]
            curr_col = data[:,col]
            curr_row = data[row,:]
            top = curr_col[:row]
            bot = curr_col[row+1:]
            left = curr_row[:col]
            right = curr_row[col+1:]
            
            # check all top trees starting from the tree, excluding the padding
            tmp_multiplier = 0
            for index in range(len(top) - 1, 0, -1):
                tmp_multiplier += 1    
                if top[index] >= tree:
                    break
            tmp_scenic_score *= tmp_multiplier

            # check all bottom trees starting from the tree, excluding the padding
            tmp_multiplier = 0
            for index in range(len(bot) - 1):
                tmp_multiplier += 1
                if bot[index] >= tree:
                    break
            tmp_scenic_score *= tmp_multiplier
            
            # check all left trees starting from the tree, excluding the padding
            tmp_multiplier = 0
            for index in range(len(left) - 1, 0, -1):
                tmp_multiplier += 1
                if left[index] >= tree:
                    break
            tmp_scenic_score *= tmp_multiplier
            
            # check all right trees starting from the tree, excluding the padding
            tmp_multiplier = 0
            for index in range(len(right) - 1):
                tmp_multiplier += 1
                if right[index] >= tree:
                    break
            tmp_scenic_score *= tmp_multiplier
            max_scenic_score = max(max_scenic_score, tmp_scenic_score)
    
    if IS_TEST and max_scenic_score != part2_expected:
        print('Part 2 check failed!')
    return max_scenic_score
    
lines = load_data(file_name)
data = format_data(lines)

print(f'Day{DAY} part 1: {solve_part1(data)}')
print(f'Day{DAY} part 2: {solve_part2(data)}')
