from abc import ABC, abstractmethod
from typing import Any
from vickie.exceptions import ValidationError

class Validator(ABC):
    pass

class Field:
    def __init__(self, field_type: type, required: bool = True):
        self.field_type = field_type
        self.required = required

    def validate(self, value: Any) -> Any:
        if value is None:
            if self.required:
                raise ValidationError(f"Field is required")
            return None

        if not isinstance(value, self.field_type):
            raise ValidationError(f"Expected {self.field_type.__name__}, got {type(value).__name__}")

        return value
