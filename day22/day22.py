# -*- coding: utf-8 -*-

import os
from time import perf_counter
import math
from typing import List

def profiler(method):
  def profiler_method(*arg, **kw):
    t = perf_counter()
    ret = method(*arg, **kw)
    print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
    return ret
  return profiler_method

def tuple_sub(p1, p2):
  return tuple(a-b for a, b in zip(p1, p2))

class Brick:
  def __init__(self, start, end):
    self.start, self.end = sorted([start, end])
    self.supporting = []
    self.supported = []

  def __repr__(self):
    return f"Brick({self.start}, {self.end})"

  def __len__(self):
    return math.prod(1+i for i in tuple_sub(self.end, self.start))
  
  def __iter__(self):
    return ((x, y, z) for x in range(self.start[0], self.end[0]+1)
                      for y in range(self.start[1], self.end[1]+1)
                      for z in range(self.start[2], self.end[2]+1))

  def __hash__(self):
    return hash((self.start, self.end))

  def intersect(self, other: "Brick"):
    xs1, ys1, zs1 = self.start
    xe1, ye1, ze1 = self.end
    xs2, ys2, zs2 = other.start
    xe2, ye2, ze2 = other.end
    return (xs1 <= xe2 and xs2 <= xe1 and
            ys1 <= ye2 and ys2 <= ye1 and
            zs1 <= ze2 and zs2 <= ze1)

  def step_down(self):
    return Brick(tuple_sub(self.start, (0, 0, 1)), tuple_sub(self.end, (0, 0, 1)))

  def key_z(self):
    return self.start[2]


def parse_line(line):
  start, end = line.split('~')
  return Brick(tuple(map(int, start.split(','))), tuple(map(int, end.split(','))))

def drop_bricks(bricks) -> None:
  for i in range(len(bricks)):
    while True:
      brick = bricks[i]
      if brick.start[2] == 1:
        break
      dropped_brick = brick.step_down()
      for j, b in enumerate(bricks[:i]):
        if i == j:
          continue
        if dropped_brick.intersect(b):
          break
      else:
        bricks[i] = dropped_brick
        continue
      break
  bricks.sort(key=Brick.key_z)

def get_support(bricks) -> None:
  for brick in bricks:
    dropped_brick = brick.step_down()
    for lower_brick in bricks:
      if brick is lower_brick:
        continue
      if dropped_brick.intersect(lower_brick):
        lower_brick.supporting.append(brick)
        brick.supported.append(lower_brick)

# Part 1:
def part1(bricks) -> int:
  return sum(all(len(top.supported)>1 for top in brick.supporting) for brick in bricks)

def count_falls(brick, fallen=None):
  if fallen is None:
    fallen = set()
  fallen.add(brick)
  for sub in brick.supporting:
    if not (set(sub.supported)-fallen):
      count_falls(sub, fallen)
  return len(fallen) - 1

# Part 2:
def part2(bricks) -> int:
  return sum(count_falls(brick) for brick in bricks)

def get_input():
  with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
    content = [s.strip() for s in f.read().rstrip().split('\n')]
  return content

@profiler
def solve():
  bricks = list(map(parse_line, get_input()))
  bricks.sort(key=Brick.key_z)
  drop_bricks(bricks)
  get_support(bricks)
  print(f'Part 1: {part1(bricks)}')
  print(f'Part 2: {part2(bricks)}')

if __name__ == "__main__":
  solve()
