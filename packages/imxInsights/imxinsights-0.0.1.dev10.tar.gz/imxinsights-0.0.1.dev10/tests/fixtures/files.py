import pytest

from tests.helpers import sample_path


@pytest.fixture(scope="module")
def get_imx_project_test_file_path() -> str:
    # return sample_path("U_O_D-003122_ERTMS_Noordelijke_lijnen_TVP01_Leeu_01_20230417_compleet_concept_imx500.xml")
    return sample_path("IMX_E-R50008_EKB_Perceel_2_V1.3_5_0_0_test_Niki.xml")
    # return sample_path("U_totaal ENL_20230501_compleet_imx500.xml")
    # return sample_path("Groningen_verrijkt.xml")
    # return sample_path("leeuwarden_verrijkt.xml")
    # return sample_path("Hanzelijn_verrijkt_latest.xml")
    # return sample_path("O_RVTOv2.0_20230602145547.xml")
