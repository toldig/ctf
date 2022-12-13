#!/usr/bin/python3

import numpy as np
import json
import functools

TERMINATE_EARLY_FALSE = -2
TERMINATE_FALSE = -1
EQUAL = 0
TERMINATE_EARLY_TRUE = 1
divider_1 = [[2]]
divider_2 = [[6]]

# Update these for each day
IS_TEST = False
DAY = 13
part1_expected = 13
part2_expected = 0

if IS_TEST:
    file_name = 'golden_input.txt'
else:
    file_name = 'input.txt'

def load_data(file_name):
    with open(file_name, 'r') as input:
        return input.readlines()

def format_data_part1(lines):
    pairs = []
    index = 0
    while True:
        left = json.loads(lines[index].strip())
        index += 1
        right = json.loads(lines[index].strip())
        index += 1
        pairs.append([left, right])
        if index >= len(lines):
            break
        index += 1
    return pairs

def format_data_part2(lines):
    packets = [divider_1, divider_2]
    for line in lines:
        line = line.strip()
        if line:
            packets.append(json.loads(line))
    return packets

def compare(_left, _right, indent=0):
    log_message(f'{" " * indent}- Compare {_left} vs {_right}')
    for li, left in enumerate(_left):
        if li >= len(_right):
            log_message(f'{" " * (indent + 2)}- Right side ran out of items, so inputs are not in the right order')
            return TERMINATE_EARLY_FALSE
        right = _right[li]
        if isinstance(left, list) and isinstance(right, list):
            tmp = compare(left, right, indent + 2)
            if tmp in [TERMINATE_EARLY_TRUE, TERMINATE_EARLY_FALSE]:
                return tmp
        elif isinstance(left, list) and isinstance(right, int):
            log_message(f'{" " * (indent + 2)}- Mixed types; convert right to [{right}] and retry comparison')
            tmp = compare(left, [right], indent + 2)
            if tmp in [TERMINATE_EARLY_TRUE, TERMINATE_EARLY_FALSE]:
                return tmp
        elif isinstance(left, int) and isinstance(right, list):
            log_message(f'{" " * (indent + 2)}- Mixed types; convert left to [{left}] and retry comparison')
            tmp = compare([left], right, indent + 2)
            if tmp in [TERMINATE_EARLY_TRUE, TERMINATE_EARLY_FALSE]:
                return tmp
        elif isinstance(left, int) and isinstance(right, int):
            log_message(f'{" " * (indent + 2)}- Compare {left} vs {right}')
            if left == right:
                continue
            if left > right:
                log_message(f'{" " * (indent + 2)}- Right side is smaller, so inputs are not in the right order')
                return TERMINATE_EARLY_FALSE
            log_message(f'{" " * (indent + 2)}- Left side is smaller, so inputs are in the right order')
            return TERMINATE_EARLY_TRUE
    log_message(f'{" " * (indent + 2)}- Left side ran out of items, so inputs are in the right order')
    if len(_right) == len(_left):
        return EQUAL
    return TERMINATE_EARLY_TRUE

def log_message(message):
    if IS_TEST:
        print(message)        

def solve_part1(data):
    ret = 0
    index = 1

    for pair in data:
        log_message(f'== Pair {index} ==')
        if compare(pair[0], pair[1]) in [TERMINATE_EARLY_TRUE, EQUAL]:
            ret += index
        index += 1

    if IS_TEST and ret != part1_expected:
        print('Part 1 check failed!')
    return ret

def solve_part2(data):
    sorted_data = sorted(data, key=functools.cmp_to_key(compare), reverse=True)
    ret = (sorted_data.index(divider_1) + 1) * (sorted_data.index(divider_2) + 1)

    if IS_TEST and ret != part2_expected:
        print('Part 2 check failed!')
    return ret

lines = load_data(file_name)

print(f'Day{DAY} part 1: {solve_part1(format_data_part1(lines))}')
print(f'Day{DAY} part 2: {solve_part2(format_data_part2(lines))}')
