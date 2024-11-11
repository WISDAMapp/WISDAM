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


import numpy
import json
from pathlib import Path

from db.dbHandler import DBHandler

from core_interface.wisdamIMAGE import WISDAMImage

# core
from WISDAMcore.mapping.base_class import MappingBase


# Will run in worker
def update_all_geoms(db_path: Path, mapper: MappingBase) -> tuple[int, int, int, int]:
    sum_images_mapped = 0
    sum_images_not_mapped = 0
    sum_nr_of_objects_all = 0
    sum_nr_of_objects_mapped = 0
    sum_nr_of_objects_not_mapped = 0

    db = DBHandler(db_path)
    images = db.load_images_list()

    update_image_dict = {}
    obj_count = 0
    image_class_dict = {}
    for image_dict in images:

        # Recalculate image -> mapped footprint, mapped centerpoint

        image = WISDAMImage.from_db(image_dict, mapper=mapper)
        image_class_dict[image.id] = image

        center = None
        footprint = None
        gsd = 0.0
        area = 0.0
        if image.is_geo_referenced:

            # object id and object type are not important
            result = image.map_footprint_to_epsg4979()
            if result is not None:
                coo_wgs84, gsd, area = result
                footprint = coo_wgs84.geojson(geom_type='Polygon')

            result = image.map_center_to_epsg4979()
            if result is not None:
                coo_wgs84, gsd_center = result
                center = coo_wgs84.geojson(geom_type='Point')

            if footprint is None or center is None:
                sum_images_not_mapped += 1

                # If mapping failed we will use gsd and area from WISDAMImage.from_db
                # which initializes to 0 anyhow if not stored in DB
                gsd = image.gsd
                area = image.area
            else:
                sum_images_mapped += 1

            # old slow version with single update call for every image
            # db.image_store_georef(image_id=image.id, gsd=gsd, area=area,
            #                      center_json=center, footprint_json=footprint)

            update_image_dict[image.id] = {"gsd": gsd, "area": area,
                                           "center_json": center, "footprint_json": footprint}
            obj_count += image_dict['s_count']

        else:
            sum_images_not_mapped += 1

    db.image_update_georef_multi(update_image_dict)

    # Recalculate objects of that image
    if obj_count > 0:
        nr_of_objects, nr_of_objects_mapped, nr_of_objects_not_mapped = update_mapped_geom_multi(db, image_class_dict)
        sum_nr_of_objects_all += nr_of_objects
        sum_nr_of_objects_mapped += nr_of_objects_mapped
        sum_nr_of_objects_not_mapped += nr_of_objects_not_mapped
        print(sum_nr_of_objects_all)

    return sum_images_mapped, sum_images_not_mapped, sum_nr_of_objects_mapped, sum_nr_of_objects_not_mapped


def update_mapped_geom_multi(db: DBHandler, image_dict: dict[int, WISDAMImage]):
    """Update the coordinates of geometries from objects of image. If image is not geo-referenced
    than delete mapping of objects. Should probably be called in threads to
    not block main gui too long
    :param db: Database Handler
    :param image_dict: Dictionary with image Classes, key is the image id
    """

    nr_of_objects = 0
    nr_of_objects_mapped = 0
    nr_of_objects_not_mapped = 0

    # We will only do this if image dict is not empty
    if image_dict:

        data = db.obj_load_all()
        update_object_dict = []

        if data:
            for row in data:

                image = image_dict.get(row['image_id'], None)
                if not image:
                    nr_of_objects_not_mapped += 1
                    continue

                if not image.is_geo_referenced:
                    # old version for single update of db of each object
                    # db.delete_object_mapping(row['id'])
                    update_object_dict.append({"geom3d": "Null", "gsd": 0.0, "area": 0.0, "id": row['id']})
                    nr_of_objects_not_mapped += 1
                    continue

                nr_of_objects += 1
                geom = json.loads(row['geo2d'])
                if geom['type'] == 'Polygon':
                    points_image = geom['coordinates'][0]

                else:
                    points_image = geom['coordinates']

                # object id and object type are not important
                result = image.map_geometry_to_epsg4979(0, '', numpy.array(points_image))

                if result is not None:
                    obj_id, geom_type, coordinates_wgs84, gsd, area = result

                    geojson = coordinates_wgs84.geojson(geom_type=geom['type'])

                    # old version for single update of db of each object
                    # db.update_object_mapping(row['id'], geojson, gsd, area)
                    # new version using executemany
                    geojson['crs'] = {"type": "name", "properties": {"name": "EPSG:4979"}}
                    update_object_dict.append({"geom3d": json.dumps(geojson),
                                               "gsd": gsd,
                                               "area": area,
                                               "id": row['id']})

                    nr_of_objects_mapped += 1
                else:
                    # The object could not be mapped although image had geo-reference
                    # old version for single update of db of each object
                    # db.delete_object_mapping(row['id'])
                    update_object_dict.append({"geom3d": "Null", "gsd": 0.0, "area": 0.0, "id": row['id']})
                    nr_of_objects_not_mapped += 1

            db.update_object_mapping_multi(update_object_dict)

    return nr_of_objects, nr_of_objects_mapped, nr_of_objects_not_mapped


def update_mapped_geom(db: DBHandler, image: WISDAMImage) -> tuple[int, int, int]:
    """Update the coordinates of geometries from objects of image. If image is not geo-referenced
    than delete mapping of objects. Should probably be called in threads to
    not block main gui too long
    :param db: Database Handler
    :param image: Image Class
    """

    nr_of_objects = 0
    nr_of_objects_mapped = 0
    nr_of_objects_not_mapped = 0

    data = db.load_geometry(image.id)

    for row in data:

        if not image.is_geo_referenced:
            db.delete_object_mapping(row['id'])
            nr_of_objects_not_mapped += 1
            continue

        nr_of_objects += 1
        geom = json.loads(row['geom'])
        if geom['type'] == 'Polygon':
            points_image = geom['coordinates'][0]

        else:
            points_image = geom['coordinates']

        # object id and object type are not important
        result = image.map_geometry_to_epsg4979(0, '', numpy.array(points_image))

        if result is not None:
            obj_id, geom_type, coordinates_wgs84, gsd, area = result

            geojson = coordinates_wgs84.geojson(geom_type=geom['type'])
            db.update_object_mapping(row['id'], geojson, gsd, area)
            nr_of_objects_mapped += 1
        else:
            db.delete_object_mapping(row['id'])
            nr_of_objects_not_mapped += 1

    return nr_of_objects, nr_of_objects_mapped, nr_of_objects_not_mapped
