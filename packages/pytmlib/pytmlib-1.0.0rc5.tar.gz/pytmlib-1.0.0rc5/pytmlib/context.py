from typing import TYPE_CHECKING

from .output import OutputBuilder
from .serializer import Serializer

if TYPE_CHECKING:
    from .abstract_exercise import AbstractExercise


class Context:
    def __init__(self, unique_id: str, secret: str, exercise: 'AbstractExercise'):
        self._unique_id: str = unique_id
        self._secret: str = secret
        self._exercise: 'AbstractExercise' = exercise

    @property
    def secret(self) -> str:
        return self._secret

    @property
    def unique_id(self) -> str:
        return self._unique_id

    @property
    def serializer(self) -> Serializer:
        return Serializer(self._secret)

    @property
    def output(self) -> OutputBuilder:
        return OutputBuilder(self.serializer)

    @property
    def exercise(self) -> 'AbstractExercise':
        return self._exercise
