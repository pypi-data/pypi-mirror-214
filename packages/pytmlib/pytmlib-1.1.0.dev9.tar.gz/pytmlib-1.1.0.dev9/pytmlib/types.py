from typing import Callable

from .output import OutputBuilder

Action = Callable[..., OutputBuilder]
