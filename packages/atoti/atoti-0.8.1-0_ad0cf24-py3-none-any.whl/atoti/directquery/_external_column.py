from __future__ import annotations

from typing import Literal, Optional, overload

from atoti_core import (
    Condition,
    Constant,
    ConstantValue,
    IsinCondition,
    OperandConvertibleWithCoordinates,
)

from ._external_column_coordinates import ExternalColumnCoordinates


class ExternalColumn(OperandConvertibleWithCoordinates[ExternalColumnCoordinates]):
    def __init__(
        self,
        name: str,
        /,
        *,
        table_name: str,
    ) -> None:
        super().__init__()

        self._name = name
        self._table_name = table_name

    @property
    def name(self) -> str:
        """The name of the column."""
        return self._name

    @property
    def _coordinates(self) -> ExternalColumnCoordinates:
        return ExternalColumnCoordinates(
            table_name=self._table_name, column_name=self.name
        )

    @property
    def _operation_operand(self) -> ExternalColumnCoordinates:
        return self._coordinates

    @overload
    def isin(
        self, *elements: ConstantValue
    ) -> Condition[ExternalColumnCoordinates, Literal["isin"], Constant, None]:
        ...

    @overload
    def isin(
        self, *elements: Optional[ConstantValue]
    ) -> Condition[
        ExternalColumnCoordinates, Literal["isin"], Optional[Constant], None
    ]:
        ...

    def isin(
        self, *elements: Optional[ConstantValue]
    ) -> Condition[
        ExternalColumnCoordinates, Literal["isin"], Optional[Constant], None
    ]:
        """Return a condition evaluating to ``True`` if a column element is among the given elements and ``False`` otherwise.

        ``table["City"].isin("Paris", "New York")`` is equivalent to ``(table["City"] == "Paris") | (table["City"] == "New York")``.

        Args:
            elements: One or more elements on which the column should be.
        """
        return IsinCondition(
            subject=self._operation_operand,
            elements=tuple(
                None if element is None else Constant(element) for element in elements
            ),
        )
