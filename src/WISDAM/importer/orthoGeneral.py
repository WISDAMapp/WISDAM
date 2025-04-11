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

from importer.loaderImageBase import ImageBaseLoader, LoaderType

# WISDAM core
from WISDAMcore.image.base_class import ImageBase
from WISDAMcore.image.ortho import IMAGEOrtho


class OrthoGeneral(ImageBaseLoader):

    def __init__(self):
        super().__init__()
        self.name = 'Orthoimagery using Rasterio'
        self.loader_type = LoaderType.Ortho_Loader
        self.crs_input_show = True

    @staticmethod
    def info_text() -> str | None:
        text = ("This importer uses Rasterio library to load orthoimagery.\n"
                "Most File formats supported by GDAL can be used. Most common are TIF files.\n\n"
                "If the file format has no meta information about the coordinate system, it needs to be stated.\n"
                "For ortho photos a 2D coordinate system is enough like EPSG:25833 (UTM-zone 33).")

        return text

    @staticmethod
    def logfile_suffix() -> list[str] | None:
        """return the possible suffixes of your logfiles in the format as: ['*.csv'] or ['*.txt', '*.csv']
        """

        return None

    def extract_logfile(self, log_file: Path, recursive: bool = False) -> object | None:
        return None

    def get(self, image_path: Path, **kwargs) -> tuple[ImageBase, int, int] | None:
        crs_manual = kwargs['crs']
        # image class for ortho photos directly from file
        image = IMAGEOrtho.from_file(path=image_path, crs=crs_manual)

        if image is None:
            return None

        return image, image.width, image.height
