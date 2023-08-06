from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List, Optional

from shapely.geometry.base import BaseGeometry

from imxInsights.diff.areaStatusEnum import AreaStatusEnum
from imxInsights.diff.change import Change, ChangeList
from imxInsights.diff.diffStatusEnum import DiffStatusEnum
from imxInsights.domain.area.imxProjectArea import ImxProjectArea
from imxInsights.repo.imxRepo import ImxObject, ObjectTree
from imxInsights.utils.log import logger
from imxInsights.utils.shapely_helpers import (
    gml_linestring_to_shapely,
    gml_point_to_shapely,
)


class ImxPropertyCompare:
    @classmethod
    def compare(cls, a: dict[str, str] | None, b: dict[str, str] | None) -> ChangeList:
        """
        Compares two flat dictionaries, detects changes & IMX specific changes (location).

        Args:
            a (Union[dict[str, str], None]): First dictionary to be compared.
            b (Union[dict[str, str], None]): Second dictionary to be compared.

        Returns:
            (ChangeList): A ChangeList object representing the changes between the two dictionaries.

        """
        keys = set(a.keys() if a is not None else []).union(b.keys() if b is not None else [])
        assert len(keys) > 0, "should find at lease 1 key in to compare"
        props = [cls._compare_property(key, a, b) for key in sorted(keys)]

        base_status = DiffStatusEnum.CREATED if a is None else DiffStatusEnum.DELETED if b is None else DiffStatusEnum.NO_CHANGE

        return ChangeList(status=base_status, props=props)

    @classmethod
    def _compare_property(cls, key: str, a: dict[str, str] | None, b: dict[str, str] | None) -> Change:
        """
        Compares a single key in two dictionaries and returns a Change object representing the changes.

        Args:
            key (str): The key to be compared.
            a (Union[dict[str, str], None]): A dictionary to be compared.
            b (Union[dict[str, str], None]): A dictionary to be compared.

        Returns:
            (Change): A Change object representing the changes between the two values of the key.

        """
        val_a = a[key] if a is not None and key in a else None
        val_b = b[key] if b is not None and key in b else None

        def make_change(status: DiffStatusEnum) -> Change:
            return Change(key=key, status=status, a=val_a, b=val_b)

        if val_a is None:
            return make_change(DiffStatusEnum.CREATED)

        if b is None or key not in b or val_b is None:
            return make_change(DiffStatusEnum.DELETED)

        if val_a == val_b:
            return make_change(DiffStatusEnum.NO_CHANGE)

        if ".coordinates" in key:
            return make_change(cls._compare_gml_coordinates(key, val_a, val_b))

        return make_change(DiffStatusEnum.UPDATED)

    @classmethod
    def _compare_gml_coordinates(cls, key: str, coords_a: str, coords_b: str) -> DiffStatusEnum:
        """
        Compares two sets of coordinates and returns the status of the comparison.

        Args:
            key (str): The key of the coordinates to be compared.
            coords_a (str): The first set of coordinates.
            coords_b (str): The second set of coordinates.

        Returns:
            (DiffStatusEnum): A DiffStatus object representing the status of the comparison.

        """
        assert coords_a is not None and coords_b is not None
        if "Point.coordinates" in key:
            geom_a = gml_point_to_shapely(coords_a)
            geom_b = gml_point_to_shapely(coords_b)
        elif "LineString.coordinates" in key:
            geom_a = gml_linestring_to_shapely(coords_a)
            geom_b = gml_linestring_to_shapely(coords_b)
        else:
            logger.warning(f"Cannot determine if {key} is data upgrade, assuming changed if not exactly equal")
            return DiffStatusEnum.NO_CHANGE if coords_a == coords_b else DiffStatusEnum.UPDATED

        return cls._compare_geometry(geom_a, geom_b)

    @classmethod
    def _compare_geometry(cls, a: BaseGeometry, b: BaseGeometry, tolerance: Optional[float] = 4e-4) -> DiffStatusEnum:
        """
        Compares two geometries.

        Args:
            a (BaseGeometry): The first geometry object to compare.
            b (BaseGeometry): The second geometry object to compare.
            tolerance (Optional[float]): the tolerance level for determining if two geometries are equal, defaults to 4e-4.

        Returns:
            (DiffStatusEnum): The status of the comparison, whether the geometries are updated, not changed, or upgraded.

        """
        # refactor abracadabra below
        match (a.has_z, b.has_z):
            case (True, True) | (False, False):
                z_status = 0
            case (True, False):
                z_status = -1
            case (False, True):
                z_status = 1

        if a.equals_exact(b, tolerance=tolerance) and z_status >= 0:
            return DiffStatusEnum.NO_CHANGE if z_status == 0 else DiffStatusEnum.UPGRADED

        return DiffStatusEnum.UPDATED


