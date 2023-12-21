# -*- coding: utf-8 -*-

import os
from time import perf_counter
from typing import List, Tuple, Set
from heapq import heapify, heappush, heappop

def profiler(method):
  def profiler_method(*arg, **kw):
    t = perf_counter()
    ret = method(*arg, **kw)
    print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
    return ret
  return profiler_method

def get_count():
  data: List[str] = get_input()
  ln: int = len(data)
  steps: int = 0
  cycle: list = []
  seen: Set[Tuple[int, int]] = set()
  even: Set[Tuple[int, int]] = set() 
  odd: Set[Tuple[int, int]] = set()
  n: int = 26501365
  grid: Dict[Tuple[int, int], str ] = {(x, y) : c for y, l in enumerate(data) for x, c in enumerate(l)}
  heapify(queue := [(steps, next((k for k, v in grid.items() if v == "S")))])
  while queue:
    new_steps, (x, y) = heappop(queue)
    if (x, y) in seen: 
      continue
    seen.add((x, y))
    if new_steps != steps:
      if steps == 64: 
        p1 = len(even)
      if steps % (ln * 2) == n % (ln * 2):
        if len(cycle := cycle + [len([even, odd][steps % 2])]) == 3:
          p2 = cycle[0]
          offset = cycle[1] - cycle[0]
          increment = (cycle[2] - cycle[1]) - (cycle[1] - cycle[0])
          for x in range(n // (ln * 2)):
            p2 += offset
            offset += increment
          return p1, p2
    steps, next_steps = new_steps, new_steps + 1
    for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
      if grid[nx % ln, ny % ln] != "#":
        if not next_steps % 2: 
          even.add((nx, ny))
        else:                  
          odd.add((nx, ny))
        heappush(queue, (next_steps, (nx, ny)))

def get_input() -> List[str]:
  with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
    content = [s.strip() for s in f.read().rstrip().split('\n')]
  return content

@profiler
def solve():
  p1, p2 = get_count()
  print(f'Part 1: {p1}\nPart 2: {p2}')

if __name__ == "__main__":
  solve()
