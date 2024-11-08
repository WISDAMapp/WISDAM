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
import os
from datetime import datetime
import time
from sqlite3 import dbapi2
from pathlib import Path
import numpy as np
from pyproj import CRS
import pyproj
from tqdm import tqdm
import sys

from db.dbHandler import DBHandler
from db.createDb import init
from core_interface.wisdamIMAGE import WISDAMImage
from core_interface.update_image_object_geometry import update_mapped_geom_multi

from WISDAMcore.mapping.plane import MappingPlane
from WISDAMcore.image.perspective import IMAGEPerspective
from WISDAMcore.camera.opencv_perspective import CameraOpenCVPerspective
from WISDAMcore.transform.rotation import Rotation
from WISDAMcore.transform.utm_converter import point_convert_utm_wgs84_egm2008
from WISDAMcore.transform.coordinates import CoordinatesTransformer

from multiprocessing import Pool


def f(x):
    return x * x


path_to_bin = Path(__file__).resolve().parent.parent.with_name("bin")


def convert_dugong_detector_to_v1(file_convert: Path, file_save: Path):
    t1 = time.time()
    pyproj.network.set_network_enabled(active=True)
    print(file_convert.name, "start conversion")

    if (path_to_bin / "project_config_dugongdetector_wisdamv1.json").exists():
        config = json.load(open(path_to_bin / "project_config_dugongdetector_wisdamv1.json", 'r'))
    else:
        config = json.load(open("project_config_dugongdetector_wisdamv1.json", 'r'))

    db_connection_old = dbapi2.connect(file_convert)
    init(db_connection_old)
    db_connection_old.row_factory = dbapi2.Row

    query = "select * from configuration"
    data = db_connection_old.execute(query).fetchone()

    if 'crated_by' in data.keys():
        user = data['crated_by']
    else:
        user = data['created_by']
    date_created = data['date_created']

    db_new = DBHandler.create(file_save, user, date_created, config)

    # db_new.con.execute("PRAGMA synchronous = NORMAL")
    # db_new.con.execute("PRAGMA journal_mode = OFF")
    # db_new.con.execute("PRAGMA synchronous = 0")
    # db_new.con.execute("PRAGMA cache_size =  1000000;")
    # db_new.con.execute("PRAGMA locking_mode = EXCLUSIVE")
    # db_new.con.execute("PRAGMA temp_store = MEMORY;")

    mapper = MappingPlane(plane_altitude=0.0, standard_crs=True)
    db_new.mapper = mapper.param_dict

    color_scheme_start = {"projection": {"attribute": "projection", "colors": {0: "#96ffaa00", 1: "#96ff007f"}}}
    db_new.color_scheme = color_scheme_start

    query = r"""select images.*, Count(sightings.image) as obj_count, 
                 asgeojson(images.footprint) as geom,
                 asgeojson(images.position) as position_json from images
                 left join sightings on images.id = sightings.image
                 group by images.id
                 order by images.id"""
    images = db_connection_old.execute(query).fetchall()

    images_dict = {}

    for data in tqdm(images):

        # if objects:
        #    print(len(objects))

        path = Path(data["path"])
        image_user = data["user"]
        width = data["width"]
        height = data["height"]

        camera = None

        # Manual import of sensor width and focal length
        if data["ior_pix"]:
            ior = json.loads(data["ior_pix"])
            focal_pixel = ior['z0']
            c_x = ior['x0']
            c_y = ior['y0']

            try:
                camera = CameraOpenCVPerspective(width, height, fx=focal_pixel, fy=focal_pixel, cx=c_x, cy=c_y)
            except:
                raise "An error occurred while creating Camera for %s" % path.as_posix()

        position = None
        utm_crs = None
        if data["X0"]:
            x_utm, y_utm, z_geod, utm_crs = point_convert_utm_wgs84_egm2008(CRS("EPSG:4326+3855"),
                                                                            x=data["X0"], y=data["Y0"],
                                                                            z=data["Z0"])
            x_utm, y_utm, z_geod_diff, utm_crs = point_convert_utm_wgs84_egm2008(CRS("EPSG:4979"),
                                                                                 x=data["X0"], y=data["Y0"], z=0)
            # print(z_geod,z_geod+abs(z_geod_diff))
            position = np.array([x_utm, y_utm, z_geod + abs(z_geod_diff)])

        orientation = None
        if data["r11"]:
            r11 = data["r11"]
            r12 = data["r12"]
            r13 = data["r13"]
            r21 = data["r21"]
            r22 = data["r22"]
            r23 = data["r23"]
            r31 = data["r31"]
            r32 = data["r32"]
            r33 = data["r33"]

            orientation = Rotation(np.array([[r11, r12, r13],
                                             [r21, r22, r23],
                                             [r31, r32, r33]]))

        image_model = IMAGEPerspective(width=width, height=height, mapper=mapper,
                                       position=position, orientation=orientation, camera=camera, crs=utm_crs)

        importer = data["uav"]
        # importer = "Aircraft AeroGlobe"
        meta_image = {"make": data["make"], "model": data["model"], "f_number": data["fnumber"], "iso": data["iso"],
                      "lens_info": data["lens"]}

        meta_user = {'operator': data["operator"], 'camera_ref': data["camera_ref"],
                     'conditions': '', 'comments': data["comments"]}

        d = datetime.strptime(data["datetime"] + '.001', "%Y:%m:%d %H:%M:%S.%f")
        image_datetime = str(d)
        transect = data["transect"]
        flight_ref = data["flight_ref"]
        block = data["survey_block"]
        group_image = data["group_image"]
        image = WISDAMImage(importer=importer, path=path, image_datetime=image_datetime,
                            width=width, height=height, image_model=image_model,
                            meta_user=meta_user, meta_image=meta_image,
                            transect=transect, block=block, flight_ref=flight_ref, group_image=group_image)

        data_env_new = None
        if data["data_env"]:
            if data["data_env"].replace(' ', ''):
                data_env = json.loads(data["data_env"])

                data_env_new = {"propagation": 1 if data_env["propagation"] else 0,
                                "data": {
                                    "Turbidity": data_env["turbidity"],
                                    "Sea State": data_env["sea_state"],
                                    "Glare": data_env["glare"]}}

            # db_new.store_image_environment_data(data_env_new, image.id)

        # if data["inspected"]:
        #    db_new.set_image_as_inspected(image.id)

        gsd = 0.0
        area = 0.0
        footprint = None
        center = None
        res = None
        if image.is_geo_referenced:
            # if the image is geo referenced try to calculate the footprint
            # as well estimate area and gsd
            try:
                res = image.image_model.map_footprint()
            except Exception as e:
                print("\nFootprint could not be mapped for %s" % path.as_posix())

            if res is not None:
                coordinates, gsd, area = res
                coo_wgs84 = CoordinatesTransformer.from_crs(image.image_model.crs, CRS.from_epsg(4979),
                                                            coordinates)
                footprint = coo_wgs84.geojson(geom_type='Polygon')

            res = None
            try:
                res = image.image_model.map_center_point()
            except:
                print("\nCenter could not be mapped for %s" % path.as_posix())

            if res is not None:
                coordinates, gsd_center = res
                point_mapped = CoordinatesTransformer.from_crs(image.image_model.crs,
                                                               CRS.from_epsg(4979), coordinates)
                center = point_mapped.geojson(geom_type='Point')

        images_dict[image.path.as_posix()] = {'image': image, 'user': image_user, 'data_env': data_env_new,
                                              'gsd': gsd, 'area': area, 'center_json': center,
                                              'inspected': data['inspected'],
                                              'footprint_json': footprint}

    print(file_convert.name, "start image insertion")
    db_new.image_create_multi_all_fields(images_dict)
    print(file_convert.name, "images inserted")

    images_new = db_new.load_images_list()

    images_new_dict = {item['path']: item for item in images_new}

    images_dict_id = {}
    for key, value in images_dict.items():
        image_id = images_new_dict[key]['id']
        images_dict_id[image_id] = value['image']
        images_dict_id[image_id].id = image_id

    print(file_convert.name, "Start object insertion")
    query = "select *, asgeojson(geom2d) as geom2d_geojson, " \
            "asgeojson(geom3d) as geom3d_geojson, images.path as img_path " \
            "from sightings join images where images.id = sightings.image"
    objects = db_connection_old.execute(query).fetchall()

    obj_list = []
    for obj in tqdm(objects):

        data = json.loads(obj["data"])

        try:
            data_env = None
            if data.get("Turbidity", False):

                if int(data["Turbidity"]) != -1:

                    data_env = {"propagation": 0,
                                "data": {
                                    "Turbidity": data["Turbidity"],
                                    "Sea State": data["SeaState"],
                                    "Glare": data["Glare"]}}

            if data["SpeciesSurety"] == 0:
                spec_surety = "Certain"
            elif data["SpeciesSurety"] == 1:
                spec_surety = "Probable"
            else:
                spec_surety = "Guess"

            data = {"Animal/Species": data["Species"].lower(), "Water Position": data["WaterPosition"],
                    "Species Surety": spec_surety, "Individual Type": data["MumCalf"],
                    "comments": data["Notes"],
                    "certainty": data["Certainty"], "firstcertain": data["FirstCertain"],
                    "resight": data["Resight"]}
        except:
            print('\n Error inserting object with ID %i' % data['id'])
            continue
        geom2d = json.loads(obj["geom2d_geojson"])

        img_new = images_new_dict.get(obj["img_path"], None)
        if img_new:

            obj_list.append({"geom2d": json.dumps(geom2d), "image": img_new['id'], "user": obj["user"],
                             "cropped_image": obj["cropped_image"],
                             "object_type": obj["object_type"].lower(), "source": obj["source"],
                             "meta_type": "wisdam_default_012024",
                             "data": json.dumps(data),
                             "reviewed": obj["reviewed"], "resight_set": obj["group_resight"],
                             "data_env": None if data_env is None else json.dumps(data_env),
                             "group_area": obj["group_area"]})

    db_new.objects_create_all_multi(obj_list)
    # print('done')

    update_mapped_geom_multi(db_new, images_dict_id)

    db_new.close()

    # db_new.store_image_all_fields_many(image_list)
    finish = file_save.parent / (file_save.stem + '_finish1.sqlite')
    os.rename(file_save.as_posix(), finish)
    print(file_save.name, "finish", (time.time() - t1) / 60)


