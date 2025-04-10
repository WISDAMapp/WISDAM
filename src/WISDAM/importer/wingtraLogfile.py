# ==============================================================================
# This file is part of the WISDAM distribution
# https://github.com/WISDAMapp/WISDAM
# Copyright (C) 2024 Martin Wieser.
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

# WISDAM core
from WISDAMcore.camera.model_selector import estimate_camera_from_meta_dict
from WISDAMcore.image.perspective import IMAGEPerspective
from WISDAMcore.image.base_class import ImageBase
from WISDAMcore.transform.utm_converter import point_convert_utm_wgs84_egm2008
from WISDAMcore.transform.rotation import Rotation

logger = logging.getLogger(__name__)


def rename_col_by_index(dataframe, index_mapping):
    dataframe.columns = [index_mapping.get(i, col) for i, col in enumerate(dataframe.columns)]
    return dataframe


class WINGRAOmegaPhiKappa(ImageBaseLoader):

    def __init__(self):
        super().__init__()
        self.name = 'Wingtra OmegaPhiKappa'
        self.loader_type = LoaderType.Logfile_Loader

    @staticmethod
    def logfile_suffix() -> list[str] | None:

        return ["*.csv"]

    def extract_logfile(self, log_file: Path, recursive: bool = False) -> object | None:

        # Load Logfile
        try:
            data_pandas = pandas.read_csv(log_file, sep=',', header=0)
            headers = data_pandas.columns
        except (pandas.errors.DataError, pandas.errors.ParserError):
            return None

        try:
            name_index = [idx for idx, s in enumerate(headers) if 'name' in s.lower()][0]
            lon_index = [idx for idx, s in enumerate(headers) if 'lon' in s.lower()][0]
            lat_index = [idx for idx, s in enumerate(headers) if 'lat' in s.lower()][0]
            alt_index = [idx for idx, s in enumerate(headers) if 'alt' in s.lower()][0]

            new_column_mapping = {name_index: 'name', lon_index: 'lon', lat_index: 'lat', alt_index: 'alt'}

        except IndexError:
            return None

        omega_index = [idx for idx, s in enumerate(headers) if 'omega' in s.lower()]
        phi_index = [idx for idx, s in enumerate(headers) if 'phi' in s.lower()]
        kappa_index = [idx for idx, s in enumerate(headers) if 'kappa' in s.lower()]
        yaw_index = [idx for idx, s in enumerate(headers) if 'yaw' in s.lower()]
        pitch_index = [idx for idx, s in enumerate(headers) if 'pitch' in s.lower()]
        roll_index = [idx for idx, s in enumerate(headers) if 'roll' in s.lower()]

        if omega_index and phi_index and kappa_index:

            new_column_mapping[omega_index[0]] = 'omega'
            new_column_mapping[phi_index[0]] = 'phi'
            new_column_mapping[kappa_index[0]] = 'kappa'

        elif yaw_index and pitch_index and roll_index:

            # Wingtra from Chris received
            # Label Longitude [decimal degrees] Latitude [decimal degrees] Altitude [meter] Yaw [degrees]
            # Pitch [degrees] Roll [degrees]
            # label, lon (dd), lat (dd), Altitude (m), Yaw (degrees), Pitch (degrees), Roll (degrees)
            new_column_mapping[yaw_index[0]] = 'yaw'
            new_column_mapping[roll_index[0]] = 'roll'
            new_column_mapping[pitch_index[0]] = 'pitch'

        else:
            return None

        data_pandas = rename_col_by_index(data_pandas, new_column_mapping)

        return data_pandas

    def get(self, image_path: Path, meta_data: dict,
            log_data: pandas.DataFrame | None = None, **kwargs) -> tuple[ImageBase, int, int] | None:

        camera, width, height = estimate_camera_from_meta_dict(meta_dict=meta_data)

        position = None
        orientation = None
        crs = None

        if width is None or height is None:
            return None

        # Find image name in log file

        # Find image name in log file
        row = log_data.loc[log_data['name'].str.contains(image_path.stem)]
        if not row.empty:
            row = row.iloc[0]

            crs = CRS("EPSG:4326+3855")
            result = point_convert_utm_wgs84_egm2008(crs, row.lon, row.lat, row.alt)

            if result is not None:
                x, y, z, crs = result
                position = np.array([x, y, z])

            # Omega Phi Kappa System
            if 'omega' in log_data.columns:
                omega_deg = row.omega * np.pi / 180
                phi_deg = row.phi * np.pi / 180
                kappa_deg = row.kappa * np.pi / 180

                som = np.sin(omega_deg)
                com = np.cos(omega_deg)
                sfi = np.sin(phi_deg)
                cfi = np.cos(phi_deg)
                ska = np.sin(kappa_deg)
                cka = np.cos(kappa_deg)

                rot_cam = np.array([[cfi * cka, -cfi * ska, sfi],
                                    [com * ska + som * sfi * cka, com * cka - som * sfi * ska, -som * cfi],
                                    [som * ska - com * sfi * cka, som * cka + com * sfi * ska, com * cfi]])
                orientation = Rotation(rot_cam)

            else:
                # NEd to ENU
                roll = row.roll * np.pi / 180
                yaw = row.yaw * np.pi / 180
                pitch = row.pitch * np.pi / 180

                # Rotation of IMAGE
                rot_cam = np.array([[cos(pitch) * cos(yaw), sin(roll) * sin(pitch) * cos(yaw) - cos(roll) * sin(yaw),
                                     cos(roll) * sin(pitch) * cos(yaw) + sin(roll) * sin(yaw)],
                                    [cos(pitch) * sin(yaw), sin(roll) * sin(pitch) * sin(yaw) + cos(roll) * cos(yaw),
                                     cos(roll) * sin(pitch) * sin(yaw) - sin(roll) * cos(yaw)],
                                    [-sin(pitch), sin(roll) * cos(pitch), cos(roll) * cos(pitch)]])
                orientation = Rotation(rot_cam)

        image = IMAGEPerspective(width=width, height=height, camera=camera, position=position,
                                 crs=crs, orientation=orientation)

        return image, width, height