@dataclass(frozen=True)
class ImxObjectCompare:
    """
    Represents the comparison of two ImxObjects.

    Args:
        a (ImxObject): The first ImxObject to compare.
        b (ImxObject): The second ImxObject to compare.
        changes (ChangeList): The list of changes between the two objects.

    """

    a: ImxObject | None
    b: ImxObject | None
    changes: ChangeList = field(init=False)

    def __post_init__(self):
        assert self.a is not None or self.b is not None, "Must have at least one object"
        if self.a is not None:
            assert self.a.can_compare(self.b)

        a_props = self.a.properties if self.a is not None else None
        b_props = self.b.properties if self.b is not None else None
        changes = ImxPropertyCompare.compare(a_props, b_props)
        super().__setattr__("changes", changes)

    def __repr__(self) -> str:
        return (
            f"<ImxObjectCompare {self.path} name='{self.name}' puic={self.puic} " f"area_status={self.area_status} diff_status={self.diff_status}/>"
        )

    def __str__(self) -> str:
        parts = [self.path, self.name, str(self.area_status), self.puic]
        return "; ".join((part for part in parts if part is not None))

    @property
    def puic(self) -> str:
        """Returns the puic of the ObjectComparison."""
        return self._any().puic

    @property
    def tag(self) -> str:
        """Returns the tag of the ObjectComparison."""
        return self._any().tag

    @property
    def path(self) -> str:
        """Returns the path of the ObjectComparison."""
        return self._any().path

    @property
    def diff_status(self) -> DiffStatusEnum:
        """Returns the diff status of the ObjectComparison."""
        return self.changes.status

    @property
    def name(self) -> str | None:
        """Returns the Combined name, '<NewName> (<OldName>)' or just the '<Name>' if same."""
        if self.only_one:
            name = self._any().name
            return name if name is not None else None

        assert self.a is not None and self.b is not None
        a = self.a.name
        b = self.b.name
        return f"*{b} {f'({a})' if len(a) > 0 else ''}".rstrip() if a != b else a

    @property
    def area_a(self) -> ImxProjectArea | None:
        """Returns the area of `a`."""
        return self.a.area if self.a is not None else None

    @property
    def area_b(self) -> ImxProjectArea | None:
        """Returns the area of `b`."""
        return self.b.area if self.b is not None else None

    @property
    def area_status(self) -> AreaStatusEnum:
        """Determines the status of the comparison of two ImxObjects based on their areas."""
        if self.area_a is None and self.a is not None or self.area_b is None and self.b is not None:
            return AreaStatusEnum.INDETERMINATE

        elif self.area_a is None and self.area_b is not None:
            return AreaStatusEnum.CREATED

        elif self.area_a is not None and self.area_b is None:
            return AreaStatusEnum.DELETED

        elif self.area_a.name == self.area_b.name:
            return AreaStatusEnum.NO_CHANGE

        elif self.area_a.name != self.area_b.name:
            return AreaStatusEnum.MOVED

        raise ValueError(f"Unknown area combination: A={self.area_a}, B={self.area_b}")

    @property
    def only_one(self) -> bool:
        """Returns a boolean value indicating whether only one object is present."""
        return (self.a is None) ^ (self.b is None)

    def _any(self) -> ImxObject:
        if self.a is not None:
            return self.a

        assert self.b is not None, "Should have a or b"
        return self.b

    @staticmethod
    def object_tree_factory(a: ObjectTree, b: ObjectTree) -> Iterable[ImxObjectCompare]:
        """
        Compares two object trees and returns an iterable of ObjectComparison instances representing the comparison between the two trees.

        Args:
            a (ObjectTree): The second object tree to compare.
            b (ObjectTree): The second object tree to compare.

        Returns:
            (Iterable[ImxObjectCompare]): An iterable of ObjectComparison instances representing the comparison between the two trees.

        """
        all_keys = a.keys.union(b.keys)
        for key in all_keys:
            match_a = a.find(key)
            match_b = b.find(key)
            yield ImxObjectCompare(match_a, match_b)

    @staticmethod
    def imx_object_list_factory(a: List[ImxObject], b: List[ImxObject]) -> Iterable[ImxObjectCompare]:
        """
        Generates `ObjectComparison` instances by comparing two lists of `ImxObject` instances.

        If an `ImxObject` instance is present in both lists, it is compared, otherwise it is compared to `None`.

        Args:
            a (List[ImxObject]): The first list of `ImxObject` instances to compare.
            b (List[ImxObject]): The second list of `ImxObject` instances to compare.

        Returns:
            (Iterable[ImxObjectCompare]): An iterable of `ObjectComparison` instances.

        """
        dict_a = {f"{item.puic}": item for item in a}
        dict_b = {f"{item.puic}": item for item in b}
        for puic, value in dict_a.items():
            if puic in dict_b.keys():
                yield ImxObjectCompare(value, dict_b[puic])
            else:
                yield ImxObjectCompare(value, None)

        for puic, value in dict_b.items():
            if puic not in dict_a.keys():
                yield ImxObjectCompare(value, None)
