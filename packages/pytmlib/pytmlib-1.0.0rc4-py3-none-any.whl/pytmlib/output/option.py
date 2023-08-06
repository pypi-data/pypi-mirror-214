from typing import Union

from .field_attribute import FieldAttribute
from ..latex import Latex


class Option:
    def __init__(self, value: Union[str, int, float, bool], label: Union[str, Latex] = None, checked: bool = False):
        """Create an option object.

        :param value: The value to return.
        :param label: The visible label. Can be omitted if similar to the value.
        """
        self._value: Union[str, int, float, bool] = value
        self._label: Union[str, Latex] = label if label is not None else str(value)
        self._checked: bool = checked

    @property
    def value(self) -> Union[str, int, float, bool]:
        return self._value

    @property
    def label(self) -> Union[str, Latex]:
        return self._label

    @property
    def checked(self) -> bool:
        return self._checked

    def to_json(self) -> dict:
        return {
            FieldAttribute.VALUE: self._value,
            'label': Latex.marshal(self._label),
            FieldAttribute.CHECKED: self._checked
        }
