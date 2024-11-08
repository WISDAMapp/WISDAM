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


import json
import logging
from pathlib import Path
from queue import Queue

import pyproj
from pyproj import datadir as pyproj_datadir
from shapely import geometry, equals_exact, bounds, Geometry, get_coordinates
from PySide6.QtCore import QRectF

from app.utils_qt import crop_image_qimage, image_to_bytes
from core_interface.image_loader import image_loader_standard, image_loader_rasterio_standard
from core_interface.wisdamIMAGE import WISDAMImage
from ai.base_class import AIDetectionImport
from app.var_classes import ObjectSourceList
from db.dbHandler import DBHandler

# WISDAM core
from WISDAMcore.mapping.type_selector import mapper_load_from_dict
from WISDAMcore.exceptions import MappingError

logger = logging.getLogger(__name__)


def process_detections_to_ai_detections(db_path: Path, user: str, ai_process_name: str,
                                        detections: dict[str, list[AIDetectionImport]],
                                        queue: Queue | None = None):
    success = 0
    try:
        # Open database
        db = DBHandler.from_path(db_path, user)

        ai_run = db.insert_ai_process(ai_process_name, user, '',
                                      output='')

        duplicate = 0
        failed = 0
        image_not_found = []
        image_id_list = []

        # query_list for DB insertion
        # We will insert every 100th object
        # As we need to crop image of the detections not sure how much memory is needed and what would be
        # the optimal/maximum number of objects which can be stored in the query_list at once
        # We could check the size of the object?
        query_list = []

        # Load existing AI detections in Database
        # Equal detections will not be imported. Equal means same original object type and the same geometry
        detections_exist = {}
        result = db.ai_load_detections_without_cropped_images()
        for item in result:

            if not detections_exist.get(item['image'], None):
                detections_exist[item['image']] = []

            detections_exist[item['image']].append({'type': item['object_type_orig'],
                                                    'geom': geometry.shape(json.loads(item['outline']))})

        image_existing_list = db.load_images_list()
        image_existing_list = {Path(item['path']).with_suffix('').as_posix(): item for item in image_existing_list}

        for idx_image, (img_path, detections_image) in enumerate(detections.items()):

            path_image = Path(img_path)
            path_image_no_suffix = path_image.with_suffix('').as_posix()

            image_db = image_existing_list.get(path_image_no_suffix, None)
            if not image_db or not path_image.exists():
                # Number of detections in that file
                failed += len(detections_image)

                if img_path not in image_not_found:
                    image_not_found.append(img_path)

                continue

            # Check if we need to load the image if the detections have all external cropped images we can skip that
            # Anyhow it could still be possible that the cropped image is not loadable, that we will check later on
            detection: AIDetectionImport
            cropped_images_missing = False
            for detection in detections_image:
                if not detection.cropped_image:
                    cropped_images_missing = True
                    break
                if not Path(detection.cropped_image).exists():
                    cropped_images_missing = True
                    break

            image_id = image_db['id']

            current_image_qimage = None
            if cropped_images_missing:

                if image_db['importer'] == 'Orthoimagery using Rasterio':
                    current_image_qimage = image_loader_rasterio_standard(path_image)
                else:
                    current_image_qimage = image_loader_standard(path_image)

            # We iterate over the detections from one image
            detection: AIDetectionImport
            for detection in detections_image:

                duplicate_found = False
                if detections_exist.get(image_id, None):

                    for _detection in detections_exist[image_id]:

                        if equals_exact(detection.geometry, _detection['geom'], 0.5) and \
                                _detection['type'] == detection.object_type:
                            # check for detections which are already imported
                            duplicate_found = True
                            break

                if duplicate_found:
                    duplicate += 1
                    continue

                geom_bounds = bounds(detection.geometry)
                x_min, y_min, x_max, y_max = geom_bounds
                # cut out detection rectangle form image
                rectangle = QRectF(x_min, y_min,
                                   abs(x_max - x_min),
                                   abs(y_max - y_min))

                cropped_image = None
                if Path(detection.cropped_image).exists():
                    cropped_image = image_to_bytes(Path(detection.cropped_image))

                # If we were not able to load the cropped image from the provided link
                # We will cut out that cropped image by ourselves
                if cropped_image is None:

                    if current_image_qimage is None:

                        if image_db['importer'] == 'Orthoimagery using Rasterio':
                            current_image_qimage = image_loader_rasterio_standard(path_image)
                        else:
                            current_image_qimage = image_loader_standard(path_image)

                    # Still there could an error occur while loading that image
                    if current_image_qimage is not None:
                        cropped_image = crop_image_qimage(current_image_qimage, rectangle.toRect())

                query_list.append({'image_id': image_id,
                                   'ai_run': ai_run,
                                   'object_type_orig': detection.object_type,
                                   'object_type': detection.object_type,
                                   'data': json.dumps(
                                       detection.object_data) if detection.object_data is not None else None,
                                   'data_orig': json.dumps(
                                       detection.object_data) if detection.object_data is not None else None,
                                   'probability': detection.probability,
                                   'outline': json.dumps(geometry.mapping(detection.geometry)),
                                   'image_detection': cropped_image})

            if image_id not in image_id_list:
                image_id_list.append(image_id)

            if idx_image % 10 == 0:
                queue.put(('progress', (len(detections), idx_image)))
            # We will store to db if query list has more than 100 entries
            if len(query_list) > 150:
                db.ai_create_detection_multi(query_list)
                query_list = []
                success += 150

        # Finally store the rest of the detections
        if query_list:
            db.ai_create_detection_multi(query_list)
            success += len(query_list)

        queue.put(('progress', (1, 1)))

        if len(image_id_list) == 0:

            return_message = "Nothing imported - No images found on paths specified in file"
            queue.put(('finished', False, return_message))

        else:
            return_message = f"""AI load finished.\nImported: %i detections in %i images - %i duplicates\nImages 
            failed: %i with %i detections""" % (success, len(image_id_list),
                                                duplicate, len(image_not_found), failed)

            queue.put(('finished', True, return_message))

    except Exception as e:
        # logger.error(e)
        # exc_type, value = sys.exc_info()[:2]
        return_message = f"""AI importing failed.\nBefore crash imported: %i detections to database!!!""" % success
        queue.put(('error', e, return_message))  # (exc_type, value, traceback.format_exc())))


