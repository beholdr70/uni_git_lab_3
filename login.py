import sqlite3
from ast import literal_eval

# Importing text used in sequences of this file
with open('dependencies/RU_loc.txt', encoding='utf-8') as loc_file:
    loc_dict = literal_eval('{' + loc_file.read() + '}')
    login_text = loc_dict['login_text']
    login_fail_text = loc_dict['login_fail_text']
    loc_file.close()

# Logging in if not first time
def login_func(cur: sqlite3.Cursor):
    message_text = login_text
    logged_in = False
    while not logged_in:
        if check_if_correct(cur, input(message_text)):
            logged_in = True
        else:
            message_text = login_fail_text

def check_if_correct(cur: sqlite3.Cursor, users_input: str):
    master_pass = cur.execute('SELECT pass_instance FROM master_pass').fetchone()[0]
    if master_pass == users_input:
        return True
    else:
        return False