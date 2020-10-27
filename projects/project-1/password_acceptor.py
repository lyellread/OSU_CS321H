#!/usr/bin/env python3

import re


def check(password):
    """
    Regex adapted from <https://stackoverflow.com/a/21456918/8704864>

    Explanation:
    - ^ : Start of string
    - (?=.*[A-Z]) : Forward search for A-Z in string
    - (?=.*[a-z]) : Forward search for a-z in string
    - (?=.*\d) : Forward search for 0-9 in string
    - (?=.*[@$!%*#?&]) : Forward search for special in string
    - [A-Za-z\d@$!%*#?&]{14,} : All string characters must total 14 or more
    - $ : End of string.
    """

    result = re.fullmatch(
        "^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{14,}$",
        password,
    )
    print(f'Password Check: {"Success" if not result ==  None else "Failure"}')


if __name__ == "__main__":

    print("Password Check Started.")
    print("This will check that a password is:")
    print("- At least 14 characters long")
    print("- Contains at least one from each {lowercase, uppercase, number, symbol}")
    print("    - Special characters are {@$!%*#?&}")

    password = input("\nPlease enter your password: ")
    check(password)
