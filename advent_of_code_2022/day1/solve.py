#!/usr/bin/python3

import numpy as np

IS_TEST = False
DAY = 1

if IS_TEST:
    file_name = 'golden_input.txt'
else:
    file_name = 'input.txt'


def load_data(file_name):
    with open(file_name, 'r') as input:
        return input.readlines()

def format_data(lines):
    elfs = []
    elf = []
    for line in lines:
        line = line.strip()
        if line:
            
            elf.append(int(line,10))
        else:
            elfs.append(elf)
            elf = []
    return elfs

def solve_part1(data):
    ret = sum(data[0])
    for elf in data[1:]:
        if ret < sum(elf):
            ret = sum(elf)
    return ret
    
def solve_part2(data):
    sums = [sum(elf) for elf in data]
    sums.sort(reverse=True)
    return sum(sums[:3])
    
lines = load_data(file_name)
data = format_data(lines)

print(f'Day{DAY} part 1: {solve_part1(data)}')
print(f'Day{DAY} part 2: {solve_part2(data)}')
