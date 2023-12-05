# -*- coding: utf-8 -*-

import os
import re
from time import perf_counter
from typing import List, Dict, Tuple, Optional

def profiler(method):
  def profiler_method(*arg, **kw):
    t = perf_counter()
    ret = method(*arg, **kw)
    print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
    return ret
  return profiler_method

class Mapper(object):
  def __init__(self):
    self.sources: List[int] = []
    self.destinations: List[int] = []
    self.lengths: List[int] = []
  
  def __getitem__(self, key: int):
    for i, s in enumerate(self.sources):
      if s <= key and s + self.lengths[i] > key:
        return self.destinations[i] + key - s
    return key
  
  def __repr__(self):
    return f'Mapper({self.sources}, {self.destinations}, {self.lengths})'
  
  def add_range(self, source: int, destination: int, length: int) -> None:
    self.sources.append(source)
    self.destinations.append(destination)
    self.lengths.append(length)
  
  def map_int(self, i: int) -> int:
    for index, source in enumerate(self.sources):
      if i in range(source, source+self.lengths[index]):
        return self.destinations[index] + (i-source)
    return i

  def _map_range_single(self, q_start: int, q_length: int, r_start: int, r_dest: int, r_length: int) -> Optional[Tuple[int, int, int]]:
    q_end = q_start + q_length # exclusive end of range
    r_end = r_start + r_length # exclusive end of range
    # check if the ranges overlaps
    if q_end <= r_start or r_end <= q_start:
      # range do not overlap
      return None

    # ranges partially overlap
    if r_start <= q_start < r_end <= q_end:
      # query range start in and ends after current range
      return q_start, q_start - r_start + r_dest, r_end - q_start
    if q_start <= r_start < q_end <= r_end:
      # query range starts before and ends in current range
      return r_start, r_dest, q_end - r_start

    # one of the ranges lies within the other
    if q_start <= r_start and r_end <= q_end:
      # query range contains current range
      return r_start, r_dest, r_length
    if r_start <= q_start and q_end <= r_end:
      # current range contains query range
      return q_start, r_dest + q_start - r_start, q_length

  def map_range(self, start: int, length: int) -> List[Tuple[int, int]]:
    mapped_range = []
    source_range = []
    for i, source in enumerate(self.sources):
      mapping = self._map_range_single(start, length, source, self.destinations[i], self.lengths[i])
      if not mapping:
        continue
      s, d, l = mapping
      #print(start, length, source, self.destinations[i], self.lengths[i], mapping)
      mapped_range.append((d, l))
      source_range.append((s, l))

    source_range.sort()
    c_start = start
    for (s, l) in source_range:
      if c_start < s:
        mapped_range.append((c_start, s - c_start))
      c_start = s + l
    if c_start < start + length:
      mapped_range.append((c_start, start + length - c_start))
    return sorted(mapped_range)


def build_maps(content: List[str]) -> List[Mapper]:
  maps = []
  parsed = re.findall(r"([a-z]+-to-[a-z]+)\ map:\n(([0-9\ ]+\n?)+\n?)", "\n".join(content[1:]))
  for p in parsed:
    mapper = Mapper()
    for d, s, l in list(map(lambda x: tuple(map(int, x.split())), p[1].strip().splitlines())):
      mapper.add_range(s, d, l)
    maps.append(mapper)
  return maps

# Part 1:
def part1(seeds, maps) -> int:
  loc = []
  for seed in seeds:
    x = seed
    for range_map in maps:
      x = range_map.map_int(x)
    loc.append(x)
  return min(loc)

# Part 2:
def part2(seeds, maps) -> int:
  for ranges in maps:
    next_seeds = []
    for start, length in seeds:
      next_seeds.extend(ranges.map_range(start, length))
    seeds = next_seeds
  next_seeds.sort()
  return next_seeds[0][0]

def get_input():
  with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
    content: List[str] = [s.strip() for s in f.read().rstrip().split('\n')]
  return content

@profiler
def solve():
  content: List[str] = get_input()
  maps: List[Mapper] = build_maps(content)
  seeds: List[int] = [int(s) for s in re.findall(r'\d+', content[0])]
  seeds2: List[Tuple[int, int]] = [(s, l) for s, l in [seeds[i:i+2] for i in range(0, len(seeds), 2)]]
  print("Part 1:", part1(seeds, maps))
  print("Part 2:", part2(seeds2, maps))

if __name__ == "__main__":
  solve()
