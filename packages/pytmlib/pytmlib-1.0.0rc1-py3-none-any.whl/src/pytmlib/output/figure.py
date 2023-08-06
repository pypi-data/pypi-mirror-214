from base64 import b64encode
from io import BytesIO
from mimetypes import guess_type
from typing import Optional

from matplotlib.figure import Figure

from .abstract import AbstractOutput


class FigureOutput(AbstractOutput):
    DEFAULT_DPI = 300

    def __init__(self, index: int, figure: Figure, description: str = None, dpi: int = None, as_png: bool = None):
        super().__init__(index)

        self._figure: Figure = figure
        self._description: str = description
        self._dpi: int = dpi if dpi is not None else self.DEFAULT_DPI
        self._as_png: bool = as_png if as_png is not None else False

    @property
    def figure(self) -> Figure:
        return self._figure

    @property
    def description(self) -> str:
        return self._description

    @property
    def dpi(self) -> int:
        return self._dpi

    @property
    def as_png(self) -> bool:
        return self._as_png

    def get_type(self) -> str:
        return 'figure'

    def to_json(self) -> dict:
        return {
            **super().to_json(),
            'src': self._get_data_url(),
            'description': self._description
        }

    def _get_format(self) -> str:
        return 'png' if self._as_png else 'svg'

    def _get_data_url(self) -> str:
        guessed_type: Optional[str] = guess_type('image.' + self._get_format())[0]
        mimetype: str = guessed_type if guessed_type else 'application/octet-stream'
        data: bytes = self._save_figure()
        b64_encoded_data: str = b64encode(data).decode('utf-8')
        return 'data:%s;base64,%s' % (mimetype, b64_encoded_data)

    def _save_figure(self) -> bytes:
        buffer: BytesIO = BytesIO()
        self._figure.savefig(fname=buffer,
                             transparent=True,
                             format=self._get_format(),
                             dpi=self._dpi,
                             pad_inches=0,
                             bbox_inches='tight')
        buffer.seek(0)
        return buffer.read()
