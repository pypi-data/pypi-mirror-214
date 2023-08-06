from collections import OrderedDict
from typing import Dict, List, Optional

import pandas as pd

from imxInsights.diff.compair import ImxObjectCompare
from imxInsights.repo.imxRepo import SituationRepo
from imxInsights.utils.shapely_geojson import (
    GeoJsonFeature,
    GeoJsonFeatureCollection,
    dumps,
)
from imxInsights.utils.shapely_helpers import ShapelyTransform


class ImxDiff:
    """
    Calculated difference between two imx situations.

    Args:
        situation_repo_1 (SituationRepo):
        situation_repo_2 (SituationRepo):

    """

    def __init__(self, situation_repo_1: SituationRepo, situation_repo_2: SituationRepo):
        self.situation_repo_1 = situation_repo_1
        self.situation_repo_2 = situation_repo_2
        self._diff = list(ImxObjectCompare.object_tree_factory(self.situation_repo_1.tree, self.situation_repo_2.tree))

    def _filter_by_types_or_path(self, object_type_or_path: str) -> List[ImxObjectCompare]:
        search = "path" if "." in object_type_or_path else "tag"
        return [item for item in self._diff if item.__getattribute__(search) == object_type_or_path]

    @staticmethod
    def _create_record_dict(item, geometry: Optional[bool] = False, compact_view: Optional[bool] = True) -> Dict:
        def _get_areas(item: ImxObjectCompare):
            area_a = ""
            area_b = ""

            if item.area_status.name == "INDETERMINATE":
                area_a = "INDETERMINATE"
                area_b = "INDETERMINATE"

            else:
                if item.a is not None:
                    area_a = item.a.area.name
                if item.b is not None:
                    area_b = item.b.area.name
            return area_a, area_b

        def _get_parent(item: ImxObjectCompare):
            parent = ""
            if hasattr(item.a, "parent") and hasattr(item.b, "parent"):
                if item.a.parent is not None and item.b.parent is not None:
                    if item.a.parent.puic != item.b.parent.puic:
                        parent = f"{item.a.parent.puic}->{item.b.parent.puic}"
                    elif item.diff_status.value == "Created":
                        parent = f"{item.b.parent.puic}"
                    else:
                        parent = f"{item.a.parent.puic}"
            return parent

        def _get_geometry(item: ImxObjectCompare):
            geometry_dict = {}
            if geometry is not None:
                if item.a is not None and item.a.shapely is not None:
                    geometry_dict["geometry_a"] = item.a.shapely
                else:
                    geometry_dict["geometry_a"] = None

                if item.b is not None and item.b.shapely is not None:
                    geometry_dict["geometry_b"] = item.b.shapely
                else:
                    geometry_dict["geometry_b"] = None
            return geometry_dict

        area_a, area_b = _get_areas(item)
        parent = _get_parent(item)
        geometry_dict = _get_geometry(item)

        props = {
            "puic": item.puic,
            "path": item.path,
            "tag": item.tag,
            "area_a": area_a,
            "area_b": area_b,
            "area_status": item.area_status.name,
            "diff_status": item.diff_status.name,
        }

        imx_props = item.changes.to_dict(compact=compact_view)
        # if compact make nested dict flat....

        if "@puic" in imx_props.keys():
            del imx_props["@puic"]

        return props | imx_props | {"parent": parent} | geometry_dict

    def _get_all_as_record_dict_path_is_key(self, geometry: Optional[bool] = False) -> OrderedDict[str, List[Dict]]:
        record_dict = OrderedDict()

        for item in self._diff:
            record = self._create_record_dict(item, geometry)

            if item.path in record_dict.keys():
                record_dict[item.path].append(record)
            else:
                record_dict[item.path] = [record]

        return record_dict

    @staticmethod
    def _get_dataframe_from_records(records: List[Dict]):
        df = pd.DataFrame.from_records(records)
        df["index"] = df["puic"]
        df.set_index("index", inplace=True)
        df = df.fillna("")
        return df

    def pandas_dataframe_dict(self, geometry: Optional[bool] = False) -> Dict[str, pd.DataFrame]:
        """
        Returns a dictionary of all difference as pandas dataframe, key is path of imx object.

        Args:
            geometry: boolean if True include wkt_hex.

        Returns
            dict of all object pandas dataframes.
        """
        return {key: self._get_dataframe_from_records(value) for key, value in self._get_all_as_record_dict_path_is_key(geometry).items()}

    def pandas_dataframe(self, object_type_or_path: str = None, geometry: Optional[bool] = False) -> pd.DataFrame:
        """
        Returns difference as pandas dataframe.

        Args:
            object_type_or_path: imx object type or imx path.
            geometry: boolean if True include shapely geometry.

        Returns:
            pandas dataframes with all references.

        """
        return self._get_dataframe_from_records(
            [self._create_record_dict(item, geometry) for item in self._filter_by_types_or_path(object_type_or_path)]
        )

    def generate_excel(self, file_path: str) -> None:
        """
        Generates Excel file with all difference.

        Args:
            file_path: output file path

        """
        record_dict = self.pandas_dataframe_dict()

        writer = pd.ExcelWriter(file_path, engine="xlsxwriter")
        workbook = writer.book

        worksheet_info = workbook.add_worksheet("info")
        worksheet_info.set_column(0, 0, 25)
        worksheet_info.set_column(1, 1, 150)

        for key, value in sorted(record_dict.items()):
            df = pd.DataFrame.from_records(value)
            df["A"] = pd.Categorical(df.diff_status, categories=["CREATED", "UPDATED", "DELETED", "NO_CHANGE"])

            if "Location.GeographicLocation.@dataAcquisitionMethod" in df.columns:
                df = df.sort_values(
                    by=["Location.GeographicLocation.@dataAcquisitionMethod", "area_b"], ascending=[True, False], na_position="first", inplace=False
                )
            else:
                df = df.sort_values(by=["area_b"], ascending=[True], na_position="first", inplace=False)

            sheet_name = f"{key[:14]}...{key[-14:]}" if len(key) > 30 else key
            df.to_excel(writer, sheet_name=sheet_name)
            worksheet = writer.sheets[sheet_name]

            # Get the dimensions of the dataframe.
            (max_row, max_col) = df.shape

            # Make the columns wider for clarity.
            worksheet.set_column(0, max_col - 1, 12)

            # Set the autofilter.
            worksheet.autofilter(0, 0, max_row, max_col - 1)

            worksheet.autofit()
            worksheet.freeze_panes(1, 0)

        writer.close()

    def as_geojson(self, object_type_or_path: str) -> str:
        """
        Returns a geojson of the difference.

        Args:
            object_type_or_path:

        Returns:
            geojson string

        """
        tester = self._filter_by_types_or_path(object_type_or_path)
        features = []
        for item in tester:
            difference_dict = item.changes.to_dict()
            if item.diff_status.value == "DELETED":
                features.append(
                    GeoJsonFeature(
                        geometry_list=[ShapelyTransform.rd_to_wgs(item.a.shapely)],
                        properties=difference_dict | {"Diff_status": item.diff_status.value},
                    )
                )
            elif item.diff_status.value == "CREATED":
                features.append(
                    GeoJsonFeature(
                        geometry_list=[ShapelyTransform.rd_to_wgs(item.b.shapely)],
                        properties=difference_dict | {"Diff_status": item.diff_status.value},
                    )
                )

            else:
                features.append(
                    GeoJsonFeature(
                        geometry_list=[ShapelyTransform.rd_to_wgs(item.a.shapely)],
                        properties=difference_dict | {"Diff_status": item.diff_status.value},
                    )
                )
                features.append(
                    GeoJsonFeature(
                        geometry_list=[ShapelyTransform.rd_to_wgs(item.b.shapely)],
                        properties=difference_dict | {"Diff_status": item.diff_status.value},
                    )
                )
        feature_collection = GeoJsonFeatureCollection(geojson_features=features)
        geojson_str = dumps(feature_collection)

        return geojson_str

    def generate_geojson_dict(self) -> Dict[str, str]:
        """
        Generates all geojson of the difference.

        Todo:
            implement

        """
        raise NotImplementedError
