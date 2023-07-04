#!/usr/bin/env python

# -----------------------------------------------------------------------
# display.py
# Author: Bob Dondero
# -----------------------------------------------------------------------

from sys import argv, stderr, exit
from sqlite3 import connect as sqlite_connect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Books, Authors, Customers, Zipcodes, Orders

# -----------------------------------------------------------------------

DATABASE_NAME = 'bookstore.sqlite'


def main():

    if len(argv) != 1:
        print('Usage: python display.py', file=stderr)
        exit(1)

    try:
        engine = create_engine('sqlite://',
                               creator=lambda: sqlite_connect(
                                   'file:' + DATABASE_NAME + '?mode=ro', uri=True))

        Session = sessionmaker(bind=engine)
        session = Session()

        print('-------------------------------------------')
        print('books')
        print('-------------------------------------------')
        for book in session.query(Books).all():
            print(book.isbn, book.title, book.quantity,
                  [a.author for a in book.authors])

        print('-------------------------------------------')
        print('authors')
        print('-------------------------------------------')
        for author in session.query(Authors).all():
            print(author.book.title, author.author)

        print('-------------------------------------------')
        print('customers')
        print('-------------------------------------------')
        for customer in session.query(Customers).all():
            print(customer.custid, customer.custname, customer.street,
                  customer.zipcode)

        print('-------------------------------------------')
        print('zipcodes')
        print('-------------------------------------------')
        for zipcode in session.query(Zipcodes).all():
            print(zipcode.zipcode, zipcode.city, zipcode.state)

        print('-------------------------------------------')
        print('orders')
        print('-------------------------------------------')
        for order in session.query(Orders).all():
            print(order.isbn, order.custid, order.quantity)

        session.close()
        engine.dispose()

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

# -----------------------------------------------------------------------


if __name__ == '__main__':
    main()
