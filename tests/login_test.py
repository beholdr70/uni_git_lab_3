import sqlite3
import os
from unittest import TestCase
from login import check_if_correct

class LoginTest(TestCase):
    def test_master_pass_correct(self):
        db = sqlite3.connect(os.path.realpath('tests/test_dependencies/TestPassDB.db'))
        cur = db.cursor()
        m_passes = ['masterP1', 'MASTER_Pass2', 'MP3_!@#+WASD']
        for password in m_passes:
            cur.execute('UPDATE master_pass SET pass_instance = ?', (password,))
            db.commit()
            self.assertTrue(check_if_correct(cur, password))
            self.assertFalse(check_if_correct(cur, password + 'abcdef'))
        db.close()