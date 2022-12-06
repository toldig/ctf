#!/usr/bin/python3

import numpy as np

IS_TEST = False
DAY = 6

if IS_TEST:
    file_name = 'golden_input.txt'
else:
    file_name = 'input.txt'


def load_data(file_name):
    with open(file_name, 'r') as input:
        return input.readlines()

def format_data(lines):
    return lines[0].strip()

def solve_part1(data):
    for i in range(len(data)):
        if len(set(data[i:i+4])) == 4:
            return i + 4
    
def solve_part2(data):
    for i in range(len(data)):
        if len(set(data[i:i+14])) == 14:
            return i + 14
    
lines = load_data(file_name)
data = format_data(lines)

print(f'Day{DAY} part 1: {solve_part1(data)}')
print(f'Day{DAY} part 2: {solve_part2(data)}')
