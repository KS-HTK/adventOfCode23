# -*- coding: utf-8 -*-

import os
from time import perf_counter
from typing import List, Tuple, Dict, Set
from collections import defaultdict
from copy import deepcopy
from itertools import count
from math import lcm

def profiler(method):
  def profiler_method(*arg, **kw):
    t = perf_counter()
    ret = method(*arg, **kw)
    print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
    return ret
  return profiler_method

def parse_inp(content: List[str]) -> Tuple[Dict[str, str], Dict[str, Set[str]], Dict[str, List[str]]]:
  typ_map: Dict[str, str] = {}
  in_map: Dict[str, Set[str]] = defaultdict(set)
  out_map: Dict[str, List[str]] = {}
  for line in content:
    name, out = line.split(' -> ')
    out = out.split(', ')
    if name != 'broadcaster':
      typ, name = name[0], name[1:]
      typ_map[name] = typ
    for o in out:
      in_map[o].add(name)
    out_map[name] = out
  return typ_map, in_map, out_map

def press_btns(content: List[str], part2: bool = False) -> int:
  typ_map, in_map, out_map = parse_inp(content)
  state: Dict[str, bool | Dict[str, bool]] = {}
  for name, typ in typ_map.items():
    match typ:
      case '%':
        state[name] = False
      case '&':
        state[name] = {k: False for k in in_map[name]}

  rx_trigger: str = in_map['rx'].pop()
  useful: Set[str] = in_map[rx_trigger]
  useful_vals: Dict[str, int] = {}

  iterate = range(1000) if not part2 else count(1)
  memory: Dict[str, Tuple[Dict[str, bool | Dict[str, bool]], Tuple[int, int]]] = {}
  totals: Tuple[int, int] = (0, 0)

  for i in iterate:
    sr = state.__repr__()
    if sr in memory:
      state, (low, high) = memory[sr]
      totals = (totals[0]+low, totals[1]+high)
      continue
  
    queue = [('broadcaster', False, 'button')]
    low, high = 0, 0
    while queue:
      name, pulse, trigger = queue.pop(0)
      if pulse:
        high += 1
      else:
        low += 1
      if part2 and not pulse:
        if name in useful and name not in useful_vals:
          useful_vals[name] = i
          if len(useful_vals) == len(useful):
            return lcm(*useful_vals.values())
      #print(f'{trigger} -{pulse}-> {name}')
      match typ_map.get(name):
        case '%':
          if not pulse:
            next_pulse = state[name] = not state[name]
            for o in out_map[name]:
              queue.append((o, next_pulse, name))
        case '&':
          state[name][trigger] = pulse
          next_pulse = not all(state[name].values())
          for o in out_map[name]:
            queue.append((o, next_pulse, name))
        case _:
          if name in out_map:
            for o in out_map[name]:
              queue.append((o, pulse, name))
    memory[sr] = deepcopy(state), (low, high)
    totals = (totals[0]+low, totals[1]+high)
  return totals[0]*totals[1]

def get_input():
  with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
    content = [s.strip() for s in f.read().rstrip().split('\n')]
  return content

@profiler
def solve():
  content = get_input()

  print(f'Part 1: {press_btns(content)}')
  print(f'Part 2: {press_btns(content, True)}')

if __name__ == "__main__":
  solve()
