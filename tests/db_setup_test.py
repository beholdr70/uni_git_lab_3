import sqlite3
import os
from unittest import TestCase
from db_setup import setup_master_pass, db_setup_func, fix_db


class DbSetupTest(TestCase):
    def test_db_setup_dir_check(self):
        with self.assertRaises(ValueError) as err:
            db_setup_func('directory/Somefile.db')
        self.assertEqual('Could not find given directory', err.exception.args[0])
        with self.assertRaises(ValueError) as err:
            db_setup_func('directory/Somefile')
        self.assertEqual('Given argument is not a path to a database file', err.exception.args[0])

    def test_check_if_exists(self):
        directory = 'tests/test_dependencies/testPDB2.db'
        if os.path.isfile(directory):
            os.remove(directory)
        db_setup_func(directory, test_mode=True)
        self.assertTrue(os.path.isfile(directory))
        db = sqlite3.connect(directory)
        cur = db.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [sub_set[0] for sub_set in cur.fetchall()]
        self.assertTrue('master_pass' in tables and 'general_pass' in tables)
        db.close()
        os.remove(directory)

    def test_setup_master_pass_wrong_pass(self):
        db = sqlite3.connect('tests/test_dependencies/TestPassDB.db')
        cur = db.cursor()
        with self.assertRaises(ValueError) as err:
            setup_master_pass(cur, master_pass_arg='ghl12')
        self.assertEqual('Given password does not meet the requirements', err.exception.args[0])
        db.close()

    def test_setup_master_pass(self):
        db = sqlite3.connect('tests/test_dependencies/TestPassDB.db')
        password = 'm0123456789'
        cur = db.cursor()
        setup_master_pass(cur, master_pass_arg=password)
        db.commit()
        pass_in_db = [item[0] for item in cur.execute('SELECT * FROM master_pass').fetchall()][-1]
        self.assertEqual(pass_in_db, password)
        cur.execute('DELETE FROM master_pass WHERE pass_instance = ?', (password,))
        db.commit()
        db.close()