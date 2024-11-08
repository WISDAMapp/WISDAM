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
from pathlib import Path
from shapely import Geometry

from PySide6.QtCore import SignalInstance


class AIDetectionImport:

    def __init__(self, image_path: str, object_type: str = '', probability: float = 0.0,
                 geometry: Geometry | None = None, object_data: dict | None = None, cropped_image: str = ''):

        self.image_path = image_path

        self.object_type: str = object_type
        self.probability: float = probability

        self.geometry = geometry
        self.object_data = object_data

        self.cropped_image = cropped_image


class AILoaderType:
    Folder = 1
    LogFile = 2


class BaseAIClass:
    """Base class for AI loaders.
    For an implementation name and loader(AILoaderType) needs to be stated.
    The following methods need to be implemented:
        is_runnable: True if it is possible to start an AI workflow from within WISDAM
        is_filesystem_loadable: Return True if
        run:
        parse_from_path: Parse AI data from filesystem
    """

    def __init__(self):
        self.name = 'baseAI'
        self.loader = AILoaderType.Folder

    @property
    @abstractmethod
    def is_runnable(self):
        pass

    @property
    @abstractmethod
    def is_filesystem_loadable(self):
        pass

    @abstractmethod
    def run(self, db_path: Path, image_folder: Path, output_folder: Path,
            user: str, path_images_input_original: Path | None = None,
            progress_callback: SignalInstance | None = None, **kwargs) -> dict[str, list[AIDetectionImport]] | None:
        """Function to start and run AI. Can as well be a wrapper for your Docker image

        :param db_path: Path to database
        :param image_folder: Path to folder containing images
        :param path_images_input_original: Path to original images if original images (e.g. NEF) can not be
        processed by your AI
        :param output_folder: Path to folder where the results should be stored
        :param user: String with the current user
        :param progress_callback: Optional Signal to emit progress (int max, int count) or None
        :returns: A dictionary with all detections sorted by images (key) and a list for each detection of the image"""
        pass

    @abstractmethod
    def parse_from_path(self, path_to_data: Path, **kwargs) -> dict[str, list[AIDetectionImport]] | None:
        """Function which is used to parse results from AI processes into AIDetectionImport class.
            The AI wrapper will then store the results into the database and check if images existing.

        :param path_to_data: Path to folder of file containing the AI results, depends on AILoaderType
        :returns: A dictionary with all detections sorted by images (key) and a list for each detection of the image
                  or None if failed due to no possible. """
        pass
