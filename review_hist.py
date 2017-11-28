import json


import glob

star_hist = {}
for name in glob.glob('reviews/*.json'):
  obj = json.loads( open(name).read() )
  star = obj['star']
  if star_hist.get(star) is None:
    star_hist[star] = 0
  star_hist[star] += 1

for star, hist in star_hist.items():
  print(star, hist)

  
