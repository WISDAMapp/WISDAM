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

import pandas
from exiftool import ExifToolHelper
from pathlib import Path
import rawpy
from PIL import Image as PILImage, ImageFile as PILImageFile
from PIL import UnidentifiedImageError as PILUnidentifiedImageError
from pyproj import CRS
from datetime import datetime

from natsort import os_sorted

from importer.importerWisdam import IMAGEImporter
from importer.loaderImageBase import LoaderType
from core_interface.update_image_object_geometry import update_mapped_geom_multi
from core_interface.meta_reader import meta_image_time
from core_interface.wisdamIMAGE import WISDAMImage
from db.dbHandler import DBHandler

# WISDAM core
from WISDAMcore.mapping.base_class import MappingBase
from WISDAMcore.transform.coordinates import CoordinatesTransformer

logger = logging.getLogger(__name__)

PILImage.MAX_IMAGE_PIXELS = None
PILImageFile.LOAD_TRUNCATED_IMAGES = True


def img_readable(file: str) -> bool:
    try:
        rawpy.imread(file)
    except rawpy.LibRawError:
        try:
            PILImage.open(file)
        except PILUnidentifiedImageError:
            return False

    return True


def process_folder(input_path: Path, db_path: Path, user: str, mapper: MappingBase, input_data_class: IMAGEImporter,
                   logfile_path: Path, meta_user: dict, flight_ref: str = '', survey_block: str = '',
                   transect: str = '',
                   crs_manual: CRS | None = None, georef_input: list | None = None,
                   flag_recursive_image: bool = False,
                   flag_recursive_log: bool = False,
                   flag_log_fom_image_folder: bool = False,
                   path_to_exiftool: Path | None = None,
                   progress_callback=None) -> dict | None:
    # Get IMAGES of folder and get Exif meta data
    # GET LIST OF ALLOWED IMAGE FORMATS in FOLDER

    progress_callback.emit((1, 0))

    # Only print warning once because for lots of images that could a lot of warnings
    folder_image_list = []

    log_data: pandas.DataFrame | None = None

    success_dict = {'log_fail': False, 'img_nr': 0, 'geo_nr': 0, 'fail_nr': 0, 'exist_nr': 0}

    if input_data_class.input_type_current.loader_type == LoaderType.Logfile_Loader:

        success_dict['log_success'] = 0

        if flag_log_fom_image_folder:
            logfile_path = input_path

        # if image path imported would be chosen and not logfile_path would be set to input_path
        # this is_file() would not work as logfile_path is then None
        if logfile_path.is_file():
            log_data = input_data_class.extract_logfile(log_file=logfile_path)

        else:

            log_suffix = input_data_class.logfile_suffix()

            all_log_files = []
            for ext in log_suffix:
                if flag_recursive_log or (flag_log_fom_image_folder and flag_recursive_image):
                    all_log_files.extend(logfile_path.rglob(ext))
                else:
                    all_log_files.extend(logfile_path.glob(ext))

            # Extract data from all logfiles

            if len(all_log_files) < 1:
                progress_callback.emit((1, 0))
                return success_dict

            log_data = pandas.DataFrame()
            for logfile in all_log_files:
                data_log_file = input_data_class.extract_logfile(logfile)

                if data_log_file is not None:
                    log_data = pandas.concat([log_data, data_log_file])
                    success_dict['log_success'] += 1

        if log_data is None or log_data.empty:
            logger.error("None of the found files worked as logfiles")
            progress_callback.emit((1, 0))

            success_dict['log_fail'] = True

            return success_dict

    # PATH handling images
    if flag_recursive_image:
        image_list = os_sorted(list(input_path.rglob('*')))
    else:
        image_list = os_sorted(list(input_path.glob('*')))

    for f in image_list:
        if f.is_file():

            if img_readable(f.as_posix()):
                folder_image_list.append(f.as_posix())

    success_dict['img_nr'] = len(folder_image_list)

    image_create_dict = {}
    image_update_dict = {}

    # This is later used for objects update
    image_existing_objects_dict = {}

    if folder_image_list:

        db = DBHandler.from_path(db_path, user)

        existing_image_data = db.load_images_list()
        image_existing_list = {item['path']: item for item in existing_image_data}

        try:
            et = ExifToolHelper(executable=path_to_exiftool.as_posix())
        except (RuntimeError, TypeError, NameError):
            logger.error('Exiftool fails')
            db.close()
            return None
        try:

            for idx, file in enumerate(folder_image_list):

                # plus 1 because 0,0 would make the progress bar always running if there is an error
                progress_callback.emit((len(folder_image_list), idx + 1))

                image_data = image_existing_list.get(file, None)
                if image_data is not None:
                    # If the image is in the database it will be loaded
                    # and new import will overwrite existing information
                    image = WISDAMImage.from_db(image_data, mapper=mapper)
                    success_dict['exist_nr'] += 1

                else:
                    image = WISDAMImage(path=Path(file))

                meta_image = None
                meta_data = None
                date_time = None

                # Standard for perspective images or non ortho-imagery
                if input_data_class.input_type_current.loader_type is not LoaderType.Ortho_Loader:
                    meta_data = et.get_tags(file, tags=None)[0]

                    # Get datetime of image from metadata, as fallback the datetime
                    # from the system is used further below
                    # We will unfortunate format all timestamps to have sub-seconds
                    # As .0 sub-second is not stored in the time format the geopandas package has problems to read
                    # timestamps with and without sub-second in the same project.
                    # Thus, all images if not sub-second is present will get the sub-second 0.01
                    date_time = meta_image_time(meta_data)

                    # ADDITIONAL metadata no must have
                    make = meta_data.get("EXIF:Make", '')
                    model = meta_data.get("EXIF:Model", '')
                    f_number = meta_data.get("EXIF:FNumber", '')
                    iso = meta_data.get("EXIF:ISO", '')
                    lens_info = meta_data.get("EXIF:LensInfo", '')
                    meta_image = {'make': make, 'model': model, 'f_number': f_number,
                                  'iso': iso, 'lens_info': lens_info}

                if date_time is None:
                    date_time = datetime.fromtimestamp(image.path.stat().st_mtime)

                if date_time.microsecond == 0:
                    date_time = date_time.replace(microsecond=1000)

                result = input_data_class.run_importer(image_path=image.path,
                                                       crs=crs_manual,
                                                       georef_input=georef_input,
                                                       log_data=log_data,
                                                       image_meta_data=meta_data)

                # result is only None if it completely fails to open the image aka not width and height can be read.
                if result is None:
                    success_dict['fail_nr'] += 1
                    continue

                image_model, width, height = result
                image.width = width
                image.height = height

                # Here if it was not successful the image is not geo-referenced anymore but there should always an
                # image_model be returned. So we overwrite the image model for existing images as well
                # if image_model is not None:
                image.image_model = image_model
                image.image_model.mapper = mapper

                image.datetime = date_time
                image.importer = input_data_class.get_current_name()

                # common to normal and ortho photos
                # check if meta user is empty but exists in image, e.g. if image is re-imported
                meta_user_new = {}
                if image.meta_user:
                    for key, value in meta_user.items():
                        meta_user_new[key] = image.meta_user[key]
                        if value:
                            meta_user_new[key] = value
                else:
                    meta_user_new = meta_user

                image.meta_user = meta_user_new
                image.meta_image = meta_image

                if transect:
                    image.transect = transect
                if flight_ref:
                    image.flight_ref = flight_ref
                if survey_block:
                    image.block = survey_block

                gsd = 0.0
                area = 0.0
                footprint = None
                center = None

                if image.is_geo_referenced:
                    # if the image is geo referenced try to calculate the footprint
                    # as well estimate area and gsd

                    result = image.map_footprint_to_epsg4979()
                    if result is not None:
                        coo_wgs84, gsd, area = result
                        footprint = coo_wgs84.geojson(geom_type='Polygon')

                    result = image.map_center_to_epsg4979()
                    if result is not None:
                        coo_wgs84, gsd_center = result
                        center = coo_wgs84.geojson(geom_type='Point')

                    if footprint is not None and center is not None:
                        success_dict['geo_nr'] += 1

                # Later we recalculate only for these images which are reloaded an object mapping
                # no matter if geo-reference or not, because if not geo-referenced the objects 3d mapping is deleted.

                if image_data:
                    if image_data['s_count'] > 0:
                        image_existing_objects_dict[image_data['id']] = image

                # if image.id is 0 it is a new image
                if image.id == 0:
                    image_create_dict[image.path] = {'image': image, 'gsd': gsd, 'area': area,
                                                     'center_json': center, 'footprint_json': footprint}
                else:
                    image_update_dict[image.path] = {'image': image, 'gsd': gsd, 'area': area,
                                                     'center_json': center, 'footprint_json': footprint}

                # Old Version saving each image at iteration
                # We always will overwrite mapped attributes even if they are None will override existing geometry
                # db.image_store_georef(image_id=image.id, gsd=gsd, area=area,
                #                      center_json=center, footprint_json=footprint)
                # Now update each 500th image, not sure if it's a good idea otherwise to wait till all images imported
                # Could be K or even Million of images
                if len(image_create_dict) > 1000:
                    db.image_create_multi(image_create_dict)
                    image_create_dict = {}
                if len(image_update_dict) > 1000:
                    db.image_creation_update_multi(image_update_dict)
                    image_update_dict = {}

            if len(image_create_dict):
                db.image_create_multi(image_create_dict)
            if len(image_update_dict):
                db.image_creation_update_multi(image_update_dict)

            if image_existing_objects_dict:
                update_mapped_geom_multi(db, image_existing_objects_dict)
            db.close()
            et.terminate()

            return success_dict

        except Exception as e:
            et.terminate()
            db.close()
            # progress_callback.emit((1, 1))
            raise e

    else:
        progress_callback.emit((1, 0))
        return success_dict
