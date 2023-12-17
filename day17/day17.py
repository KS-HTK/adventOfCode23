# -*- coding: utf-8 -*-

import os
from time import perf_counter
from typing import List
import heapq

def profiler(method):
  def profiler_method(*arg, **kw):
    t = perf_counter()
    ret = method(*arg, **kw)
    print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
    return ret
  return profiler_method

def find_path(grid: List[List[int]], pt2=False) -> int:
  ly = len(grid)
  lx = len(grid[0])
  queue = [(0,0,0,-1,-1)] # (loss, y, x, direction, direction_count)
  visited = set()
  while queue:
    loss, y, x, direction, dir_count = heapq.heappop(queue)
    if (y, x, direction, dir_count) in visited:
      continue
    visited.add((y, x, direction, dir_count))
    for new_dir,(dy,dx) in enumerate([[-1,0],[0,1],[1,0],[0,-1]]):
      yy = y+dy
      xx = x+dx
      
      new_dir_count = (1 if new_dir!=direction else dir_count+1)
      not_reverse = ((new_dir + 2)%4 != direction)

      is_valid1 = (new_dir_count <= 3)
      is_valid2 = (new_dir_count <= 10 and (new_dir==direction or dir_count >= 4 or dir_count == -1))
      is_valid = (is_valid2 if pt2 else is_valid1)

      if 0<=yy<len(grid) and 0<=xx<len(grid[0]) and not_reverse and is_valid:
        if yy == len(grid)-1 and xx == len(grid[0])-1:
          return loss+grid[yy][xx]
        heapq.heappush(queue, (loss+grid[yy][xx], yy, xx, new_dir, new_dir_count))

def get_input():
  with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
    content = [s.strip() for s in f.read().rstrip().split('\n')]
  return content

@profiler
def solve():
  grid: List[List[int]] = [[int(c) for c in l] for l in get_input()]
  print(f'Part 1: {find_path(grid)}')
  print(f'Part 2: {find_path(grid, True)}')

if __name__ == "__main__":
  solve()
