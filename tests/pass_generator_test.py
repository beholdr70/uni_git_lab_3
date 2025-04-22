from unittest import TestCase
from pass_generator import generate_pass


class PassGenTest(TestCase):
    def test_pass_correct_len_passed(self):
        with self.assertRaises(ValueError) as err:
            generate_pass(41, 'a1', '')
        self.assertEqual('Invalid password length was given', err.exception.args[0])

    def test_pass_correct_symbols_passed(self):
        with self.assertRaises(ValueError) as err:
            generate_pass(40, '', '')
        self.assertEqual('Available password symbols can not be an empty string and should contain at least one number',
                         err.exception.args[0])

    def test_pass_symbols_num_passed(self):
        with self.assertRaises(ValueError) as err:
            generate_pass(40, 'a', '')
        self.assertEqual('Available password symbols can not be an empty string and should contain at least one number',
                         err.exception.args[0])

    def test_special_symbols(self):
        special = '()-+!?,<>'
        symbol = 'abcdefg123456' + special
        password = generate_pass(40, symbol, special)
        self.assertTrue(any(spec in password for spec in special))

    def test_pass_len_equal(self):
        lengths = [7, 25, 39]
        for length in lengths:
            self.assertEqual(len(generate_pass(length, 'abcdef123', '')), length)

    def test_pass_only_given_symbols(self):
        symbols = 'aHJKlpO{}-=+123_0!'
        for i in range(10):
            password = generate_pass(25, symbols, '')
            self.assertTrue(all(symbol in symbols for symbol in password))
