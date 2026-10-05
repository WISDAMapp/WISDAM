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


# Todo
# Support relative paths in the CSV. Requiring full paths is strict. If the CSV path is relative, you could resolve it
# relative to the CSV file directory.
# Case-insensitive path normalization on Windows should also normalize slashes. Path(...).as_posix() helps, but for
# safety you can Path(...).resolve() when possible (only if the file exists) before building the key.

import logging
import numpy as np
import pandas
from pathlib import Path
from pyproj import CRS

from importer.loaderImageBase import ImageBaseLoader, LoaderType

# weitsicht
from weitsicht.exceptions import CoordinateTransformationError
from weitsicht.image.base_class import ImageBase
from weitsicht.image.perspective import ImagePerspective
from weitsicht.metadata.camera_estimator_metadata import ior_from_meta
from weitsicht.metadata.tag_systems.pyexiftool_tags import PyExifToolTags
from weitsicht.transform.rotation import Rotation
from weitsicht.transform.utm_converter import point_convert_utm_wgs84_egm2008
from proj_warnings import log_proj_grid_warning_once

logger = logging.getLogger(__name__)

mandatory_header = ["path", "x", "y", "z", "omega", "phi", "kappa"]


class OmegaPhiKappCSV(ImageBaseLoader):
    def __init__(self):
        super().__init__()
        self.name = "Omega Phi Kappa CSV"
        self.loader_type = LoaderType.Logfile_Loader
        self.crs_input_show = True
        self.crs_input_mandatory = True
        self.log_file_contains_image_path = True

    @staticmethod
    def info_text() -> str | None:

        text = (
            "Importer for CSV files with exterior orientation in omega/phi/kappa.\n\n"
            "CSV format:\n"
            "- Separator: ','\n"
            "- Header row required with columns: path,x,y,z,omega,phi,kappa\n\n"
            "Notes:\n"
            "- omega/phi/kappa are in degrees\n"
            "- path must be the full path to an existing image\n"
            "- a coordinate system (CRS) must be specified for x/y/z"
        )

        return text

    @staticmethod
    def logfile_suffix() -> list[str] | None:

        return ["*.csv"]

    def extract_logfile(self, log_file: Path) -> pandas.DataFrame | None:

        try:
            # By "usecols" we make sure all columns needed are present and the dataframe look the same for
            # concatenation later on
            data_ascii = pandas.read_csv(
                log_file.as_posix(), comment="#", sep=",", header=0
            )
            # Rename the columns to be lower case, just in case if logfile uses lower and upper case

            data_ascii.columns = [x.lower() for x in data_ascii.columns]

            if not all(x in data_ascii.columns for x in mandatory_header):
                logger.error(
                    "Mandatory header columns missing " + ",".join(mandatory_header)
                )
                return None

            # Validate numeric columns early. Invalid rows can't be used for pose anyway.
            numeric_cols = ["x", "y", "z", "omega", "phi", "kappa"]
            for col in numeric_cols:
                data_ascii[col] = pandas.to_numeric(data_ascii[col], errors="coerce")

            # Just make sure that the formatting of the path is from pathlib for later comparison
            data_ascii["path"] = pandas.Series(
                [Path(str(x)).as_posix() for x in data_ascii["path"]]
            )
            data_ascii["path_key"] = data_ascii["path"].apply(
                lambda p: Path(p).with_suffix("").as_posix().casefold()
            )

            invalid_mask = (
                data_ascii[numeric_cols].isna().any(axis=1)
                | data_ascii["path_key"].isna()
            )
            if bool(invalid_mask.any()):
                invalid_count = int(invalid_mask.sum())
                logger.warning(
                    "Dropping %d invalid rows from logfile '%s' (missing/invalid numeric values or path).",
                    invalid_count,
                    str(log_file),
                )
                data_ascii = data_ascii.loc[~invalid_mask].copy()

            # If the logfile has multiple rows for the same image, keep the last one deterministically.
            # We warn here (instead of in get()) so the user learns about ambiguous logfiles early.
            dup_mask = data_ascii["path_key"].duplicated(keep=False)
            if bool(dup_mask.any()):
                dup_count_keys = int(data_ascii.loc[dup_mask, "path_key"].nunique())
                dup_count_rows = int(dup_mask.sum())
                logger.warning(
                    "Duplicate image entries in logfile '%s' (%d duplicate rows across %d image keys). "
                    "Keeping the last occurrence for each image.",
                    str(log_file),
                    dup_count_rows,
                    dup_count_keys,
                )
                data_ascii = data_ascii.drop_duplicates(
                    subset=["path_key"], keep="last"
                )

            data_ascii = data_ascii.set_index("path_key", drop=False)

        except (
            pandas.errors.DataError,
            pandas.errors.ParserError,
            pandas.errors.EmptyDataError,
            ValueError,
        ):
            # Catch all possible errors and return None
            # We will not forward errors in this stage as its more data related and thus it can anyhow not be used
            # by the importer further. User gets a message if one of his logfile does not work
            logger.error("Logfile not working")
            return None

        return data_ascii

    def get(
        self,
        image_path: Path,
        meta_data: dict | None = None,
        log_data: pandas.DataFrame | None = None,
        **kwargs,
    ) -> tuple[ImageBase, int, int] | None:

        # the names of the log_data pandas dataframe is defined in extract logfiles

        crs_data: CRS = kwargs["crs"]

        if not crs_data:
            return None

        if meta_data is None:
            return None

        tags = PyExifToolTags(meta_data)
        ior_res = ior_from_meta(
            tags_ior=tags.get_ior_base(), tags_ior_extended=tags.get_ior_extended()
        )
        if ior_res.ok is False:
            logger.warning(
                "weitsicht ior_from_meta failed: %s",
                getattr(ior_res, "error", "unknown error"),
            )
            return None

        camera, width, height = ior_res.camera, ior_res.width, ior_res.height

        position = None
        orientation = None
        crs = None

        if log_data is None:
            return None

        # Exact match on normalized path key (case-insensitive, without suffix).
        key = image_path.with_suffix("").as_posix().casefold()
        row = None
        try:
            match = log_data.loc[key]
            # extract_logfile() already de-duplicates by keeping the last entry, but be defensive:
            row = match.iloc[-1] if isinstance(match, pandas.DataFrame) else match
        except KeyError:
            row = None

        if row is not None:
            try:
                x, y, z, crs = point_convert_utm_wgs84_egm2008(
                    crs_data, float(row.x), float(row.y), float(row.z)
                )
                position = np.array([x, y, z])
            except CoordinateTransformationError as exc:
                log_proj_grid_warning_once(
                    logger,
                    "image-import-proj-grid",
                    "Image import coordinate transformation",
                    exc,
                    image_path,
                )
                position = None
                crs = None
            except ValueError:
                position = None
                crs = None

            orientation = Rotation.from_opk_degree(
                float(row.omega), float(row.phi), float(row.kappa)
            )

        image = ImagePerspective(
            width=width,
            height=height,
            camera=camera,
            position=position,
            crs=crs,
            orientation=orientation,
        )

        return image, width, height
