import bs4

import glob

import pickle

import gzip

import sys

import re

import json

import os

import concurrent.futures
if '--contents' in sys.argv:
  for name in glob.glob('htmls/*'):
    html, links = pickle.loads( gzip.decompress(open(name,'rb').read()) )
    soup = bs4.BeautifulSoup(html)

    content = soup.find('div', {'class':'widget-episode'} )
    if content is None:
      continue

    episode_title = soup.find('p', {'class':'widget-episodeTitle'})
    span = soup.find('span', {'class':'js-toggle-cheers-button-cheer-count'})
    print( episode_title.text )
    print( span.text )
    #print( content.text )

if '--reviews' in sys.argv:
  def _map1(names):
    try:
      for name in names:
        if re.search(r'reviews.pkl.gz$', name) is None:
          continue
        print(name)
        html, links = pickle.loads( gzip.decompress(open(name,'rb').read()) ) 
        soup = bs4.BeautifulSoup(html)
        work_title = soup.find('title').text.replace('のおすすめレビュー - カクヨム', '')
        for index, art in enumerate(soup.find_all('article', {'class':'widget-workReview-review'})):
          #print(art)
          star = art.find('span').text
          title = art.find('span', {'class':'widget-workReview-reviewTitleLabel'}).text
          body = art.find('p', {'class':'widget-workReview-reviewBody'}).text
          print('title', work_title)
          print('star', star)
          print('title', title)
          print('body', body)
          meta = {}
          meta['star'] = star
          meta['title'] = title
          meta['body'] = re.sub(r'\s{1,}', ' ', body.replace('\n', ''))
          open('./reviews/{}_{}.json'.format(work_title.replace('/', '_'), index), 'w').write( json.dumps(meta, indent=2, ensure_ascii=False) ) 
    except Exception as ex:
      print('Deep Exception', ex)

  arrs = {} 
  for index, name in enumerate(glob.glob('htmls/*')):
    key = index%4
    if arrs.get(key) is None:
      arrs[key] = []
    arrs[key].append(name)
  arrs = [ v for k,v in arrs.items() ]
  with concurrent.futures.ProcessPoolExecutor(max_workers=6) as exe:
    exe.map(_map1, arrs)
  #_map1(arrs[0])

if '--time_persist' in sys.argv:
  def _map1(arr):
    try:
      for name in arr:
        html, links = pickle.loads( gzip.decompress(open(name,'rb').read()) ) 
        soup = bs4.BeautifulSoup(html)
       
        title = soup.find('h1', {'id':'workTitle'})
        if title is None:
          continue
        if os.path.exists('stars-parsist/{}.json'.format(title.text)) is True:
          continue

        stars = soup.find('span', {'class':'js-total-review-point-element'})
        if stars is None:
          continue

        if soup.find('ul', {'id':'workMeta-tags'}) is None:
          continue
        tags = [li.text for li in soup.find('ul', {'id':'workMeta-tags'}).find_all('li') ]
        times = [re.split(r'[年|月|日]', time.text)[:-1] for time in soup.find_all('time', {'class':'widget-toc-episode-datePublished'}) ]
        #print(title.text, stars.text, tags , time.text)
        start_time = times[0]
        last_time = times[-1]
        syear = int(start_time[0])
        eyear = int(last_time[0])

        smonth = int(start_time[1])
        emonth = int(last_time[1])

        persist = -1*(syear*12+smonth) + (eyear*12+emonth)
        print( title.text, stars.text, persist, start_time, last_time )
        meta = {'title':title.text, 'stars':stars.text, 'persist':persist, 'start_time':start_time, 'last_time':last_time, 'tags':tags }
        open('stars-parsist/{}.json'.format(title.text.replace('/','_')), 'w').write( json.dumps(meta, indent=2, ensure_ascii=False) )
    except Exception as ex:
      print('Deep Exception', ex)
  arrs = {}
  for index, name in enumerate(glob.glob('htmls/*')):
    key = index%4
    if arrs.get(key) is None:
      arrs[key] = []
    arrs[key].append(name)
  #for k,v in arrs.items():
  #  print(k, v)
  arrs = [ v for k,v in arrs.items() ]
  #_map1(arrs[0])
  with concurrent.futures.ProcessPoolExecutor(max_workers=6) as exe:
    exe.map(_map1, arrs)
