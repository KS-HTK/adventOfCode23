# -*- coding: utf-8 -*-

import os
from math import lcm
from time import perf_counter
from typing import List, Callable

def profiler(method):
  def profiler_method(*arg, **kw):
    t = perf_counter()
    ret = method(*arg, **kw)
    print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
    return ret
  return profiler_method

def get_go_to_exit(directions, instructions):
  def go_to_exit(escape_func: Callable[[str], bool], pos: str) -> int:
    step_count = 0
    i = instructions
    while escape_func(pos):
      step_count += 1
      pos = directions[pos][0 if i[0] == 'L' else 1]
      i = i[1:]
      if len(i) == 0:
        i = instructions
    return step_count
  return go_to_exit

# Part 1:
def part1(go_to_exit: Callable[[Callable[[str], bool]], int]) -> int:
  return go_to_exit(lambda x: x != 'ZZZ', 'AAA')

# Part 2:
def part2(go_to_exit: Callable[[Callable[[str], bool]], int], positions: List[str]) -> int:
  counts = []
  for p in positions:
    counts.append(go_to_exit(lambda x: not x.endswith('Z'), p))
  return lcm(*counts)

def get_input():
  with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
    content = [s.strip() for s in f.read().rstrip().split('\n')]
  return content

@profiler
def solve():
  content = get_input()
  instructions = content.pop(0)
  content.pop(0)
  directions = {}
  for p, d in [s.replace('(', '').replace(')', '').split(' = ') for s in content]:
    d = d.split(', ')
    directions[p] = (d[0], d[1])
  gte = get_go_to_exit(directions, instructions)
  print("Part 1:", part1(gte))
  print("Part 2:", part2(gte, [p for p in directions.keys() if p.endswith('A')]))

if __name__ == "__main__":
  solve()
