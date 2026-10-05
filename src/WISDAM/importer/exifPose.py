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

# We follow the specifications from here, but there is nothing standardized at all
# https://support.pix4d.com/hc/en-us/articles/360016450032

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


class EXIFPose(ImageBaseLoader):
    def __init__(self):
        super().__init__()
        self.name = "EXIF Pose"
        self.loader_type = LoaderType.EXIF_Loader
        self.crs_input_show = True

    @staticmethod
    def info_text() -> str | None:

        text = (
            "General metadata importer (EXIF/XMP).\n\n"
            "This importer reads camera intrinsics + pose from the image metadata and builds a geo-referenced image "
            "model.\n"
            "If the image does not contain enough metadata (e.g. missing GPS or orientation), the image will be "
            "loaded\n"
            "without geo-reference.\n\n"
            "Vertical reference modes:\n"
            "- Orthometric: heights are geoid-based (EGM2008 / mean sea level)\n"
            "- Ellipsoidal: heights are WGS84 ellipsoid heights\n"
            "- Relative: uses RelativeAltitude + the provided reference height\n\n"
            "For RTK workflows you can override the CRS if the flight used a specific projected CRS.\n"
            "If projections look wrong, switching the vertical reference mode is the most common fix."
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

        # We keep the legacy behavior of this importer: map the pose to a UTM CRS (EGM2008 heights).
        # weitsicht internally applies the appropriate CRS logic based on tags and vertical_ref.
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
