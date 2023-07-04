#!/usr/bin/env python

#-----------------------------------------------------------------------
# authorsearch.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

from sys import argv, stderr, exit
from sqlite3 import connect as sqlite_connect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Books, Authors

#-----------------------------------------------------------------------

DATABASE_NAME = 'bookstore.sqlite'

def main():

    if len(argv) != 2:
        print('Usage: python authorsearch.py author', file=stderr)
        exit(1)

    author = argv[1]

    try:
        engine = create_engine('sqlite://',
            creator=lambda: sqlite_connect(
                'file:' + DATABASE_NAME + '?mode=ro', uri=True))

        Session = sessionmaker(bind=engine)
        session = Session()

        book_author_pairs = (session.query(Books, Authors)
            .filter(Books.isbn == Authors.isbn)
            .filter(Authors.author == author)
            .all())

        for book_author_pair in book_author_pairs:
            book = book_author_pair[0]
            print('ISBN:', book.isbn)
            print('Title:', book.title)
            print('Quantity:', book.quantity)
            print()

        session.close()
        engine.dispose()

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
