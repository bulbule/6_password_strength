import os
import re


def load_bad_passwords(filepath):

    if not os.path.exists(filepath):
        return None
    with open(filepath, "r") as data_file:
        return data_file.read()


def check_dates(password):  # matches years 1900-2099

    indicator = 0
    yymmdd = re.compile(
        '(19|20)\d\d(-| |/|.|_)?(0[1-9]|1[012])(-| |/|.|_)?(0[1-9]|[12][0-9]|3[01])')
    mmddyy = re.compile(
        '(0[1-9]|[1-9]|1[012])(-| |/|.|_)?(0[1-9]|[12][0-9]|3[01])(-| |/|.|_)?(19|20)\d\d')
    ddmmyy = re.compile(
        '(0[1-9]|[1-9]|[12][0-9]|3[01])(-| |/|.|_)?(0[1-9]|1[012])(-| |/|.|_)?(19|20)\d\d')

    if (len(re.findall(yymmdd, password)) >= 1) or (len(re.findall(
            mmddyy, password)) >= 1) or (len(re.findall(ddmmyy, password)) >= 1):
        indicator -= 2

    return indicator


def check_length(password):

    optimal_length = 12
    indicator = 0

    if 0.5 * optimal_length <= len(password) < 0.7 * optimal_length:
        indicator += 1
    elif 0.7 * optimal_length < len(password) < optimal_length:
        indicator += 2
    elif len(password) >= optimal_length:
        indicator += 3

    return indicator


def check_digits(password):

    indicator = 0

    if len(re.findall('\d', password)) == 1:
        indicator += 1
    elif len(re.findall('\d', password)) > 1:
        indicator += 2

    return indicator


def check_special_characters(password):

    indicator = 0

    if len(re.findall('[^a-zA-Z0-9]', password)) == 1:
        indicator += 1
    elif len(re.findall('[^a-zA-Z0-9]', password)) > 1:
        indicator += 2

    return indicator


def check_letters(password):

    indicator = 0

    if len(re.findall('[a-zA-Z]', password)) > 0:
        indicator += 1

    return indicator


def check_case_sensitivity(password):

    indicator = 0

    if len(
        re.findall(
            '[a-z]',
            password)) > 0 and len(
            re.findall(
                '[A-Z]',
                password)) > 0:
        indicator += 1

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

    password = input("Enter a password:")
    if not password:
        raise ValueError('You did not enter anything.')
    else:
        blacklist = load_bad_passwords('blacklist.txt')
        print('''Password's strength is {}/10'''
              .format(get_password_strength(password, blacklist)))
