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


import logging
import numpy as np
from pathlib import Path
from numpy import sin, cos
import pandas

from pyproj import CRS

from importer.loaderImageBase import ImageBaseLoader, LoaderType

# weitsicht
from weitsicht.image.base_class import ImageBase
from weitsicht.image.perspective import ImagePerspective
from weitsicht.metadata.camera_estimator_metadata import ior_from_meta
from weitsicht.metadata.tag_systems.pyexiftool_tags import PyExifToolTags
from weitsicht.transform.rotation import Rotation
from weitsicht.transform.utm_converter import point_convert_utm_wgs84_egm2008
from weitsicht.exceptions import CoordinateTransformationError
from proj_warnings import log_proj_grid_warning_once

logger = logging.getLogger(__name__)


def rename_col_by_index(dataframe, index_mapping):
    dataframe.columns = [
        index_mapping.get(i, col) for i, col in enumerate(dataframe.columns)
    ]
    return dataframe


def _normalize_image_stem(name_value) -> str:
    """
    Normalize logfile image identifiers to a comparable stem.
    Handles entries like 'IMG_0001.JPG', 'folder\\IMG_0001.JPG', or already-stem values.
    """
    try:
        return Path(str(name_value)).stem.casefold()
    except Exception:
        return str(name_value).casefold()


