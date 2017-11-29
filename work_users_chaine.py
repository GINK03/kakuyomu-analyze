
import json

import glob

book_users = {}
for name in glob.glob('user_works/*.json'):
  obj = json.loads(open(name).read() )
  user = obj['user']
  books = obj['works']

  for book in books:
    if book_users.get(book) is None:
      book_users[book] = []
    book_users[book].append(user)

for book, users in book_users.items():
  print(book, users)
