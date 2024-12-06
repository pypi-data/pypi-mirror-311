import re
from vickie.base import Validator
from typing import List

class URIValidator(Validator):

    @staticmethod
    def is_url(inp:str):
        url_pattern = re.compile(
            r'^(https?|ftp):\/\/'  # Protocol (http, https, ftp)
            r'((\w+:\w+)?@)?'  # Optional authentication (user:pass)
            r'(([\w-]+\.)+[a-zA-Z]{2,63})'  # Domain and TLD
            r'(:\d{1,5})?'  # Optional port
            r'(\/[^\s]*)?$'  # Optional path
        )

        return re.match(url_pattern, inp) is not None

    @staticmethod
    def is_ftp(inp: str) -> bool:
        if not URIValidator.is_url(inp):
            return False
        return inp.startswith('ftp://') or inp.startswith('sftp://')

    @staticmethod
    def is_http(inp: str) -> bool:
        if not URIValidator.is_url(inp):
            return False
        return inp.startswith('http://') or inp.startswith('https://')

    @staticmethod
    def is_magnet(inp:str)->bool:
        magnet_regex = re.compile(
            r'^magnet:\?'  # Protocol
            r'(xt=urn:btih:[0-9a-fA-F]{40})'  # Info hash (40 hex characters)
            r'(&dn=[^&]*)?'  # Optional name (dn)
            r'(&tr=[^&]*)*'  # Optional tracker URLs (tr), can be multiple
            r'(&x-[^&]*)*'  # Optional additional parameters starting with 'x-' (extended parameters)
            r'(&[^&]*)*$'  # Optional other parameters
            )
        return bool(re.match(magnet_regex, inp))
