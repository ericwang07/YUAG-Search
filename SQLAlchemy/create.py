#!/usr/bin/env python

# -----------------------------------------------------------------------
# create.py
# Author: Bob Dondero
# -----------------------------------------------------------------------

from sys import argv, stderr, exit
from sqlite3 import connect as sqlite_connect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, Books, Authors, Customers, Zipcodes, Orders

# -----------------------------------------------------------------------

DATABASE_NAME = 'bookstore.sqlite'


def main():

    if len(argv) != 1:
        print('Usage: python create.py', file=stderr)
        exit(1)

    try:
        engine = create_engine('sqlite://',
                               creator=lambda: sqlite_connect(
                                   'file:' + DATABASE_NAME + '?mode=rwc', uri=True))

        Session = sessionmaker(bind=engine)
        session = Session()

        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        # ---------------------------------------------------------------

        book = Books(isbn=123, title='The Practice of Programming',
                     quantity=500)
        session.add(book)
        book = Books(isbn=234, title='The C Programming Language',
                     quantity=800)
        session.add(book)
        book = Books(isbn=345, title='Algorithms in C',
                     quantity=650)
        session.add(book)
        session.commit()

        # ---------------------------------------------------------------

        author = Authors(isbn=123, author='Kernighan')
        session.add(author)
        author = Authors(isbn=123, author='Pike')
        session.add(author)
        author = Authors(isbn=234, author='Kernighan')
        session.add(author)
        author = Authors(isbn=234, author='Ritchie')
        session.add(author)
        author = Authors(isbn=345, author='Sedgewick')
        session.add(author)
        session.commit()

        # ---------------------------------------------------------------

        customer = Customers(custid='111', custname='Princeton',
                             street='114 Nassau St', zipcode='08540')
        session.add(customer)
        customer = Customers(custid='222', custname='Harvard',
                             street='1256 Mass Ave', zipcode='02138')
        session.add(customer)
        customer = Customers(custid='333', custname='MIT',
                             street='292 Main St', zipcode='02142')
        session.add(customer)
        session.commit()

        # ---------------------------------------------------------------

        zipcode = Zipcodes(zipcode='08540', city='Princeton',
                           state='NJ')
        session.add(zipcode)
        zipcode = Zipcodes(zipcode='02138', city='Cambridge',
                           state='MA')
        session.add(zipcode)
        zipcode = Zipcodes(zipcode='02142', city='Cambridge',
                           state='MA')
        session.add(zipcode)
        session.commit()

        # ---------------------------------------------------------------

        order = Orders(isbn='123', custid='222', quantity=20)
        session.add(order)
        order = Orders(isbn='345', custid='222', quantity=100)
        session.add(order)
        order = Orders(isbn='123', custid='111', quantity=30)
        session.add(order)
        session.commit()

        session.close()
        engine.dispose()

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

# -----------------------------------------------------------------------


if __name__ == '__main__':
    main()
