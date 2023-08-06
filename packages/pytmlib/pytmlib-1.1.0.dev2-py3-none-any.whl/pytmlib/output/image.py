from base64 import b64encode
from mimetypes import guess_type
from typing import Optional

from .abstract import AbstractOutput


class ImageOutput(AbstractOutput):
    def __init__(self, index: int, path: str, description: str = None):
        super().__init__(index)

        self._path: str = path
        self._description: str = description

    @property
    def path(self) -> str:
        return self._path

    @property
    def description(self) -> str:
        return self._description

    def get_type(self) -> str:
        return 'image'

    def to_json(self) -> dict:
        return {
            **super().to_json(),
            'src': self._get_data_url(),
            'description': self._description
        }

    def _get_data_url(self) -> str:
        guessed_type: Optional[str] = guess_type(self._path)[0]
        mimetype: str = guessed_type if guessed_type else 'application/octet-stream'
        with open(self._path, 'rb') as image:
            data: bytes = image.read()
            b64_encoded_data: str = b64encode(data).decode('utf-8')
            return 'data:%s;base64,%s' % (mimetype, b64_encoded_data)
