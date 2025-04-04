import sqlite3
import os
from db_setup import db_setup_func, fix_db

# Run the project
if __name__ == '__main__':
    # Check for database with login/password data
    if os.path.isfile('dependencies/passDB.db'):

        # Connecting database and setting up cursor
        db = sqlite3.connect('dependencies/passDB.db')
        cur = db.cursor()

        # Checking db if any required tables are missing
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [sub_set[0] for sub_set in cur.fetchall()]
        if not all(table in tables for table in ('master_pass', 'general_pass')):
            fix_db(tables)
    else:
        # Initiate setup sequence if not found
        db_setup_func()
