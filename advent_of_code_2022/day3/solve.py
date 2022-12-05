#!/usr/bin/python3

import numpy as np
import string

IS_TEST = False
DAY = 3

if IS_TEST:
    file_name = 'golden_input.txt'
else:
    file_name = 'input.txt'

value = '0' + string.ascii_lowercase + string.ascii_uppercase

def load_data(file_name):
    with open(file_name, 'r') as input:
        return input.readlines()

def format_data_part1(lines):
    data = []
    for line in lines:
        line = line.strip()
        mid = len(line) // 2
        data.append([line[:mid], line[mid:]])
    return data

def format_data_part2(lines):
    data = []
    index = 0
    while index < len(lines):
        group = []
        for _ in range(3):
            group.append(lines[index].strip())
            index += 1
        data.append(sorted(group, key=len))   
    return data

def solve_part1(data):
    part1 = 0
    for ruck in data:
        letter = set(ruck[0]).intersection(set(ruck[1]))
        part1 += value.index(list(letter)[0])   
    return part1
    
def solve_part2(data):
    part2 = 0
    for group in data:
        letter = set(group[0]).intersection(set(group[1]), set(group[2]))
        part2 += value.index(list(letter)[0])
    return part2
    
lines = load_data(file_name)

print(f'Day{DAY} part 1: {solve_part1(format_data_part1(lines))}')
print(f'Day{DAY} part 2: {solve_part2(format_data_part2(lines))}')
