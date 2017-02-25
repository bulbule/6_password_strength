# Password Strength Calculator

A program asks the user for a password and assesses its strength from 1 (very weak) to 10 (very strong).
It is done by first checking if the password belongs to a certain blacklist, which is contained in
the file 10k_most_common.txt. Then it proceeds with checking if the password:
* contains digits
* contains letters
* is case-sensitive
* does not contain a calendar date in a certain format
* contains any special characters

# Usage

```#!bash

$ python password_strength.py
Enter a password:Kn0pk@
Password's strength is 6

```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
