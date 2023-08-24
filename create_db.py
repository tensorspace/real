#!/usr/bin/python

import sqlite3

import db_config

conn = sqlite3.connect(db_config.DATABASE_NAME)
c = conn.cursor()
# Create the table
sql_query = f'''CREATE TABLE IF NOT EXISTS {db_config.TABLE_NAME}
       (
       {db_config.ADDRESS_COL}           TEXT    PRIMARY KEY ,
       {db_config.DESCRIPTION_COL}       TEXT
       );'''
c.execute(sql_query)
conn.commit()
# Insert sample data
data = ['''\'123 Main Street', 'A 3-bedroom house, the price is 568,000 dollars\'''',
        '''\'456 Broad Way', 'A 4-bedroom townhouse, the price is 1,568,000 dollars\'''',
        '''\'789 Newton Court', 'A 2-bedroom apartment, the price is 68,000 dollars\'''']

for row in data:
    try:
        sql_query = f"INSERT INTO {db_config.TABLE_NAME} ({db_config.ADDRESS_COL}, {db_config.DESCRIPTION_COL} ) \
            VALUES ({row})"
        c.execute(sql_query)
        conn.commit()
    except:
        pass

conn.close()
