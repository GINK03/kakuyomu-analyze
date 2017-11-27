import json

import glob


stars_freq = {}
for name in glob.glob('stars-parsist/*.json'):
  obj = json.loads(open(name).read() )
  stars =  int( obj['stars'] )
  stars = stars//10

  if stars_freq.get(stars) is None:
    stars_freq[stars] = 0
  stars_freq[stars] += 1

for stars, freq in sorted(stars_freq.items(), key=lambda x:x[0]):
  print(stars*10, freq)
