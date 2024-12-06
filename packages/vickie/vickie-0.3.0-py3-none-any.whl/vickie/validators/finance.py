import re
from vickie.base import Validator
from typing import List, Tuple
from vickie.utils import *

class FValidator(Validator):


    @staticmethod
    def is_iban(iban: str) -> bool:
        iban = iban.replace(' ', '').upper()
        if not re.match(r'^[A-Z]{2}[0-9A-Z]{13,32}$', iban):
            return False

        iban = iban[4:] + iban[:4]
        digits = ''
        for ch in iban:
            if ch.isdigit():
                digits += ch
            else:
                digits += str(ord(ch) - ord('A') + 10)

        return int(digits) % 97 == 1

    @staticmethod
    def is_valid(card_number: str) -> Tuple[bool, str]:
        """
        Validate the credit card number and return its type.
        """
        # Remove any spaces or hyphens
        card_number = re.sub(r'[\s-]', '', card_number)

        if not card_number.isdigit():
            return False, "Invalid: Contains non-digit characters"

        if not luhn_check(card_number):
            return False, "Invalid: Failed Luhn check"

    @staticmethod
    def is_visa(card_number:str)->bool:
        return bool(re.match(r'^4[0-9]{12}(?:[0-9]{3})?$', card_number))

    @staticmethod
    def is_mastercard(card_number):
        return bool(re.match(r'^5[1-5][0-9]{14}$', card_number))

    @staticmethod
    def is_amex(card_number):    # American Express
        return bool(re.match(r'^3[47][0-9]{13}$', card_number))
