import pytest

from imxInsights import Imx


@pytest.fixture(scope="module")
def imx_test_file(get_imx_project_test_file_path) -> Imx:
    return Imx(get_imx_project_test_file_path)
