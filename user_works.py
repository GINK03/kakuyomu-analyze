import glob

import gzip

import pickle

import re

import bs4

import json

from multiprocessing import Process

import os

import sys
def _map(arr):
  key, names = arr
  for name in names:
    html, links = pickle.loads( gzip.decompress( open(name, 'rb').read() ))
    soup = bs4.BeautifulSoup(html)
    
    user = soup.find('p', {'id': 'user-name-userId'})
    if user is None:
      continue
    user = user.text

    if os.path.exists(f'user_works/{user}.json') is True:
      continue
    works = []
    for h4 in soup.find_all('h4', {'class':'widget-workCatchphrase-title'}):
      works.append( re.sub(r'\s{1,}', ' ', h4.text)  )

    print(name)
    print('index', key, 'finished', user)
    open(f'user_works/{user}.json', 'w').write( json.dumps({'user':user, 'works':works}, indent=2, ensure_ascii=False) )

if '--init' in sys.argv:
  arrs = {}
  for index, name in enumerate(glob.glob('htmls/*')):
    if re.search(r'following_works.pkl.gz$', name) is None:
      continue
    key = index%16
    if arrs.get(key) is None:
      arrs[key] = []
    arrs[key].append( name )
  arrs = [(key, names) for key, names in arrs.items() ]
  open('user_books_arrs.json', 'w').write( json.dumps(arrs, indent=2) )
  sys.exit()

arrs = json.loads(open('user_books_arrs.json').read() )
#_map(arrs[0])
ps = []
for arr in arrs:
  p = Process(target=_map, args=(arr,))
  p.start()
  ps.append(p)
[p.join() for p in ps]
  
