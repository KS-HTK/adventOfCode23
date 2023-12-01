# -*- coding: utf-8 -*-

import os
import re
from time import perf_counter
from typing import List

def profiler(method):
  def profiler_method(*arg, **kw):
    t = perf_counter()
    ret = method(*arg, **kw)
    print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
    return ret
  return profiler_method

# Part 1:
def part1(content = None) -> str|int:
  return sum([int(re.search(r'\d', line)[0]+re.search(r'.*\d', line)[0][-1]) for line in content])

# Part 2:
def part2(content = None) -> str|int:
  digit_map = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4, 
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
  }
  firsts = [re.search( "(" + "|".join(digit_map.keys()) + ")", line).group(1) for line in content]
  lasts = [re.search( "(?s:.*)(" + "|".join(digit_map.keys()) + ")", line ).group(1) for line in content]
  numbers = [digit_map[x] * 10 + digit_map[y] for x, y in zip(firsts, lasts)]
  return sum(numbers)

def get_input():
  with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
    content = [s.strip() for s in f.read().rstrip().split('\n')]
  return content

@profiler
def solve():
  content = get_input()
  print("Part 1:", part1(content))
  print("Part 2:", part2(content))

if __name__ == "__main__":
  solve()
