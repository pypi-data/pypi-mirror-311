from vickie.base import Validator
from typing import List
from vickie.utils import *


class ProductValidator(Validator):


    @staticmethod
    def is_ean(code):
        if not code.isdigit() or len(code) not in [8, 13]:
            return False
        return validate_check_digit(code)

    @staticmethod
    def is_gtin(code):
        if not code.isdigit() or len(code) not in [8, 12, 13, 14]:
            return False
        return validate_check_digit(code)

    @staticmethod
    def is_upc(code):
        if not code.isdigit() or len(code) != 12:
            return False
        return validate_check_digit(code)

    @staticmethod
    def is_isbn10(input_string: str) -> bool:
        if len(input_string) != 10:
            return False

        total = 0
        for i in range(9):
            if input_string[i] == 'X':
                return False
            total += int(input_string[i]) * (10 - i)

        check = (11 - (total % 11)) % 11
        return (check == 10 and input_string[-1] == 'X') or (str(check) == input_string[-1])

    @staticmethod
    def is_isbn13(input_string: str) -> bool:
        if len(input_string) != 13 or not input_string.isdigit():
            return False

        total = sum(int(digit) * (3 if i % 2 else 1) for i, digit in enumerate(input_string[:-1]))
        check_digit = (10 - (total % 10)) % 10
        return str(check_digit) == input_string[-1]
