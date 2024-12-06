from vickie.base import Field
from vickie.exceptions import ValidationError
from typing import Any


class Int(Field):
    def __init__(self, min_value: int = None, max_value: int = None, **kwargs):
        super().__init__(int, **kwargs)
        self.min = min_value
        self.max = max_value

    def validate(self, value: Any) -> int:
        value = super().validate(value)
        if value is None:
            return None

        if self.min_value is not None and value < self.min_value:
            raise ValidationError(f"Value should be at least {self.min_value}")
        if self.max_value is not None and value > self.max_value:
            raise ValidationError(f"Value should be at most {self.max_value}")

        return value

class Float(Field):
    def __init__(self, min_value: float = None, max_value: float = None, **kwargs):
        super().__init__((int, float), **kwargs)
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: Any) -> float:
        value = super().validate(value)
        if value is None:
            return None

        value = float(value)
        if self.min_value is not None and value < self.min_value:
            raise ValidationError(f"Value should be at least {self.min_value}")
        if self.max_value is not None and value > self.max_value:
            raise ValidationError(f"Value should be at most {self.max_value}")

        return value

class Boolean(Field):
    def __init__(self, required=True):
        super().__init__((bool, str, int), required)

    def validate(self, value):
        super().validate(value)
        truthy_values = ['true', '1', 1, True]
        falsy_values = ['false', '0', 0, False]

        if value in truthy_values:
            return True
        elif value in falsy_values:
            return False
        else:
            raise ValueError(f"Invalid boolean value: {value}")