def process_ai_detections_to_objects(db_path: Path, user: str,
                                     mapper_dict: dict | None, path_to_proj_dir: Path,
                                     queue: Queue | None = None):
    """Store AI-detections in objects table

    :param db_path: Path to the database
    :param user: User which will be stored in the new objets
    :param mapper_dict: Mapper Class used for geometrie mapping
    :param path_to_proj_dir: Path to additional data_dir
    :param queue: Progress as integer tuple (max,i) as signal"""

    pyproj.network.set_network_enabled(True)
    pyproj_datadir.append_data_dir(path_to_proj_dir.as_posix())
    success = 0
    try:
        # Open a new DB Connection within the multiprocess
        db = DBHandler.from_path(db_path, user)

        mapper = None
        if mapper_dict:
            try:
                mapper = mapper_load_from_dict(mapper_dict)
            except MappingError:
                pass

        ai_detections_db = db.ai_load_detections_for_import()

        ai_detections = {}
        for item in ai_detections_db:
            if not ai_detections.get(item['image'], None):
                ai_detections[item['image']] = []

            ai_detections[item['image']].append(item)

        del ai_detections_db

        object_types = []
        query_list = []
        id_list = []
        failed_due_missing_image = 0
        duplicates = 0
        mapping_failed = 0
        if ai_detections:

            # Load existing Database of objects
            objects_result = db.obj_load_for_ai_import_no_cropped_image()
            objects_database: dict[int, list[geometry.Polygon]] = {}
            for item in objects_result:
                if not objects_database.get(item['image'], None):
                    objects_database[item['image']] = []

                objects_database[item['image']].append(geometry.shape(json.loads(item['geo2d'])))

            del objects_result

            for idx_image, (key_image_id, image_items) in enumerate(ai_detections.items()):

                image = WISDAMImage.from_db(db.load_image(key_image_id), mapper=mapper)

                if not image.path.exists() or image is None:
                    failed_due_missing_image += len(image_items)
                    continue

                if image.importer == 'Orthoimagery using Rasterio':
                    current_image_qimage = image_loader_rasterio_standard(image.path)
                else:
                    current_image_qimage = image_loader_standard(image.path)

                if current_image_qimage is None:
                    failed_due_missing_image += len(image_items)
                    continue

                for idx, detection in enumerate(image_items):

                    if (not detection['imported']) and detection['active']:

                        geom_json = json.loads(detection['outline'])

                        # This is to be compatible to version 1.0.x
                        if geom_json.get('xmin', False):

                            geom = geometry.Polygon([[geom_json['xmin'], geom_json['ymin']],
                                                     [geom_json['xmax'], geom_json['ymin']],
                                                     [geom_json['xmax'], geom_json['ymax']],
                                                     [geom_json['xmin'], geom_json['ymax']],
                                                     [geom_json['xmin'], geom_json['ymin']]])

                        else:
                            geom = geometry.shape(geom_json)

                        geom_bounds = bounds(geom)
                        x_min, y_min, x_max, y_max = geom_bounds
                        # cut out detection rectangle form image
                        rectangle = QRectF(x_min, y_min,
                                           abs(x_max - x_min),
                                           abs(y_max - y_min))

                        duplicate_found = False
                        if objects_database.get(key_image_id, None):

                            obj_shape: Geometry
                            for obj_shape in objects_database[key_image_id]:

                                if equals_exact(obj_shape, geom, 0.5):
                                    # check for detections which are already imported
                                    duplicate_found = True
                                    break

                        if duplicate_found:
                            duplicates += 1
                            continue

                        # Data is no duplicate as geometry is not found for that image
                        geojson = geometry.mapping(geom)

                        cropped_image = crop_image_qimage(current_image_qimage, rectangle.toRect())

                        # obj_id = db.create_object(image.id, geojson=geojson, cropped_image=thumbnail)
                        # db.store_ai_detection_objects()

                        area = 0.0
                        gsd = 0.0
                        geojson3d = "Null"
                        if image.is_geo_referenced:

                            # coordinates = geometry_to_np_array(geom)
                            # Found a function called get_coordinates from shapely which does this already
                            coordinates = get_coordinates(geom, include_z=False)

                            result = image.map_geometry_to_epsg4979(obj_id=0, geom_type=geom.geom_type,
                                                                    points_image=coordinates)

                            if result:
                                obj_id, geom_type, coordinates_wgs84, gsd, area = result

                                geojson3d = coordinates_wgs84.geojson(geom.geom_type)
                                geojson3d['crs'] = {"type": "name", "properties": {"name": "EPSG:4979"}}

                        object_types.append(detection['object_type'])

                        if geojson3d == "Null":
                            mapping_failed += 1

                        id_list.append(detection['id'])
                        query_list.append({"image": image.id,
                                           "user": user,
                                           "cropped_image": cropped_image,
                                           "object_type": detection["object_type"],
                                           "source": ObjectSourceList.ai,
                                           "data": json.dumps(detection['data']) if detection[
                                                                                        'data'] is not None else None,
                                           "geom2d": json.dumps(geojson),
                                           "gsd": gsd, "area": area,
                                           'geom3d': json.dumps(geojson3d)})
                        success += 1

                queue.put((len(ai_detections), idx_image))
                # We will store to db if query list has more than 100 entries
                if len(query_list) > 150:
                    db.objects_create_from_ai_multi(query_list)
                    # db.set_imported_ai(x['id'], obj_id)
                    db.set_imported_ai(id_list)
                    id_list = []
                    query_list = []

            if query_list:
                db.objects_create_from_ai_multi(query_list)
                db.set_imported_ai(id_list)

            queue.put(('progress', (1, 1)))

            if len(object_types) > 0:
                db.add_object_types(object_types_to_add=object_types)

            return_message = 'Imported: %i - Duplicates: %i - Not mapped: %i\n\tFailed due to missing image: %i' % \
                             (success, duplicates, mapping_failed, failed_due_missing_image)
            queue.put(('finished', True, return_message))

        else:
            return_message = "No active Ai detections found in database"
            queue.put(('finished', True, return_message))

    except Exception as e:
        return_message = f"""AI importing failed.\nBefore crash imported: %i detections to database!!!""" % success
        queue.put(('error', e, return_message))  # (exc_type, value, traceback.format_exc())))
