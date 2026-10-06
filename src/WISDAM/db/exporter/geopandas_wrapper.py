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
import math

import fiona
import warnings
import geopandas as gpd
from shapely import geometry

from db.dbHandler import DBHandler
from .geojson_wisdam import (
    export_footprints_json,
    export_objects_as_point_json,
    export_objects_json,
    geometry_export_result,
)

# Filter out warning for shapefile truncation
warnings.filterwarnings("ignore", category=UserWarning)

logging.getLogger("fiona").setLevel(logging.ERROR)

logger = logging.getLogger(__name__)
fiona.supported_drivers["KML"] = "rw"
fiona.drvsupport.supported_drivers["KML"] = "rw"


def image_pixel_geom_type(value):
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return None

    if isinstance(value, str):
        value = json.loads(value)

    if not value:
        return None

    return geometry.shape(value).geom_type


def unlink_same_shapefile_name(path_shp: Path):
    for path in path_shp.parent.glob(f"{path_shp.stem}.*"):
        if path.is_file():
            try:
                path.unlink()
            except PermissionError:
                logger.warning("Export failed. File probably looked")
                return False

    return True


def repair_shp_time(gp_dataframe: gpd.GeoDataFrame):
    date_string = gp_dataframe["datetime"].dt.strftime("%Y-%m-%d")
    time_string = gp_dataframe["datetime"].dt.strftime("%H-%M-%S")
    gp_dataframe["datetime"] = date_string
    gp_dataframe["time"] = time_string


def geopandas_export_result(
    gdf: gpd.GeoDataFrame,
    no_geometry_available: int,
    no_geometry_label: str = "objects",
) -> dict:
    return {
        "count": len(gdf),
        "no_geometry_available": no_geometry_available,
        "no_geometry_label": no_geometry_label,
    }


def export_footprints_geopandas_export(db: DBHandler, outfile: Path, export_format=""):
    format_export = outfile.suffix
    success, geo_dict = export_footprints_json(db, outfile, dict_return_only=True)
    if success:
        gdf = gpd.read_file(
            json.dumps(geo_dict), engine="fiona", allow_unsupported_drivers=True
        )
        if format_export == ".shp":
            repair_shp_time(gdf)
            if not unlink_same_shapefile_name(outfile):
                return False
        gdf.to_file(
            outfile.as_posix(),
            driver=export_format,
            engine="fiona",
            allow_unsupported_drivers=True,
        )

        if isinstance(success, dict):
            return success

        return geometry_export_result(len(geo_dict["features"]), 0, "footprints")

    return 0


def export_objects_geopandas_export(
    db,
    outfile: Path,
    flag_first_certain,
    flag_include_ai: bool = False,
    flag_only_ai: bool = False,
    export_format="",
):
    format_export = outfile.suffix
    success, geo_dict = export_objects_json(
        db,
        outfile,
        flag_first_certain,
        flag_include_ai,
        flag_only_ai,
        dict_return_only=True,
    )
    if success:
        gdf = gpd.read_file(
            json.dumps(geo_dict), engine="fiona", allow_unsupported_drivers=True
        )

        export_geom_type = gdf.geom_type.copy()
        missing_geom = export_geom_type.isna()
        no_geometry_available = int(missing_geom.sum())

        if format_export == ".shp":
            repair_shp_time(gdf)
            if not unlink_same_shapefile_name(outfile):
                return False

            export_geom_type.loc[missing_geom] = (
                gdf.loc[missing_geom, "image_pixel_geometry"].apply(
                    image_pixel_geom_type
                )
            )

            for geomtype in export_geom_type.dropna().unique():
                outfile_geomtype = outfile.parent / f"{outfile.stem}_{geomtype}.shp"
                if not unlink_same_shapefile_name(outfile_geomtype):
                    return False
                gdf[export_geom_type == geomtype].to_file(
                    outfile_geomtype.as_posix(),
                    driver=export_format,
                    layer=geomtype,
                    engine="fiona",
                    allow_unsupported_drivers=True,
                )
        elif len(gdf):
            gdf.to_file(
                outfile.as_posix(),
                driver=export_format,
                engine="fiona",
                allow_unsupported_drivers=True,
            )

        return geopandas_export_result(gdf, no_geometry_available)

    return 0


def export_objects_as_points_geopandas_export(
    db,
    outfile: Path,
    flag_first_certain,
    flag_include_ai: bool = False,
    flag_only_ai: bool = False,
    export_format="",
):
    format_export = outfile.suffix
    success, geo_dict = export_objects_as_point_json(
        db,
        outfile,
        flag_first_certain,
        flag_include_ai,
        flag_only_ai,
        dict_return_only=True,
    )
    if success:
        gdf = gpd.read_file(
            json.dumps(geo_dict), engine="fiona", allow_unsupported_drivers=True
        )

        missing_geom = gdf.geom_type.isna()
        no_geometry_available = int(missing_geom.sum())

        if format_export == ".shp":
            repair_shp_time(gdf)
            if not unlink_same_shapefile_name(outfile):
                return False
        if len(gdf):
            gdf.to_file(
                outfile.as_posix(),
                driver=export_format,
                engine="fiona",
                allow_unsupported_drivers=True,
            )

        return geopandas_export_result(gdf, no_geometry_available)

    return 0
