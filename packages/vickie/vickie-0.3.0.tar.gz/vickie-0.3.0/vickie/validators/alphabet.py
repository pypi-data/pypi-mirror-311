import re
from vickie.base import Validator

class ABValidator(Validator):

    @staticmethod
    def clean(inp:str)->str:
        """Clean the input string by removing all spaces and non-alphabetic characters."""
        return ''.join(char for char in inp if char.isalpha())

    @staticmethod
    def is_latin(text):
        pattern = r'^[a-zA-Z]+$'
        text = ABValidator.clean(text)
        return bool(re.match(pattern, text))

    @staticmethod
    def is_cyrillic(text):
        text = ABValidator.clean(text)
        pattern = r'^[а-яА-ЯёЁ]+$'
        return bool(re.match(pattern, text))

    @staticmethod
    def is_greek(text):
        pattern = r'^[\u0370-\u03FF\u1F00-\u1FFF]+$'
        text = ABValidator.clean(text)
        return bool(re.match(pattern, text))

    @staticmethod
    def is_arabic(text):
        pattern = r'^[ا-ي]+$'
        text = ABValidator.clean(text)
        return bool(re.match(pattern, text))

    @staticmethod
    def is_chinese(text):
        pattern = r'^[\u4e00-\u9fff]+$'
        text = ABValidator.clean(text)
        return bool(re.match(pattern, text))

    @staticmethod
    def is_japanese(text):
        pattern = r'^[\u3040-\u309f\u30a0-\u30ff\u4e00-\u9fff]+$'
        text = ABValidator.clean(text)
        return bool(re.match(pattern, text))

    @staticmethod
    def is_korean(text):
        pattern = r'^[\uac00-\ud7a3]+$'
        text = ABValidator.clean(text)
        return bool(re.match(pattern, text))

    @staticmethod
    def is_thai(text):
        pattern = r'^[\u0e00-\u0e7f]+$'
        text = ABValidator.clean(text)
        return bool(re.match(pattern, text))

    @staticmethod
    def is_hebrew(text):
        pattern = r'^[\u0590-\u05ff]+$'
        text = ABValidator.clean(text)
        return bool(re.match(pattern, text))

    @staticmethod
    def is_armenian(text):
        pattern = r'^[\u0530-\u058f]+$'
        text = ABValidator.clean(text)
        return bool(re.match(pattern, text))

    @staticmethod
    def is_georgian(text):
        pattern = r'^[\u10a0-\u10ff]+$'
        text = ABValidator.clean(text)
        return bool(re.match(pattern, text))

    @staticmethod
    def is_devanagari(text):
        pattern = r'^[\u0900-\u097f]+$'
        text = ABValidator.clean(text)
        return bool(re.match(pattern, text))

    @staticmethod
    def is_tamil(text):
        pattern = r'^[\u0b80-\u0bff]+$'
        text = ABValidator.clean(text)
        return bool(re.match(pattern, text))

    @staticmethod
    def is_telugu(text):
        pattern = r'^[\u0c00-\u0c7f]+$'
        text = ABValidator.clean(text)
        return bool(re.match(pattern, text))

    @staticmethod
    def is_kannada(text):
        pattern = r'^[\u0c80-\u0cff]+$'
        text = ABValidator.clean(text)
        return bool(re.match(pattern, text))

    @staticmethod
    def is_malayalam(text):
        pattern = r'^[\u0d00-\u0d7f]+$'
        text = ABValidator.clean(text)
        return bool(re.match(pattern, text))
