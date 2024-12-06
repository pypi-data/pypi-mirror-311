from vickie.base import Validator
from typing import List
import phonenumbers

class PhoneValidator(Validator):

    @staticmethod
    def is_phone(number: str, region: str = None) -> bool:
        try:
            parsed_number = phonenumbers.parse(number, region)
            return phonenumbers.is_valid_number(parsed_number)
        except phonenumbers.NumberParseException:
            return False

    def is_imei(code:str)->bool:
        # Remove any non-digit characters
        imei = ''.join(filter(str.isdigit, code))

        # Check if the IMEI is exactly 15 digits long
        if len(imei) != 15:
            return False

        # Apply the Luhn algorithm
        total = 0
        double = False

        for digit in imei[::-1]:  # Iterate from right to left
            digit = int(digit)
            if double:
                digit *= 2
                if digit > 9:
                    digit -= 9
            total += digit
            double = not double

        # If the total is divisible by 10, the IMEI is valid
        return total % 10 == 0
