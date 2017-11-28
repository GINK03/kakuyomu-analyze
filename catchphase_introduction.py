import os

import sys

import glob

import bs4

import gzip

import pickle

import re

import json

for name in glob.glob('htmls/*'):
  save_name = 'finished/{}.finishe.catchphrase'.format(name.split('/').pop())[:128]
  if os.path.exists(save_name) is True:
    print('already process', name)
    continue
  
  open(save_name,'a')
  html, link = pickle.loads( gzip.decompress( open(name,'rb').read() ) )
  soup = bs4.BeautifulSoup(html)

  intro = soup.find('p', {'id':'introduction'})
  catch = soup.find('p', {'id':'catchphrase'})

  if intro is None or catch is None:
    continue

  title = soup.find('title')
  title = title.text.replace(' - カクヨム', '')
  intro = re.sub(r'\s{1,}', ' ', intro.text)
  catch = max(catch.text.split('\n'), key=lambda x:len(x))
  meta = {}
  meta['title'] = title
  meta['catch'] = catch
  meta['intro'] = intro

  open('catchphrase_introduction/{}.json'.format(title.replace('/', '_')), 'w').write( json.dumps(meta, indent=2, ensure_ascii=False)[:128] )
  print('finished', name)
