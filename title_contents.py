import json

import pickle

import gzip

import glob

import re

import bs4

import sys

import json

import os
if '--step1' in sys.argv:
  for name in glob.glob('htmls/*'):

    # parse title <-> hashid
    if re.search('works_\d{1,}.pkl.gz$', name) is not None:
      try:
        html, links = pickle.loads( gzip.decompress( open(name, 'rb').read() ) )
      except:
        continue
      
      soup = bs4.BeautifulSoup(html)
      
      title = soup.find('h1', {'id':'workTitle'})
      
      if title is None: 
        continue
      
      title = title.text

      hashid = re.search('works_(\d{1,}).pkl.gz$', name).group(1)
      s1 = { 'title':title, 'hashid':hashid } 
      print(name, s1)
      open('hashid_title/{}.json'.format(hashid), 'w').write( json.dumps(s1, indent=2) )

if '--step2' in sys.argv:
  # parse hashid <-> contents
  def _map2(arr):
    index, names = arr
    for name in names:
      try:
        html, links = pickle.loads( gzip.decompress( open(name, 'rb').read() ) )
      except:
        continue
      soup = bs4.BeautifulSoup(html)
      try:
        contents = soup.find('div', {'class':'widget-episode'})
        episode_title = soup.find('p', {'class':'widget-episodeTitle'})

        hashid = re.search('works_(\d{1,})_episodes_\d{1,}.pkl.gz$', name).group(1)
        if os.path.exists('hashid_title/{}.json'.format(hashid)) is not True:
          continue
        obj = json.loads( open('hashid_title/{}.json'.format(hashid)).read() )
        episode_title = episode_title.text.strip()
        contents = re.sub(r'\s{1,}', ' ', contents.text)
        print( episode_title )
        obj[episode_title] = contents
        open('hashid_title/{}.json'.format(hashid), 'w').write( json.dumps(obj, indent=2, ensure_ascii=False) )
      except Exception as ex:
        continue
  
  arrs = {}
  for index, name in enumerate(glob.glob('htmls/*')):
    if re.search('works_\d{1,}_episodes_\d{1,}.pkl.gz$', name) is not None:
      key = index%4
      if arrs.get(key) is None:
        arrs[key] = []
      arrs[key].append( name )
  arrs = [ (key, names) for key, names in arrs.items() ]

  import concurrent.futures 
  with concurrent.futures.ProcessPoolExecutor(max_workers=4) as exe:
    exe.map(_map2, arrs)
