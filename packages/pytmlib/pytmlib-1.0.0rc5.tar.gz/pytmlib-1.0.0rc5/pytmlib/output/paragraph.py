from typing import Union

from .abstract import AbstractOutput
from ..latex import Latex


class ParagraphOutput(AbstractOutput):
    def __init__(self, index: int, text: Union[str, Latex]):
        super().__init__(index)

        self._text: Union[str, Latex] = text

    @property
    def text(self) -> Union[str, Latex]:
        return self._text

    def get_type(self) -> str:
        return 'paragraph'

    def to_json(self) -> dict:
        return {
            **super().to_json(),
            'text': Latex.marshal(self._text)
        }
