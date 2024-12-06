from typing import Dict, List
from .base import Validator

def luhn_check(card_number: str) -> bool:
    """
    Implement the Luhn algorithm for credit card number validation.
    """
    digits = [int(d) for d in card_number if d.isdigit()]
    checksum = 0
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(divmod(d * 2, 10))
    return checksum % 10 == 0

def validate_check_digit(code):
    total_sum = 0
    reverse_digits = list(map(int, reversed(code)))
    for i, digit in enumerate(reverse_digits[1:], start=1):
        if i % 2 == 0:
            total_sum += digit
        else:
            total_sum += digit * 3
    check_digit = (10 - (total_sum % 10)) % 10
    return check_digit == reverse_digits[0]

def verhoeff_check(number):
    """
    Implements the Verhoeff algorithm for check digit calculation and validation.
    """
    multiplication_table = [
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
        [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
        [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
        [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
        [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
        [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
        [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
        [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
        [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    ]

    permutation_table = [
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
        [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
        [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
        [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
        [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
        [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
        [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]
    ]

    inverse_table = [0, 4, 3, 2, 1, 5, 6, 7, 8, 9]

    check = 0
    for i, digit in enumerate(reversed(str(number))):
        check = multiplication_table[check][permutation_table[i % 8][int(digit)]]
    return check == 0

def damm_check(number):
    """
    Implements the Damm algorithm for check digit calculation and validation.
    """
    damm_matrix = [
        [0, 3, 1, 7, 5, 9, 8, 6, 4, 2],
        [7, 0, 9, 2, 1, 5, 4, 8, 6, 3],
        [4, 2, 0, 6, 8, 7, 1, 3, 5, 9],
        [1, 7, 5, 0, 9, 8, 3, 4, 2, 6],
        [6, 1, 2, 3, 0, 4, 5, 9, 7, 8],
        [3, 6, 7, 4, 2, 0, 9, 5, 8, 1],
        [5, 8, 6, 9, 7, 2, 0, 1, 3, 4],
        [8, 9, 4, 5, 3, 6, 2, 0, 1, 7],
        [9, 4, 3, 8, 6, 1, 7, 2, 0, 5],
        [2, 5, 8, 1, 4, 3, 6, 7, 9, 0]
    ]

    interim = 0
    for digit in str(number):
        interim = damm_matrix[interim][int(digit)]
    return interim == 0
