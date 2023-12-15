# -*- coding: utf-8 -*-

import os
from time import perf_counter
from typing import List
from collections import defaultdict

def profiler(method):
  def profiler_method(*arg, **kw):
    t = perf_counter()
    ret = method(*arg, **kw)
    print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
    return ret
  return profiler_method

def hash(s: str) -> int:
  cv = 0
  for c in s:
    cv += ord(c)
    cv *= 17
    cv %= 256
  return cv

# Part 1:
def part1(content = None) -> int:
  return sum([hash(s) for s in content])

# Part 2: not 312453970
def part2(content = None) -> str|int:
  hashmap = defaultdict(dict)
  for s in content:
    if '-' in s:
      label, focal_length = s.split('-')
    if '=' in s:
      label, focal_length = s.split('=')
    h = hash(label)
    if '-' in s:
      hashmap[h].pop(label, None)
    else:
      hashmap[h][label] = int(focal_length)

  fp = 0
  for k, v in hashmap.items():
    for i, fl in enumerate(v.values()):
      fp += (k+1) * (i+1) * fl
  return fp

def get_input():
  with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
    content = [s.strip() for s in f.read().rstrip().split(',')]
  return content

@profiler
def solve():
  content = get_input()
  print(f'Part 1: {part1(content)}')
  print(f'Part 2: {part2(content)}')

if __name__ == "__main__":
  solve()
