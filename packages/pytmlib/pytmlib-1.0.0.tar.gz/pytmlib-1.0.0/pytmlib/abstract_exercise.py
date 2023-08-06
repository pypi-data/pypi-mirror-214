import abc
from os import getenv

from .context import Context
from .create_app import create_app
from .output import OutputBuilder as Output


class AbstractExercise(abc.ABC):
    def __new__(cls, unique_id: str, static_folder_path: str = None, *args, **kwargs):
        exercise: AbstractExercise = super().__new__(cls, *args, **kwargs)
        secret: str = getenv('PYTM_SECRET', 'b9ceb55b-4ee4-4af4-b7b0-a01c4814f4c7')
        context: Context = Context(unique_id, secret, exercise)
        exercise._context = context

        return create_app(context, static_folder_path)

    @property
    def output(self) -> Output:
        return self._context.output

    @abc.abstractmethod
    def start(self) -> Output:
        pass
