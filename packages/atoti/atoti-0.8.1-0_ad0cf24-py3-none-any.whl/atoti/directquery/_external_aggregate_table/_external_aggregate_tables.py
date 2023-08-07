from collections.abc import Iterable, Mapping
from typing import Optional

from atoti_core import DelegateMutableMapping

from ..._java_api import JavaApi
from .external_aggregate_table import ExternalAggregateTable


class ExternalAggregateTables(DelegateMutableMapping[str, ExternalAggregateTable]):
    def __init__(
        self,
        *,
        java_api: JavaApi,
    ):
        self._java_api = java_api

    def _delete_keys(self, keys: Optional[Iterable[str]] = None, /) -> None:
        self._java_api.remove_external_aggregate_tables(keys)
        self._java_api.refresh()

    def _update(self, other: Mapping[str, ExternalAggregateTable]) -> None:
        self._java_api.set_external_aggregate_tables(other)
        self._java_api.refresh()

    def _get_underlying(self) -> dict[str, ExternalAggregateTable]:
        return self._java_api.get_external_aggregate_tables()
