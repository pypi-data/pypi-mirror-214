import pytest

# from imxInsights.diff.imxDiff import ImxDiff
from imxInsights.domain.imx import Imx


@pytest.mark.slow
def test_imx_parse_project_v500(get_imx_project_test_file_path, tmp_path: str):
    imx = Imx(get_imx_project_test_file_path)
    assert imx.imx_version == "5.0.0", "imx version should be 5.0.0"

    # diff = ImxDiff(imx.project.initial_situation, imx.project.new_situation)
    # dict_of_df_of_all_types = diff.pandas_dataframe_dict()
    # df_micro_nodes = diff.pandas_dataframe("MicroNode", geometry=False)
    # df_signals = diff.pandas_dataframe("Signal", geometry=True)
    # df_rail_con = diff.pandas_dataframe("RailConnection", geometry=True)
    #
    # geojson = diff.as_geojson("RailConnection")
    # diff.generate_excel("./diff.xlsx")

    # signaling_routes = imx.project.initial_situation.get_by_paths("SignalingRoute")
    #
    # rail_cons_missing = []
    # route_missing_rail_cons = []
    # possible_bug = []
    # for signaling_route in signaling_routes:
    #     for track_fragment in signaling_route.track_fragments.rail_infos:
    #         rail_con_in_data = imx.project.initial_situation.get_by_puic(track_fragment.ref)
    #         if rail_con_in_data is None:
    #             rail_cons_missing.append(track_fragment.ref)
    #             route_missing_rail_cons.append(signaling_route.puic)
    #         else:
    #             if track_fragment.geometry is None:
    #                 possible_bug.append([signaling_route.puic, track_fragment.ref])
    #                 # groningen: '304e40d3-4a1b-4583-8e54-3a55722f1748' do not have geometry.... negative measure in  input.
    #                 # leeuwarden: none
    #                 # hanzelijn: none
    #
    # route_missing_rail_cons = list(set(route_missing_rail_cons))
    # rail_cons_missing = list(set(rail_cons_missing))

    #
    # tester1 = imx.project.initial_situation.get_all_paths()
    # tester2 = imx.project.new_situation.get_all_paths()
    # all_paths = list(set([*tester1, *tester2]))
    #
    # out_dict = {}
    # for path in all_paths:
    #     print(path)
    #     df_1 = imx.project.initial_situation.get_pandas_df(path)  # "Signal"
    #     df_2 = imx.project.new_situation.get_pandas_df(path)
    #
    #     left, right = df_1.align(df_2, join="outer", axis=1)
    #     left = left.fillna("")
    #     right = right.fillna("")
    #
    #     # check same columns and same column names
    #     left_columns = list(left.columns)
    #     right_columns = list(right.columns)
    #     same_columns = left_columns == right_columns
    #
    #     # index
    #     left_index = list(left.index)
    #     right_index = list(right.index)
    #     index_both = list(set([*left_index, *right_index]))
    #
    #     index_values = ({
    #         'NewIndex': index_both,
    #         'idx': index_both
    #     })
    #     index_both_df = pd.DataFrame(index_values)
    #     index_both_df.set_index("idx", inplace=True)
    #
    #     right = right.merge(index_both_df, left_index=True, right_index=True, how='outer', sort=True)
    #     right = right.fillna("")
    #     del right['NewIndex']
    #
    #     left = left.merge(index_both_df, left_index=True, right_index=True, how='outer', sort=True)
    #     left = left.fillna("")
    #     del left['NewIndex']
    #
    #     try:
    #         diff_df = left.compare(right, align_axis=1, keep_shape=True, keep_equal=True)
    #     except Exception as e:
    #         # looks like this happens on empty dataframe...
    #         print(e)
    #
    #     def classify_row_change(row):
    #         value_1 = row['path']['self']
    #         value_2 = row['path']['other']
    #
    #         if not value_2:
    #             return "Deleted"
    #         if not value_1:
    #             return "Created"
    #         index_values = [value[0] for value in list(row.index)]
    #
    #         for item in index_values:
    #             if row[item]['self'] != row[item]['other'] and item not in ["area"]:
    #                 return "Updated"
    #         return "Unchanged"
    #
    #     def classify_area_change(row):
    #         value_1 = row['area']['self']
    #         value_2 = row['area']['other']
    #
    #         if not value_2:
    #             return "Deleted"
    #         if not value_1:
    #             return "Created"
    #
    #         if value_1 != value_2:
    #             return f"Moved: {value_1} -> {value_2}"
    #         return "Unchanged"
    #
    #
    #     diff_df['data_change'] = diff_df.apply(lambda row: classify_row_change(row), axis=1)
    #     diff_df['area_change'] = diff_df.apply(lambda row: classify_area_change(row), axis=1)
    #
    #     out_dict[path] = diff_df
    #

    #

    # custom_puic_object = imx.project.new_situation.get_by_types(
    #     ["FlankProtectionConfiguration", "ErtmsLevelCrossing", "ErtmsSignal", "ErtmsBaliseGroup", "ErtmsRoute"]
    # )

    # object_of_intrest_0 = imx.project.initial_situation.get_by_puic("b8cd3915-35e9-4d53-a47f-fc85b6d6bb2f")
    # object_of_intrest_1 = imx.project.initial_situation.get_by_puic("81cb20ca-9573-4686-b47d-f1bd9b4b6693")
    # object_of_intrest_2 = imx.project.initial_situation.get_by_puic("3ffb809f-3ad6-4089-b194-5ea47a936586")
    # illuminated_signs = imx.project.initial_situation.get_pandas_df("IlluminatedSign")

    #

    # project = imx.project
    # init_situation = imx.get_situation_repository(ImxSituationsEnum.InitialSituation)

    # should contain metadata
    # should define areax
    # count puic objects in both areas
    # count by type in both areas
    # check railConnections


# 'Signal.IlluminatedSign'

#
# def test_imx_parse_situation_v500(get_imx_project_test_file_path, tmp_path: str):
#     imx = Imx(get_imx_project_test_file_path)
#     assert imx.imx_version == "5.0.0", "imx version should be 5.0.0"
