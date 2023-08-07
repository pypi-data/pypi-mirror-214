from collections.abc import Sequence
from dataclasses import dataclass

from atoti_core import ColumnCoordinates, keyword_only_dataclass

from .._external_column_coordinates import ExternalColumnCoordinates


@keyword_only_dataclass
@dataclass(frozen=True)
class ExternalMeasure:
    """Links the aggregated columns to their result."""

    aggregation_key: str
    granular_columns: Sequence[ColumnCoordinates]
    aggregate_columns: Sequence[ExternalColumnCoordinates]
