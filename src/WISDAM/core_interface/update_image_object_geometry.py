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


import numpy
import json
import logging
import multiprocessing as mp
import queue as queue_module
import traceback
from pathlib import Path

import pyproj
from pyproj import datadir as pyproj_datadir

from db.dbHandler import DBHandler

from core_interface.wisdamIMAGE import WISDAMImage

# core
from weitsicht.mapping.base_class import MappingBase
from weitsicht.mapping.mapping_dict_selector import get_mapper_from_dict
from weitsicht.geometry.coo_geojson import get_geojson
from proj_warnings import (
    collect_proj_grid_warnings,
    log_collected_proj_grid_warnings_once,
    log_proj_grid_warning_once,
)


logger = logging.getLogger(__name__)


# Will run in worker
def update_all_geoms(db_path: Path, mapper: MappingBase) -> tuple[int, int, int, int]:
    sum_images_mapped = 0
    sum_images_not_mapped = 0
    sum_nr_of_objects_all = 0
    sum_nr_of_objects_mapped = 0
    sum_nr_of_objects_not_mapped = 0
    georeferenced_images = 0
    georeferenced_images_not_mapped = 0

    db = DBHandler(db_path)
    try:
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
                georeferenced_images += 1
                # object id and object type are not important
                result = image.map_footprint_to_epsg4979()
                if result is not None:
                    coo_wgs84, gsd, area = result
                    footprint = get_geojson(coo_wgs84, geom_type="Polygon")

                result = image.map_center_to_epsg4979()
                if result is not None:
                    coo_wgs84, gsd_center = result
                    center = get_geojson(coo_wgs84, geom_type="Point")

                if footprint is None or center is None:
                    sum_images_not_mapped += 1
                    georeferenced_images_not_mapped += 1

                    # If mapping failed we will use gsd and area from WISDAMImage.from_db
                    # which initializes to 0 anyhow if not stored in DB
                    gsd = image.gsd
                    area = image.area
                else:
                    sum_images_mapped += 1

                # old slow version with single update call for every image
                # db.image_store_georef(image_id=image.id, gsd=gsd, area=area,
                #                      center_json=center, footprint_json=footprint)

                update_image_dict[image.id] = {
                    "gsd": gsd,
                    "area": area,
                    "center_json": center,
                    "footprint_json": footprint,
                }
                obj_count += image_dict["s_count"]

            else:
                sum_images_not_mapped += 1

        db.image_update_georef_multi(update_image_dict)

        # Recalculate objects of that image
        if obj_count > 0:
            nr_of_objects, nr_of_objects_mapped, nr_of_objects_not_mapped = (
                update_mapped_geom_multi(db, image_class_dict)
            )
            sum_nr_of_objects_all += nr_of_objects
            sum_nr_of_objects_mapped += nr_of_objects_mapped
            sum_nr_of_objects_not_mapped += nr_of_objects_not_mapped

        if georeferenced_images_not_mapped:
            log_proj_grid_warning_once(
                logger,
                "geometry-recalculation-mapping-failed",
                "Geometry recalculation",
                (
                    f"{georeferenced_images_not_mapped} of {georeferenced_images} "
                    "georeferenced images could not be mapped. Check mapper CRS/elevation "
                    "settings, raster coverage, and whether required PROJ transformation "
                    "grids are available for coordinate conversion."
                ),
            )

        return (
            sum_images_mapped,
            sum_images_not_mapped,
            sum_nr_of_objects_mapped,
            sum_nr_of_objects_not_mapped,
        )
    finally:
        db.close()


def _update_all_geoms_process_target(
    result_queue, db_path: Path, mapper_config: dict, proj_data_dir: Path | None = None
) -> None:
    try:
        if proj_data_dir is not None:
            pyproj.network.set_network_enabled(True)
            pyproj_datadir.append_data_dir(Path(proj_data_dir).as_posix())

        mapper = get_mapper_from_dict(mapper_config)
        result = update_all_geoms(db_path, mapper)
    except Exception as exc:
        result_queue.put(
            ("error", type(exc).__name__, str(exc), traceback.format_exc())
        )
    else:
        result_queue.put(("ok", result, collect_proj_grid_warnings()))


def update_all_geoms_in_process(
    db_path: Path, mapper_config: dict, proj_data_dir: Path | None = None
) -> tuple[int, int, int, int]:
    ctx = mp.get_context("spawn")
    result_queue = ctx.Queue()
    process = ctx.Process(
        target=_update_all_geoms_process_target,
        args=(result_queue, db_path, mapper_config, proj_data_dir),
    )

    process.start()
    process.join()

    try:
        result = result_queue.get(timeout=1)
    except queue_module.Empty:
        if process.exitcode == 0:
            raise RuntimeError(
                "Geometry update process finished without returning a result"
            )
        raise RuntimeError(
            f"Geometry update process crashed with exit code {process.exitcode}"
        )

    status = result[0]
    if status == "ok":
        warnings = result[2] if len(result) > 2 else None
        log_collected_proj_grid_warnings_once(logger, warnings)
        return result[1]

    _, exc_type, message, traceback_text = result
    raise RuntimeError(
        f"Geometry update process failed with {exc_type}: {message}\n{traceback_text}"
    )


