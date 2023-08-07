from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TypeVar

from atoti_core import HasCoordinates, ReprJson, ReprJsonable

from .._external_table_coordinates import ExternalTableCoordinates
from ..type import DataType
from ._external_column import ExternalColumn


class ExternalTable(HasCoordinates[ExternalTableCoordinates], ReprJsonable):
    _coords: ExternalTableCoordinates

    _database_key: str

    types: Mapping[str, DataType]
    """Mapping from the name of each column to their type."""

    def __init__(
        self,
        *,
        _coordinates: ExternalTableCoordinates,
        _database_key: str,
        types: Mapping[str, DataType],
    ) -> None:
        object.__setattr__(self, "_coords", _coordinates)
        object.__setattr__(self, "_database_key", _database_key)
        object.__setattr__(self, "types", types)

    def _repr_json_(self) -> ReprJson:
        data = {name: str(datatype) for name, datatype in self.types.items()}
        return data, {"expanded": True, "root": self._coordinates.table_name}

    @property
    def name(self) -> str:
        """Name of the table."""
        return self._coordinates.table_name

    @property
    def _coordinates(self) -> ExternalTableCoordinates:
        return self._coords

    @property
    def columns(self) -> Sequence[str]:
        """Columns of the table."""
        return list(self.types)

    def __getitem__(self, column_name: str, /) -> ExternalColumn:
        return ExternalColumn(
            column_name,
            table_name=self.name,
        )


ExternalTableT = TypeVar("ExternalTableT", bound=ExternalTable, covariant=True)