class WINGRAOmegaPhiKappa(ImageBaseLoader):
    def __init__(self):
        super().__init__()
        self.name = "Wingtra OmegaPhiKappa"
        self.loader_type = LoaderType.Logfile_Loader

    @staticmethod
    def info_text() -> str | None:

        text = (
            "Logfile importer for Wingtra pre 2023 (System used by Amanda H.)"
            "\nSupported are Roll,Pitch,Yaw and Omega,Phi,Kappa angles"
        )

        return text

    @staticmethod
    def logfile_suffix() -> list[str] | None:

        return ["*.csv"]

    def extract_logfile(self, log_file: Path, recursive: bool = False) -> object | None:

        # Load Logfile
        try:
            data_pandas = pandas.read_csv(log_file, sep=",", header=0)
            headers = data_pandas.columns
        except (pandas.errors.DataError, pandas.errors.ParserError):
            return None

        try:
            name_index = [idx for idx, s in enumerate(headers) if "name" in s.lower()][
                0
            ]
            lon_index = [idx for idx, s in enumerate(headers) if "lon" in s.lower()][0]
            lat_index = [idx for idx, s in enumerate(headers) if "lat" in s.lower()][0]
            alt_index = [idx for idx, s in enumerate(headers) if "alt" in s.lower()][0]

            new_column_mapping = {
                name_index: "name",
                lon_index: "lon",
                lat_index: "lat",
                alt_index: "alt",
            }

        except IndexError:
            return None

        omega_index = [idx for idx, s in enumerate(headers) if "omega" in s.lower()]
        phi_index = [idx for idx, s in enumerate(headers) if "phi" in s.lower()]
        kappa_index = [idx for idx, s in enumerate(headers) if "kappa" in s.lower()]
        yaw_index = [idx for idx, s in enumerate(headers) if "yaw" in s.lower()]
        pitch_index = [idx for idx, s in enumerate(headers) if "pitch" in s.lower()]
        roll_index = [idx for idx, s in enumerate(headers) if "roll" in s.lower()]

        if omega_index and phi_index and kappa_index:
            new_column_mapping[omega_index[0]] = "omega"
            new_column_mapping[phi_index[0]] = "phi"
            new_column_mapping[kappa_index[0]] = "kappa"

        elif yaw_index and pitch_index and roll_index:
            # Wingtra from Chris received
            # Label Longitude [decimal degrees] Latitude [decimal degrees] Altitude [meter] Yaw [degrees]
            # Pitch [degrees] Roll [degrees]
            # label, lon (dd), lat (dd), Altitude (m), Yaw (degrees), Pitch (degrees), Roll (degrees)
            new_column_mapping[yaw_index[0]] = "yaw"
            new_column_mapping[roll_index[0]] = "roll"
            new_column_mapping[pitch_index[0]] = "pitch"

        else:
            return None

        data_pandas = rename_col_by_index(data_pandas, new_column_mapping)

        # Validate numeric columns early. Invalid rows can't be used for pose anyway.
        numeric_cols = ["lon", "lat", "alt"]
        if {"omega", "phi", "kappa"} <= set(new_column_mapping.values()):
            numeric_cols += ["omega", "phi", "kappa"]
        elif {"roll", "pitch", "yaw"} <= set(new_column_mapping.values()):
            numeric_cols += ["roll", "pitch", "yaw"]

        for col in numeric_cols:
            if col in data_pandas.columns:
                data_pandas[col] = pandas.to_numeric(data_pandas[col], errors="coerce")

        # Add a normalized key for fast exact lookup in get().
        # Keep it as both a column (for debugging) and index (for performance).
        data_pandas["name_stem"] = data_pandas["name"].apply(_normalize_image_stem)

        invalid_mask = (
            data_pandas[numeric_cols].isna().any(axis=1)
            | data_pandas["name_stem"].isna()
        )
        if bool(invalid_mask.any()):
            invalid_count = int(invalid_mask.sum())
            logger.warning(
                "Dropping %d invalid rows from logfile '%s' (missing/invalid numeric values or name).",
                invalid_count,
                str(log_file),
            )
            data_pandas = data_pandas.loc[~invalid_mask].copy()

        # If the logfile has multiple rows for the same image, keep the last one deterministically.
        dup_mask = data_pandas["name_stem"].duplicated(keep=False)
        if bool(dup_mask.any()):
            dup_count_keys = int(data_pandas.loc[dup_mask, "name_stem"].nunique())
            dup_count_rows = int(dup_mask.sum())
            logger.warning(
                "Duplicate image entries in logfile '%s' (%d duplicate rows across %d image keys). "
                "Keeping the last occurrence for each image.",
                str(log_file),
                dup_count_rows,
                dup_count_keys,
            )
            data_pandas = data_pandas.drop_duplicates(subset=["name_stem"], keep="last")

        data_pandas = data_pandas.set_index("name_stem", drop=False)

        return data_pandas

    def get(
        self,
        image_path: Path,
        meta_data: dict,
        log_data: pandas.DataFrame | None = None,
        **kwargs,
    ) -> tuple[ImageBase, int, int] | None:

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

        # Exact match on normalized stem to avoid accidental substring matches (e.g. IMG_001 vs IMG_0012).
        key = image_path.stem.casefold()
        row = None
        try:
            match = log_data.loc[key]
            row = match.iloc[-1] if isinstance(match, pandas.DataFrame) else match
        except KeyError:
            row = None

        if row is not None:
            crs_source = CRS("EPSG:4326+3855")
            try:
                x, y, z, crs = point_convert_utm_wgs84_egm2008(
                    crs_source, float(row.lon), float(row.lat), float(row.alt)
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

            # Omega Phi Kappa System
            if {"omega", "phi", "kappa"} <= set(log_data.columns) and pandas.notna(
                row.get("omega", None)
            ):
                orientation = Rotation.from_opk_degree(
                    float(row.omega), float(row.phi), float(row.kappa)
                )

            else:
                if not ({"roll", "pitch", "yaw"} <= set(log_data.columns)):
                    orientation = None
                elif (
                    pandas.isna(row.get("roll", None))
                    or pandas.isna(row.get("pitch", None))
                    or pandas.isna(row.get("yaw", None))
                ):
                    orientation = None
                else:
                    roll = float(row.roll) * np.pi / 180
                    yaw = float(row.yaw) * np.pi / 180
                    pitch = float(row.pitch) * np.pi / 180

                    # Rotation of IMAGE
                    rot_cam = np.array(
                        [
                            [
                                cos(pitch) * cos(yaw),
                                sin(roll) * sin(pitch) * cos(yaw)
                                - cos(roll) * sin(yaw),
                                cos(roll) * sin(pitch) * cos(yaw)
                                + sin(roll) * sin(yaw),
                            ],
                            [
                                cos(pitch) * sin(yaw),
                                sin(roll) * sin(pitch) * sin(yaw)
                                + cos(roll) * cos(yaw),
                                cos(roll) * sin(pitch) * sin(yaw)
                                - sin(roll) * cos(yaw),
                            ],
                            [
                                -sin(pitch),
                                sin(roll) * cos(pitch),
                                cos(roll) * cos(pitch),
                            ],
                        ]
                    )
                    orientation = Rotation(rot_cam)

        image = ImagePerspective(
            width=width,
            height=height,
            camera=camera,
            position=position,
            crs=crs,
            orientation=orientation,
        )

        return image, width, height
