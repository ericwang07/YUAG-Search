DROP TABLE IF EXISTS books;

CREATE TABLE books
(isbn TEXT, title TEXT, quantity INTEGER);

INSERT INTO books (isbn, title, quantity)
   VALUES ('123','The Practice of Programming',500);
INSERT INTO books (isbn, title, quantity)
   VALUES ('234','The C Programming Language',800);
INSERT INTO books (isbn, title, quantity)
   VALUES ('345','Algorithms in C',650);

-- ---------------------------------------------------------------------

DROP TABLE IF EXISTS authors;

CREATE TABLE authors
(isbn TEXT, author TEXT);

INSERT INTO authors (isbn, author)
   VALUES ('123','Kernighan');
INSERT INTO authors (isbn, author)
   VALUES ('123','Pike');
INSERT INTO authors (isbn, author)
   VALUES ('234','Kernighan');
INSERT INTO authors (isbn, author)
   VALUES ('234','Ritchie');
INSERT INTO authors (isbn, author)
   VALUES ('345','Sedgewick');

-- ---------------------------------------------------------------------

DROP TABLE IF EXISTS customers;

CREATE TABLE customers
(custid TEXT, custname TEXT,
 street TEXT, zipcode TEXT);

INSERT INTO customers (custid, custname, street, zipcode)
   VALUES ('111','Princeton', '114 Nassau St', '08540');
INSERT INTO customers (custid, custname, street, zipcode)
   VALUES ('222','Harvard', '1256 Mass Ave', '02138');
INSERT INTO customers (custid, custname, street, zipcode)
   VALUES ('333','MIT', '292 Main St', '02142');

-- ---------------------------------------------------------------------

DROP TABLE IF EXISTS zipcodes;

CREATE TABLE zipcodes
(zipcode TEXT, city TEXT, state TEXT);

INSERT INTO zipcodes (zipcode, city, state)
   VALUES ('08540','Princeton', 'NJ');
INSERT INTO zipcodes (zipcode, city, state)
   VALUES ('02138','Cambridge', 'MA');
INSERT INTO zipcodes (zipcode, city, state)
   VALUES ('02142','Cambridge', 'MA');

-- ---------------------------------------------------------------------

DROP TABLE IF EXISTS orders;

CREATE TABLE orders
(isbn TEXT, custid TEXT, quantity INTEGER);

INSERT INTO orders (isbn, custid, quantity)
   VALUES ('123','222',20);
INSERT INTO orders (isbn, custid, quantity)
   VALUES ('345','222',100);
INSERT INTO orders (isbn, custid, quantity)
   VALUES ('123','111',30);
