from enum import Enum


class FieldAttribute(str, Enum):
    MAX_LENGTH = 'maxlength'
    REQUIRED = 'required'
    MIN = 'min'
    MAX = 'max'
    STEP = 'step'
    NAME = 'name'
    VALUE = 'value'
    TYPE = 'type'
    CHECKED = 'checked'
