#!/usr/bin/python3

import numpy as np

# Update these for each day
IS_TEST = False
DAY = 9
part1_expected = 88
part2_expected = 36

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
        for _ in range(int(line[1])):
            data.append(line[0])
    return data

def distance(head, tail):
    dist = 0
    horizontal_distance = 1
    for _ in (range(min([head[0], tail[0]]), max([head[0], tail[0]]))):
       dist += horizontal_distance
       horizontal_distance += 1

    vertical_distance = 1
    for _ in (range(min([head[1], tail[1]]), max([head[1], tail[1]]))):
        dist += vertical_distance
        vertical_distance += 1
    return dist

def move_tail(head, tail):
    if distance(head, tail) <= 2:                       # No need to move
        return (tail[0], tail[1])
    if head[0] == tail[0]:                              # If ROW is the same
        new_tail = (tail[0],(head[1] + tail[1])//2)
    elif head[1] == tail[1]:                            # If COL is the same
        new_tail = ((head[0] + tail[0])//2, tail[1])
    else:                                               # Move diagonally
        if head[0] > tail[0] and head[1] > tail[1]:     # Move right-up
            new_tail = (tail[0] + 1, tail[1] + 1)
        elif head[0] > tail[0] and head[1] < tail[1]:   # Move left-up
            new_tail = (tail[0] + 1, tail[1] - 1)
        elif head[0] < tail[0] and head[1] < tail[1]:   # Move left-down
            new_tail = (tail[0] - 1, tail[1] - 1)
        elif head[0] < tail[0] and head[1] > tail[1]:   # Move right-down
            new_tail = (tail[0] - 1, tail[1] + 1)
    return new_tail 

def solve_part1(data):
    ret = set()
    # Visited coordinates stored as ROW, COL both starting at 0, 0
    head_coordinates = [(0,0)]
    tail_coordinates = [(0,0)]
    
    for direction in data:
        head_current = list(head_coordinates[-1])
        if direction == 'R':
            head_current[1] += 1
        elif direction == 'L':
            head_current[1] -= 1
        elif direction == 'U':
            head_current[0] += 1
        elif direction == 'D':
            head_current[0] -= 1
        else:
            print(f'Unknown direction {direction}')
            exit()
        head_coordinates.append((head_current[0], head_current[1]))
        tail_coordinates.append(move_tail(head_current, tail_coordinates[-1]))

    ret.update(tail_coordinates)
    if IS_TEST and len(ret) != part1_expected:
        print('Part 1 check failed!')
    return len(set(ret))
    
def solve_part2(data):
    ret = set()
    rope = []

    for _ in range(10):
        rope.append([(0,0)])    
    for direction in data:
        # Move the head first according to the direction !!
        head_current = list(rope[0][-1])
        if direction == 'R':
            head_current[1] += 1
        elif direction == 'L':
            head_current[1] -= 1
        elif direction == 'U':
            head_current[0] += 1
        elif direction == 'D':
            head_current[0] -= 1
        else:
            print(f'Unknown direction {direction}')
            exit()
        rope[0].append((head_current[0], head_current[1]))
        
        # Move tails if needed
        for knot_index in range(1, len(rope)):
            head_current = list(rope[knot_index - 1][-1])
            tail_current = list(rope[knot_index][-1])
            new_tail = move_tail(head_current, tail_current)
            if tuple(tail_current) == new_tail:     # No need to move
                break
            rope[knot_index].append(new_tail)

    ret.update(rope[-1])
    if IS_TEST and len(ret) != part2_expected:
        print('Part 2 check failed!')
    return len(ret)
    
lines = load_data(file_name)
data = format_data(lines)

print(f'Day{DAY} part 1: {solve_part1(data)}')
print(f'Day{DAY} part 2: {solve_part2(data)}')
