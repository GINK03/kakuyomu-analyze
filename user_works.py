import glob

import gzip

import pickle

import re

import bs4

import json

from multiprocessing import Process

def _map(name):
  print(name)

  html, links = pickle.loads( gzip.decompress( open(name, 'rb').read() ))
  soup = bs4.BeautifulSoup(html)
  
  user = soup.find('p', {'id': 'user-name-userId'})
  if user is None:
    return
  user = user.text

  works = []
  for h4 in soup.find_all('h4'):
    works.append( re.sub(r'\s{1,}', ' ', h4.text)  )

  print('finished', user)
  open(f'user_works/{user}.json', 'w').write( json.dumps({'books':works}, indent=2, ensure_ascii=False) )

ps = []
for name in glob.glob('htmls/*'):
  if re.search(r'following_works.pkl.gz$', name) is None:
    continue
  p = Process(target=_map, args=(name,))
  p.start()
  ps.append(p)
  if len(ps) > 16:
    [p.join() for p in ps]
    ps = []
  
