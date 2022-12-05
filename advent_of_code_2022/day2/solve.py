#!/usr/bin/python3

import numpy as np

IS_TEST = False
DAY = 2
ROCK = 1
PAPER = 2
SCISSORS = 3
WIN = 6
DRAW = 3
LOSE = 0

opponent = {'A': ROCK, 'B': PAPER, 'C': SCISSORS}
mine = {'X': ROCK, 'Y': PAPER, 'Z': SCISSORS}
match_results = {'X': LOSE, 'Y': DRAW, 'Z': WIN}

eval_part1 = {ROCK: {PAPER: LOSE, ROCK: DRAW, SCISSORS: WIN},
              SCISSORS: {PAPER: WIN, ROCK: LOSE, SCISSORS: DRAW},
              PAPER: {PAPER: DRAW, ROCK: WIN, SCISSORS: LOSE}}

eval_part2 = {ROCK: {LOSE: SCISSORS, DRAW: ROCK, WIN: PAPER},
              SCISSORS: {LOSE: PAPER, DRAW: SCISSORS, WIN: ROCK},
              PAPER: {LOSE: ROCK, DRAW: PAPER, WIN: SCISSORS}}

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
        data.append(line.split())
    return data

def evaluate_match_part1(match):
    opponent_play = opponent[match[0]]
    my_play = mine[match[1]]
    return my_play + eval_part1[my_play][opponent_play]

def solve_part1(data):
    score = 0
    for match in data:
        score += evaluate_match_part1(match)
    return score

def evaluate_match_part2(match):
    opponent_play = opponent[match[0]]
    match_result = match_results[match[1]]
    return match_result + eval_part2[opponent_play][match_result]

def solve_part2(data):
    score = 0
    for match in data:
        score += evaluate_match_part2(match)
    return score
    
lines = load_data(file_name)
data = format_data(lines)

print(f'Day{DAY} part 1: {solve_part1(data)}')
print(f'Day{DAY} part 2: {solve_part2(data)}')
