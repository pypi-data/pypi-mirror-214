from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Literal, Optional

from atoti_core import (
    ColumnCoordinates,
    Condition,
    Constant,
    CoordinatesLike,
    get_coordinates,
    keyword_only_dataclass,
)

from ..._external_table_coordinates import ExternalTableCoordinates
from ..._table_coordinates import TableCoordinates
from .._external_column_coordinates import ExternalColumnCoordinates
from ._external_measure import ExternalMeasure

_Filter = Condition[
    ExternalColumnCoordinates,
    Literal["eq", "isin"],
    Constant,
    Optional[Literal["and"]],
]


@keyword_only_dataclass
@dataclass(frozen=True, init=False)
class ExternalAggregateTable:
    """An external aggregate table is a table in the external database containing aggregated data.

    It is used to feed some partial providers faster.
    For instance, if the same aggregate query is run every day to feed the same partial provider with the same data, the result of the query can instead be stored into an external table and this table used to feed the provider every day.
    """

    _granular_table: TableCoordinates
    _aggregate_table: ExternalTableCoordinates
    _mapping: Mapping[ColumnCoordinates, ExternalColumnCoordinates]
    _measures: tuple[ExternalMeasure, ...]
    _filter: Optional[_Filter] = None

    def __init__(
        self,
        *,
        granular_table: CoordinatesLike[TableCoordinates],
        aggregate_table: CoordinatesLike[ExternalTableCoordinates],
        mapping: Mapping[
            CoordinatesLike[ColumnCoordinates],
            CoordinatesLike[ExternalColumnCoordinates],
        ],
        measures: Iterable[ExternalMeasure],
        filter: Optional[_Filter] = None,  # noqa: A002
    ):
        """Initialize an external aggregate table.

        Args:
            granular_table: The table containing the granular facts, i.e. the base table of which the data have been aggregated into the aggregate table.
            aggregate_table: The aggregate table.
            mapping: The mapping from one column in *granular_table* (or a table joined to it) to the corresponding column in *aggregate_table*.
            measures: The measures provided by the *aggregate_table*.
            filter: The condition describing which facts have been pre-aggregated.
        """
        object.__setattr__(self, "_granular_table", get_coordinates(granular_table))
        object.__setattr__(self, "_aggregate_table", get_coordinates(aggregate_table))
        object.__setattr__(
            self,
            "_mapping",
            {
                get_coordinates(granular_column): get_coordinates(aggregate_column)
                for granular_column, aggregate_column in mapping.items()
            },
        )
        object.__setattr__(self, "_measures", tuple(measures))
        object.__setattr__(self, "_filter", filter)
