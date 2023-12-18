# -*- coding: utf-8 -*-

import os
from time import perf_counter
from itertools import tee, pairwise
from typing import List, Tuple, Dict

def profiler(method):
  def profiler_method(*arg, **kw):
    t = perf_counter()
    ret = method(*arg, **kw)
    print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
    return ret
  return profiler_method

directions: Dict[str, Tuple[int, int]] = {
  'L': (0, -1),
  'R': (0, 1),
  'U': (-1, 0),
  'D': (1, 0),
  '0': (0, 1),
  '1': (1, 0),
  '2': (0, -1),
  '3': (-1, 0)
}

def shoelace(vertices: List[Tuple[int, int]]) -> int:
  area: int = 0
  for (y1, x1), (y2, x2) in pairwise(vertices):
    area += (y2 + y1) * (x2 - x1)
  return abs(area) // 2


def get_area(vertices: List[Tuple[int, int]], perimeter: int) -> int:
  area: int = shoelace(vertices)
  return int(area - perimeter / 2 + 1) + perimeter

def get_input():
  with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
    content = [s.strip() for s in f.read().rstrip().split('\n')]
  return content

@profiler
def solve():
  content: List[str] = get_input()

  vertices1: List[Tuple[int, int]] = []
  vertices2: List[Tuple[int, int]] = []
  perimeter1: int = 0
  perimeter2: int  = 0
  y1: int = 0
  x1: int = 0
  y2: int = 0
  x2: int = 0

  for line in content:
    d, s, c = line.split()
    s = int(s)

    dy, dx = directions[d]
    y1 += s * dy
    x1 += s * dx
    vertices1.append((y1, x1))
    perimeter1 += s

    d = c[-2]
    s = int(c[2:-2], 16)
    dy, dx = directions[d]
    y2 += s * dy
    x2 += s * dx
    vertices2.append((y2, x2))
    perimeter2 += s
    
  print(f'Part 1: {get_area(vertices1, perimeter1)}')
  print(f'Part 2: {get_area(vertices2, perimeter2)}')

if __name__ == "__main__":
  solve()
