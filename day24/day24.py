# -*- coding: utf-8 -*-

import os
import sympy
import numpy as np
from itertools import combinations
from time import perf_counter

def profiler(method):
  def profiler_method(*arg, **kw):
    t = perf_counter()
    ret = method(*arg, **kw)
    print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
    return ret
  return profiler_method

# Part 1:
def part1(vectors) -> int:
  min_ = 200000000000000
  max_ = 400000000000000
  def intersect(a, b):
    ax, ay, _, adx, ady, _ = a
    bx, by, _, bdx, bdy, _ = b
    try:
      t, u = np.linalg.solve([[adx, -bdx], [ady, -bdy]], [bx-ax, by-ay])
    except:
      return False
    x = ax+adx*t
    y = ay+ady*t
    if t<0 or u<0:
      return False
    if min_ <= x <= max_ and min_ <= y <= max_:
      return True
    return False
  return sum(intersect(i, j) for i, j in combinations(vectors, 2))

# Part 2:
def part2(vectors) -> int:
  p, v, t = (sympy.symbols(f'{ch}(:3)') for ch in 'pvt')
  equations = [vectors[i, j] + t[i] * vectors[i, 3 + j] - p[j] - v[j] * t[i] for i in range(3) for j in range(3)]
  return sum(sympy.solve(equations, (*p, *v, *t))[0][:3])

def get_input():
  with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
    content = [s.strip() for s in f.read().rstrip().split('\n')]
  return content

@profiler
def solve():
  content = get_input()
  vectors = np.array([line.replace('@', ',').split(',') for line in content], dtype='int64')
  print(f'Part 1: {part1(vectors)}')
  print(f'Part 2: {part2(vectors)}')

if __name__ == "__main__":
  solve()
