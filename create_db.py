#!/usr/bin/python

import sqlite3
conn = sqlite3.connect('test.db')
c = conn.cursor()
# Create the table
c.execute('''CREATE TABLE IF NOT EXISTS properties
       (
       address           TEXT    PRIMARY KEY ,
       description       TEXT
       );''')
conn.commit()
# Insert sample data
c.execute("INSERT INTO properties (address, description) \
      VALUES ('123 Main Street', 'A 3-bedroom house, the price is 568,000 dollars')")
conn.commit()
conn.close()