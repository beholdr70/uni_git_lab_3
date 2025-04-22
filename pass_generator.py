from string import ascii_letters, digits, whitespace
from random import randint
from ast import literal_eval
import os

path = os.path.realpath('dependencies/RU_loc.txt')
path = os.path.realpath('dependencies/RU_loc.txt').replace('tests\\', '') if 'tests\\' in path else path

# Importing text used in sequences of this file
with open(path, encoding='utf-8') as loc_file:
    loc_dict = literal_eval('{' + loc_file.read() + '}')
    pass_generator_len_text = loc_dict['pass_generator_len_text']
    pass_generator_len_fail_text = loc_dict['pass_generator_len_fail_text']
    special_symbols_text = loc_dict['special_symbols_text']
    loc_file.close()


def get_user_input_pass_gen():
    pass_len = input(pass_generator_len_text)
    while not pass_len.isnumeric() or int(pass_len) > 40 or int(pass_len) < 5:
        pass_len = input(pass_generator_len_fail_text)
    special_symbols = ''.join(
        i for i in filter(lambda x: x not in ascii_letters and x not in digits and x not in whitespace,
                          input(special_symbols_text)))
    symbols = ascii_letters + digits + special_symbols
    print('\n' + generate_pass(int(pass_len), symbols, special_symbols))


# Generating a password
def generate_pass(pass_len, symbols, special_symbols):
    if pass_len > 40 or pass_len < 5:
        raise ValueError('Invalid password length was given')
    if not symbols or not any(symbol.isnumeric() for symbol in symbols):
        raise ValueError('Available password symbols can not be an empty string and should contain at least one number')
    result = ''
    while not any(i in result for i in special_symbols if special_symbols) and not len(
            list(filter(lambda x: x.isnumeric(), result))) >= 2:
        result = ''
        for i in range(pass_len):
            result += symbols[randint(0, len(symbols) - 1)]
    return result


if __name__ == '__main__':
    get_user_input_pass_gen()
