from enum import Enum


class FieldType(str, Enum):
    TEXT = 'text'
    PASSWORD = 'password'
    NUMBER = 'number'
    RANGE = 'range'
