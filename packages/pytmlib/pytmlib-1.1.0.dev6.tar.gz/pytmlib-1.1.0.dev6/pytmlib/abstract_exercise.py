import abc
import logging
import os
import uuid
from typing import List
from typing import Tuple

from .context import Context
from .create_app import create_app
from .decorators import ENTRYPOINT_MARKER
from .output import OutputBuilder as Output
from .types import Entrypoint


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

    def get_entrypoints(self) -> List[Entrypoint]:
        entrypoints = []
        for name in dir(self):
            func = getattr(self, name)

            if hasattr(func, ENTRYPOINT_MARKER):
                entrypoints.append(func)

        return entrypoints

    @staticmethod
    def _get_secret() -> Tuple[str, bool]:
        hostname: str = os.getenv('HOSTNAME', os.name)
        fallback: uuid = uuid.uuid5(uuid.NAMESPACE_DNS, hostname)
        secret: str = os.getenv('PYTM_SECRET')
        use_fallback: bool = secret is None

        return str(fallback) if use_fallback else secret, use_fallback
