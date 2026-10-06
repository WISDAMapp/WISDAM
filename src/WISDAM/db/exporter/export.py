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
import multiprocessing as mp
import queue as queue_module
import traceback

from db.dbHandler import DBHandler

logger = logging.getLogger(__name__)


# from WISDAMapp.exporter.kml import export_kml_footprint


def export_count_and_warnings(export_result) -> tuple[int, int, str]:
    if isinstance(export_result, dict):
        return (
            export_result.get("count", 0),
            export_result.get("no_geometry_available", 0),
            export_result.get("no_geometry_label", "objects"),
        )

    return export_result, 0, "objects"


def export_log_message(
    file_suffix: str | None,
    export_path: str | None,
    export_count: int,
    no_geometry_available: int,
    no_geometry_label: str,
) -> str:
    if file_suffix and export_path:
        message = 'Created "%s" file in %s - Nr of exports: %i' % (
            file_suffix.upper(),
            export_path,
            export_count,
        )
    else:
        message = "Export finished - Nr of exports: %i" % export_count

    if no_geometry_available:
        message += " - %i %s have no geometry available" % (
            no_geometry_available,
            no_geometry_label,
        )

    return message


def get_path_create_export(db: DBHandler):
    path_db = db.path
    path_export = Path.joinpath(Path(path_db.parent), path_db.stem + "_export")
    if not path_export.exists():
        path_export.mkdir()
    return path_export, path_db.stem


def export_file(
    db_path: Path,
    format_export,
    flag_first_certain: bool = False,
    flag_include_ai: bool = False,
    flag_only_ai: bool = False,
) -> bool:
    db = DBHandler(db_path, "")
    try:
        path_export, path_stem = get_path_create_export(db)

        outfile = Path.joinpath(path_export, path_stem + "_" + format_export)

        if outfile.exists():
            try:
                outfile.unlink()
                logger.info("Export file is overwritten")
            except PermissionError:
                logger.warning("Export failed. File probably looked")
                return False

        if format_export == "footprint_csv.csv":
            from db.exporter.csv_wisdam import export_footprints_csv

            success_nr = export_footprints_csv(db, outfile)
        elif format_export == "object_csv.csv":
            from db.exporter.csv_wisdam import export_objects_csv

            success_nr = export_objects_csv(
                db, outfile, flag_first_certain, flag_include_ai, flag_only_ai
            )
        elif format_export == "footprint_json.json":
            from db.exporter.geojson_wisdam import export_footprints_json

            success_nr, _ = export_footprints_json(db, outfile)
        elif format_export == "object_json.json":
            from db.exporter.geojson_wisdam import export_objects_json

            success_nr, _ = export_objects_json(
                db, outfile, flag_first_certain, flag_include_ai, flag_only_ai
            )
        elif format_export == "object_point_json.json":
            from db.exporter.geojson_wisdam import export_objects_as_point_json

            success_nr, _ = export_objects_as_point_json(
                db, outfile, flag_first_certain, flag_include_ai, flag_only_ai
            )
        elif format_export == "footprint_shp.shp":
            from db.exporter.geopandas_wrapper import export_footprints_geopandas_export

            success_nr = export_footprints_geopandas_export(
                db, outfile, export_format="ESRI Shapefile"
            )
        elif format_export == "object_shp.shp":
            from db.exporter.geopandas_wrapper import export_objects_geopandas_export

            success_nr = export_objects_geopandas_export(
                db,
                outfile,
                flag_first_certain,
                flag_include_ai,
                flag_only_ai,
                export_format="ESRI Shapefile",
            )
        elif format_export == "object_point_shp.shp":
            from db.exporter.geopandas_wrapper import (
                export_objects_as_points_geopandas_export,
            )

            success_nr = export_objects_as_points_geopandas_export(
                db,
                outfile,
                flag_first_certain,
                flag_include_ai,
                flag_only_ai,
                export_format="ESRI Shapefile",
            )
        elif format_export == "footprint_kml.kml":
            from db.exporter.geopandas_wrapper import export_footprints_geopandas_export

            success_nr = export_footprints_geopandas_export(
                db, outfile, export_format="KML"
            )
            # success = export_kml_footprint(db, outfile)
        elif format_export == "object_kml.kml":
            from db.exporter.geopandas_wrapper import export_objects_geopandas_export

            success_nr = export_objects_geopandas_export(
                db,
                outfile,
                flag_first_certain,
                flag_include_ai,
                flag_only_ai,
                export_format="KML",
            )
        elif format_export == "object_point_kml.kml":
            from db.exporter.geopandas_wrapper import (
                export_objects_as_points_geopandas_export,
            )

            success_nr = export_objects_as_points_geopandas_export(
                db,
                outfile,
                flag_first_certain,
                flag_include_ai,
                flag_only_ai,
                export_format="KML",
            )
        elif format_export == "project_information.txt":
            from db.exporter.project_info import export_project_information

            success_nr = export_project_information(db, outfile)
        else:
            logger.warning("Export format not implemented")
            return False

        if success_nr is False:
            return False

        (
            success_count,
            no_geometry_available,
            no_geometry_label,
        ) = export_count_and_warnings(success_nr)

        if success_count:
            logger.info(
                export_log_message(
                    outfile.suffix,
                    outfile.parent.as_posix(),
                    success_count,
                    no_geometry_available,
                    no_geometry_label,
                ),
                extra={"finished": True},
            )
        elif no_geometry_available:
            logger.warning(
                "Nothing to export - %i %s have no geometry available"
                % (no_geometry_available, no_geometry_label)
            )

        else:
            logger.warning("Nothing to export")

        return success_nr
    finally:
        db.close()


def _export_file_process_target(
    result_queue,
    db_path: Path,
    format_export,
    flag_first_certain: bool,
    flag_include_ai: bool,
    flag_only_ai: bool,
) -> None:
    try:
        result = export_file(
            db_path, format_export, flag_first_certain, flag_include_ai, flag_only_ai
        )
    except Exception as exc:
        result_queue.put(
            ("error", type(exc).__name__, str(exc), traceback.format_exc())
        )
    else:
        result_queue.put(("ok", result))


def export_file_in_process(
    db_path: Path,
    format_export,
    flag_first_certain: bool = False,
    flag_include_ai: bool = False,
    flag_only_ai: bool = False,
) -> bool:
    ctx = mp.get_context("spawn")
    result_queue = ctx.Queue()
    process = ctx.Process(
        target=_export_file_process_target,
        args=(
            result_queue,
            db_path,
            format_export,
            flag_first_certain,
            flag_include_ai,
            flag_only_ai,
        ),
    )

    process.start()
    process.join()

    try:
        result = result_queue.get(timeout=1)
    except queue_module.Empty:
        if process.exitcode == 0:
            raise RuntimeError("Export process finished without returning a result")
        raise RuntimeError(f"Export process crashed with exit code {process.exitcode}")

    status = result[0]
    if status == "ok":
        return result[1]

    _, exc_type, message, traceback_text = result
    raise RuntimeError(
        f"Export process failed with {exc_type}: {message}\n{traceback_text}"
    )
