import sqlite3
from ast import literal_eval

# Importing text used in sequences of this file
with open('dependencies/RU_loc.txt', encoding='utf-8') as loc_file:
    loc_dict = literal_eval('{' + loc_file.read() + '}')
    login_add_text = loc_dict['login_add_text']
    pass_add_text = loc_dict['pass_add_text']
    display_interaction_text = loc_dict['display_interaction_text']
    display_interaction_fail_text = loc_dict['display_interaction_fail_text']
    id_select_text = loc_dict['id_select_text']
    id_select_fail_text = loc_dict['id_select_fail_text']
    update_instance_text = loc_dict['update_instance_text']
    update_instance_fail_text = loc_dict['update_instance_fail_text']
    data_update_text = loc_dict['data_update_text']
    loc_file.close()

# Writing new user's data into database
def write_new_data(db: sqlite3.Connection, cur: sqlite3.Cursor):
    # Getting data from user
    new_login = input(login_add_text)
    new_password = input(pass_add_text)

    # Inserting new data into general_pass table
    cur.execute('INSERT INTO general_pass (login_instance, pass_instance) VALUES (?, ?)', (new_login, new_password))

    # Commiting changes into database
    db.commit()

# Outputting data from general_pass table in console
def display_data(db: sqlite3.Connection, cur: sqlite3.Cursor):
    # Outputting user's logins and password
    print('№   Login     Password')
    for data_pack in cur.execute('SELECT * FROM general_pass').fetchall():
        print(f'{data_pack[0]}. {data_pack[1]} - {data_pack[2]}')

    # Asking user for action
    interation_type = input(display_interaction_text)
    valid_option = ['Удалить', 'Редактировать', 'Выйти']
    while interation_type not in valid_option:
        interation_type = input(display_interaction_fail_text)

    # Actions handler
    if interation_type == 'Выйти':
        return
    else:
        interation_data_id = input(id_select_text)
        while interation_data_id not in [str(item[0]) for item in cur.execute('SELECT id FROM general_pass').fetchall()]:
            interation_data_id = input(id_select_fail_text)
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
    data_to_edit = input(update_instance_text)

    # Repeating request until valid option is selected
    while data_to_edit not in valid_option:
        data_to_edit = input(update_instance_fail_text)

    if data_to_edit in ['Логин', 'Пароль']:
        data_to_edit = 'login_instance' if data_to_edit == 'Логин' else 'pass_instance'
        new_data = input(data_update_text)

        # Updating data in general_pass table
        cur.execute(f'UPDATE general_pass SET {data_to_edit} = ? WHERE id = ?', (new_data, id))

        # Commiting changes into database
        db.commit()
    else:
        return