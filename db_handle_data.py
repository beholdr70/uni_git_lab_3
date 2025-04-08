import sqlite3
from ast import literal_eval

# Importing text used in sequences of this file
with open('dependencies/RU_loc.txt', encoding='utf-8') as loc_file:
    loc_dict = literal_eval('{' + loc_file.read() + '}')
    first_time_user_text = loc_dict['first_time_user_text']
    try_again_text = loc_dict['try_again_text']
    master_pass_recovery_text = loc_dict['master_pass_recovery_text']
    loc_file.close()

# Writing new user's data into database
def write_new_data(db: sqlite3.Connection, cur: sqlite3.Cursor):
    # Getting data from user
    new_login = input()
    new_password = input()

    # Inserting new data into general_pass table
    cur.execute('INSERT INTO general_pass (login_instance, pass_instance) VALUES (?, ?)', (new_login, new_password))

    # Commiting changes into database
    db.commit()

# Outputting data from general_pass table in console
def display_data(db: sqlite3.Connection, cur: sqlite3.Cursor):
    print('№   Login     Password')
    for data_pack in cur.execute('SELECT * FROM general_pass').fetchall():
        print(f'{data_pack[0]}. {data_pack[1]} - {data_pack[2]}')
    valid_option = ['Удалить', 'Редактировать', 'Выйти']
    interation_type = input()
    while interation_type not in valid_option:
        interation_type = input()
    if interation_type == 'Выйти':
        return
    else:
        interation_data_id = input()
        while not interation_data_id.isnumeric():
            interation_data_id = input()
        if interation_type == 'Удалить':
            delete_data(db, cur, interation_data_id)
        elif interation_type == 'Редактировать':
            update_data(db, cur, interation_data_id)

# Deleting existing data from the general_pass table
def delete_data(db: sqlite3.Connection, cur: sqlite3.Cursor, id: str):
    cur.execute('DELETE FROM general_pass WHERE id = ?', (id, ))

    # Updating all ids bigger than passed id so they would correctly render during displaying
    cur.execute('UPDATE general_pass SET id = id - 1 WHERE id > ?', (id, ))

    # Commiting changes into database
    db.commit()

# Editing already existing data in database
def update_data(db: sqlite3.Connection, cur: sqlite3.Cursor, id: str):
    # Choosing what instance to edit
    valid_option = ['Логин', 'Пароль', 'Отмена']
    data_to_edit = input()

    # Repeating request until valid option is selected
    while data_to_edit not in valid_option:
        data_to_edit = input()

    if data_to_edit in ['Логин', 'Пароль']:
        data_to_edit = 'login_instance' if data_to_edit == 'Логин' else 'pass_instance'
        new_data = input()

        # Updating data in general_pass table
        cur.execute(f'UPDATE general_pass SET {data_to_edit} = ? WHERE id = ?', (new_data, id))

        # Commiting changes into database
        db.commit()
    else:
        return

if __name__ == '__main__':
    db = sqlite3.connect('dependencies/passDB.db')
    cur = db.cursor()
    display_data(db, cur)
    display_data(db, cur)
    db.close()