from unittest import TestCase
from unittest.mock import patch, MagicMock
import sqlite3
from io import StringIO
import db_handle_data as db_module


class TestDatabaseFunctions(TestCase):

    def clear_data(self):
        db = sqlite3.connect('tests/test_dependencies/TestPassDB.db')
        cur = db.cursor()
        cur.execute('DELETE FROM general_pass')
        db.commit()
        db.close()

    def test_write_new_data(self):
        self.clear_data()
        db = sqlite3.connect('tests/test_dependencies/TestPassDB.db')
        cur = db.cursor()
        with patch('builtins.input', side_effect=['test_login', 'test_pass']):
            db_module.write_new_data(db, cur)
        result = cur.execute("SELECT * FROM general_pass").fetchall()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1:], ('test_login', 'test_pass'))
        db.close()

    def test_display_data_output(self):
        self.clear_data()
        db = sqlite3.connect('tests/test_dependencies/TestPassDB.db')
        cur = db.cursor()
        cur.executemany(
            'INSERT INTO general_pass VALUES (?, ?, ?)',
            [(1, 'login1', 'pass1'), (2, 'login2', 'pass2')]
        )
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('builtins.input', return_value='Выйти'):
                db_module.display_data(db, cur)
            output = fake_out.getvalue().strip()
            self.assertIn('1. login1 - pass1', output)
            self.assertIn('2. login2 - pass2', output)
        db.close()

    def test_delete_data(self):
        self.clear_data()
        db = sqlite3.connect('tests/test_dependencies/TestPassDB.db')
        cur = db.cursor()
        cur.executemany(
            'INSERT INTO general_pass VALUES (?, ?, ?)',
            [(1, 'login1', 'pass1'), (2, 'login2', 'pass2')]
        )

        db_module.delete_data(db, cur, '1')
        result = cur.execute("SELECT * FROM general_pass").fetchall()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], 1)
        db.close()

    @patch('builtins.input', side_effect=['Логин', 'new_login'])
    def test_update_data_login(self, mock_input):
        self.clear_data()
        db = sqlite3.connect('tests/test_dependencies/TestPassDB.db')
        cur = db.cursor()
        cur.execute('INSERT INTO general_pass VALUES (1, "old_login", "old_pass")')

        db_module.update_data(db, cur, '1')

        result = cur.execute("SELECT * FROM general_pass").fetchone()
        self.assertEqual(result[1], 'new_login')
        db.close()
