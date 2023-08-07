from dataclasses import dataclass

from atoti_core import Coordinates, keyword_only_dataclass


@keyword_only_dataclass
@dataclass(frozen=True)
class ExternalTableCoordinates(Coordinates):
    database_name: str
    schema_name: str
    table_name: str

    @property
    def key(self) -> tuple[str, str, str]:
        return self.database_name, self.schema_name, self.table_name
