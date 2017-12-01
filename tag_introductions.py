import re

import glob

import pickle

import gzip

import bs4

import json

import concurrent.futures 

def _map1(name):
  try:
    html, links = pickle.loads( gzip.decompress( open(name, 'rb').read() ) )
  except Exception as ex:
    return
  
  soup = bs4.BeautifulSoup(html)

  h1 = soup.find('h1', {'id':'workTitle'})

  intro = soup.find('p', {'id':'introduction'})
  li = soup.find('ul', {'id':'workMeta-tags'})
  if intro is None or li is None or h1 is None:
    return
  title = h1.text.strip()
  tags =  [l.text.strip() for l in li.find_all('a') ] 
  intro = intro.text 

  obj = json.dumps( {'title':title, 'tags':tags, 'intro':intro}, indent=2, ensure_ascii=False) 
  print( obj )
  open('tag_introduction/{}.json'.format(title.replace('/','_')), 'w').write( obj )

names = []
for name in glob.glob('htmls/*'):
  if re.search(r'works_\d{1,}.pkl.gz$', name) is None:
    continue
  names.append(name)

with concurrent.futures.ProcessPoolExecutor(max_workers=8) as exe:
  exe.map(_map1, names)
