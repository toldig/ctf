#!/usr/bin/python3

import numpy as np
import re
from functools import lru_cache

# Update these for each day
IS_TEST = False
DAY = 15
part1_expected = 26
part2_expected = 56000011

if IS_TEST:
    file_name = 'golden_input.txt'
else:
    file_name = 'input.txt'

def load_data(file_name):
    with open(file_name, 'r') as input:
        return input.readlines()

class Sensor:
    def __init__(self, sx, sy, bx, by):
        self.sensor_x = int(sx)
        self.sensor_y = int(sy)
        self.beacon_x = int(bx)
        self.beacon_y = int(by)
        self.range = abs(self.sensor_x - self.beacon_x) + abs(self.sensor_y - self.beacon_y)
        self.max_x = max(self.sensor_x + self.range, self.beacon_x)
        self.min_x = min(self.sensor_x - self.range, self.beacon_x)
        self.max_y = max(self.sensor_y + self.range, self.beacon_y)
        self.min_y = min(self.sensor_y - self.range, self.beacon_y)

def is_in_range(sx, sy, r, x, y):
    if abs(sx - x) + abs(sy - y) <= r:
        return True
    return False

def shift_x(sx, sy, r, x, y):
    if abs(sx - x) + abs(sy - y) <= r:
        test = sy + r - abs(sx - x)
        return test
    return 0

def format_data(lines):
    data = {'maxX': 0, 'minX': 0, 'maxY': 0, 'minY': 0}
    sensors = []
    pattern = r'Sensor at x=(?P<sx>-?\d+), y=(?P<sy>-?\d+): closest beacon is at x=(?P<bx>-?\d+), y=(?P<by>-?\d+)'
    for line in lines:
        match = re.match(pattern, line)
        if match is None:
            print(f'Failed to parse line: {line}')
            exit()
        extracted = match.groupdict()
        sensor = Sensor(extracted['sx'], extracted['sy'], extracted['bx'], extracted['by'])
        data['maxX'] = max(data['maxX'], sensor.max_x)
        data['maxY'] = max(data['maxY'], sensor.max_y)
        data['minX'] = min(data['minX'], sensor.min_x)
        data['minY'] = min(data['minY'], sensor.min_y)
        sensors.append(sensor)
    data['sensors'] = sensors
    
    return data

def solve_part1(data):
    ret = 0
    
    target_y = 2000000
    if IS_TEST:
        target_y = 10
    
    for x in range(data['minX'], data['maxX'] + 1):
        in_range = False
        is_beacon = False
        print(f'Checking range {data["minX"]} -> {data["maxX"]}: {x}    \r', end='')
        # check if location is beacon
        for sensor in data['sensors']:
            if sensor.beacon_x == x and sensor.beacon_y == target_y:
                is_beacon = True
                break
        if is_beacon:
            continue
        for sensor in data['sensors']:
            if is_in_range(sensor.sensor_x, sensor.sensor_y, sensor.range, x, target_y):
                in_range = True
                break
        if in_range:
            ret += 1
    print()
    if IS_TEST and ret != part1_expected:
        print('Part 1 check failed!')
    return ret

def copy_value(value_to_copy):
    return value_to_copy
 
def solve_part2(data):
    ret = 0
    
    target = 4000000
    if IS_TEST:
        target = 20
    
    print()
    for y in range(0, target + 1):
        x = -1
        print(f'Rows : {y}/{target}\r', end='')
        while x <= target:
            x += 1
            is_beacon = False
            found = True
            # check if location is beacon
            for sensor in data['sensors']:
                if sensor.beacon_x == x and sensor.beacon_y == y:
                    is_beacon = True
                    break
            if is_beacon:
                continue
            newX = x
            for sensor in data['sensors']:
                
                tmpX = shift_x(sensor.sensor_x, sensor.sensor_y, sensor.range, y, newX)
                if tmpX:
                    found = False
                newX = max(tmpX, newX)
            x = newX
            if found:
                ret = y * 4000000 + x
                print()
                if IS_TEST and ret != part2_expected:
                    print('Part 2 check failed!')
                return ret

lines = load_data(file_name)
data = format_data(lines)

print(f'Day{DAY} part 1: {solve_part1(data)}')
print(f'Day{DAY} part 2: {solve_part2(data)}')
