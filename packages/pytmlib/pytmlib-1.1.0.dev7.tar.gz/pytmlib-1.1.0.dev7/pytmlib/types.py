from typing import Callable

from .output import OutputBuilder

Entrypoint = Callable[..., OutputBuilder]
