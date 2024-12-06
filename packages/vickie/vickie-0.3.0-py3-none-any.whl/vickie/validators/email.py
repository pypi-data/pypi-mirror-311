import re
from vickie.base import Validator
from typing import List
import dns.resolver


common_providers = [
            "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "aol.com",
            "icloud.com", "protonmail.com", "mail.com", "zoho.com", "yandex.com",
            "gmx.com", "live.com", "msn.com", "fastmail.com", "mailchimp.com",
            "comcast.net", "verizon.net", "att.net", "sbcglobal.net", "me.com",
            "mac.com", "googlemail.com", "rocketmail.com", "orange.fr", "wanadoo.fr",
            "free.fr", "skynet.be", "telenet.be", "web.de", "t-online.de",
            "mail.ru", "rambler.ru", "yandex.ru", "163.com", "qq.com",
            "sina.com", "sohu.com", "yeah.net"
        ]

class EmailValidator(Validator):

    @staticmethod
    def check_mx_record(domain):
        try:
            mx_records = dns.resolver.resolve(domain, 'MX')
            return len(mx_records) > 0
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.exception.Timeout):
            return False

    def is_common(domain):
        return domain in common_providers

    @staticmethod
    def is_email(input_string: str) -> bool:
        # This is a simplified regex for email validation
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, input_string))

