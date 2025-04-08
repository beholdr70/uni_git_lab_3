from string import ascii_letters, digits, whitespace
from random import randint
from ast import literal_eval

# Importing text used in sequences of this file
with open('dependencies/RU_loc.txt', encoding='utf-8') as loc_file:
    loc_dict = literal_eval('{' + loc_file.read() + '}')
    pass_generator_len_text = loc_dict['pass_generator_len_text']
    pass_generator_len_fail_text = loc_dict['pass_generator_len_fail_text']
    special_symbols_text = loc_dict['special_symbols_text']
    loc_file.close()


# Generating a password
def generate_pass():
    pass_len = input(pass_generator_len_text)
    while not pass_len.isnumeric() or (int(pass_len) > 40 and int(pass_len) > 4):
        pass_len = input(pass_generator_len_fail_text)
    special_symbols = ''.join(
        i for i in filter(lambda x: x not in ascii_letters and x not in digits and x not in whitespace,
                          input(special_symbols_text)))
    symbols = ascii_letters + digits + special_symbols
    result = ''
    for i in range(int(pass_len)):
        result += symbols[randint(0, len(symbols) - 1)]
    print('\n' + result)
