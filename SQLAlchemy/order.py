#!/usr/bin/env python

# -----------------------------------------------------------------------
# order.py
# Author: Bob Dondero
# -----------------------------------------------------------------------

from sys import argv, stderr, exit
from sqlite3 import connect as sqlite_connect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Orders

# -----------------------------------------------------------------------

DATABASE_NAME = 'bookstore.sqlite'


def main():

    if len(argv) != 3:
        print('Usage: python order.py isbn custid', file=stderr)
        exit(1)

    isbn = argv[1]
    custid = argv[2]

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

        session.commit()

        session.close()
        engine.dispose()

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

# -----------------------------------------------------------------------


if __name__ == '__main__':
    main()
