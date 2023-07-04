#!/usr/bin/env python

#-----------------------------------------------------------------------
# recovery.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

from sys import argv, stderr, exit
from random import randrange
from sqlite3 import connect as sqlite_connect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Orders, Books

#-----------------------------------------------------------------------

DATABASE_NAME = 'bookstore.sqlite'

def main():

    if len(argv) != 1:
        print('Usage: python recovery.py', file=stderr)
        exit(1)

    try:

        engine = create_engine('sqlite://',
            creator=lambda: sqlite_connect(
                'file:' + DATABASE_NAME + '?mode=rw', uri=True))

        Session = sessionmaker(bind=engine)
        session = Session()

        for i in range(20):

            order = (session.query(Orders)
                .filter(Orders.isbn == '123')
                .filter(Orders.custid == '222')
                .one())
            order.quantity += 1

            # Simulate a HW/SW failure occurring randomly,
            # on average every 5th time through the loop.
            if randrange(5) == 0:
                print('Simulated failure with i = %d' % i)
                session.rollback()
                print('Transaction rolled back.')
                continue

            book = (session.query(Books)
                .filter(Books.isbn == '123')
                .one())
            book.quantity -= 1

            session.commit()
            print('Transaction %d committed.' % i)

        session.close()
        engine.dispose()

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
