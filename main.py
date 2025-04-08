import sqlite3
import os
from db_setup import db_setup_func, fix_db
from login import login_func
from db_handle_data import display_data, write_new_data
from pass_generator import generate_pass
from ast import literal_eval

# Importing text used in sequences of this file
with open('dependencies/RU_loc.txt', encoding='utf-8') as loc_file:
    loc_dict = literal_eval('{' + loc_file.read() + '}')
    action_choice_text = loc_dict['action_choice_text']
    loc_file.close()

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

    run = True

    while run:
        action = input(action_choice_text)
        if action == 'Добавить логин и пароль':
            write_new_data(db, cur)
        elif action == 'Вывести сохранённые логины и пароли':
            display_data(db, cur)
        elif action == 'Сгенерировать пароль':
            generate_pass()
        elif action == 'Выйти':
            run = False

    db.close()
