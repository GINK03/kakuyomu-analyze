import json

import glob

genre_hist = {}

genre_stars = {}
for name in glob.glob('stars-parsist/*.json'):
  obj = json.loads( open(name).read() )
  tags = obj['tags']
  stars = float(obj['stars'])
  for tag in tags:
    if genre_hist.get(tag) is None:
      genre_hist[tag] = 0
    genre_hist[tag] += 1

    if genre_stars.get(tag) is None:
      genre_stars[tag] = []
    genre_stars[tag].append( stars )

import statistics

genre_mean = {}
for genre, stars in genre_stars.items():
  if len(stars) > 50:
    genre_mean[genre] = statistics.mean(stars)

for genre, mean in sorted(genre_mean.items(), key=lambda x:x[1]*-1):
  print(genre, mean)
#for genre, hist in sorted(genre_hist.items(), key=lambda x:x[1]*-1):
#  print( genre, hist )


