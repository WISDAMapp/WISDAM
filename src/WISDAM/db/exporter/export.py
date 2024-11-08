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
import logging

from db.exporter.geojson_wisdam import export_objects_json, export_footprints_json, export_objects_as_point_json
from db.exporter.csv_wisdam import export_objects_csv, export_footprints_csv
from db.exporter.project_info import export_project_information
from db.exporter.geopandas_wrapper import (export_objects_geopandas_export, export_objects_as_points_geopandas_export,
                                           export_footprints_geopandas_export)
from db.dbHandler import DBHandler

logger = logging.getLogger(__name__)


# from WISDAMapp.exporter.kml import export_kml_footprint


def get_path_create_export(db: DBHandler):
    path_db = db.path
    path_export = Path.joinpath(Path(path_db.parent), path_db.stem + '_export')
    if not path_export.exists():
        path_export.mkdir()
    return path_export, path_db.stem


def export_file(db_path: Path, format_export, flag_first_certain: bool = False) -> bool:
    db = DBHandler(db_path, '')
    path_export, path_stem = get_path_create_export(db)

    outfile = Path.joinpath(path_export, path_stem + '_' + format_export)

    if outfile.exists():
        try:
            outfile.unlink()
            logger.info('Export file is overwritten')
        except PermissionError:
            logger.warning('Export failed. File probably looked')
            return False

    if format_export == 'footprint_csv.csv':
        success_nr = export_footprints_csv(db, outfile)
    elif format_export == 'object_csv.csv':
        success_nr = export_objects_csv(db, outfile, flag_first_certain)
    elif format_export == 'footprint_json.json':
        success_nr, _ = export_footprints_json(db, outfile)
    elif format_export == 'object_json.json':
        success_nr, _ = export_objects_json(db, outfile, flag_first_certain)
    elif format_export == 'object_point_json.json':
        success_nr, _ = export_objects_as_point_json(db, outfile, flag_first_certain)
    elif format_export == 'footprint_shp.shp':
        success_nr = export_footprints_geopandas_export(db, outfile, export_format='ESRI Shapefile')
    elif format_export == 'object_shp.shp':
        success_nr = export_objects_geopandas_export(db, outfile, flag_first_certain, export_format='ESRI Shapefile')
    elif format_export == 'object_point_shp.shp':
        success_nr = export_objects_as_points_geopandas_export(db, outfile, flag_first_certain,
                                                               export_format='ESRI Shapefile')
    elif format_export == 'footprint_kml.kml':
        success_nr = export_footprints_geopandas_export(db, outfile, export_format='KML')
        # success = export_kml_footprint(db, outfile)
    elif format_export == 'object_kml.kml':
        success_nr = export_objects_geopandas_export(db, outfile, flag_first_certain, export_format='KML')
    elif format_export == 'object_point_kml.kml':
        success_nr = export_objects_as_points_geopandas_export(db, outfile, flag_first_certain, export_format='KML')
    elif format_export == 'project_information.txt':
        success_nr = export_project_information(db, outfile)
    else:
        logger.warning("Export format not implemented")
        return False

    if success_nr:
        logger.info('Created "%s" file in %s - Nr of exports: %i' % (outfile.suffix.upper(),
                                                                     outfile.parent.as_posix(),
                                                                     success_nr),
                    extra={'finished': True})

    else:
        logger.warning('Nothing to export')

    return success_nr
