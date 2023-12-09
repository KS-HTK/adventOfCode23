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

def get_next_sequence(lst: List[int]) -> List[int]:
  rst: List[int] = []
  for i in range(len(lst)-1):
    rst.append(lst[i+1]-lst[i])
  return rst

def ext_sequence(lst: List[int], ext_left=False) -> int:
  ext_ind: int = 0 if ext_left else -1
  prefix: int = -1 if ext_left else 1
  if len(lst) == 0:
    return 0
  next_sq = get_next_sequence(lst)
  if all([i == 0 for i in next_sq]):
    return lst[ext_ind]
  return lst[ext_ind]+prefix*ext_sequence(next_sq, ext_left)

# Part 1:
def part1(content: List[List[int]]) -> int:
  return sum([ext_sequence(line) for line in content])

# Part 2:
def part2(content: List[List[int]]) -> int:
  return sum([ext_sequence(line, True) for line in content])

def get_input():
  with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
    content = [s.strip() for s in f.read().rstrip().split('\n')]
  return content

@profiler
def solve():
  content = get_input()
  content = [re.findall(r'-?\d+', line) for line in content]
  content = [[int(i) for i in line] for line in content]
  print("Part 1:", part1(content))
  print("Part 2:", part2(content))

if __name__ == "__main__":
  solve()
