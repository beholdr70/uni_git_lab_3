import sqlite3
import os
from db_setup import db_setup_func, fix_db
from login import login_func

# Running the project
if __name__ == '__main__':
    # Check for database with login/password data
    if not os.path.isfile('dependencies/passDB.db'):
        # Initiate setup sequence if not found
        db_setup_func()
        first_time = True
    else:
        first_time = False

    # Connecting database and setting up cursor
    db = sqlite3.connect('dependencies/passDB.db')
    cur = db.cursor()

    # Checking db if any required tables are missing
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [sub_set[0] for sub_set in cur.fetchall()]
    if not all(table in tables for table in ('master_pass', 'general_pass')):
        fix_db(db, cur, tables)

    # Running log in sequence if not first time user
    if not first_time:
        login_func(cur)

    db.close()
