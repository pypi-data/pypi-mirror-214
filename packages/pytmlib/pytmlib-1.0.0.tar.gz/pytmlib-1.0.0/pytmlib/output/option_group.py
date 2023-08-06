from typing import List
from typing import Union

from .abstract import AbstractOutput
from .field_attribute import FieldAttribute
from .option import Option
from ..latex import Latex


class OptionGroupOutput(AbstractOutput):
    def __init__(
            self,
            index: int,
            name: str,
            label: Union[str, Latex, None],
            options: List[Union[Option, str, int, float, bool]],
            required: bool = True,
            inline: bool = True,
            multiple: bool = False
    ):
        super().__init__(index)

        self._name: str = name
        self._label: Union[str, Latex, None] = label
        self._options: List[Option] = [] if options is None else map(self._normalize_option, options)
        self._required: bool = required
        self._inline: bool = inline
        self._multiple: bool = multiple

    @property
    def name(self) -> str:
        return self._name

    @property
    def label(self) -> Union[str, Latex, None]:
        return self._label

    @property
    def options(self) -> List[Option]:
        return self._options

    @property
    def inline(self) -> bool:
        return self._inline

    @property
    def required(self) -> bool:
        return self._required

    @property
    def multiple(self) -> bool:
        return self._multiple

    def get_type(self) -> str:
        return 'option-group'

    def to_json(self) -> dict:
        return {
            **super().to_json(),
            FieldAttribute.NAME: self._name,
            'label': Latex.marshal(self._label),
            'options': list(map(lambda option: option.to_json(), self._options)),
            'inline': self._inline,
            'multiple': self._multiple,
            FieldAttribute.REQUIRED: self._required
        }

    @staticmethod
    def _normalize_option(option: Union[Option, str, int, float, bool]) -> Option:
        return option if isinstance(option, Option) else Option(option)
