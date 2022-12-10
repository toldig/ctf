#!/usr/bin/python3

import numpy as np

# Update these for each day
IS_TEST = False
DAY = 1
part1_expected = 13140
part2_expected = 0

if IS_TEST:
    file_name = 'golden_input.txt'
else:
    file_name = 'input.txt'

def load_data(file_name):
    with open(file_name, 'r') as input:
        return input.readlines()

def format_data(lines):
    data = []
    for line in lines:
        line = line.strip().split()
        if len(line) == 1:
            data.append({'instruction': line[0], 'value': 0, 'cycle': 1})
        else:
            data.append({'instruction': line[0], 'value': int(line[1]), 'cycle': 2})
    return data

def solve_part1(data):
    ret = 0
    x = 1
    cycle = 0
    target_cycles = [20, 60, 100, 140, 180, 220]
    for instructions in data:
        for _ in range(instructions['cycle']):
            cycle += 1
            if cycle in target_cycles:
                ret += cycle * x
        x += instructions['value']
    
    if IS_TEST and ret != part1_expected:
        print('Part 1 check failed!')
    return ret
    
def solve_part2(data):
    ret = '\n'
    x = 1
    cycle = 0
    for instructions in data:
        for _ in range(instructions['cycle']):
            if cycle % 40 in range(x-1, x+2):
                ret += '#'
            else:
                ret += '.'
            cycle += 1
            if not cycle % 40:
                ret += '\n'
        x += instructions['value']
    
    if IS_TEST and ret != part2_expected:
        print('Part 2 check failed!')
    return ret
    
lines = load_data(file_name)
data = format_data(lines)

print(f'Day{DAY} part 1: {solve_part1(data)}')
print(f'Day{DAY} part 2: {solve_part2(data)}')
