import re
from vickie.base import Validator
from typing import List

class NetValidator(Validator):

    @staticmethod
    def is_ipv4(input_string: str) -> bool:
        pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        if not re.match(pattern, input_string):
            return False
        return all(0 <= int(num) <= 255 for num in input_string.split('.'))

    @staticmethod
    def is_ipv6(input_string: str) -> bool:
        pattern = r'^(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}$'
        return bool(re.match(pattern, input_string, re.IGNORECASE))

    @staticmethod
    def is_mac(mac: str) -> bool:
        patterns = [
            r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$',
            r'^([0-9A-Fa-f]{4}[.]){2}([0-9A-Fa-f]{4})$',
            r'^([0-9A-Fa-f]{12})$'
        ]
        return any(re.match(pattern, mac) for pattern in patterns)
