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

def get_chances(time: int, distance: int) -> int:
  return time-2*bin_search(time, distance, 0, time//2)+1

def bin_search(t: int, d: int, l: int, h: int) -> int:
  if l > h:
    return l
  mid = (l+h)//2
  dist = (t-mid)*mid
  if d < dist:
    return bin_search(t, d, l, mid-1)
  return bin_search(t, d, mid+1, h)

# Part 1:
def part1(content: List[str]) -> int:
  times = [int(t) for t in re.findall(r'\d+', content[0])]
  distances = [int(t) for t in re.findall(r'\d+', content[1])]
  prod = 1
  for t, d in zip(times, distances):
    prod *= get_chances(t, d)
  return prod

# Part 2:
def part2(content: List[str]) -> int:
  time = [int(t) for t in re.findall(r'\d+', content[0].replace(' ', ''))][0]
  distance = [int(t) for t in re.findall(r'\d+', content[1].replace(' ', ''))][0]
  return get_chances(time, distance)

def get_input():
  with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
    content = [s.strip() for s in f.read().rstrip().split('\n')]
  return content

@profiler
def solve():
  content = get_input()
  print(f'Part 1: {part1(content)}')
  print(f'Part 2: {part2(content)}')

if __name__ == "__main__":
  solve()
