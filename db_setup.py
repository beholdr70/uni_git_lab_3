import sqlite3
import os
from ast import literal_eval
from string import ascii_letters

# Importing text used in sequences of this file
with open('dependencies/RU_loc.txt', encoding='utf-8') as loc_file:
    loc_dict = literal_eval('{' + loc_file.read() + '}')
    first_time_user_text = loc_dict['first_time_user_text']
    try_again_text = loc_dict['try_again_text']
    master_pass_recovery_text = loc_dict['master_pass_recovery_text']
    loc_file.close()


def setup_master_pass(cur: sqlite3.Cursor, recovery=False, master_pass_arg=''):
    # Choosing initial text according to usage case
    initial_text = first_time_user_text
    if recovery:
        initial_text = master_pass_recovery_text

    # Asking user for master-password and inserting it into relating table
    master_pass = input(initial_text) if not master_pass_arg else master_pass_arg
    while len(master_pass) < 10 or not any(letter.isdigit() for letter in master_pass) or not all(
            letter in ascii_letters if letter.isalpha() else True for letter in master_pass) or not any(
        letter.isalpha() for letter in master_pass):
        if master_pass_arg:
            raise ValueError('Given password does not meet the requirements')
        master_pass = input(try_again_text)
    cur.execute(f'INSERT INTO master_pass (pass_instance) VALUES (?)', (master_pass,))


# Creating database for password if one wasn't found
def db_setup_func(directory: str, test_mode=False):

    if not directory[-3:] == '.db':
        raise ValueError('Given argument is not a path to a database file')
    elif not os.path.isdir(directory.replace(directory.split('/')[-1], '')):
        raise ValueError('Could not find given directory')

    # Creating database file
    db = sqlite3.connect(directory)
    cur = db.cursor()

    # Creating required tables in connected database
    cur.execute('CREATE TABLE master_pass(pass_instance TEXT)')
    cur.execute('CREATE TABLE general_pass(id INTEGER PRIMARY KEY, login_instance TEXT, pass_instance TEXT)')

    # Setting up master password
    if not test_mode:
        setup_master_pass(cur)

    # Commiting changes into database
    db.commit()

    db.close()


# Creating required tables in database if they're missing
def fix_db(db: sqlite3.Connection, cur: sqlite3.Cursor, existing_table: list):
    # Creating missing tables in connected database
    cur.execute('CREATE TABLE IF NOT EXISTS master_pass(pass_instance TEXT)')
    cur.execute(
        'CREATE TABLE IF NOT EXISTS general_pass(id INTEGER PRIMARY KEY, login_instance TEXT, pass_instance TEXT)')

    # Setting up new master password if master_pass table was corrupted
    if 'master_pass' not in existing_table:
        setup_master_pass(cur, recovery=True)

    # Commiting changes into database
    db.commit()
