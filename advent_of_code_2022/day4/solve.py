#!/usr/bin/python3

import numpy as np

IS_TEST = False
DAY = 4

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
        line_data = {'elf1_low': 0, 'elf1_high': 0, 'elf2_low': 0, 'elf2_high': 0}
        line = line.strip().split(',')
        line_data['elf1_low'] = int(line[0].split('-')[0])
        line_data['elf1_high'] = int(line[0].split('-')[1])
        line_data['elf2_low'] = int(line[1].split('-')[0])
        line_data['elf2_high'] = int(line[1].split('-')[1])
        data.append(line_data)
    return data

def solve_part1(data):
    overlap = 0
    for pair in data:
        elf1 = range(pair['elf1_low'], pair['elf1_high'] + 1)
        elf2 = range(pair['elf2_low'], pair['elf2_high'] + 1)
        if set(elf1).issubset(elf2) or set(elf2).issubset(elf1):
           overlap += 1
    return overlap
    
    
def solve_part2(data):
    overlap = 0
    for pair in data:
        elf1 = range(pair['elf1_low'], pair['elf1_high'] + 1)
        elf2 = range(pair['elf2_low'], pair['elf2_high'] + 1)
        if set(elf1).intersection(elf2) or set(elf2).intersection(elf1):
           overlap += 1
    return overlap
    
lines = load_data(file_name)
data = format_data(lines)

print(f'Day{DAY} part 1: {solve_part1(data)}')
print(f'Day{DAY} part 2: {solve_part2(data)}')
