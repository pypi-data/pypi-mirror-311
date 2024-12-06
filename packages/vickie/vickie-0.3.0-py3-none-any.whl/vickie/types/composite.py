from vickie.base import Field
from vickie.exceptions import ValidationError
from typing import Any, Callable
from datetime import datetime

class List(Field):
    def __init__(self, item_type: Field, min_length: int = None, max_length: int = None, **kwargs):
        super().__init__(list, **kwargs)
        self.item_type = item_type
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, value: Any) -> list:
        value = super().validate(value)
        if value is None:
            return None

        if self.min_length is not None and len(value) < self.min_length:
            raise ValidationError(f"List should have at least {self.min_length} items")
        if self.max_length is not None and len(value) > self.max_length:
            raise ValidationError(f"List should have at most {self.max_length} items")

        return [self.item_type.validate(item) for item in value]

class Dict(Field):
    def __init__(self, schema: dict, **kwargs):
        super().__init__(dict, **kwargs)
        self.schema = schema

    def validate(self, value: Any) -> dict:
        value = super().validate(value)
        if value is None:
            return None

        return self.schema.validate(value)

class DateTime(Field):
    def __init__(self, format: str = "%Y-%m-%d %H:%M:%S", **kwargs):
        super().__init__(str, **kwargs)
        self.format = format

    def validate(self, value: Any) -> datetime:
        value = super().validate(value)
        if value is None:
            return None

        try:
            return datetime.strptime(value, self.format)
        except ValueError:
            raise ValidationError(f"Invalid datetime format. Expected {self.format}")

class EnumField(Field):
    def __init__(self, choices: List[Any], **kwargs):
        super().__init__(type(choices[0]), **kwargs)
        self.choices = set(choices)

    def validate(self, value: Any) -> Any:
        value = super().validate(value)
        if value is None:
            return None

        if value not in self.choices:
            raise ValidationError(f"Value must be one of {self.choices}")

        return value



class CustomField(Field):
    def __init__(self, validation_func: Callable[[Any], Any], **kwargs):
        super().__init__(object, **kwargs)
        self.validation_func = validation_func

    def validate(self, value: Any) -> Any:
        value = super().validate(value)
        if value is None:
            return None

        return self.validation_func(value)
