# -*- coding: utf-8 -*-

import os
from time import perf_counter
from typing import List, Tuple, Dict
from copy import deepcopy

def profiler(method):
  def profiler_method(*arg, **kw):
    t = perf_counter()
    ret = method(*arg, **kw)
    print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
    return ret
  return profiler_method

def parse_workflows(workflow_str):
  workflows = {}
  for w in workflow_str:
    name, rules = w[:-1].split('{')
    workflows[name] = []
    rules = rules.split(',')
    end = rules[-1]
    for r in rules[:-1]:
      cond, nxt = r.split(':')
      var, op, val = cond[0], cond[1], int(cond[2:])
      workflows[name].append(((var, op, val), nxt))
    workflows[name].append((('x', '>', -1), end))
  return workflows

# Part 1:
def part1(workflows: Dict[str, List[Tuple[Tuple[str, str, int], str]]], parts: List[Dict[str, int]]) -> int:
  res: List[int] = []
  p: Dict[str, int]
  for p in parts:
    nxt: str = 'in'
    while nxt not in 'AR':
      for ((var, op, val), r) in workflows[nxt]:
        if (op == '>' and p[var] > val) or (op == '<' and p[var] < val):
          nxt = r
          break
    res.extend([p[k] for k in p.keys() if nxt == 'A'])
  return sum(res)

# Part 2:
def part2(workflows: Dict[str, List[Tuple[Tuple[str, str, int], str]]]) -> int:
  stack: List[Tuple[Dict[str, int], str]] = [({k: (1,4000) for k in 'xmas'}, 'in')]
  accepted_cases: int = 0
  while stack:
    ranges, nxt = stack.pop()
    for ((var, op, val), r) in workflows[nxt]:
      range_var = ranges[var]
      if op == '>':
        if range_var[1] > val:
          range_copy = deepcopy(ranges)
          range_copy[var] = (max(range_var[0], val + 1), range_var[1])
        ranges[var] = (range_var[0], val)
      else:
        if range_var[0] < val:
          range_copy = deepcopy(ranges)
          range_copy[var] = (range_var[0], min(range_var[1], val - 1))
        ranges[var] = (val, range_var[1])
      if r == 'A':
        res: int = 1
        for val in range_copy.values():
          res *= 1 + val[1] - val[0]
        accepted_cases += res
      elif r != 'R':
        stack.append((range_copy, r))
  return accepted_cases

def get_input() -> Tuple[Dict[str, List[Tuple[Tuple[str, str, int], str]]], List[Dict[str, int]]]:
  with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
    content = [s.strip() for s in f.read().rstrip().split('\n\n')]
  inst = parse_workflows(content[0].split('\n'))
  parts = []
  for p in [s[1:-1].split(',') for s in content[1].split('\n')]:
    parts.append({k: int(v) for k, v in [s.split('=') for s in p]})
  return inst, parts

@profiler
def solve():
  inst, parts = get_input()
  print(f'Part 1: {part1(inst, parts)}')
  print(f'Part 2: {part2(inst)}')

if __name__ == "__main__":
  solve()
