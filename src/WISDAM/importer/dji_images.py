# ==============================================================================
# This file is part of the WISDAM distribution
# https://github.com/WISDAMapp/WISDAM
# Copyright (C) 2026 Martin Wieser.
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


# Some info about DJI tags and values

# For older DJI models there was some inconsistency in the tags
# Also the altitude was quite strange for some old models

# https://dl.djicdn.com/downloads/p4-multispectral/20200717/P4_Multispectral_Image_Processing_Guide_EN.pdf
# https://dl.djicdn.com/downloads/DJI_Mavic_3_Enterprise/20230829/Mavic_3M_Image_Processing_Guide_EN.pdf
# https://exiftool.org/TagNames/DJI.html


import logging
from pathlib import Path
from pyproj import CRS

from importer.loaderImageBase import ImageBaseLoader, LoaderType

# weitsicht
from weitsicht.image.base_class import ImageBase
from weitsicht.image.perspective import ImagePerspective
from weitsicht.metadata.camera_estimator_metadata import ior_from_meta
from weitsicht.metadata.image_from_meta import image_from_meta
from weitsicht.metadata.tag_systems.pyexiftool_tags import PyExifToolTags
from proj_warnings import (
    is_probable_proj_grid_error,
    log_proj_grid_warning_once,
)

logger = logging.getLogger(__name__)


class DJIStandard(ImageBaseLoader):
    def __init__(self):
        super().__init__()
        self.name = "DJI Different Versions"
        self.loader_type = LoaderType.EXIF_Loader
        self.crs_input_show = True

    @staticmethod
    def info_text() -> str | None:

        text = (
            "DJI metadata importer (EXIF/XMP).\n\n"
            "This importer reads camera + pose directly from the image metadata and builds a geo-referenced image "
            "model.\n"
            "It supports the common DJI tag variants (XMP/MakerNotes, gimbal angles, RelativeAltitude).\n\n"
            "Altitude handling depends on your drone/firmware and processing chain:\n"
            "- Orthometric: heights are geoid-based (EGM2008 / mean sea level)\n"
            "- Ellipsoidal: heights are WGS84 ellipsoid heights\n"
            "- Relative: uses RelativeAltitude + the provided reference height\n\n"
            "If projections look wrong, the most common fix is switching the vertical reference mode.\n"
            "You can also override the CRS for RTK workflows where the flight used a specific projected CRS."
        )

        return text

    @staticmethod
    def logfile_suffix() -> list[str] | None:
        """return the possible suffixes of your logfiles in the format as: ['*.csv'] or ['*.txt', '*.csv']"""

        return None

    def extract_logfile(self, log_file: Path, recursive: bool = False) -> object | None:

        return None

    def get(
        self, image_path: Path, meta_data: dict, **kwargs
    ) -> tuple[ImageBase, int, int] | None:

        crs_data: CRS | None = kwargs["crs"]
        vertical_ref: str = kwargs["vertical_ref"]
        height_rel: float = float(kwargs.get("height_rel", 0.0))

        tags = PyExifToolTags(meta_data)

        # Match EXIFPose behavior: build image from metadata using weitsicht and output pose in UTM (EGM2008).
        result = image_from_meta(
            tags=tags,
            crs=crs_data,
            vertical_ref=vertical_ref,
            height_rel=height_rel,
            to_utm=True,
        )
        if result.ok is False:
            error = getattr(result, "error", "unknown error")
            if is_probable_proj_grid_error(error):
                log_proj_grid_warning_once(
                    logger,
                    "image-import-proj-grid",
                    "Image import coordinate transformation",
                    error,
                    image_path,
                )
            logger.warning(
                "weitsicht image_from_meta failed: %s",
                error,
            )
            return self._image_from_ior(tags, crs_data)

        image = result.image
        return image, int(image.width), int(image.height)

    @staticmethod
    def _image_from_ior(
        tags: PyExifToolTags, crs_data: CRS | None
    ) -> tuple[ImageBase, int, int] | None:
        ior_res = ior_from_meta(
            tags_ior=tags.get_ior_base(), tags_ior_extended=tags.get_ior_extended()
        )
        if ior_res.ok is False:
            logger.warning(
                "weitsicht ior_from_meta failed: %s",
                getattr(ior_res, "error", "unknown error"),
            )
            return None

        image = ImagePerspective(
            width=ior_res.width,
            height=ior_res.height,
            camera=ior_res.camera,
            crs=crs_data,
        )
        return image, int(image.width), int(image.height)
