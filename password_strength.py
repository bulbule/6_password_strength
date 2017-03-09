import os
import re
import argparse
from getpass import getpass
from datetime import datetime

STRENGTH_POINTS = {'length': 3,
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
    dates_formats = ['%Y%m%d', '%Y-%m-%d', '%Y.%m.%d', '%Y_%m_%d', '%Y/%m/%d',
                     '%d%m%Y', '%d-%m-%Y', '%d.%m.%Y', '%d_%m_%Y', '%d/%m/%Y',
                     '%m%d%Y', '%m-%d-%Y', '%m.%d.%Y', '%m_%d_%Y', '%m/%d/%Y',
                     '%e%m%Y', '%e-%m-%Y', '%e.%m.%Y', '%e_%m_%Y', '%e/%m/%Y'
                     ]

    for date_format in dates_formats:
        try:
            if datetime.strptime(password, date_format):
                indicator += STRENGTH_POINTS['date']
                break
        except ValueError:
            pass

    return indicator


def check_length(password):

    optimal_length = 12
    indicator = 0

    if 0.5 * optimal_length <= len(password) < 0.7 * optimal_length:
        indicator += STRENGTH_POINTS['length'] // 3
    elif 0.7 * optimal_length < len(password) < optimal_length:
        indicator += 2 * STRENGTH_POINTS['length'] // 3
    elif len(password) >= optimal_length:
        indicator += STRENGTH_POINTS['length']

    return indicator


def check_digits(password):

    indicator = 0

    if re.search('\d', password):
        indicator += STRENGTH_POINTS['digits'] // 2
        if len(re.findall('\d', password)) > 1:
            indicator += STRENGTH_POINTS['digits'] // 2

    return indicator


def check_special_characters(password):

    indicator = 0

    if re.search('[^a-zA-Z0-9]', password):
        indicator += STRENGTH_POINTS['sp_chars'] // 2
        if len(re.findall('[^a-zA-Z0-9]', password)) > 1:
            indicator += STRENGTH_POINTS['sp_chars'] // 2

    return indicator


def check_letters(password):

    indicator = 0

    if re.search('[a-zA-Z]', password):
        indicator += STRENGTH_POINTS['letters']

    return indicator


def check_case_sensitivity(password):

    indicator = 0

    if re.search('[a-z]', password) and re.search('[A-Z]', password):
        indicator += STRENGTH_POINTS['case_sense']

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

    password = getpass("Enter a password:")
    if not password:
        raise ValueError('You did not enter anything.')
    else:
        blacklist = load_blacklist(args.path_to_blacklist)
        print('''Password's strength is {}/10'''
              .format(get_password_strength(password, blacklist)))
