# -*- coding: utf-8 -*-

import os
import re
from time import perf_counter
from collections import defaultdict
from typing import List

def profiler(method):
  def profiler_method(*arg, **kw):
    t = perf_counter()
    ret = method(*arg, **kw)
    print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
    return ret
  return profiler_method

def get_totals() -> (int, int):
  content = get_input()
  total = 0
  len_y = len(content)
  gear_nums = defaultdict(list)
  num_pattern = re.compile(r'\d+')

  for row_num in range(len_y):
    for match in re.finditer(num_pattern, content[row_num]):
      num = int(match.group(0))
      for y in range(row_num-1, row_num+2):
        for x in range(match.start()-1, match.end()+1):
          if y >= 0 and y < len(content) and x >= 0 and x < len(content[y]):
            if content[y][x] not in '0123456789.':
              if content[y][x] == '*':
                gear_nums[ (y,x) ].append(num)
              total += num
  
  gear_total = 0
  for k,v in gear_nums.items():
    if len(v) == 2:
      gear_total += v[0]*v[1]
  return total, gear_total
  

def get_input():
  with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
    content = [s.strip() for s in f.read().rstrip().split('\n')]
  return content

@profiler
def solve():
  p1, p2 = get_totals()
  print("Part 1:", p1)
  print("Part 2:", p2)

if __name__ == "__main__":
  solve()
