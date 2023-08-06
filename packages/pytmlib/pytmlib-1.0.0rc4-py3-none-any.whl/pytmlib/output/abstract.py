from abc import ABC
from abc import abstractmethod
from uuid import UUID
from uuid import uuid5

ID_NAMESPACE_UUID: UUID = UUID('d55c3931-7f92-4fcc-bca0-decc94749704')


class AbstractOutput(ABC):
    def __init__(self, index: int):
        self._index: int = index
        self._id: UUID = uuid5(ID_NAMESPACE_UUID, str(index))

    @property
    def index(self) -> int:
        return self._index

    @property
    def id(self) -> UUID:
        return self._id

    @abstractmethod
    def get_type(self) -> str:
        pass

    def to_json(self) -> dict:
        return {
            'id': self.id
        }
