from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from lxml import etree as ET
from shapely import GeometryCollection
from shapely.geometry.base import BaseGeometry


@dataclass
class RailConnectionInfos:
    """
    Dataclass to list to list all RailConnectionInfo nodes of a value object.

    Args:
        rail_infos (List[RailConnectionInfoPoint | RailConnectionInfoLine | RailConnectionInfo]): list of all railConnectionInfo's.

    """

    rail_infos: List[RailConnectionInfoPoint | RailConnectionInfoLine | RailConnectionInfo] = field(default_factory=list)

    @staticmethod
    def from_element(element: ET.Element, object_type: str) -> Optional[RailConnectionInfos]:
        """Rail connection info factory."""
        rail_connection_infos_elements = element.findall(f".//{{*}}{object_type}")
        if len(rail_connection_infos_elements) == 0:
            return None

        # # todo: make xpath query, trackFragments are nested.....
        # if object_type != "TrackFragment":
        #     rail_connection_infos_elements = [thing for thing in element if thing.tag == "{http://www.prorail.nl/IMSpoor}" + str(object_type)]

        _out = RailConnectionInfos()
        for rail_connection_info_element in rail_connection_infos_elements:
            ref = rail_connection_info_element.get("railConnectionRef")
            at_measure = rail_connection_info_element.get("atMeasure")
            from_measure = rail_connection_info_element.get("fromMeasure")
            to_measure = rail_connection_info_element.get("toMeasure")
            direction = rail_connection_info_element.get("direction")

            if ref and at_measure and direction:
                _out.rail_infos.append(RailConnectionInfoPoint(ref, float(at_measure), direction))
            elif ref and from_measure and to_measure:
                _out.rail_infos.append(RailConnectionInfoLine(ref, float(from_measure), float(to_measure), direction))
            else:
                _out.rail_infos.append(RailConnectionInfo(ref))

        return _out

    def __iter__(self):
        for rail_info in self.rail_infos:
            yield rail_info

    def get_geometry_collection(self):
        return GeometryCollection([item.geometry for item in self.rail_infos])


@dataclass
class RailConnectionInfo:
    """
    RailConnectionInfo base object.

    Geometry and project will be set by repo.

    Args:
        ref (str): unique key (puic) to railConnection
        geometry (Optional[BaseGeometry]): geometry if line else None.
        projection (Optional[BaseGeometry]): project if point else None.

    """

    ref: str
    geometry: Optional[BaseGeometry] = field(init=False, default=None)
    projection: Optional[BaseGeometry] = field(init=False, default=None)


@dataclass
class RailConnectionInfoPoint(RailConnectionInfo):
    """
    RailConnectionInfo Point extension.

    Args:
        at_measure (float): at measure along railConnection.
        direction (): direction along railConnection.
    """

    at_measure: float
    direction: str


@dataclass
class RailConnectionInfoLine(RailConnectionInfo):
    """
    RailConnectionInfo Line extension.

    A to measure can be lower than a from measure and vice verse.

    Args:
        from_measure (float): from measure along railConnection.
        to_measure (float): from measure along railConnection.
        direction (): direction along railConnection.
    """

    from_measure: float
    to_measure: float
    direction: str