def multi_conversion(parent_path: Path, path_out: Path):
    sqlite_files = parent_path.rglob('*.sqlite')

    with Pool(6) as pool:
        mapping_list = []
        for sqlite in sqlite_files:
            p = sqlite

            datetime_str = datetime.now().strftime("%y%m%d_%H%M%S")
            p_output = path_out / (p.stem + '_wisdam_104_%s.sqlite' % datetime_str)

            p_output.unlink(missing_ok=True)
            mapping_list.append((p, p_output))

        print("Number of conversions %i" % len(mapping_list))
        pool.starmap(convert_dugong_detector_to_v1, mapping_list)
        # convert_dugong_detector_to_v1(p, p1)


if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("First parameter: Either file path or folder where sqlites are converted.")
        print("Second parameter: Output folder")
        sys.exit()

    path_src = Path(sys.argv[1])
    path_out = Path(sys.argv[2])

    if path_out.is_file():
        print("The second parameter has to bhe the output directory and not a file")
        sys.exit()

    sqlite_extension = path_to_bin / 'spatialite-loadable-modules-5.0.0-win-amd64'
    if not sqlite_extension.exists():
        sqlite_extension = Path(__file__).resolve().parent.parent.with_name(
            "bin") / 'spatialite-loadable-modules-5.0.0-win-amd64'

    os.environ['PATH'] = ';'.join([sqlite_extension.as_posix(), os.environ['PATH']])
    # enable pyproj network capabilities for downloading raster and transformation grids
    pyproj.network.set_network_enabled(active=True)

    if path_src.is_dir():
        multi_conversion(path_src, path_out)
    else:
        datetime_string = datetime.now().strftime("%y%m%d_%H%M%S")
        p_out = path_out / (path_out.stem + '_wisdam_105_%s.sqlite' % datetime_string)
        p_out.unlink(missing_ok=True)
        convert_dugong_detector_to_v1(path_src, p_out)
