import re
from vickie.base import Validator
from typing import List

class CryptoValidator(Validator):

    @staticmethod
    def is_bitcoin(address):
        pattern = r"^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$"
        return bool(re.match(pattern, address))

    @staticmethod
    def is_ethereum(address):
        pattern = r"^0x[a-fA-F0-9]{40}$"
        return bool(re.match(pattern, address))

    @staticmethod
    def is_litecoin(address):
        pattern = r"^[LM3][a-km-zA-HJ-NP-Z1-9]{25,34}$"
        return bool(re.match(pattern, address))

    @staticmethod
    def is_tether(address):
        pattern = r"^0x[a-fA-F0-9]{40}$"
        return bool(re.match(pattern, address))

    @staticmethod
    def is_monero(address):
        pattern = r"^[48][0-9AB][1-9A-HJ-NP-Za-km-z]{93}$"
        return bool(re.match(pattern, address))

    @staticmethod
    def is_bnb(address):
        pattern = r"^bnb1[a-z0-9]{38}$"
        return bool(re.match(pattern, address))


    @staticmethod
    def is_solana(address):
        pattern = r"^[1-9A-HJ-NP-Za-km-z]{32,44}$"
        return bool(re.match(pattern, address))

    @staticmethod
    def is_dogecoin(address):
        pattern = r"^D{1}[5-9A-HJ-NP-U]{1}[1-9A-Za-z]{32}$"
        return bool(re.match(pattern, address))

    @staticmethod
    def is_xrp(address):
        pattern = r"^r[0-9a-zA-Z]{24,34}$"
        return bool(re.match(pattern, address))
