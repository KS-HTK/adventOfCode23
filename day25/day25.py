# -*- coding: utf-8 -*-

import os
from time import perf_counter
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations
from typing import List, Dict, Tuple

def profiler(method):
  def profiler_method(*arg, **kw):
    t = perf_counter()
    ret = method(*arg, **kw)
    print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
    return ret
  return profiler_method

def parse(content):
  content = [l.split(' ') for l in content]
  nodelist = {s[0][:-1]:s[1:] for s in content}

  G = nx.Graph()
  for k, v in nodelist.items():
    for vv in v:
      G.add_edge(k, vv)
  return G

# Part 1:
def part1(graph) -> int:
  """ Not the most elegant solution, but it works. Just note down the observations in cut_edges"""
  #nx.draw(graph, with_labels=True)
  #plt.show()
  cut_edges = [('xqh', 'ssd'), ('khn', 'nrs'), ('qlc', 'mqb')]
  dc_graph = graph.copy()
  dc_graph.remove_edges_from(cut_edges)
  a, b = [len(sg) for sg in nx.connected_components(dc_graph)]
  return a*b

def get_input():
  with open(os.path.dirname(os.path.realpath(__file__))+'/input', 'r', encoding='utf-8') as f:
    content = [s.strip() for s in f.read().rstrip().split('\n')]
  return content

@profiler
def solve():
  graph = parse(get_input())
  print(f'Part 1: {part1(graph)}')

if __name__ == "__main__":
  solve()
