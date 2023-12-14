# -*- coding: utf-8 -*-

import os
from time import perf_counter
from typing import List

def profiler(method):
  def profiler_method(*arg, **kw):
    t = perf_counter()
    ret = method(*arg, **kw)
    print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
    return ret
  return profiler_method

def rotate(grid: List[str]) -> List[str]:
  return [''.join([c[i] for c in grid][::-1]) for i in range(len(grid))]

def roll(lst: List[str]) -> List[str]:
  for x, line in enumerate(lst):
    ln = line.split('#')
    for i, s in enumerate(ln):
      count_O = s.count('O')
      ln[i] = '.' * (len(s) - count_O) + 'O' * count_O
    lst[x] = '#'.join(ln)
  return lst

def calc_load(lst: List[str]) -> int:
  return sum(i+1 for s in lst for i, c in enumerate(s) if c == 'O')

# Part 1:
def part1(grid: List[str]) -> int:
  grid = roll(grid)
  return calc_load(grid)

# Part 2:
def part2(g: List[str]) -> int:
  gridmap = {}
  target = 10**9
  t = 0
  while t < target:
    t += 1
    for j in range(4):
      g = roll(g)
      g = rotate(g)
    gh = tuple(tuple(row) for row in g)
    if gh in gridmap:
      cycle_length = t-gridmap[gh]
      amt = (target-t)//cycle_length
      t += amt * cycle_length
    gridmap[gh] = t
  return calc_load(g)

def get_input():
  with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
    content = [s.strip() for s in f.read().rstrip().split('\n')]
  return content

@profiler
def solve():
  content: List[str] = get_input()
  content = rotate(content)
  print(f'Part 1: {part1(content)}')
  print(f'Part 2: {part2(content)}')

if __name__ == "__main__":
  solve()
