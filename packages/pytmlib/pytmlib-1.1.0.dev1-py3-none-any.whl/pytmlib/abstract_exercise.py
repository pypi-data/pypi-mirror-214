import abc
import logging
import os
import typing
import uuid

from .context import Context
from .create_app import create_app
from .output import OutputBuilder as Output

if typing.TYPE_CHECKING:
    from .output import OutputBuilder


class AbstractExercise(abc.ABC):
    def __new__(cls, unique_id: str, static_folder_path: str = None, *args, **kwargs):
        exercise: AbstractExercise = super().__new__(cls, *args, **kwargs)

        secret, fallback = AbstractExercise._get_secret()
        context: Context = Context(unique_id, secret, exercise)

        exercise._context = context

        if fallback:
            logging.warning('missing PYTM_SECRET environment variable')

        return create_app(context, static_folder_path)

    @property
    def output(self) -> Output:
        return self._context.output

    @abc.abstractmethod
    def start(self) -> Output:
        pass

    def entrypoints(self) -> typing.List[typing.Callable[..., 'OutputBuilder']]:
        return [
            self.start
        ]

    @staticmethod
    def _get_secret() -> typing.Tuple[str, bool]:
        hostname: str = os.getenv('HOSTNAME', os.name)
        fallback: uuid = uuid.uuid5(uuid.NAMESPACE_DNS, hostname)
        secret: str = os.getenv('PYTM_SECRET')
        use_fallback: bool = secret is None

        return str(fallback) if use_fallback else secret, use_fallback
