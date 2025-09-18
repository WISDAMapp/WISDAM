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


import logging
import subprocess
import os
from pathlib import Path
import csv
from shapely import Polygon
import pandas
from PySide6.QtCore import SignalInstance

from db.dbHandler import DBHandler
from ai.base_class import BaseAIClass, AILoaderType, AIDetectionImport
from app.utils_qt import image_to_bytes

logger = logging.getLogger(__name__)
# Subprocess Flag
CREATE_NO_WINDOW = 0x08000000


def read_file_detections(path_file: Path) -> list | None:
    """Load AI detections created by MAD from folders. This is a recursive call

    :arg path_file: Path to the MAD text file which should be parsed
    :return: List with detections or None if file not found"""

    ai_detections = []
    if not path_file.exists():
        return None

    # With the first line we will test which version we are using of MAD
    # Old version should be not in 5 commas in each row

    with open(path_file) as csvfile:
        line_reader = csv.reader(csvfile, delimiter=',')
        for row in line_reader:

            if not row:
                continue

            if len(row) >= 8:
                # We should now have a line of the version 2

                # We start from end because it could be theoretically that there is a , in the path
                image = ','.join(row[:-7])
                image = Path(image)
                if not image.is_absolute():
                    logger.error("Your results file contains relative paths.\n"
                                 "Please specify absolute paths at running MadV2")
                    return None
                ai_detection_image = path_file.parent / (row[-7]+'.jpg')
                object_type = row[-6]
                probability = float(row[-5])
                detection = [image.as_posix(), ai_detection_image.as_posix(), object_type, probability,
                             float(row[-3]), float(row[-4]), float(row[-1]), float(row[-2])]
                ai_detections.append(detection)
                continue

            else:
                # Now we treat old version of the detections files

                if len(row) < 4:
                    joined_row = ','.join(row)
                    if Path(joined_row).parent == Path():

                        ai_detection_image = path_file.parent / joined_row
                        if not ai_detection_image.suffix:
                            ai_detection_image = path_file.parent / (joined_row + '.jpg')

                    else:
                        image = joined_row

                else:  # len(row) >= 4:

                    ai_values = ','.join(row).split(' ')
                    object_type = ai_values[0]
                    probability = float(ai_values[2].replace('%', '')) / 100.0
                    rectangle = [float(x) for x in ai_values[3].split(',')]
                    detection = [image, ai_detection_image, object_type, probability, rectangle[1], rectangle[0], rectangle[3], rectangle[2]]
                    ai_detections.append(detection)

    return ai_detections


def convert_ai_results(db_path: Path, path_images_input: Path, path_images_input_original: Path | None,
                       path_results: Path, ai_name: str, user: str):
    """Parse the output of MAD run and store into AI_detection table. Optional original image folder path
    can be passed as MAD in the current version only supports "jpg".
    :arg db_path: Path to database to load into
    :arg path_images_input: Path to folder where images are located which have been used for the AI
    :arg path_images_input_original: Path to folder where original images are located
    :arg path_results: Path of the MAD detection result folder
    :arg ai_name: The name to put in the AI runs database table
    :arg user: String with user which is used to import detections
    :return: String with information about success"""

    db = DBHandler.from_path(db_path, user)

    if not os.listdir(path_results.as_posix()):
        return False

    path_detections = path_results / 'detection_results.txt'
    detections = read_file_detections(path_detections)
    success = 0
    failed = 0
    duplicate = 0
    image_id_list = []

    if detections is not None:

        ai_run = db.insert_ai_process(ai_name, user, path_images_input.as_posix(), output=path_detections.as_posix())

        for detection in detections:

            path_image = path_images_input / detection[0].replace('/Data/', '')
            path_image = path_image.as_posix()

            if path_images_input_original is not None:
                path_search = Path(path_images_input_original) / detection[0].replace('/Data/', '')
                path_image, extension = os.path.splitext(path_search.as_posix())
                path_image = path_image.lower() + '%'

            images_found = db.load_image_id_path_parts(path_image)
            if images_found is not None:
                path_image_detection = path_results / (detection[1] + '.jpg')

                try:
                    image_detection = image_to_bytes(path_image_detection)
                except:
                    failed += 1
                    continue

                coo = [int(v) for v in detection[4].split(',')]
                outline = {'xmin': coo[0], 'ymin': coo[1], 'xmax': coo[2], 'ymax': coo[3]}

                new_id = db.store_ai_detection(images_found[0]['id'], object_type=detection[2], ai_run=ai_run, object_data='',
                                               outline=outline, probability=detection[3],
                                               image_detection=image_detection)
                if new_id:
                    success += 1
                else:
                    duplicate += 1
                if images_found[0]['id'] not in image_id_list:
                    image_id_list.append(images_found[0]['id'])
            else:
                logger.warning('\tImage of AI result not found in Database: ' + path_image)

    else:
        logger.error('\tAI results could not be parsed or empty.')
        return False

    logger.info('AI load finished.\nImported: %i detections in %i images - %i duplicates\n'
                '\t%i detections failed to import' %
                (success, len(image_id_list), duplicate, failed), extra={"finished": True})

    return True


