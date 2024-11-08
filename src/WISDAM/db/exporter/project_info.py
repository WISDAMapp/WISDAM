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
from pathlib import Path

import numpy as np
from pyproj import Geod
from shapely import geometry
from shapely.ops import unary_union

from db.dbHandler import DBHandler


def export_project_information(db: DBHandler, path_txt: Path | str) -> int:
    """Export objects as CSV File in utf-8
    :param db: DBHandler to use for export
    :param path_txt: The path to the text file to write. Will be replaced if exists
    :return: True, if success"""

    geoid = Geod(ellps="WGS84")
    gsd_mean = 0.0
    area_mean = 0.0
    area_union = 0.0

    outfile = Path(path_txt)

    with open(outfile, 'w', encoding='utf8') as fid:

        fid.write("Project information of: " + db.path.as_posix())
        fid.write("\n")

        user = []

        data_image = db.load_image_export()

        configuration: dict = db.load_config()

        fid.write("Version project was created: " + configuration['version'])
        fid.write("\n")

        img_inspected = []
        image_importers = []
        multi_poly = []
        area = []
        gsd = []

        for data in data_image:
            user.append(data['user'])
            img_inspected.append(data['inspected'])
            image_importers.append(data['importer'])
            if data['geom']:
                poly = geometry.shape(json.loads(data['geom']))
                multi_poly.append(poly)
                area_poly = abs(geoid.geometry_area_perimeter(poly)[0])
                if data['gsd'] > 0:
                    gsd.append(data['gsd'])
                else:
                    gsd.append(np.sqrt(area_poly / (data['width'] * data['height'])))
                if data['area'] > 0:
                    area.append(data['area'])
                else:
                    area.append(area_poly)

        if len(multi_poly) > 0:
            union = unary_union(multi_poly)
            area_union = abs(geoid.geometry_area_perimeter(union)[0])
            if len(area) > 0:
                area_mean = np.array(area).mean()
            if len(gsd) > 0:
                gsd_mean = np.array(gsd).mean()

        data_sightings = db.obj_load_all()

        obj_type = []
        obj_group = []
        obj_images = []
        for data in data_sightings:
            obj_type.append(data['object_type'])
            if data['resight_set'] > 0:
                obj_group.append(data['resight_set'])
            obj_images.append(data['image'])
            user.append(data['user'])

        fid.write("\nUser worked on project:\n")
        for x in set(user):
            fid.write('\t\t' + str(x) + '\n')

        fid.write("\nImages:\n")
        fid.write("\tNr of images: " + str(len(image_importers)) + '\n')
        fid.write("\tDifferent import types: " + str(len(set(image_importers))) + '\n')
        fid.write("\tGeo-referenced images: " + str(len(area)) + '\n')
        fid.write("\tMean GSD [cm]: " + str(gsd_mean) + '\n')
        fid.write("\tMean area [m²]: " + str(round(area_mean)) + '\n')

        fid.write("\tArea of dissolved polygons [m²]: " + str(round(area_union)) + "\n")

        fid.write("\nObjects:\n")
        fid.write("\tNr of objects: " + str(len(obj_type)) + '\n')
        fid.write("\tObject types:\n")
        for x in set(obj_type):
            fid.write('\t\t' + str(x) + '\n')

        fid.write("\tNumber of resight sets: " + str(len(set(obj_group))) + '\n')

    return 1
