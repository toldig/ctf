#!/usr/bin/python3

import numpy as np

# Update these for each day
IS_TEST = True
DAY = 1
part1_expected = 0
part2_expected = 0

if IS_TEST:
    file_name = 'golden_input.txt'
else:
    file_name = 'input.txt'

def load_data(file_name):
    with open(file_name, 'r') as input:
        return input.readlines()

def format_data(lines):
    # Format data here
    return lines

def solve_part1(data):
    ret = 0
    
    # Solve part 1 here
    
    if IS_TEST and ret != part1_expected:
        print('Part 1 check failed!')
    return ret
    
def solve_part2(data):
    ret = 0
    
    # Solve part 2 here
    
    if IS_TEST and ret != part2_expected:
        print('Part 2 check failed!')
    return ret
    
lines = load_data(file_name)
data = format_data(lines)

print(f'Day{DAY} part 1: {solve_part1(data)}')
print(f'Day{DAY} part 2: {solve_part2(data)}')
