from typing import List
from typing import Union

from .abstract import AbstractOutput
from .table_cell import TableCell
from ..latex import Latex


class TableOutput(AbstractOutput):
    def __init__(self, index: int, data: List[List[Union[str, int, float, Latex, TableCell]]]):
        super().__init__(index)

        self._data: List[List[TableCell]] = list(map(self.map_table_row_to_cells, data))

    @property
    def data(self) -> List[List[TableCell]]:
        return self._data

    def get_type(self) -> str:
        return 'table'

    def to_json(self) -> dict:
        return {
            **super().to_json(),
            'data': list(map(self.map_table_row_to_json, self._data))
        }

    @staticmethod
    def map_table_row_to_cells(row: List[Union[str, int, float, Latex, TableCell]]) -> List[TableCell]:
        return list(map(TableCell.to_table_cell, row))

    @staticmethod
    def map_table_row_to_json(row: List[TableCell]) -> List[dict]:
        return list(map(lambda cell: cell.to_json(), row))
