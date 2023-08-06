from typing import Dict
from typing import Union

from .abstract import AbstractOutput
from .field_attribute import FieldAttribute
from .field_type_enum import FieldType
from ..latex import Latex


class FieldOutput(AbstractOutput):
    def __init__(
            self,
            index: int,
            field_type: FieldType,
            name: str,
            label: Union[str, Latex],
            value: Union[int, float, str, None] = None,
            required: bool = True,
            **attrs: Union[int, float, str]
    ):
        super().__init__(index)

        self._type: FieldType = field_type
        self._name: str = name
        self._label: Union[str, Latex] = label
        self._value: Union[int, float, str, None] = value
        self._required: bool = required
        self._attributes: Dict[str, Union[int, float, str]] = attrs

    @property
    def type(self) -> FieldType:
        return self._type

    @property
    def name(self) -> str:
        return self._name

    @property
    def label(self) -> Union[str, Latex]:
        return self._label

    @property
    def value(self) -> Union[int, float, str, None]:
        return self._value

    @property
    def required(self) -> bool:
        return self._required

    @property
    def attributes(self) -> Dict[str, Union[int, str]]:
        return self._attributes

    def get_type(self) -> str:
        return 'field'

    def to_json(self) -> dict:
        return {
            **super().to_json(),
            'additionalAttributes': self._attributes,
            'type': self._type,
            'name': self._name,
            'label': Latex.marshal(self._label),
            'value': self._value,
            FieldAttribute.REQUIRED: self._required
        }
