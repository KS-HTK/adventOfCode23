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

# Part 1:
def part1(content = None) -> str|int:
  valid = []
  for line in content:
    line = line.split(': ')
    game_id = re.search(r'\d+', line[0])[0]
    revealed_sets = [[st.split(' ') for st in s.split(', ')] for s in line[1].split('; ')]
    invalid = False
    for rset in revealed_sets:
      for amount, color in rset:
        if (color == 'red' and int(amount) > 12) or (color == 'green' and int(amount) > 13) or (color == 'blue' and int(amount) > 14):
          invalid = True
          break
    if invalid: 
      continue
    valid.append(int(game_id))
  return sum(valid)

# Part 2:
def part2(content = None) -> str|int:
  powers = []
  for line in content:
    game_id, sets = line.split(': ')
    amount_color = [ac.split(' ') for x in (s.split(', ') for s in sets.split('; ')) for ac in x]
    reds = [int(amount) for amount, color in amount_color if color == 'red']
    greens = [int(amount) for amount, color in amount_color if color == 'green']
    blues = [int(amount) for amount, color in amount_color if color == 'blue']
    powers.append(max(reds, default=0) * max(greens, default=0) * max(blues, default=0))
  return sum(powers)

def get_input():
  with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
    content = [s.strip() for s in f.read().rstrip().split('\n')]
  return content

@profiler
def solve():
  content = get_input()
  print("Part 1:", part1(content))
  print("Part 2:", part2(content))

if __name__ == "__main__":
  solve()
