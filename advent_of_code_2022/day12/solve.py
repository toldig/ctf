#!/usr/bin/python3

import string
import numpy as np

# Update these for each day
IS_TEST = False
DAY = 12
part1_expected = 31
part2_expected = 29

if IS_TEST:
    file_name = 'golden_input.txt'
else:
    file_name = 'input.txt'

def load_data(file_name):
    with open(file_name, 'r') as input:
        return input.readlines()

class Location:
    def __init__(self):
        self.height = 0
        self.letter = ''
        self.distance = 0
        self.visited = False
    def set_letter(self, letter):
        self.letter = letter
        if letter == 'S':
            letter = 'a'
        elif letter == 'E':
            letter = 'z'
        self.height = string.ascii_lowercase.index(letter)

    def __repr__(self):
        return f'{self.distance}'

def format_data(lines):
    data = {'start': [], 'end': [], 'map': None}
    heatmap = np.empty((len(lines), len(lines[0].strip())), dtype=object)

    for row, tmp in enumerate(heatmap):
        for col, _ in enumerate(tmp):
            heatmap[row][col] = Location()
            heatmap[row][col].set_letter(lines[row].strip()[col])
            if heatmap[row][col].letter == 'S':
                data['start'].append((row, col))
            elif heatmap[row][col].letter == 'E':
                data['end'].append((row, col))
    data['map'] = heatmap

    return data

def update_neighbors_part1(coord, heatmap):
    updated = []
    current_height = heatmap[coord[0]][coord[1]].height
    current_distance = heatmap[coord[0]][coord[1]].distance
    
    for neighbor in [(coord[0], coord[1] - 1), (coord[0], coord[1] + 1), (coord[0] - 1, coord[1]), (coord[0] + 1, coord[1])]:
        row = neighbor[0]
        col = neighbor[1]
        if row < 0 or col < 0 or row > len(heatmap) or col > len(heatmap[0]):
            continue
        try:
            if heatmap[row][col].height <= current_height + 1:
                if heatmap[row][col].distance == 0 and heatmap[row][col].letter != 'S':
                    heatmap[row][col].distance = current_distance + 1
                    updated.append((row, col))
                elif current_distance + 1 < heatmap[row][col].distance:
                    heatmap[row][col].distance = current_distance + 1
                    updated.append((row, col))
        except IndexError:    
            pass
    return updated, heatmap

def solve_part1(data):
    ret = 0
    updates = data['start'][:]
    target = data['end'][0]
    heatmap = data['map']

    while len(updates):
        new_updates = []
        for update in updates:
            tmp_updates, heatmap = update_neighbors_part1(update, heatmap)
            new_updates += tmp_updates
        updates = new_updates

    ret = heatmap[target[0]][target[1]].distance

    if IS_TEST and ret != part1_expected:
        print('Part 1 check failed!')

    return ret

def update_neighbors_part2(coord, heatmap):
    updated = []
    current_height = heatmap[coord[0]][coord[1]].height
    current_distance = heatmap[coord[0]][coord[1]].distance
    
    for neighbor in [(coord[0], coord[1] - 1), (coord[0], coord[1] + 1), (coord[0] - 1, coord[1]), (coord[0] + 1, coord[1])]:
        row = neighbor[0]
        col = neighbor[1]
        if row < 0 or col < 0 or row > len(heatmap) or col > len(heatmap[0]):
            continue
        try:
            if heatmap[row][col].height + 1 >= current_height:
                if heatmap[row][col].distance == 0 and heatmap[row][col].letter != 'E':
                    heatmap[row][col].distance = current_distance + 1
                    updated.append((row, col))
                elif current_distance + 1 < heatmap[row][col].distance:
                    heatmap[row][col].distance = current_distance + 1
                    updated.append((row, col))
        except IndexError:    
            pass
    return updated, heatmap

def solve_part2(data):
    ret = 0
    updates = data['end'][:]
    heatmap = data['map']

    while len(updates):
        new_updates = []
        for update in updates:
            tmp_updates, heatmap = update_neighbors_part2(update, heatmap)
            new_updates += tmp_updates
        updates = new_updates

    ret = min([item.distance for item in heatmap.flatten() if item.letter == 'a' and item.distance != 0])

    if IS_TEST and ret != part2_expected:
        print('Part 2 check failed!')
    return ret

lines = load_data(file_name)

print(f'Day{DAY} part 1: {solve_part1(format_data(lines))}')
print(f'Day{DAY} part 2: {solve_part2(format_data(lines))}')
