#!/usr/bin/python

import sqlite3

DATABASE_NAME = 'test.db'
TABLE_NAME = 'properties'
ADDRESS_COL = 'address'
DESCRIPTION_COL = 'description'

conn = sqlite3.connect(DATABASE_NAME)
c = conn.cursor()
# Create the table
sql_query = f'''CREATE TABLE IF NOT EXISTS {TABLE_NAME}
       (
       {ADDRESS_COL}           TEXT    PRIMARY KEY ,
       {DESCRIPTION_COL}       TEXT
       );'''
c.execute(sql_query)
conn.commit()
# Insert sample data
try:
    sql_query = f"INSERT INTO {TABLE_NAME} ({ADDRESS_COL}, {DESCRIPTION_COL} ) \
          VALUES ('123 Main Street', 'A 3-bedroom house, the price is 568,000 dollars')"
    c.execute()
    conn.commit()
except:
    pass

conn.close()
