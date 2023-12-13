# -*- coding: utf-8 -*-

import os
from time import perf_counter
from typing import List, Set, Tuple, Callable

def profiler(method):
  def profiler_method(*arg, **kw):
    t = perf_counter()
    ret = method(*arg, **kw)
    print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
    return ret
  return profiler_method

def transpose(m):
  return [''.join([m[j][i] for j in range(len(m))]) for i in range(len(m[0]))]

def get_reflection(mirror: List[str]) -> int | Exception:
  for x in range(1, len(mirror)):
    if all(c1 == c2 for (c1, c2) in zip(mirror[x:], mirror[x-1::-1])):
      return x
  return Exception('No reflection found')

def get_reflection2(mirror: List[str]) -> int | Exception:
  for x in range(len(mirror)):
    errors = 0
    errors += sum(s1!=s2 for c1, c2 in zip(mirror[x:], mirror[x-1::-1]) for s1, s2 in zip(c1, c2))
    if errors == 1:
      return x
  return Exception('No reflection found')

def get_reflection_line(func: Callable[[List[str]], int], mirror: List[str]) -> int:
  # check for vertical reflection across a horizontal line
  ind = func(mirror)
  if isinstance(ind, int):
    return 100*ind
  # check for horizontal reflection across a vertical line
  ind = func(transpose(mirror))
  if isinstance(ind, int):
    return ind
  raise ind

# Part 1:
def part1(mirrors: List[List[str]]) -> int:
  return sum([get_reflection_line(get_reflection, mirror) for mirror in mirrors])

# Part 2:
def part2(mirrors: List[List[str]]) -> int:
  return sum([get_reflection_line(get_reflection2, mirror) for mirror in mirrors])

def get_input():
  with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
    content = [s.strip().split('\n') for s in f.read().rstrip().split('\n\n')]
  return content

@profiler
def solve():
  mirrors = get_input()
  print(f'Part 1: {part1(mirrors)}')
  print(f'Part 2: {part2(mirrors)}')

if __name__ == "__main__":
  solve()
