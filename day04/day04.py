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

def get_winners(content: List[str]) -> dict:
  winners = {}
  for line in content:
    if line == '':
      continue
    head, tail = line.split(': ')
    winning, numbers = tail.split(' | ')
    cardnum = re.findall(r'\d+', head)[0]
    winning = re.findall(r'\d+', winning)
    numbers = re.findall(r'\d+', numbers)
    winners[int(cardnum)] = len([int(n) for n in numbers if n in winning])
  return winners

# Part 1:
def part1(winners: dict) -> int:
  return sum([int(2**(v-1)) for v in winners.values()])

# Part 2:
def part2(winners: dict) -> int:
  cardcount = 0
  stack = {}
  for k in winners.keys():
    stack[k] = 1
  for k in stack.keys():
    cardcount += stack[k]
    for i in range(1, winners[k]+1):
      if k+i not in winners:
        break
      stack[k+i] += stack[k]
  return cardcount

def get_input():
  with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
    content = [s.strip() for s in f.read().rstrip().split('\n')]
  return content

@profiler
def solve():
  content = get_input()
  winners = get_winners(content)
  print("Part 1:", part1(winners))
  print("Part 2:", part2(winners))

if __name__ == "__main__":
  solve()