def _map_geometry_process_target(
    result_queue,
    db_path: Path,
    mapper_config: dict | None,
    image_id: int,
    obj_id: int,
    geom_type: str,
    pixel_coordinates: list,
    proj_data_dir: Path | None = None,
) -> None:
    db = None
    try:
        if proj_data_dir is not None:
            pyproj.network.set_network_enabled(True)
            pyproj_datadir.append_data_dir(Path(proj_data_dir).as_posix())

        mapper = (
            get_mapper_from_dict(mapper_config) if mapper_config is not None else None
        )
        db = DBHandler(db_path)
        image = WISDAMImage.from_db(db.load_image(image_id), mapper=mapper)
        result = image.map_geometry_to_epsg4979(obj_id, geom_type, pixel_coordinates)
    except Exception as exc:
        result_queue.put(
            ("error", type(exc).__name__, str(exc), traceback.format_exc())
        )
    else:
        result_queue.put(("ok", result, collect_proj_grid_warnings()))
    finally:
        if db is not None:
            db.close()


def map_geometry_to_epsg4979_in_process(
    db_path: Path,
    mapper_config: dict | None,
    image_id: int,
    obj_id: int,
    geom_type: str,
    pixel_coordinates: list,
    proj_data_dir: Path | None = None,
) -> tuple[int, str, numpy.ndarray, float, float] | None:
    ctx = mp.get_context("spawn")
    result_queue = ctx.Queue()
    process = ctx.Process(
        target=_map_geometry_process_target,
        args=(
            result_queue,
            db_path,
            mapper_config,
            image_id,
            obj_id,
            geom_type,
            pixel_coordinates,
            proj_data_dir,
        ),
    )

    process.start()
    process.join()

    try:
        result = result_queue.get(timeout=1)
    except queue_module.Empty:
        if process.exitcode == 0:
            raise RuntimeError(
                "Object mapping process finished without returning a result"
            )
        raise RuntimeError(
            f"Object mapping process crashed with exit code {process.exitcode}"
        )

    status = result[0]
    if status == "ok":
        warnings = result[2] if len(result) > 2 else None
        log_collected_proj_grid_warnings_once(logger, warnings)
        return result[1]

    _, exc_type, message, traceback_text = result
    raise RuntimeError(
        f"Object mapping process failed with {exc_type}: {message}\n{traceback_text}"
    )


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
                image = image_dict.get(row["image_id"], None)
                if not image:
                    nr_of_objects_not_mapped += 1
                    continue

                if not image.is_geo_referenced:
                    # old version for single update of db of each object
                    # db.delete_object_mapping(row['id'])
                    update_object_dict.append(
                        {"geom3d": "Null", "gsd": 0.0, "area": 0.0, "id": row["id"]}
                    )
                    nr_of_objects_not_mapped += 1
                    continue

                nr_of_objects += 1
                geom = json.loads(row["geo2d"])
                if geom["type"] == "Polygon":
                    points_image = geom["coordinates"][0]

                else:
                    points_image = geom["coordinates"]

                # object id and object type are not important
                result = image.map_geometry_to_epsg4979(
                    0, geom["type"], numpy.array(points_image)
                )

                if result is not None:
                    obj_id, geom_type, coordinates_wgs84, gsd, area = result

                    geojson = get_geojson(coordinates_wgs84, geom_type=geom["type"])

                    # old version for single update of db of each object
                    # db.update_object_mapping(row['id'], geojson, gsd, area)
                    # new version using executemany
                    geojson["crs"] = {
                        "type": "name",
                        "properties": {"name": "EPSG:4979"},
                    }
                    update_object_dict.append(
                        {
                            "geom3d": json.dumps(geojson),
                            "gsd": gsd,
                            "area": area,
                            "id": row["id"],
                        }
                    )

                    nr_of_objects_mapped += 1
                else:
                    # The object could not be mapped although image had geo-reference
                    # old version for single update of db of each object
                    # db.delete_object_mapping(row['id'])
                    update_object_dict.append(
                        {"geom3d": "Null", "gsd": 0.0, "area": 0.0, "id": row["id"]}
                    )
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
            db.delete_object_mapping(row["id"])
            nr_of_objects_not_mapped += 1
            continue

        nr_of_objects += 1
        geom = json.loads(row["geom"])
        if geom["type"] == "Polygon":
            points_image = geom["coordinates"][0]

        else:
            points_image = geom["coordinates"]

        # object id and object type are not important
        result = image.map_geometry_to_epsg4979(
            0, geom["type"], numpy.array(points_image)
        )

        if result is not None:
            obj_id, geom_type, coordinates, gsd, area = result

            geojson = get_geojson(coordinates, geom_type=geom["type"])
            db.update_object_mapping(row["id"], geojson, gsd, area)
            nr_of_objects_mapped += 1
        else:
            db.delete_object_mapping(row["id"])
            nr_of_objects_not_mapped += 1

    return nr_of_objects, nr_of_objects_mapped, nr_of_objects_not_mapped
