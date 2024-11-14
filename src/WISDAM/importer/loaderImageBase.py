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


from abc import abstractmethod
from enum import Enum
from pathlib import Path

import pandas

# WISDAM core
from WISDAMcore.image.base_class import ImageBase


class LoaderType(Enum):
    EXIF_Loader = 1
    Logfile_Loader = 2
    Ortho_Loader = 3
    SimpleImage_Loader = 4


class ImageBaseLoader:

    def __init__(self):
        self.name = 'base'
        self.loader_type = LoaderType.EXIF_Loader
        self.crs_input_show = False
        self.crs_input_mandatory = False
        self.log_file_contains_image_path = False

    @abstractmethod
    def get(self, **kwargs) -> tuple[ImageBase, int, int] | None:
        """Gets image model from inputs.

        :return: Image Class otherwise None if failed
        """
        pass

    @staticmethod
    @abstractmethod
    def logfile_suffix() -> list[str] | None:
        """return the possible suffixes of your logfiles in the format as: ['*.csv'] or ['*.txt', '*.csv']
        Will be used for recursive import of logfiles or if image folder is used to search for logfiles
        """

        pass

    @abstractmethod
    def extract_logfile(self, log_file: Path) -> pandas.DataFrame | None:
        """Extract the needed information from the logfile
        You need to return a pandas Dataframe.

        !!! Accumulation of data !!!
        In the call of the "process_folder" an iteration over several logfiles is implemented with
        log_data = pandas.concat([log_data, data_log_file])
        Thus you need to make sure that either a pandas dataframe is returned or set to None if the logfile did not work
        As well you will need to make sure that the dataframes can be concatenated, for example by stripping columns
        only to the needed ones if there could be other files with the same suffix and similar content.

        It is best to implement it so that all files which could have the suffix used are tested for the correct
        data as it is possible to get a single logfile, or a folder to search for logfiles which can be also recursive
        If a logfile with the correct suffix is found but without correct the function should not error out

        For importer without extract_logfile simple return None. It is an abstractmethod
        that it is not forgotten to implement for a new loader.

        As well, you should make sure if searching for the row in the dataframe it could be that there are multiple
        entries of the same image if for example a logfile is stored in multiple times.
        Thus best use:
            data = log_data.loc[log_data['id'].str.contains(image_path.stem)] # 'id' is defined by you (e.g 'imgname')
            if not data.empty:
                data = data.iloc[0]

        You can have a look at the aeroglob importer, how columns can be renamed or only needed columns are extracted

        IF your logfile contains absolute image paths which can be used for image import, the image paths have to be in
        a collumn named "path"
        Check the opk_csv.py importer to see an example

        :arg log_file: Path to the logfile used to read info or path to folder containing log files.
        :return: Pandas Dataframe or None if failed
        """

        pass
