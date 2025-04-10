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
import pandas
from pathlib import Path
from pyproj import CRS

from importer.loaderImageBase import ImageBaseLoader, LoaderType

# WISDAM core
from WISDAMcore.camera.model_selector import estimate_camera_from_meta_dict
from WISDAMcore.image.base_class import ImageBase
from WISDAMcore.image.perspective import IMAGEPerspective
from WISDAMcore.transform.utm_converter import point_convert_utm_wgs84_egm2008
from WISDAMcore.transform.rotation import Rotation

logger = logging.getLogger(__name__)


mandatory_header = ["path", "x", "y", "z", "omega", "phi", "kappa"]


class OmegaPhiKappCSV(ImageBaseLoader):

    def __init__(self):
        super().__init__()
        self.name = 'Omega Phi Kappa CSV'
        self.loader_type = LoaderType.Logfile_Loader
        self.crs_input_show = True
        self.crs_input_mandatory = True
        self.log_file_contains_image_path = True
        self.info_text = "Columns for the CSV file path,x,y,z,omega,phi,kappa"

    @staticmethod
    def logfile_suffix() -> list[str] | None:

        return ["*.csv"]

    def extract_logfile(self, log_file: Path) -> pandas.DataFrame | None:

        try:
            # By "usecols" we make sure all columns needed are present and the dataframe look the same for
            # concatenation later on
            data_ascii = pandas.read_csv(log_file, comment="#", sep=',', header=0)
            # Rename the columns to be lower case, just in case if logfile uses lower and upper case

            data_ascii.columns = [x.lower() for x in data_ascii.columns]

            if not all(x in data_ascii.columns for x in mandatory_header):
                logger.error("Mandatory header columns missing " + ','.join(mandatory_header))
                return None

            # Just make sure that the formatting of the path is from pathlib for later comparison
            data_ascii['path'] = pandas.Series([Path(x).as_posix() for x in data_ascii['path']])

        except (pandas.errors.DataError, pandas.errors.ParserError, pandas.errors.EmptyDataError, ValueError):
            # Catch all possible errors and return None
            # We will not forward errors in this stage as its more data related and thus it can anyhow not be used
            # by the importer further. User gets a message if one of his logfile does not work
            logger.error("Logfile not working")
            return None

        return data_ascii

    def get(self, image_path: Path, meta_data: dict | None = None,
            log_data: pandas.DataFrame | None = None, **kwargs) -> tuple[ImageBase, int, int] | None:

        # the names of the log_data pandas dataframe is defined in extract logfiles

        crs_data: CRS = kwargs['crs']

        if not crs_data:
            return None

        camera, width, height = estimate_camera_from_meta_dict(meta_dict=meta_data)

        position = None
        orientation = None
        crs = None

        if width is None or height is None:
            return None

        # Find image name in log file
        data = log_data.loc[log_data['path'].str.contains(image_path.with_suffix('').as_posix())]
        if not data.empty:

            data = data.iloc[0]

            result = point_convert_utm_wgs84_egm2008(crs_data, data.x, data.y, data.z)

            if result is not None:
                x, y, z, crs = result
                position = np.array([x, y, z])

            orientation = Rotation.from_opk_degree(data.omega, data.phi, data.kappa)

        image = IMAGEPerspective(width=width, height=height, camera=camera, position=position,
                                 crs=crs, orientation=orientation)

        return image, width, height
