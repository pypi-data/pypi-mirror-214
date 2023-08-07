from os import path
from tarfile import TarInfo
from tarfile import open
from tempfile import TemporaryFile
from typing import List
from typing import Union


class Archiver:
    EXCLUDES_FOLDERS: List[str] = [
        '.git',
        '.idea',
        '__pycache__',
        'venv'
    ]

    def __init__(self, base_path: str):
        self._base_path: str = base_path

    def create_tar(self) -> bytes:
        with TemporaryFile() as temp_archive:
            with open(mode='w|gz', fileobj=temp_archive) as tar:
                tar.add(name=self._base_path, recursive=True, filter=self._filter_tar_member)
            temp_archive.seek(0)
            return temp_archive.read()

    def _filter_tar_member(self, info: TarInfo) -> Union[TarInfo, None]:
        basename: str = path.basename(info.path)
        if info.isdir() and basename in self.EXCLUDES_FOLDERS:
            return None
        info.name = info.name[2:]
        return info
