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

from __future__ import annotations

import csv
from io import StringIO
from pathlib import Path
from typing import Any

from db.dbHandler import DBHandler
from importer.object_loader_json import (
    ENV_OBJECT_PREFIX,
    GEOMETRY_2D_KEYS,
    GEOMETRY_3D_KEYS,
    IMAGE_PATH_KEYS,
    META_DATA_PREFIX,
    OBJECT_SUBTYPE_KEYS,
    OBJECT_TYPE_KEYS,
    ImportObjectOptions,
    ImportObjectRecord,
    ImportObjectSummary,
    import_object_records,
    load_project_configuration,
    record_from_properties,
    _first_geometry,
)


def load_objects_from_csv(
    path_csv: Path | str,
    db_path: Path,
    user: str,
    image_base_path: Path | None = None,
    config_name: str | None = None,
    delimiter: str = ",",
    metadata_version_expected: str | None = None,
    dry_run: bool = False,
    progress_callback=None,
) -> ImportObjectSummary:
    """Load external objects from a CSV file into an existing WISDAM project.

    Draft CSV columns are intentionally close to the current WISDAM object CSV
    export and to the JSON properties shape:

    Required:
        img_path, object_type, image_pixel_geometry

    Optional:
        geometry3d, meta_type, reviewed, resight_set, group_area,
        meta_data: <project metadata name>,
        environment_object: propagation,
        environment_object: <environment metadata name>

    A first comment line can define the metadata version:
        # metadata_version=wisdam-object-import-v1
    """

    db = DBHandler.from_path(db_path, user)
    if db is None:
        raise ValueError(f"Could not open WISDAM database: {db_path}")

    try:
        configuration = load_project_configuration(db)
        records, metadata_version = records_from_csv_file(
            Path(path_csv), delimiter=delimiter, configuration=configuration
        )
        options = ImportObjectOptions(
            image_base_path=image_base_path,
            config_name=config_name,
            metadata_version_expected=metadata_version_expected,
            dry_run=dry_run,
        )
        summary = import_object_records(
            db, records, user=user, options=options, progress_callback=progress_callback
        )
        summary.metadata_version = metadata_version
        if metadata_version_expected and metadata_version != metadata_version_expected:
            summary.warnings.append(
                f"Metadata version mismatch: expected {metadata_version_expected}, found {metadata_version}"
            )
        return summary
    finally:
        db.close()


def records_from_csv_file(
    path_csv: Path, delimiter: str = ",", configuration: dict[str, Any] | None = None
) -> tuple[list[ImportObjectRecord], str | None]:
    metadata_version, csv_text = _read_csv_text(path_csv)
    reader = csv.DictReader(StringIO(csv_text), delimiter=delimiter)
    records = [record_from_csv_row(row, configuration=configuration) for row in reader]
    return records, metadata_version


def record_from_csv_row(
    row: dict[str, Any], configuration: dict[str, Any] | None = None
) -> ImportObjectRecord:
    properties = _normalise_csv_row(row)
    image_pixel_geometry = _first_geometry(properties, GEOMETRY_2D_KEYS)
    geometry3d = _first_geometry(properties, GEOMETRY_3D_KEYS)
    return record_from_properties(
        properties,
        image_pixel_geometry=image_pixel_geometry,
        geometry3d=geometry3d,
        configuration=configuration,
    )


def _normalise_csv_row(row: dict[str, Any]) -> dict[str, Any]:
    properties: dict[str, Any] = {}

    for key, value in row.items():
        if key is None:
            continue
        key = key.strip()
        if value is None:
            continue
        value = value.strip() if isinstance(value, str) else value
        if value == "":
            continue

        normalised_key = _normalise_header_key(key)
        properties[normalised_key] = value

    return properties


def _normalise_header_key(key: str) -> str:
    lower_key = key.lower().strip()

    for candidate in IMAGE_PATH_KEYS:
        if lower_key == candidate.lower():
            return candidate
    for candidate in OBJECT_TYPE_KEYS:
        if lower_key == candidate.lower():
            return "object_type"
    for candidate in OBJECT_SUBTYPE_KEYS:
        if lower_key == candidate.lower():
            return "subspecies"
    for candidate in GEOMETRY_2D_KEYS:
        if lower_key == candidate.lower():
            return "image_pixel_geometry"
    for candidate in GEOMETRY_3D_KEYS:
        if lower_key == candidate.lower():
            return "geometry3d"

    if lower_key.startswith(META_DATA_PREFIX.lower()):
        return META_DATA_PREFIX + key[len(META_DATA_PREFIX) :].strip()
    if lower_key.startswith(ENV_OBJECT_PREFIX.lower()):
        return ENV_OBJECT_PREFIX + key[len(ENV_OBJECT_PREFIX) :].strip()

    return key


def _read_csv_text(path_csv: Path) -> tuple[str | None, str]:
    metadata_version = None
    lines = path_csv.read_text(encoding="utf-8-sig").splitlines()

    while lines and lines[0].strip().startswith("#"):
        comment = lines.pop(0).strip().lstrip("#").strip()
        key, separator, value = comment.partition("=")
        if separator and key.strip() in {"metadata_version", "wisdam_metadata_version"}:
            metadata_version = value.strip()

    return metadata_version, "\n".join(lines)
