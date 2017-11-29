
import json

import glob

for name in glob.glob('user_works/*.json'):
  obj = json.loads(open(name).read() )
  print( obj )
