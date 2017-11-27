
import glob

import json

import os

persist_stars = {}
for name in glob.glob('stars-parsist/*.json'):
  obj =  json.loads(open(name).read() ) 
  stars = float(obj['stars'])
  persist = abs(obj['persist'])
  if persist_stars.get(persist) is None:
    persist_stars[persist] = []
  persist_stars[persist].append( stars )

import statistics

persist_mean = {}
for persist, stars in persist_stars.items():
  if len(stars) >= 15:
    print( persist, statistics.mean(stars) )
