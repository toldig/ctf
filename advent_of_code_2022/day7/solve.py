#!/usr/bin/python3

import numpy as np

IS_TEST = False
DAY = 7

if IS_TEST:
    file_name = 'golden_input.txt'
else:
    file_name = 'input.txt'

class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size

class Dir:
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.files = []
        self.directories = []
        self.total_size = 0
    
    def add_directory(self, name):
        # Check if directory present already
        for directory in self.directories:
            if directory.name == name:
                print(f'Directory {name} already present')
                return
        self.directories.append(Dir(self, name))
    
    def add_file(self, name, size):
        # Check if directory present already
        for file in self.files:
            if file.name == name:
                print(f'File {name} already present with size {size}, old size is {file.size}')
                return
        self.files.append(File(name, size))
    
    def change_directory(self, name):
        if name == '..':
            return self.parent
        for directory in self.directories:
            if directory.name == name:
                return directory
    
    def print(self, indent):
        print(f'- {" " * indent}{self.name} (dir, total={self.total_size})')
        for cur_dir in self.directories:
            cur_dir.print(indent + 2)
        for cur_file in self.files:
            print(f'- {" " * (indent + 2)}{cur_file.name} (file, size={cur_file.size})')

    def update_total(self):
        self.total_size = 0
        for cur_dir in self.directories:
            cur_dir.update_total()
            self.total_size += cur_dir.total_size
        for cur_file in self.files:
             self.total_size += cur_file.size
        

def load_data(file_name):
    with open(file_name, 'r') as input:
        return input.readlines()

def format_data(lines):
    root = Dir(None, '/')
    current = root
    i = 1
    while i < len(lines):
        line = lines[i].strip().split()
        i += 1
        # Check if it is a command line
        if line[0] == '$':
            if line[1] == 'ls':
               continue
            elif line[1] ==  'cd':
                current = current.change_directory(line[2])
                continue
            else:
                print(f'Unknown command {line[1]}')
                exit(1)
        # Reading directory data
        elif line[0] == 'dir':
            current.add_directory(line[1])
        # Reading file data
        else:
            current.add_file(line[1], int(line[0]))
    return root

def solve_part1(data):
    ret = 0
    for cur_dir in data.directories:
        ret += solve_part1(cur_dir)
        if cur_dir.total_size <= 100000:
           ret += cur_dir.total_size 
    return ret
    
def solve_part2(data, unused):
    ret = []
    for cur_dir in data.directories:
        ret += solve_part2(cur_dir, unused)
        if unused + cur_dir.total_size >= 30000000:
           ret.append(cur_dir.total_size)
    return ret
    
lines = load_data(file_name)
data = format_data(lines)
data.update_total()

data.print(0)

print(f'Day{DAY} part 1: {solve_part1(data)}')
print(f'Day{DAY} part 2: {min(solve_part2(data, 70000000 - data.total_size))}')
