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
import numpy as np

from shapely import geometry
from shapely.ops import unary_union
from pyproj import Geod


# TODO maybe also calculate mean area here and change in update_info
def image_gsd_union_area_calculate(images: list) -> tuple[float, float]:

    geoid = Geod(ellps="WGS84")

    multi_poly = []

    area_union = 0.0
    gsd = []

    for data in images:
        if data['geom']:
            poly = geometry.shape(json.loads(data['geom']))
            multi_poly.append(poly)
        gsd.append(data['gsd'])

    if len(multi_poly) > 0:
        union = unary_union(multi_poly)
        area_union = abs(geoid.geometry_area_perimeter(union)[0])

    gsd_median = 0.0
    if len(gsd) > 0:
        gsd_array = np.array(gsd)
        # it happened because of a bug that all GSD are 0.0 even if footprint was possible
        # and the later gsd_array[gsd_array>0.0] did fail
        # so to prevent that we will check if there are enough non 0 gsd values
        if len(gsd_array[gsd_array > 0.0]) > 0:
            gsd_median = np.mean(gsd_array[gsd_array>0.0])

    return area_union, gsd_median

