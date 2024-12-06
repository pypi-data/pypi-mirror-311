import re
from vickie.exceptions import ValidationError
from typing import Any, Dict, List, Union, Callable
from datetime import datetime
import string
import json


class Schema:
    def __init__(self, **fields):
        self.fields = fields

    def validate(self, data: Dict) -> Dict:
        if not isinstance(data, dict):
            raise ValidationError("Data must be a dictionary")

        validated_data = {}
        for field_name, field in self.fields.items():
            if field_name in data:
                validated_data[field_name] = field.validate(data[field_name])
            elif field.required:
                raise ValidationError(f"Required field '{field_name}' is missing")

        return validated_data