class MADSeafrog(BaseAIClass):

    def __init__(self):
        super().__init__()
        self.name = 'MAD_v1_v2'
        self.loader = AILoaderType.Folder

    @property
    def is_runnable(self):
        return False

    @property
    def is_filesystem_loadable(self):
        return True

    def run(self, db_path: Path, image_folder: Path, output_folder: Path,
            user: str, path_images_input_original: Path | None = None,
            progress_callback: SignalInstance | None = None, **kwargs):

        path_input_convert = r'"/' + image_folder.as_posix().replace(':', '') + ':/Data"'
        path_out_convert = r'"/' + output_folder.as_posix().replace(':', '') + ':/Detections"'

        try:
            subprocess.run('docker run --rm -v ' + path_input_convert + ' -v ' + path_out_convert +
                           ' seafrogbert/marine_animal_detector', creationflags=CREATE_NO_WINDOW)
        except Exception as e:
            logger.error("seafrogbert/marine_animal_detector Docker command was not possible to run")
            return False

        if os.listdir(output_folder.as_posix()):

            success = convert_ai_results(db_path, image_folder, path_images_input_original, output_folder, self.name,
                                         user)

            return success
        else:
            return False

    def parse_from_path(self, path_to_data: Path, **kwargs) -> dict[str, list[AIDetectionImport]] | None:
        """Load AI detections created by MAD from folders. This is a recursive call"""

        detections_glob = list(path_to_data.rglob('detection_results.txt'))
        number_detection_files = len(detections_glob)

        if number_detection_files == 0:
            logger.error('No MAD detection files found.')
            return None

        ai_detections = {}

        for idx, path_detections in enumerate(detections_glob):

            detections = read_file_detections(path_detections)

            if detections:

                for detection in detections:

                    path_image = Path(detection[0])

                    if not ai_detections.get(path_image.as_posix(), None):
                        ai_detections[path_image.as_posix()] = []

                    path_image_detection = Path(detection[1])

                    xmin = detection[4]
                    ymin = detection[5]
                    xmax = detection[6]
                    ymax = detection[7]

                    x_min = xmin if xmax >= xmin else xmax
                    y_min = ymin if ymax >= ymin else ymax
                    x_max = xmax if xmax > xmin else xmin
                    y_max = ymax if ymax > ymin else ymin

                    points_image = [[x_min, y_min],
                                    [x_max, y_min],
                                    [x_max, y_max],
                                    [x_min, y_max],
                                    [x_min, y_min]]

                    geom = Polygon(points_image)

                    ai_det = AIDetectionImport(image_path=path_image.as_posix(), object_type=detection[2],
                                               object_data=None,
                                               geometry=geom, probability=detection[3],
                                               cropped_image=path_image_detection.as_posix())

                    ai_detections[path_image.as_posix()].append(ai_det)

            else:
                logger.error('AI results could not be parsed or empty for %s.' % path_detections.as_posix())

        if ai_detections:

            return ai_detections
        else:
            return None
