import os
import re
import argparse
from getpass import getpass

strength_points = {'length': 3,
                   'date': -2,
                   'digits': 2,
                   'sp_chars': 2,
                   'letters': 1,
                   'case_sense': 1,
                   }


def load_blacklist(filepath):

    if not os.path.exists(filepath):
        return None
    with open(filepath, "r") as data_file:
        return data_file.read()


def check_dates(password):

    indicator = 0
    yymmdd = re.compile(
        '(1[0-9]|20)\d\d(-| |/|.|_)?(0[1-9]|1[012])(-| |/|.|_)?(0[1-9]|[12][0-9]|3[01])')
    mmddyy = re.compile(
        '(0[1-9]|[1-9]|1[012])(-| |/|.|_)?(0[1-9]|[12][0-9]|3[01])(-| |/|.|_)?(1[0-9]|20)\d\d')
    ddmmyy = re.compile(
        '(0[1-9]|[1-9]|[12][0-9]|3[01])(-| |/|.|_)?(0[1-9]|1[012])(-| |/|.|_)?(1[0-9]|20)\d\d')

    if re.search(yymmdd, password) or re.search(
            mmddyy, password) or re.search(ddmmyy, password):
        indicator += strength_points['date']

    return indicator


def check_length(password):

    optimal_length = 12
    indicator = 0

    if 0.5 * optimal_length <= len(password) < 0.7 * optimal_length:
        indicator += strength_points['length'] // 3
    elif 0.7 * optimal_length < len(password) < optimal_length:
        indicator += 2 * strength_points['length'] // 3
    elif len(password) >= optimal_length:
        indicator += strength_points['length']

    return indicator


def check_digits(password):

    indicator = 0

    if re.search('\d', password):
        indicator += strength_points['digits'] // 2
        if len(re.findall('\d', password)) > 1:
            indicator += strength_points['digits'] // 2

    return indicator


def check_special_characters(password):

    indicator = 0

    if re.search('[^a-zA-Z0-9]', password):
        indicator += strength_points['sp_chars'] // 2
        if len(re.findall('[^a-zA-Z0-9]', password)) > 1:
            indicator += strength_points['sp_chars'] // 2

    return indicator


def check_letters(password):

    indicator = 0

    if re.search('[a-zA-Z]', password):
        indicator += strength_points['letters']

    return indicator


def check_case_sensitivity(password):

    indicator = 0

    if re.search('[a-z]', password) and re.search('[A-Z]', password):
        indicator += strength_points['case_sense']

    return indicator


def get_password_strength(password, blacklist):

    strength = 1

    if str.lower(password) in blacklist or len(password) == 1:
        pass
    else:
        strength += (check_letters(password)
                     + check_digits(password)
                     + check_length(password)
                     + check_special_characters(password)
                     + check_case_sensitivity(password)
                     + check_dates(password))

    return strength


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('path_to_blacklist')
    args = parser.parse_args()
    blacklist = load_blacklist(args.path_to_blacklist)

    password = getpass("Enter a password:")
    if not password:
        raise ValueError('You did not enter anything.')
    else:
        blacklist = load_blacklist(args.path_to_blacklist)
        print('''Password's strength is {}/10'''
              .format(get_password_strength(password, blacklist)))
