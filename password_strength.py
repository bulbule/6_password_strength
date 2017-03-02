import os
import re


def load_bad_passwords(filepath):

    if not os.path.exists(filepath):
        return None
    with open(filepath, "r") as data_file:
        return data_file.read()


def dates_match(password, strength):  # matches years 1900-2099

    yymmdd = re.compile(
        '(19|20)\d\d(-| |/|.|_)?(0[1-9]|1[012])(-| |/|.|_)?(0[1-9]|[12][0-9]|3[01])')
    mmddyy = re.compile(
        '(0[1-9]|[1-9]|1[012])(-| |/|.|_)?(0[1-9]|[12][0-9]|3[01])(-| |/|.|_)?(19|20)\d\d')
    ddmmyy = re.compile(
        '(0[1-9]|[1-9]|[12][0-9]|3[01])(-| |/|.|_)?(0[1-9]|1[012])(-| |/|.|_)?(19|20)\d\d')

    if (len(re.findall(yymmdd, password)) >= 1) or (len(re.findall(
            mmddyy, password)) >= 1) or (len(re.findall(ddmmyy, password)) >= 1):
        strength -= 2

    return strength


def get_password_strength(password, blacklist):

    strength = 1

    if str.lower(password) in blacklist or len(password) == 1:
        pass
    else:
        if len(re.findall('[a-z]', password)) > 0:
            strength += 1
        if len(re.findall('[A-Z]', password)) > 0:
            strength += 1
        if len(re.findall('\d', password)) == 1:
            strength += 1
        elif len(re.findall('\d', password)) > 1:
            strength += 2
        if len(re.findall('[^a-zA-Z0-9]', password)) == 1:
            strength += 1
        elif len(re.findall('[^a-zA-Z0-9]', password)) > 1:
            strength += 2
        if 4 < len(password) < 8:
            strength += 1
        elif 7 < len(password) < 11:
            strength += 2
        elif len(password) > 10:
            strength += 3

        strength = dates_match(password, strength)

    return strength


if __name__ == '__main__':

    password = input("Enter a password:")
    if not password:
        raise ValueError('You did not enter anything.')
    else:
        blacklist = load_bad_passwords('blacklist.txt')
        print('''Password's strength is {}/10'''
              .format(get_password_strength(password, blacklist)))
