# -*- coding: utf-8 -*-

import os
from time import perf_counter
from typing import List, Tuple
from collections import defaultdict, deque

def profiler(method):
  def profiler_method(*arg, **kw):
    t = perf_counter()
    ret = method(*arg, **kw)
    print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
    return ret
  return profiler_method

def get_s_coordinates(pipes) -> Tuple[int, int]:
  for i in range(len(pipes)):
    if 'S' in pipes[i]:
      x = i
      y = pipes[i].index('S')
  return x, y

def next_tile(y: int, x: int, pipes) -> Tuple[Tuple[int, int], Tuple[int, int]]:
  match pipes[y][x]:
    case '|':
      return (y-1, x), (y+1, x)
    case '-':
      return (y, x-1), (y, x+1)
    case 'L':
      return (y, x+1), (y-1, x)
    case 'J':
      return (y, x-1), (y-1, x)
    case '7':
      return (y, x-1), (y+1, x)
    case 'F':
      return (y, x+1), (y+1, x)
    case 'S':
      rtn: List[Tuple[int, int]] = []
      if pipes[y-1][x] in '|F7':
        rtn.append((y-1, x))
      if pipes[y+1][x] in '|JL':
        rtn.append((y+1, x))
      if pipes[y][x-1] in '-FL':
        rtn.append((y, x-1))
      if pipes[y][x+1] in '-J7':
        rtn.append((y, x+1))
      return rtn[0], rtn[1]
    case _:
      return None, None

def get_next(n1, n2, pipes, visited) -> Tuple[Tuple[int, int], Tuple[int, int]]:
  a, b = next_tile(*n1, pipes)
  c, d = next_tile(*n2, pipes)
  n = [a, b, c, d]
  n = [x for x in n if x not in visited]
  if len(n) == 0:
    return None, None
  return n

# Part 1:
def part1(pipes) -> int:
  x, y = get_s_coordinates(pipes)
  n1, n2 = next_tile(x, y, pipes)
  visited = [(x, y), n1, n2]
  steps = 1
  while True:
    o1, o2 = get_next(n1, n2, pipes, visited)
    if o1 == None and o2 == None:
      return steps
    steps += 1
    visited.append(o1)
    visited.append(o2)
    n1, n2 = o1, o2
  return -1

def next_tile2(y: int, x: int, pipes) -> Tuple[Tuple[int, int], Tuple[int, int]]:
  match pipes[y][x]:
    case "|":
      return (2*y-1, 2*x), (2*y+1, 2*x)
    case "-":
      return (2*y, 2*x-1), (2*y, 2*x+1)
    case "L":
      return (2*y-1, 2*x), (2*y, 2*x+1)
    case "J":
      return (2*y-1, 2*x), (2*y, 2*x-1)
    case "7":
      return (2*y+1, 2*x), (2*y, 2*x-1)
    case "F":
      return (2*y+1, 2*x), (2*y, 2*x+1)
    case "S":
      rtn: List[Tuple[int, int]] = []
      if pipes[y-1][x] in '|F7':
        rtn.append((2*y-1, 2*x))
      if pipes[y+1][x] in '|JL':
        rtn.append((2*y+1, 2*x))
      if pipes[y][x-1] in '-FL':
        rtn.append((2*y, 2*x-1))
      if pipes[y][x+1] in '-J7':
        rtn.append((2*y, 2*x+1))
      return rtn[0], rtn[1]
    case _:
      return None, None

# Part 2:
def part2(content) -> int:
  start = None
  start_adj = []
  adj = defaultdict(list)
  for i, line in enumerate(content):
    for j, cell in enumerate(line):
      if cell == 'S':
        start = (2*i, 2*j)
        continue
      neighbors = next_tile2(i, j, content)
      if neighbors == (None, None):
        continue
      for x, y in neighbors:
        if x >= 0 and x < 2*len(content) and y >= 0 and y < 2*len(line):
          adj[(2*i, 2*j)].append((x, y))

  for i in range(len(content)):
    xs = []
    if i > 0: xs.append(2*i-1)
    if i+1 < len(content): xs.append(2*i+1)
    for j in range(len(content[i])):
      ys = []
      if j > 0: ys.append(2*j-1)
      if j+1 < len(line): ys.append(2*j+1)
      for nx in xs:
        adj[(nx, 2*j)].append((2*i, 2*j))
      for ny in ys:
        adj[(2*i, ny)].append((2*i, 2*j))
                
  inv_start = []
  indeg = defaultdict(int)
  for vert in adj:
    for vert2 in adj[vert]:
      indeg[vert2] += 1
      if vert2 == start:
        inv_start.append(vert)
  for vert in inv_start:
    if indeg[vert] > 0:
      adj[start].append(vert)

  INF = 1000000000
  dst = defaultdict(lambda: INF)
  bfs_q = deque()
  bfs_q.append(start)
  dst[start] = 0
  ans = (0, start)
  inloop = set()
  while len(bfs_q) > 0:
    curcell = bfs_q.popleft()
    inloop.add(curcell)
    for nxt in adj[curcell]:
      if dst[nxt] == INF:
        dst[nxt] = dst[curcell] + 1
        ans = max(ans, (dst[nxt], nxt))
        bfs_q.append(nxt)

  ans2 = 0
  vis = set()
  for i, line in enumerate(content):
    for j, cell in enumerate(line):
      if (2*i, 2*j) in inloop or (2*i, 2*j) in vis:
        continue
      added_to_q = set()
      cur_q = deque()
      cur_q.append((2*i, 2*j))
      added_to_q.add((2*i, 2*j))
      enclosed = True
      while len(cur_q) > 0:
        cx, cy = cur_q.popleft()
        for nx, ny in [(cx-1, cy), (cx+1, cy), (cx, cy-1), (cx, cy+1)]:
          if (nx, ny) in inloop or (nx, ny) in added_to_q:
            continue
          assert((nx, ny) not in vis)
          if nx < 0 or nx >= 2*len(content) or ny < 0 or ny >= 2*len(line):
            enclosed = False
            continue
          cur_q.append((nx, ny))
          added_to_q.add((nx, ny))
      for c in added_to_q:
        if c[0] % 2 == 0 and c[1] % 2 == 0 and enclosed:
          ans2 += 1
        vis.add(c)
  return ans2

def get_input():
  with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
    content = [s.strip() for s in f.read().rstrip().split('\n')]
  return content

@profiler
def solve():
  content = get_input()
  content = [[c for c in line] for line in content]

  print("Part 1:", part1(content))
  print("Part 2:", part2(content))

if __name__ == "__main__":
  solve()
