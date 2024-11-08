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
import pandas
import logging
import json
from shapely import geometry, Polygon

from ai.base_class import BaseAIClass, AILoaderType, AIDetectionImport


logger = logging.getLogger(__name__)


class GenericCSV(BaseAIClass):
    """Base class for AI loaders. You need to specify name, loader and the methods run and import from filesystem"""

    def __init__(self):
        super().__init__()
        self.name = 'Generic CSV'
        self.loader = AILoaderType.LogFile

    @property
    def is_runnable(self):
        return False

    @property
    def is_filesystem_loadable(self):
        return True

    @abstractmethod
    def run(self, args, **kwargs) -> bool:
        return False

    @abstractmethod
    def parse_from_path(self, path_to_data: Path, **kwargs) -> dict[str, list[AIDetectionImport]] | None:
        """Parse AI detections from generic CSV file in utf-8 into AIDetectionImport class
           ImagePath, Object Type, Probability, bbox(bounding box) x min, bbox y min, bbox x max, bbox y max
           x is along width of image
           Header has to be:
           path,type,probability,xmin,ymin,xmax,ymax

        :arg path_to_data: Path to CSV file containing the data
        :return: Dict with detections. More info about the structure see the base class"""

        detections = pandas.read_csv(path_to_data, sep=',', header=0,
                                     dtype={"image_path": str, "type": str,
                                            "probability": float,
                                            "xmin": int, "ymin": int, "xmax": int, "ymax": int})

        # Test if all columns present for minimum information
        for column_to_test in ["image_path", "type", "probability", "xmin", "ymin", "xmax", "ymax"]:
            if column_to_test not in list(detections.columns):
                logger.error(""""CSV file is missing header info\nHas to be "image_path,type,probability,xmin,ymin,
                xmax,ymax" """)
                return None

        unique_path: list[str] = list(set(detections.image_path))

        result_dict = {}
        for idx_path, img_path in enumerate(unique_path):

            result_dict[img_path] = []

            for idx_detection, item in detections[detections.image_path == img_path].iterrows():
                x_max = item.xmax if item.xmax > item.xmin else item.xmin
                x_min = item.xmin if item.xmax > item.xmin else item.xmax
                y_max = item.ymax if item.ymax > item.ymin else item.ymin
                y_min = item.ymin if item.ymax > item.ymin else item.ymax

                points_image = [[x_min, y_min],
                                [x_max, y_min],
                                [x_max, y_max],
                                [x_min, y_max],
                                [x_min, y_min]]

                geom = Polygon(points_image)

                cropped_image = item.get("cropped_image", '')
                if pandas.isna(cropped_image):
                    cropped_image = ''
                detection = AIDetectionImport(image_path=img_path, object_type=item.type,
                                              geometry=geom, probability=item.probability,
                                              cropped_image=cropped_image)

                result_dict[img_path].append(detection)

        return result_dict
