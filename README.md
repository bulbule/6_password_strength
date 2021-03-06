# Password Strength Calculator

A program asks the user for a password and assesses its strength from 1 (very weak) to 10 (very strong).
It is done by first checking if the password belongs to a certain blacklist, to which you need to indicate a path. In case it does not, the script proceeds with checking if the password:
* contains digits
* contains letters
* is case-sensitive
* does not contain a calendar date in a certain format
* contains any special characters

You can download various lists of most common passwords, for instance, from this [repository](https://github.com/danielmiessler/SecLists/tree/master/Passwords).

# Usage

```#!bash

$ python password_strength.py blacklist.txt
Enter a password:
Password's strength is 6/10

```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
