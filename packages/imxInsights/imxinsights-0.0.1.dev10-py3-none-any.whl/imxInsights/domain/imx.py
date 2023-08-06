from pathlib import Path
from typing import Optional

from imxInsights.domain.models.imxEnums import ImxSituationsEnum
from imxInsights.domain.models.imxSituations import ImxProject, ImxSituation
from imxInsights.utils.log import logger
from imxInsights.utils.xml_helpers import XmlFile


class Imx:
    """
    Imx main object is used as an entry point for imx files.

    Args:
        imx_file_path (str): File path of the IMX file.

    Attributes:
        situation (Optional[ImxSituation]): The situation of an IMX file if present.
        project (Optional[ImxProject]): The ImxProject of an IMX file if present.
    """

    def __init__(self, imx_file_path: str):
        logger.info(f"Loading file {imx_file_path}")

        self.file_path = Path(imx_file_path)
        self._xml_file = XmlFile(self.file_path)
        self._imx_version: str = self._xml_file.root.find("[@imxVersion]").attrib["imxVersion"]
        logger.info(f"IMX version: {self.imx_version}")

        self.situation: Optional[ImxSituation] = None
        self.project: Optional[ImxProject] = None
        if self._xml_file.root.find(".//{*}Project") is not None:
            self.project = ImxProject(self._xml_file)
        else:
            self.situation = ImxSituation(self._xml_file)
            raise NotImplementedError

        logger.info("IMX parsed, DONE!")

    @property
    def imx_version(self) -> str:
        """Returns the IMX version of the file, *read only property*."""
        return self._imx_version

    def get_situation_repository(self, situation_type: ImxSituationsEnum) -> Optional[ImxSituation]:
        """
        Get a specific situation repository  from an IMX project or situation file.

        Args:
            situation_type (ImxSituationsEnum): The IMX situation to get the repo.

        Returns:
            (SituationRepo): The given situation if exists in file.

        """
        if situation_type == ImxSituationsEnum.InitialSituation:
            if self.project is not None:
                return self.project.initial_situation
            else:
                return None

        elif situation_type == ImxSituationsEnum.NewSituation:
            if self.project is not None:
                return self.project.new_situation
            else:
                return None

        else:
            if self.situation is not None:
                return self.situation
            return None
