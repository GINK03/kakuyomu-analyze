import glob

import json

size_hist = {}
for name in glob.glob('user_works/*.json'):
  obj = json.loads(open(name).read())
  size = len(obj['user'])//2
  if size_hist.get(size) is None:
    size_hist[size] = 0
  size_hist[size] += 1

for size, hist in sorted(size_hist.items()):
  print(size, hist)
