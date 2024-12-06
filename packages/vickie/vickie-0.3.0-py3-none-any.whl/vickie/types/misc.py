from vickie.base import Field
from vickie.exceptions import ValidationError
from ipaddress import ip_address, AddressValueError
import phonenumbers
import string
import re

class PhoneNumber(Field):
    def __init__(self, required=True, region=None):
        super().__init__(str, required)
        self.region = region

    def validate(self, value):
        super().validate(value)
        try:
            parsed_number = phonenumbers.parse(value, self.region)
            if not phonenumbers.is_valid_number(parsed_number):
                raise ValueError(f"Invalid phone number: {value}")
        except phonenumbers.NumberParseException as e:
            raise ValueError(f"Error parsing phone number: {value}. {str(e)}")
        return True

class IPAddress(Field):
    def __init__(self, required=True):
        super().__init__(str, required)

    def validate(self, value):
        super().validate(value)
        try:
            ip_address(value)  # Checks if it's a valid IPv4 or IPv6 address
        except ValueError as e:
            raise ValueError(f"Invalid IP address: {value}. {str(e)}")
        return True

class IBAN(Field):
    def __init__(self, required=True):
        super().__init__(str, required)

    def validate(self, value):
        super().validate(value)
        value = value.replace(' ', '').replace('-', '')  # Remove spaces and hyphens

        # Check if IBAN length is valid based on the country code
        if len(value) < 15 or len(value) > 34:
            raise ValueError(f"Invalid IBAN length: {len(value)} for IBAN {value}")

        if not value[:2].isalpha() or not value[2:].isdigit():
            raise ValueError(f"Invalid IBAN format: {value}")

        # Move the first four characters to the end
        rearranged = value[4:] + value[:4]

        # Replace each letter in the string with two digits (A=10, B=11, ..., Z=35)
        numeric_iban = ''.join(str(string.ascii_uppercase.index(c) + 10) if c.isalpha() else c for c in rearranged)

        # Validate the checksum using mod 97 (IBAN validation)
        if int(numeric_iban) % 97 != 1:
            raise ValueError(f"Invalid IBAN checksum: {value}")

        return True

class HexColor(Field):
    HEX_COLOR_REGEX = re.compile(r'^#[0-9A-Fa-f]{6}$')

    def validate(self, value):
        super().validate(value)
        if not self.HEX_COLOR_REGEX.match(value):
            raise ValueError(f"Invalid hex color code: {value}")
        return True
