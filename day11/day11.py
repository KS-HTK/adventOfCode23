# -*- coding: utf-8 -*-

import os
from time import perf_counter
from typing import List, Tuple

def profiler(method):
  def profiler_method(*arg, **kw):
    t = perf_counter()
    ret = method(*arg, **kw)
    print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
    return ret
  return profiler_method

def expand(universe: List[str]) -> List[str]:
  new_universe = []
  for row in universe:
    if all([c=='.' for c in row]):
      new_universe.append(''.join(['1' for _ in row]))
      continue
    new_universe.append(row)
  for i in range(len(new_universe[0])-1, -1, -1):
    col = [row[i] in '.1' for row in new_universe]
    if all(col):
      for j, row in enumerate(new_universe):
        new_universe[j] = row[:i] + '1' + row[i+1:]
  return new_universe

def get_coord_pairs(universe: List[str]) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
  coords = []
  for i, row in enumerate(universe):
    for j, col in enumerate(row):
      if col=='#':
        coords.append((i, j))
  return [(a, b) for idx, a in enumerate(coords) for b in coords[idx + 1:]]

def measure_distance(a: Tuple[int, int], b: Tuple[int, int], universe: List[str], expansion: int) -> int:
  x, y = a
  x2, y2 = b
  d = 0
  while x != x2:
    x = x-1 if x > x2 else x+1
    if universe[x][y] != '1':
      d+=1
      continue
    d += expansion

  while y != y2:
    y = y-1 if y > y2 else y+1
    if universe[x][y] != '1':
      d += 1
      continue
    d += expansion
  return d

# Part 1:
def part1(universe: List[str]) -> int:
  return sum([measure_distance(a, b, universe, 2) for a, b in get_coord_pairs(universe)])

# Part 2:
def part2(universe: List[List[int]]) -> int:
  return sum([measure_distance(a, b, universe, 1000000) for a, b in get_coord_pairs(universe)])

def get_input():
  with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
    content = [s.strip() for s in f.read().rstrip().split('\n')]
  return content

@profiler
def solve():
  content = get_input()
  universe = expand(content)
  print("Part 1:", part1(universe))
  print("Part 2:", part2(universe))

if __name__ == "__main__":
  solve()
