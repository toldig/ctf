#!/usr/bin/python3

import numpy as np

IS_TEST = False
DAY = 5

# Hardcoding stacks because the input is not so wild
'''
Golden input stacks:
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3
'''
golden_stack = [['N', 'Z'],
                ['D', 'C', 'M'],
                ['P']]
'''
Real input stacks:
        [G]         [D]     [Q]    
[P]     [T]         [L] [M] [Z]    
[Z] [Z] [C]         [Z] [G] [W]    
[M] [B] [F]         [P] [C] [H] [N]
[T] [S] [R]     [H] [W] [R] [L] [W]
[R] [T] [Q] [Z] [R] [S] [Z] [F] [P]
[C] [N] [H] [R] [N] [H] [D] [J] [Q]
[N] [D] [M] [G] [Z] [F] [W] [S] [S]
 1   2   3   4   5   6   7   8   9 
'''
real_stack = [['P', 'Z', 'M', 'T', 'R', 'C', 'N'],
              ['Z', 'B', 'S', 'T', 'N', 'D'],
              ['G', 'T', 'C', 'F', 'R', 'Q', 'H', 'M'],
              ['Z', 'R', 'G'],
              ['H', 'R', 'N', 'Z'],
              ['D', 'L', 'Z', 'P', 'W', 'S', 'H', 'F'],
              ['M', 'G', 'C', 'R', 'Z', 'D', 'W'],
              ['Q', 'Z', 'W', 'H', 'L', 'F', 'J', 'S'],
              ['N', 'W', 'P', 'Q', 'S']]


if IS_TEST:
    file_name = 'golden_input.txt'
    stacks = golden_stack[:]
else:
    file_name = 'input.txt'
    stacks = real_stack[:]

def load_data(file_name):
    with open(file_name, 'r') as input:
        return input.readlines()

def format_data(lines):
    data = []
    for line in lines:
        template = {'move': 0, 'from': 0, 'to': 0}
        line = line.strip().split()
        template['move'] = int(line[1])
        template['from'] = int(line[3]) - 1
        template['to'] = int(line[5]) - 1
        data.append(template)
    return data

def copy_stacks():
    ret = []
    for stack in stacks:
        ret.append(stack[:])
    return ret

def solve_part1(moves):
    input_stacks = copy_stacks()
    for move in moves:
        for _ in range(move['move']):
            item = input_stacks[move['from']].pop(0)
            input_stacks[move['to']].insert(0, item)
    ret = ''
    for stack in input_stacks:
        ret += stack[0]
    return ret
    
def solve_part2(moves):
    input_stacks = copy_stacks()
    for move in moves:
        moved = ''
        for _ in range(move['move']):
            moved += input_stacks[move['from']].pop(0)
        for letter in moved[::-1]:
            input_stacks[move['to']].insert(0, letter)
    ret = ''
    for stack in input_stacks:
        ret += stack[0]
    return ret
    
lines = load_data(file_name)
moves = format_data(lines)
print(f'Day{DAY} part 1: {solve_part1(moves)}')
print(f'Day{DAY} part 2: {solve_part2(moves)}')
