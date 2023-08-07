from typing import Union

from ..latex import Latex


class TableCell:
    def __init__(self, value: Union[str, int, float, Latex]):
        self._value: Union[str, int, float, Latex] = value
        self._type: str = 'numeric' if isinstance(value, (int, float)) else 'string'

    @property
    def value(self) -> Union[str, int, float, Latex]:
        return self._value

    @property
    def type(self) -> str:
        return self._type

    def to_json(self) -> dict:
        return {
            'type': self._type,
            'value': Latex.marshal(self._value)
        }

    @staticmethod
    def to_table_cell(value: Union[str, int, float, Latex, 'TableCell']) -> 'TableCell':
        return value if isinstance(value, TableCell) else TableCell(value)
