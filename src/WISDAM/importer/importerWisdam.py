# ==============================================================================
# This file is part of the WISDAM distribution
# https://github.com/WISDAMapp/WISDAM
# Copyright (C) 2025 Martin Wieser.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/.
# ==============================================================================


from pathlib import Path
from pyproj import CRS

from importer.loaderImageBase import ImageBaseLoader
from importer.wingtraLogfile import WINGRAOmegaPhiKappa
from importer.murdochVarda import VARDAMurdoch
from importer.aircraftAeroglob import AircraftAeroGlobe
from importer.simpleImage import SimpleImage
from importer.exifPose import EXIFPose
from importer.orthoGeneral import OrthoGeneral
from importer.dji_images import DJIStandard
from importer.sd_cam_no_focal import SdXlsxNoFocal
from importer.opk_csv import OmegaPhiKappCSV
from importer.yrp_csv import YawPitchRollCSV

from WISDAMcore.image.base_class import ImageBase


# WISDAM core


class IMAGEImporter:
    """Holder Class to add all Importers and call/show them"""
    def __init__(self):
        self.input_class_list = [SimpleImage(), EXIFPose(), DJIStandard(), OmegaPhiKappCSV(), WINGRAOmegaPhiKappa(),
                                 VARDAMurdoch(), OrthoGeneral(), SdXlsxNoFocal(),
                                 YawPitchRollCSV(), AircraftAeroGlobe()]
        self.input_type_current = ImageBaseLoader()

    def get_input_names(self):

        return [input_types.name for input_types in self.input_class_list]

    def get_current_name(self):

        return self.input_type_current.name

    def get_current_loader_type(self):

        return self.input_type_current.loader_type

    def get_current_info_text(self):

        return self.input_type_current.info_text()

    def set_input_class(self, name: str):
        for input_type in self.input_class_list:
            if input_type.name == name:
                self.input_type_current = input_type

    def logfile_suffix(self):

        return self.input_type_current.logfile_suffix()

    def extract_logfile(self, log_file: Path | None = None) -> object:
        """Extract a single logfile"""

        result = self.input_type_current.extract_logfile(log_file=log_file)

        return result

    def run_importer(self, image_path: Path, crs: CRS | None = None,
                     georef_input=None, log_data: list[object] | None = None,
                     vertical_ref: str = '', height_rel: float = 0.0,
                     image_meta_data: dict | None = None) -> tuple[ImageBase, int, int] | None:
        if image_meta_data is None:
            image_meta_data = {}
        if georef_input is None:
            georef_input = []

        result = self.input_type_current.get(image_path=image_path, crs=crs,
                                             georef_input=georef_input, meta_data=image_meta_data, log_data=log_data,
                                             vertical_ref=vertical_ref, height_rel=height_rel)

        return result
