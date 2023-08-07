from .abstract import AbstractOutput
from ..serializer import Serializer


class ButtonOutput(AbstractOutput):
    PARAMETERS_FIELD: str = 'parameters'
    DATA_FIELD: str = 'data'
    SIGNATURE_FIELD: str = 'signature'

    def __init__(self, index: int, serializer: Serializer, name: str, action: str, additional_parameters: dict):
        super().__init__(index)

        self._serializer: Serializer = serializer
        self._name: str = name
        self._action: str = action
        self._additional_parameters: dict = additional_parameters

    @property
    def name(self) -> str:
        return self._name

    @property
    def action(self) -> str:
        return self._action

    @property
    def additional_parameters(self) -> dict:
        return self._additional_parameters

    def get_type(self) -> str:
        return 'button'

    def to_json(self) -> dict:
        signature, data = self._serializer.serialize(self._additional_parameters)
        return {
            **super().to_json(),
            'name': self._name,
            'action': self._action,
            ButtonOutput.PARAMETERS_FIELD: {
                ButtonOutput.DATA_FIELD: data,
                ButtonOutput.SIGNATURE_FIELD: signature
            }
        }
