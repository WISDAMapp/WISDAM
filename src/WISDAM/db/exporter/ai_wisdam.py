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


from pathlib import Path
import json
import datetime
import shutil
import csv
import logging


from db.dbHandler import DBHandler
from app.var_classes import ObjectSourceList

logger = logging.getLogger(__name__)


def export_trainings_data_worker(db_path: Path, flag_images: bool, path_export: str, exclude_ai: bool,
                                 progress_callback=None) -> bool:
    """Export digitized objects which can be used for AI training
    :param db_path:
    :param flag_images:
    :param path_export:
    :param exclude_ai:
    :param progress_callback: progress callback for worker signal
    :return: True is success"""

    db = DBHandler.from_path(db_path)

    # export path with string formatting, create if not exists
    str_day = datetime.datetime.now().strftime("trainings_data-%Y_%d_%m-%H_%M")
    path_export = Path(path_export) / str_day
    if not path_export.exists():
        # create also parent folder of export if not exists
        path_export.mkdir(parents=True)

    path_images = path_export / "images"

    data = db.obj_load_all()

    # if also images shall be exported create image folder in export
    if flag_images:

        if not path_images.exists():
            path_images.mkdir()

    images_exported = []

    # File with the trainings information
    with open(path_export / "objects.txt", 'w', newline='', encoding='utf-8') as fid:

        csv_writer = csv.writer(fid, delimiter=',', quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)

        csv_writer.writerow(['image', 'object_type', 'object_image', 'geometry'])

        for obj in data:

            if exclude_ai and obj['source'] == ObjectSourceList.ai:
                continue

            if obj['data']:
                dt = json.loads(obj['data'])
                if dt.get('certainty', 'no') == 'no':
                    continue
            else:
                continue

            object_type = obj['object_type']
            path_object = path_export / object_type
            image_name = Path(obj['image_name'])
            image_path = Path(obj['img_path'])
            if not path_object.exists():
                path_object.mkdir()

            thumbnail_name = image_name.stem + '_' + object_type + '_' + str(obj['id']) + '.jpg'
            path_thumbnail = path_object / thumbnail_name

            if flag_images:
                path_full_image = path_images / image_name
                if path_full_image.as_posix() not in images_exported:
                    images_exported.append(image_path)
                    if image_path.exists():
                        shutil.copy(image_path, path_full_image.as_posix())
                    else:
                        logger.error('Error on image export')

            csv_writer.writerow([image_name.as_posix(), object_type, thumbnail_name, obj['geo2d']])

            # Save thumbnail file
            try:
                with open(path_thumbnail.as_posix(), 'wb') as file:
                    file.write(obj['cropped_image'])
            except IOError:
                logger.error('Error on object image export')

    logger.info('AI Export to be found under: ' + path_export.as_posix(),
                extra={'finished': True})
    return True
