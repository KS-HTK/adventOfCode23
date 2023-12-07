# -*- coding: utf-8 -*-

import os
from collections import defaultdict, Counter
from functools import cmp_to_key
from time import perf_counter
from typing import List

def profiler(method):
  def profiler_method(*arg, **kw):
    t = perf_counter()
    ret = method(*arg, **kw)
    print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
    return ret
  return profiler_method

cards = {
  'A': 14,
  'K': 13,
  'Q': 12,
  'J': 11,
  'T': 10,
  '9': 9,
  '8': 8,
  '7': 7,
  '6': 6,
  '5': 5,
  '4': 4,
  '3': 3,
  '2': 2,
}

def get_comp(gt_func):
  def comparator(a, b):
    ah = a[0]
    bh = b[0]
    ca = Counter(ah)
    cb = Counter(bh)
    ta = gt_func(ca)
    tb = gt_func(cb)
    if ta != tb:
      return ta - tb

    for i in range(5):
      if ah[i] != bh[i]:
        return cards[ah[i]] - cards[bh[i]]
  return comparator

def get_type(h):
  if len(h) == 1:
    return 5
  if len(h) == 2 and 4 in h.values():
    return 4
  if len(h) == 2 and 3 in h.values():
    return 3
  if len(h) == 3 and 3 in h.values():
    return 2
  if len(h) == 3:
    return 1
  if len(h) == 4:
    return 0
  return -1
  
def get_type2(h):
  if 'J' not in h.keys():
    return get_type(h)
  if h['J'] == 5:
    return 5
  if h['J'] == 4:
    return 5
  if h['J'] == 3:
    if len(h) == 2:
      return 5
    return 4
  if len(h) == 2:
    return 5
  if len(h) == 3 and (4-h['J']) in h.values():
    return 4
  if len(h) == 3 and ((3-h['J']) in h.values() or (2-h['J']) in h.values()):
    return 3
  if len(h) == 4 and (3-h['J']) in h.values():
    return 2
  if len(h) == 4 and (2-h['J']) in h.values():
    return 1
  if len(h) == 5:
    return 0
  return -1

# Part 1:
def part1(content = None) -> str|int:
  lst = sorted(content, key=cmp_to_key(get_comp(get_type)))
  res = 0
  for i, p in enumerate(lst):
    res += (i+1)*p[1]
  return res

# Part 2:
def part2(content = None) -> str|int:
  cards['J'] = -1
  lst = sorted(content, key=cmp_to_key(get_comp(get_type2)))
  res = 0
  for i, p in enumerate(lst):
    res += (i+1)*p[1]
  return res

def get_input():
  with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
    content = [s.strip() for s in f.read().rstrip().split('\n')]
  return content

@profiler
def solve():
  content = get_input()
  content = [([c for c in s[0]], int(s[1])) for s in [l.split(' ') for l in content]]
  print("Part 1:", part1(content))
  
  content = get_input()
  content = [([c for c in s[0]], int(s[1])) for s in [l.split(' ') for l in content]]
  print("Part 2:", part2(content))

if __name__ == "__main__":
  solve()
