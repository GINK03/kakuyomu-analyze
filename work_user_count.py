import json

import sys

import glob

work_users = {}
for name in glob.glob('user_works/*.json'):
  user = name.split('/').pop().replace('.json', '')
  obj =  json.loads(open(name).read())

  works = obj['user']

  for work in works:
    if work_users.get(work) is None:
      work_users[work] = []
    work_users[work].append( user )

for work, users in sorted(work_users.items(), key=lambda x:len(x[1])*-1):
  print( work.replace(' ',''), len(users) )
