from dataclasses import dataclass

from .coordinates import Coordinates


@dataclass(frozen=True)
class HierarchyCoordinates(Coordinates):  # pylint: disable=keyword-only-dataclass
    dimension_name: str
    hierarchy_name: str

    @property
    def key(self) -> tuple[str, str]:
        return self.dimension_name, self.hierarchy_name

    def __repr__(self) -> str:
        return f"h[{self.key}]"
