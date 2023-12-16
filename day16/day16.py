# -*- coding: utf-8 -*-

import os
from time import perf_counter
from typing import List, Dict, Tuple, Set

def profiler(method):
  def profiler_method(*arg, **kw):
    t = perf_counter()
    ret = method(*arg, **kw)
    print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
    return ret
  return profiler_method

directions = {
  'U': (-1, 0),
  'D': (1, 0),
  'R': (0, 1),
  'L': (0, -1)
}
reflections = {
  'R': {'/': 'U', '\\': 'D'},
  'L': {'/': 'D', '\\': 'U'},
  'U': {'/': 'R', '\\': 'L'},
  'D': {'/': 'L', '\\': 'R'},
}

def beam_deflect(beam, char):
  match char:
    case '-':
      return beam[2] if beam[2] in 'RL' else 'RL'
    case '|':
      return beam[2] if beam[2] in 'UD' else 'UD'
  return reflections[beam[2]][char]

def propagate(initial, grid):
  beams = [initial]
  ly = len(grid)
  lx = len(grid[0])

  energized = set()
  seen = set()
  while len(beams) > 0:
    beam = beams.pop()
    y = beam[0] + directions[beam[2]][0]
    x = beam[1] + directions[beam[2]][1]

    if ly <= y or y < 0 or lx <= x or x < 0 or beam in seen:
      continue
    
    seen.add(beam)
    energized.add((y,x))
    if grid[y][x] == '.':
      beam = (y,x,beam[2])
      beams.append(beam)
      continue

    for d in beam_deflect(beam, grid[y][x]):
      beam = (y,x,d)
      beams.append(beam)
  return len(energized)

# Part 1:
def part1(grid: List[List[str]]) -> int:
  return propagate((0, -1, 'R'), grid)
  

# Part 2:
def part2(grid: List[List[str]]) -> int:
  lx = len(grid[0])
  ly = len(grid)
  res = 0
  for x in range(lx):
    res = max(propagate((-1, x, 'D'), grid), propagate((ly, x, 'U'), grid), res)
  for y in range(ly):
    res = max(propagate((y, -1, 'R'), grid), propagate((y, lx, 'L'), grid), res)
  return res

def get_input():
  with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
    content = [s.strip() for s in f.read().rstrip().split('\n')]
  return content

@profiler
def solve():
  grid = [[c for c in l] for l in get_input()]
  print(f'Part 1: {part1(grid)}')
  print(f'Part 2: {part2(grid)}')

if __name__ == "__main__":
  solve()
