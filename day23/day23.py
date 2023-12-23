# -*- coding: utf-8 -*-

import os
from time import perf_counter
from collections import deque, defaultdict
from typing import List, Dict, Tuple, Set

def profiler(method):
  def profiler_method(*arg, **kw):
    t = perf_counter()
    ret = method(*arg, **kw)
    print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
    return ret
  return profiler_method

# Part 1:
def part1(grid: List[str]) -> int:
  lr, lc = len(grid), len(grid[0])
  sr, sc = 0, grid[0].index(".")
  er, ec = lr - 1, grid[-1].index(".")

  edges: Dict[Tuple[int, int], Set[Tuple[int, int]]] = defaultdict(set)
  for row, row_v in enumerate(grid):
    for col, v in enumerate(row_v):
      match v:
        case ".":
          for dr, dc in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
            ar, ac = row + dr, col + dc
            if not (0 <= ar < lr and 0 <= ac < lc):
              continue
            if grid[ar][ac] == ".":
              edges[(row, col)].add((ar, ac))
              edges[(ar, ac)].add((row, col))
        case ">":
          edges[(row, col)].add((row, col + 1))
          edges[(row, col - 1)].add((row, col))
        case "v":
          edges[(row, col)].add((row + 1, col))
          edges[(row - 1, col)].add((row, col))

  queue = deque([(sr, sc, 0)])
  visited: Set[Tuple[int, int]] = set()
  best: int = 0
  while queue:
    row, col, dist = queue.pop()
    if dist == -1:
      visited.remove((row, col))
      continue
    if (row, col) == (er, ec):
      best = max(best, dist)
      continue
    if (row, col) in visited:
      continue
    visited.add((row, col))
    queue.append((row, col, -1))
    for ar, ac in edges[(row, col)]:
      queue.append((ar, ac, dist + 1))
  return best

# Part 2:
def part2(grid):
  lr, lc = len(grid), len(grid[0])
  sr, sc = 0, grid[0].index(".")
  er, ec = lr - 1, grid[-1].index(".")
  edges: Dict[Tuple[int, int], Set[Tuple[int, int]]] = defaultdict(set)
  for row, row_v in enumerate(grid):
    for col, v in enumerate(row_v):
      if v in ".>v":
        for dr, dc in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
          ar, ac = row + dr, col + dc
          if not (0 <= ar < lr and 0 <= ac < lc):
            continue
          if grid[ar][ac] in ".>v":
            edges[(row, col)].add((ar, ac, 1))
            edges[(ar, ac)].add((row, col, 1))

  # Remove nodes with degree 2
  while True:
    for n, e in edges.items():
      if len(e) == 2:
        a, b = e
        edges[a[:2]].remove(n + (a[2],))
        edges[b[:2]].remove(n + (b[2],))
        edges[a[:2]].add((b[0], b[1], a[2] + b[2]))
        edges[b[:2]].add((a[0], a[1], a[2] + b[2]))
        del edges[n]
        break
    else:
      break

  queue = deque([(sr, sc, 0)])
  visited: Set[Tuple[int, int]] = set()
  best: int = 0
  while queue:
    row, col, dist = queue.pop()
    if dist == -1:
      visited.remove((row, col))
      continue
    if (row, col) == (er, ec):
      best = max(best, dist)
      continue
    if (row, col) in visited:
      continue
    visited.add((row, col))
    queue.append((row, col, -1))
    for ar, ac, l in edges[(row, col)]:
      queue.append((ar, ac, dist + l))
  return best

def get_input():
  with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
    content = [s.strip() for s in f.read().rstrip().split('\n')]
  return content

@profiler
def solve():
  grid = get_input()
  print(f'Part 1: {part1(grid)}')
  print(f'Part 2: {part2(grid)}')

if __name__ == "__main__":
  solve()
