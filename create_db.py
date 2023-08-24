import logging
import sqlite3

import db_config

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Sample data
data = [
    ('123 Main Street', 'A 3-bedroom house, the price is 568,000 dollars'),
    ('456 Broad Way', 'A 4-bedroom townhouse, the price is 1,568,000 dollars'),
    ('789 Newton Court', 'A 2-bedroom apartment, the price is 68,000 dollars')
]

with sqlite3.connect(db_config.DATABASE_NAME) as conn:
    c = conn.cursor()

    # Create the table
    try:
        sql_query = f'''CREATE TABLE IF NOT EXISTS {db_config.TABLE_NAME}
                       (
                       {db_config.ADDRESS_COL} TEXT PRIMARY KEY,
                       {db_config.DESCRIPTION_COL} TEXT
                       );'''
        c.execute(sql_query)
    except sqlite3.DatabaseError as e:
        logger.error(f"Failed to create table: {e}")
        # If table creation failed, no point to proceed further
        raise

    # Insert data
    for address, description in data:
        try:
            sql_query = f'''INSERT INTO {db_config.TABLE_NAME} ({db_config.ADDRESS_COL}, {db_config.DESCRIPTION_COL})
                            VALUES (?, ?)'''
            c.execute(sql_query, (address, description))
        except sqlite3.IntegrityError:
            logger.warning(f"Duplicate entry for address: {address}")
        except sqlite3.DatabaseError as e:
            logger.error(f"Failed to insert data for address {address}: {e}")
