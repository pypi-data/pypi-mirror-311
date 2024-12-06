from vickie.base import Field
from vickie.exceptions import ValidationError
from typing import Any
import re
from urllib.parse import urlparse
import uuid
import json

class String(Field):
    def __init__(self, min_length: int = None, max_length: int = None, pattern: str = None, **kwargs):
        super().__init__(str, **kwargs)
        self.min_length = min_length
        self.max_length = max_length
        self.pattern = re.compile(pattern) if pattern else None

    def validate(self, value: Any) -> str:
        value = super().validate(value)
        if value is None:
            return None

        if self.min_length and len(value) < self.min_length:
            raise ValidationError(f"String length should be at least {self.min_length}")
        if self.max_length and len(value) > self.max_length:
            raise ValidationError(f"String length should be at most {self.max_length}")
        if self.pattern and not self.pattern.match(value):
            raise ValidationError(f"String does not match the required pattern")

        return value

class URL(String):
    def __init__(self, schemes: List[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.schemes = schemes or ['http', 'https']

    def validate(self, value: Any) -> str:
        value = super().validate(value)
        if value is None:
            return None

        try:
            parsed_url = urlparse(value)
            if not parsed_url.scheme or not parsed_url.netloc:
                raise ValidationError("Invalid URL format")
            if self.schemes and parsed_url.scheme not in self.schemes:
                raise ValidationError(f"URL scheme must be one of: {', '.join(self.schemes)}")
        except Exception:
            raise ValidationError("Invalid URL")

        return value

class Email(String):
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

    def validate(self, value: Any) -> str:
        value = super().validate(value)
        if value is None:
            return None

        if not self.EMAIL_REGEX.match(value):
            raise ValidationError("Invalid email format")

        return value

class Password(String):
    def __init__(self, min_length=8, uppercase=True,lowercase=True,
                 digits=True, special=True, required=True):
        super().__init__(str, required)
        self.min_length = min_length
        self.uppercase = uppercase
        self.lowercase = lowercase
        self.digits = digits
        self.special = special

    def validate(self, value):
        super().validate(value)
        if len(value) < self.min_length:
            raise ValueError(f"Password must be at least {self.min_length} characters long")

        if self.require_uppercase and not any(c.isupper() for c in value):
            raise ValueError("Password must contain at least one uppercase letter")
        if self.require_lowercase and not any(c.islower() for c in value):
            raise ValueError("Password must contain at least one lowercase letter")
        if self.require_digits and not any(c.isdigit() for c in value):
            raise ValueError("Password must contain at least one digit")
        if self.require_special and not any(c in '!@#$%^&*()-_=+[{]};:,<.>/?' for c in value):
            raise ValueError("Password must contain at least one special character")

        return True

class UUID(Field):
    def __init__(self, required=True):
        super().__init__(str, required)

    def validate(self, value):
        super().validate(value)
        try:
            uuid.UUID(value)
        except ValueError:
            raise ValueError(f"Invalid UUID: {value}")
        return True

class JSON(Field):
    def __init__(self, required=True):
        super().__init__(str, required)

    def validate(self, value):
        super().validate(value)
        try:
            json.loads(value)
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON string: {value}")
        return True
