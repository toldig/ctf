#!/usr/bin/python3

import numpy as np
import re

# Update these for each day
IS_TEST = True
DAY = 16
part1_expected = 1651
part2_expected = 0

if IS_TEST:
    file_name = 'golden_input.txt'
else:
    file_name = 'input.txt'

def load_data(file_name):
    with open(file_name, 'r') as input:
        return input.readlines()

class Node:
    def __init__(self, n, r, v):
        self.name = n
        self.rate = r
        self.distance = 0
        self.valves_str = v
        self.links = []
    
    def delete_link_to_node(name):
        for link in list(self.links):
            if link.dst == name:
                self.links.remove(link)

class Link:
    def __init__(self, c, s, d):
        self.cost = c
        self.src = s
        self.dst = d

def get_node(nodes, name):
    for node in nodes:
        if node.name == name:
            return node

def format_data(lines):
    pattern = r'Valve (?P<name>\w+) has flow rate=(?P<rate>\d+); tunnel[s]? lead[s]? to valve[s]? (?P<valves>.+)'
    nodes = []
    # Create only nodes first
    for line in lines:
        match = re.match(pattern, line)
        if match is None:
            print(f'Failed to parse line: {line}')
            exit()
        extracted = match.groupdict()
        nodes.append(Node(extracted['name'], extracted['rate'], extracted['valves']))
    for node in nodes:
        for valve in node.valves_str.split(','):
            node.links.append(Link(1, node, get_node(nodes, valve.strip())))
    
    return get_node(nodes, 'AA')

def delete_empty_nodes(node):
    # Not is 0 and not the head node
    if node.name != 'AA' and node.rate == 0:
        for link in node.links:
            node.delete_link_to_node(link.src)
        

def solve_part1(data):
    ret = 0
    
    # Solve part 1 here
    
    if IS_TEST and ret != part1_expected:
        print('Part 1 check failed!')
    return ret
    
def solve_part2(data):
    ret = 0
    
    # Solve part 2 here
    
    if IS_TEST and ret != part2_expected:
        print('Part 2 check failed!')
    return ret
   
lines = load_data(file_name)
data = format_data(lines)

print(f'Day{DAY} part 1: {solve_part1(data)}')
print(f'Day{DAY} part 2: {solve_part2(data)}')
