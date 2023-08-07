from typing import Union


class Latex:
    def __init__(self, code: str):
        self._code: str = code

    @property
    def code(self) -> str:
        return self._code

    def to_json(self) -> dict:
        return {
            'code': self._code
        }

    @staticmethod
    def marshal(text: Union[str, int, float, 'Latex']) -> Union[str, dict, None]:
        return text if isinstance(text, (str, int, float)) or text is None else text.to_json()
