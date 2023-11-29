from time import perf_counter

def profiler(method):
  def profiler_method(*arg, **kw):
    t = perf_counter()
    ret = method(*arg, **kw)
    print(f'{method.__name__} method took : {perf_counter()-t:.4f} sec')
    return ret
  return profiler_method

@profiler
def timeall():
  times = {}
  for i in range(25):
    name = f'day{i+1:02d}.day{i+1:02d}'
    try:
      day = __import__(name, fromlist=[''])
    except ModuleNotFoundError:
      continue

    t = perf_counter()
    day.solve()
    times[perf_counter()-t] = name
  if not times:
    return
  max_time = max(times.keys())
  print(times[max_time], f'{max_time:,.4f}', 'sec')

if __name__ == "__main__":
  timeall()