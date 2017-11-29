
import json

import glob

import pickle

import sys

if '--invert1' in sys.argv:
  book_users = {}
  for name in glob.glob('user_works/*.json'):
    obj = json.loads(open(name).read() )
    user = obj['user']
    books = obj['works']

    for book in books:
      book = book.strip()
      if book_users.get(book) is None:
        book_users[book] = set()
      book_users[book].add(user)
  open('book_users.pkl', 'wb').write( pickle.dumps(book_users) )

if '--relevancy' in sys.argv:
  book_users = pickle.loads( open('book_users.pkl', 'rb').read() )

  for book, users in book_users.items():
    _book_scores = {}
    for _book, _users in book_users.items():
      _book_scores[_book] = len(users & _users)
    
    _book_scores = dict( [ (_book, _score) for _book, _score in sorted(_book_scores.items(), key=lambda x:x[1]*-1)[:20] if _score != 0.0 ] )
    # normalize
    vmax = max(_book_scores.values())
    
    _book_scores = { _book:_score/vmax for _book, _score in _book_scores.items() }
    book_book_score = {'book':book, 'vmax':vmax, 'book_scores':_book_scores}
    print(book_book_score)

