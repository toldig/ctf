#!/usr/bin/python3

import numpy as np

# Update these for each day
IS_TEST = False
DAY = 11
part1_expected = 10605
part2_expected = 2713310158

if IS_TEST:
    file_name = 'golden_input.txt'
else:
    file_name = 'input.txt'

def load_data(file_name):
    with open(file_name, 'r') as input:
        return input.readlines()

class Monkey:
    def __init__(self):
        self.items = []
        self.operation = ''
        self.div = 0
        self.true_path = 0
        self.false_path = 0
        self.inspected = 0
    def __str__(self):
        return f'Items: {self.items}\nOperation: {self.operation}\nDiv: {self.div}\nTrue: {self.true_path}, False: {self.false_path}\nInspected: {self.inspected}'

def format_data(lines):
    monkeys = []
    index = 0
    while (index < len(lines)):
        new_monkey = Monkey()
        # Skip monkey id
        index += 1
        # Read items
        new_monkey.items = [int(item.strip()) for item in lines[index].strip().split(':')[-1].split(',')]
        index += 1
        # Read operation
        new_monkey.operation = lines[index].strip().split('=')[-1].strip()
        index += 1
        # Read test
        new_monkey.div = int(lines[index].strip().split()[-1])
        index += 1
        # Read true
        new_monkey.true_path = int(lines[index].strip().split()[-1])
        index += 1
        # Read false
        new_monkey.false_path = int(lines[index].strip().split()[-1])
        index += 1
        # Skip empty line
        index += 1
        monkeys.append(new_monkey)
    return monkeys

def solve_part1(data):
    ret = 0
    for _ in range(20):
        for monkey in data:
            for item in monkey.items:
                monkey.inspected += 1
                new_item = eval(monkey.operation.replace('old', str(item)))//3
                if not new_item % monkey.div:
                    data[monkey.true_path].items.append(new_item)
                    # print(f'{new_item} true goes to {monkey.true_path}')
                else:
                    data[monkey.false_path].items.append(new_item)
                    # print(f'{new_item} true goes to {monkey.false_path}')
            monkey.items.clear()
    insp = sorted([monkey.inspected for monkey in data])
    ret = insp[-1] * insp[-2]
            
    if IS_TEST and ret != part1_expected:
        print('Part 1 check failed!')
    return ret
    
def solve_part2(data):
    ret = 0
    
    divs = [monkey.div for monkey in data]
    magic = np.prod(divs)
    
    for i in range(10000):
        for monkey in data:
            for item in monkey.items:
                monkey.inspected += 1
                new_item = eval(monkey.operation.replace('old', str(item)))
                if not new_item % monkey.div:
                    data[monkey.true_path].items.append(new_item % magic)
                else:
                    data[monkey.false_path].items.append(new_item)
            monkey.items.clear()    
    
    insp = sorted([monkey.inspected for monkey in data])
    ret = insp[-1] * insp[-2]
    
    if IS_TEST and ret != part2_expected:
        print('Part 2 check failed!')
    return ret
    
lines = load_data(file_name)
data = format_data(lines)

# print(f'Day{DAY} part 1: {solve_part1(data)}')
print(f'Day{DAY} part 2: {solve_part2(data)}')
