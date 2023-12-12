# -*- coding: utf-8 -*-

import os
from time import perf_counter
from typing import List

def profiler(method):
  def profiler_method(*arg, **kw):
    t = perf_counter()
    ret = method(*arg, **kw)
    print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
    return ret
  return profiler_method

def getcount(memo, line, counts, pos, current_count, countpos):
  key = (pos, current_count, countpos)
  if key in memo:
    return memo[key]
  if pos == len(line):
    ret = 1 if len(counts) == countpos else 0
  elif line[pos] == '#':
    ret = getcount(memo, line, counts, pos + 1, current_count + 1, countpos)
  elif line[pos] == '.' or countpos == len(counts):
    if countpos < len(counts) and current_count == counts[countpos]:
      ret = getcount(memo, line, counts, pos + 1, 0, countpos + 1)
    elif current_count == 0:
      ret = getcount(memo, line, counts, pos + 1, 0, countpos)
    else:
      ret = 0
  else:
    hash_count = getcount(memo, line, counts, pos + 1, current_count + 1, countpos)
    dot_count = 0
    if current_count == counts[countpos]:
      dot_count = getcount(memo, line, counts, pos + 1, 0, countpos + 1)
    elif current_count == 0:
      dot_count = getcount(memo, line, counts, pos + 1, 0, countpos)
    ret = hash_count + dot_count
  memo[key] = ret
  return ret

def count_options(content, folded=False) -> int:
  res = 0
  for line, counts in content:
    if folded:
      counts *= 5
      line = (line+'?')*4+line
    res += getcount({}, line+'.', counts, 0, 0, 0)
  return res

def get_input():
  with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
    content = [s.strip() for s in f.read().rstrip().split('\n')]
  return content

@profiler
def solve():
  content = get_input()
  content = [c.split(' ') for c in content if c != '']
  content = [(c[0], [int(x) for x in c[1].split(',')]) for c in content]
  print("Part 1:", count_options(content))
  print("Part 2:", count_options(content, True))

if __name__ == "__main__":
  solve()
