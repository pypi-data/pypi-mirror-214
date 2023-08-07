from dataclasses import dataclass

from atoti_core import Coordinates


@dataclass(frozen=True)
class ExternalColumnCoordinates(Coordinates):  # pylint: disable=keyword-only-dataclass
    table_name: str
    column_name: str

    @property
    def key(self) -> tuple[str, str]:
        return self.table_name, self.column_name

    def __repr__(self) -> str:
        return f"""t["{self.table_name}"]["{self.column_name}"]"""
