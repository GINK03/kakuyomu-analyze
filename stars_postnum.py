
import glob

import json

post_stars = {}
for name in glob.glob('stars-parsist/*.json'):
  obj =  json.loads(open( name ).read() )
  stars = float( obj['stars'] )
  post = len(obj['times'])//5
  
  if post_stars.get(post) is None:
    post_stars[post] = []
  post_stars[post].append( stars ) 

import statistics
for post, stars in sorted( post_stars.items(), key=lambda x:x[0]):
  if len(stars) >= 50:
    print(post*5, statistics.mean(stars) )
