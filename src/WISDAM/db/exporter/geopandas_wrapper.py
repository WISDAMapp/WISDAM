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
import logging

import fiona
import warnings
import geopandas as gpd

from db.dbHandler import DBHandler
from .geojson_wisdam import export_footprints_json, export_objects_as_point_json, export_objects_json


# Filter out warning for shapefile truncation
warnings.filterwarnings("ignore", category=UserWarning)

logging.getLogger("fiona").setLevel(logging.ERROR)

logger = logging.getLogger(__name__)
fiona.supported_drivers['KML'] = 'rw'
fiona.drvsupport.supported_drivers['KML'] = 'rw'


def repair_shp_time(gp_dataframe: gpd.GeoDataFrame):
    date_string = gp_dataframe['datetime'].dt.strftime("%Y-%m-%d")
    time_string = gp_dataframe['datetime'].dt.strftime("%H-%M-%S")
    gp_dataframe['datetime'] = date_string
    gp_dataframe['time'] = time_string


def export_footprints_geopandas_export(db: DBHandler, outfile: Path, export_format=''):
    format_export = outfile.suffix
    success, geo_dict = export_footprints_json(db, outfile, dict_return_only=True)
    if success:
        gdf = gpd.read_file(json.dumps(geo_dict), engine="fiona", allow_unsupported_drivers=True)
        if format_export == ".shp":
            repair_shp_time(gdf)
        gdf.to_file(outfile.as_posix(), driver=export_format, engine="fiona", allow_unsupported_drivers=True)

        return len(geo_dict["features"])

    return 0


def export_objects_geopandas_export(db, outfile: Path, flag_first_certain, export_format=''):
    format_export = outfile.suffix
    success, geo_dict = export_objects_json(db, outfile, flag_first_certain, dict_return_only=True)
    if success:
        gdf = gpd.read_file(json.dumps(geo_dict), engine="fiona", allow_unsupported_drivers=True)

        if format_export == ".shp":
            repair_shp_time(gdf)

            for geomtype in gdf.geom_type.unique():
                gdf[gdf.geom_type == geomtype].to_file(
                    (outfile.parent / ('%s_%s.shp' % (outfile.stem, geomtype))).as_posix(), driver=export_format,
                    layer=geomtype, engine="fiona", allow_unsupported_drivers=True)
        else:
            gdf.to_file(outfile.as_posix(), driver=export_format, engine="fiona", allow_unsupported_drivers=True)

        return len(geo_dict["features"])

    return 0


def export_objects_as_points_geopandas_export(db, outfile: Path, flag_first_certain, export_format=''):
    format_export = outfile.suffix
    success, geo_dict = export_objects_as_point_json(db, outfile, flag_first_certain, dict_return_only=True)
    if success:

        gdf = gpd.read_file(json.dumps(geo_dict), engine="fiona", allow_unsupported_drivers=True)
        if format_export == ".shp":
            repair_shp_time(gdf)
        gdf.to_file(outfile.as_posix(), driver=export_format, engine="fiona", allow_unsupported_drivers=True)

        return len(geo_dict["features"])

    return 0
