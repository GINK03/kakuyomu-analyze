import glob

import json

import MeCab

import sys

import json

import math
if '--idf' in sys.argv:
  term_freq = {}
  c = 0
  m = MeCab.Tagger('-Owakati')
  for name in glob.glob('./hashid_title/*'):
    try:
      o = json.loads( open(name).read() )
    except:
      continue
    c += 1 
    title = o['title']
    print(title)

    doc = ' '.join( o.values())
    # max threthold is 100000 chars
    wakati = m.parse(doc[:100000])
    if wakati is None:
      continue
    for term in set(wakati.split()):
      if  term_freq.get(term) is None:
        term_freq[term] = 0
      term_freq[term] += 1
  
  idf = {}
  for term, freq in term_freq.items():
    idf[term] = math.log(c/freq)

  open('idf.json', 'w').write(json.dumps( idf, indent=2, ensure_ascii=False) )
