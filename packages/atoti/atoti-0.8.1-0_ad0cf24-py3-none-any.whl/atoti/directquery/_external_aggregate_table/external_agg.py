from __future__ import annotations

from collections.abc import Iterable

from ...column import Column
from .._external_column import ExternalColumn
from ._external_measure import ExternalMeasure


def agg(
    *,
    key: str,
    granular_columns: Iterable[Column],
    aggregate_columns: Iterable[ExternalColumn],
) -> ExternalMeasure:
    return ExternalMeasure(
        aggregation_key=key,
        granular_columns=[col._coordinates for col in granular_columns],
        aggregate_columns=[col._coordinates for col in aggregate_columns],
    )


def avg(
    granular_column: Column,
    /,
    *,
    sum_aggregate_column: ExternalColumn,
    count_aggregate_column: ExternalColumn,
) -> ExternalMeasure:
    return ExternalMeasure(
        aggregation_key="AVG",
        granular_columns=[granular_column._coordinates],
        aggregate_columns=[
            sum_aggregate_column._coordinates,
            count_aggregate_column._coordinates,
        ],
    )


def count(*, aggregate_column: ExternalColumn) -> ExternalMeasure:
    return ExternalMeasure(
        aggregation_key="COUNT",
        granular_columns=[],
        aggregate_columns=[aggregate_column._coordinates],
    )


def max(  # noqa: A001
    granular_column: Column, /, *, aggregate_column: ExternalColumn
) -> ExternalMeasure:
    return ExternalMeasure(
        aggregation_key="MAX",
        granular_columns=[granular_column._coordinates],
        aggregate_columns=[aggregate_column._coordinates],
    )


def min(  # noqa: A001
    granular_column: Column, /, *, aggregate_column: ExternalColumn
) -> ExternalMeasure:
    return ExternalMeasure(
        aggregation_key="MIN",
        granular_columns=[granular_column._coordinates],
        aggregate_columns=[aggregate_column._coordinates],
    )


def sum(  # noqa: A001
    granular_column: Column, /, *, aggregate_column: ExternalColumn
) -> ExternalMeasure:
    return ExternalMeasure(
        aggregation_key="SUM",
        granular_columns=[granular_column._coordinates],
        aggregate_columns=[aggregate_column._coordinates],
    )


def sum_product(
    granular_columns: Iterable[Column], /, *, aggregate_column: ExternalColumn
) -> ExternalMeasure:
    return ExternalMeasure(
        aggregation_key="ATOTI_SUM_PRODUCT",
        granular_columns=[col._coordinates for col in granular_columns],
        aggregate_columns=[aggregate_column._coordinates],
    )
