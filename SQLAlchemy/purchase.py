#!/usr/bin/env python

#-----------------------------------------------------------------------
# purchase.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

from sys import argv, stderr, exit
from sqlite3 import connect as sqlite_connect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Orders, Books

#-----------------------------------------------------------------------

DATABASE_NAME = 'bookstore.sqlite'

def main():

    if len(argv) != 3:
        print('Usage: python purchase.py isbn custid', file=stderr)
        exit(1)

    isbn = int(argv[1])
    custid = int(argv[2])

    try:
        engine = create_engine('sqlite://',
            creator=lambda: sqlite_connect(
                'file:' + DATABASE_NAME + '?mode=rw', uri=True))

        Session = sessionmaker(bind=engine)
        session = Session()

        order = (session.query(Orders)
            .filter(Orders.isbn == isbn)
            .filter(Orders.custid == custid)
            .one())
        order.quantity += 1

        book = (session.query(Books)
            .filter(Books.isbn == isbn)
            .one())
        book.quantity -= 1

        session.commit()
        print('Transaction committed.')

        session.close()
        engine.dispose()

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
