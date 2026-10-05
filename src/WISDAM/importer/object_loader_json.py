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

from dataclasses import dataclass, field
import json
import logging
from pathlib import Path
from typing import Any

from shapely import equals_exact, geometry
from shapely.errors import GEOSException

from db.dbHandler import DBHandler

logger = logging.getLogger(__name__)


META_DATA_PREFIX = "meta_data: "
ENV_OBJECT_PREFIX = "environment_object: "
ENV_IMAGE_PREFIX = "environment_image: "
SOURCE_EXTERNAL = 2

IMAGE_PATH_KEYS = ("img_path", "image_path", "path", "file", "filename")
OBJECT_TYPE_KEYS = ("object_type", "type", "taxa", "Taxa")
OBJECT_SUBTYPE_KEYS = ("object_sub_type", "subspecies", "species", "Animal/Species")
GEOMETRY_2D_KEYS = ("image_pixel_geometry", "geom2d", "geo2d", "outline")
GEOMETRY_3D_KEYS = ("geometry3d", "geom3d", "geo3d", "geometry")


@dataclass
class ImportObjectRecord:
    """Normalized object row before it is written to the WISDAM database."""

    image_path: Path | None
    object_type: str
    image_pixel_geometry: dict[str, Any] | None
    metadata: dict[str, Any] = field(default_factory=dict)
    subspecies: str = ""
    geometry3d: dict[str, Any] | None = None
    environment_object: dict[str, Any] = field(default_factory=dict)
    environment_object_propagation: int = 0
    meta_type: str | None = None
    reviewed: int = 1
    resight_set: int = 0
    group_area: int = 0
    tags: str | None = None


@dataclass
class ImportObjectOptions:
    """Options expected to come from the GUI later."""

    image_base_path: Path | None = None
    config_name: str | None = None
    metadata_version_expected: str | None = None
    allow_unknown_object_types: bool = True
    duplicate_tolerance: float = 0.5
    dry_run: bool = False


@dataclass
class ImportObjectSummary:
    parsed: int = 0
    imported: int = 0
    duplicates: int = 0
    failed: int = 0
    missing_images: list[str] = field(default_factory=list)
    missing_geometry: int = 0
    metadata_version: str | None = None
    unknown_object_types: dict[str, list[str]] = field(default_factory=dict)
    unknown_metadata_keys: list[str] = field(default_factory=list)
    unknown_environment_keys: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def load_objects_from_json(
    path_json: Path | str,
    db_path: Path,
    user: str,
    image_base_path: Path | None = None,
    config_name: str | None = None,
    metadata_version_expected: str | None = None,
    dry_run: bool = False,
    progress_callback=None,
) -> ImportObjectSummary:
    """Load external objects from JSON/GeoJSON into an existing WISDAM project.

    Draft JSON shape:
        {
          "type": "FeatureCollection",
          "metadata_version": "wisdam-object-import-v1",
          "features": [
            {
              "type": "Feature",
              "properties": {
                "img_path": "survey/image_001.jpg",
                "object_type": "dugong",
                "meta_data: Animal/Species": "dugong",
                "image_pixel_geometry": { ... required local image geometry ... }
              },
              "geometry": { ... optional 3D world geometry ... }
            }
          ]
        }

    The GUI can later decide whether image paths are absolute, relative to a
    selected base folder, or matched by a path suffix already stored in WISDAM.
    """

    db = DBHandler.from_path(db_path, user)
    if db is None:
        raise ValueError(f"Could not open WISDAM database: {db_path}")

    try:
        document = _read_json_document(Path(path_json))
        options = ImportObjectOptions(
            image_base_path=image_base_path,
            config_name=config_name,
            metadata_version_expected=metadata_version_expected,
            dry_run=dry_run,
        )
        configuration = load_project_configuration(db)
        records = records_from_json_document(document, configuration=configuration)
        summary = import_object_records(
            db, records, user=user, options=options, progress_callback=progress_callback
        )
        summary.metadata_version = _metadata_version(document)
        _check_metadata_version(summary, options)
        return summary
    finally:
        db.close()


def records_from_json_document(
    document: dict[str, Any], configuration: dict[str, Any] | None = None
) -> list[ImportObjectRecord]:
    if document.get("type") == "FeatureCollection":
        features = document.get("features", [])
    elif document.get("type") == "Feature":
        features = [document]
    elif isinstance(document.get("objects"), list):
        features = document["objects"]
    else:
        raise ValueError(
            "JSON object import expects a FeatureCollection, Feature, or {'objects': [...]} document"
        )

    records: list[ImportObjectRecord] = []
    for feature in features:
        if feature.get("type") == "Feature":
            properties = feature.get("properties", {})
            geometry3d = _parse_geometry(feature.get("geometry"))
            image_pixel_geometry = _first_geometry(properties, GEOMETRY_2D_KEYS)
            if (
                image_pixel_geometry is None
                and geometry3d is not None
                and not _geometry_has_z(geometry3d)
            ):
                image_pixel_geometry = geometry3d
                geometry3d = None
            record = record_from_properties(
                properties,
                image_pixel_geometry=image_pixel_geometry,
                geometry3d=geometry3d,
                configuration=configuration,
            )
        else:
            record = record_from_properties(feature, configuration=configuration)

        records.append(record)

    return records


def record_from_properties(
    properties: dict[str, Any],
    image_pixel_geometry: dict[str, Any] | None = None,
    geometry3d: dict[str, Any] | None = None,
    configuration: dict[str, Any] | None = None,
) -> ImportObjectRecord:
    meta_config = _first_meta_config(configuration) if configuration else {}
    configured_metadata_keys = (
        _configured_metadata_keys(configuration) if configuration else set()
    )
    main_type_name = meta_config.get("object_main_type", {}).get("naming")
    subtype_name = meta_config.get("object_sub_type", {}).get("naming")

    image_path = _first_path(properties, IMAGE_PATH_KEYS)
    object_type = _first_text(properties, OBJECT_TYPE_KEYS)
    if not object_type and main_type_name:
        object_type = str(properties.get(main_type_name, "")).strip()

    subspecies = _first_text(properties, OBJECT_SUBTYPE_KEYS)
    if not subspecies and subtype_name:
        subspecies = str(properties.get(subtype_name, "")).strip()

    metadata = _normalise_dict(properties.get("data"))
    metadata.update(_normalise_dict(properties.get("metadata")))
    metadata.update(_normalise_dict(properties.get("meta_data")))

    environment_object = _normalise_environment(properties.get("data_env"))

    for key, value in properties.items():
        if key.startswith(META_DATA_PREFIX):
            metadata[key.removeprefix(META_DATA_PREFIX)] = value
        elif key in configured_metadata_keys:
            metadata[key] = value
        elif key.startswith(ENV_OBJECT_PREFIX):
            env_key = key.removeprefix(ENV_OBJECT_PREFIX)
            if env_key == "propagation":
                environment_object["propagation"] = _coerce_int(value, default=0)
            else:
                environment_object.setdefault("data", {})[env_key] = value
        elif key.startswith("environment_object_"):
            env_key = key.removeprefix("environment_object_")
            if env_key == "propagation":
                environment_object["propagation"] = _coerce_int(value, default=0)
            else:
                environment_object.setdefault("data", {})[env_key] = value

    if not object_type and main_type_name and metadata.get(main_type_name):
        object_type = str(metadata[main_type_name]).strip()

    if not subspecies and subtype_name and metadata.get(subtype_name):
        subspecies = str(metadata[subtype_name]).strip()

    if subspecies and subtype_name and subtype_name not in metadata:
        metadata[subtype_name] = subspecies

    return ImportObjectRecord(
        image_path=image_path,
        object_type=object_type,
        subspecies=subspecies,
        image_pixel_geometry=image_pixel_geometry
        or _first_geometry(properties, GEOMETRY_2D_KEYS),
        geometry3d=geometry3d or _first_geometry(properties, GEOMETRY_3D_KEYS),
        metadata=metadata,
        environment_object=environment_object.get("data", {}),
        environment_object_propagation=environment_object.get("propagation", 0),
        meta_type=_text_or_none(properties.get("meta_type")),
        reviewed=_coerce_int(properties.get("reviewed"), default=1),
        resight_set=_coerce_int(properties.get("resight_set"), default=0),
        group_area=_coerce_int(properties.get("group_area"), default=0),
        tags=_text_or_none(properties.get("tags")),
    )


def import_object_records(
    db: DBHandler,
    records: list[ImportObjectRecord],
    user: str,
    options: ImportObjectOptions | None = None,
    progress_callback=None,
) -> ImportObjectSummary:
    if options is None:
        options = ImportObjectOptions()

    summary = ImportObjectSummary(parsed=len(records))
    configuration = load_project_configuration(db)
    config_name = options.config_name or _first_config_name(configuration)
    meta_config = configuration["meta_config"][config_name]

    _validate_metadata_against_config(records, configuration, summary)
    if options.allow_unknown_object_types:
        _add_unknown_object_types(
            db, records, configuration, config_name, summary, dry_run=options.dry_run
        )

    existing_geometries = _load_existing_geometries(db)
    query_list: list[dict[str, Any]] = []

    for idx, record in enumerate(records):
        image = _load_image_for_record(db, record, options.image_base_path)
        if image is None:
            summary.failed += 1
            if record.image_path is not None:
                summary.missing_images.append(record.image_path.as_posix())
            _emit_progress(progress_callback, len(records), idx)
            continue

        if record.image_pixel_geometry is None:
            summary.failed += 1
            summary.missing_geometry += 1
            _emit_progress(progress_callback, len(records), idx)
            continue

        if _is_duplicate(
            record.image_pixel_geometry,
            existing_geometries.get(image["id"], []),
            tolerance=options.duplicate_tolerance,
        ):
            summary.duplicates += 1
            _emit_progress(progress_callback, len(records), idx)
            continue

        data_env = None
        if record.environment_object:
            data_env = json.dumps(
                {
                    "propagation": record.environment_object_propagation,
                    "data": record.environment_object,
                }
            )

        geometry3d = _geometry3d_for_insert(record.geometry3d, summary, idx)

        query_list.append(
            {
                "geom2d": json.dumps(record.image_pixel_geometry),
                "geom3d": json.dumps(geometry3d) if geometry3d else None,
                "image": image["id"],
                "user": user,
                "cropped_image": None,
                "object_type": record.object_type,
                "source": SOURCE_EXTERNAL,
                "meta_type": record.meta_type or config_name,
                "data": json.dumps(record.metadata) if record.metadata else None,
                "reviewed": record.reviewed,
                "resight_set": record.resight_set,
                "data_env": data_env,
                "group_area": record.group_area,
                "tags": record.tags,
            }
        )
        summary.imported += 1

        try:
            existing_geometries.setdefault(image["id"], []).append(
                geometry.shape(record.image_pixel_geometry)
            )
        except (GEOSException, ValueError, TypeError):
            pass

        _emit_progress(progress_callback, len(records), idx)

    if query_list and not options.dry_run:
        _insert_objects(db, query_list)

    _emit_progress(progress_callback, 1, 1)
    if not meta_config.get("object_sub_type"):
        summary.warnings.append(
            "Project configuration has no object_sub_type; imported subspecies stay in metadata."
        )
    return summary


def load_project_configuration(db: DBHandler) -> dict[str, Any]:
    config_row = db.load_config()
    if not config_row or not config_row.get("configuration"):
        raise ValueError("WISDAM project has no stored configuration")
    return json.loads(config_row["configuration"])


def _insert_objects(db: DBHandler, query_list: list[dict[str, Any]]) -> None:
    query = r"""Insert into objects
        (geom2d, geom3d, image, user, cropped_image, object_type, source, meta_type, data, reviewed,
         resight_set, data_env, group_area, tags)
        Values
        (SETSrid(GeomFromGEOJSON(:geom2d), -1),
         CASE WHEN :geom3d IS NULL THEN NULL ELSE SETSrid(GeomFromGeoJSON(:geom3d), 4979) END,
         :image, :user, :cropped_image, :object_type, :source, :meta_type, :data, :reviewed,
         :resight_set, :data_env, :group_area, :tags)"""

    db.con.executemany(query, query_list)
    db.con.commit()


def _geometry3d_for_insert(
    geojson: dict[str, Any] | None, summary: ImportObjectSummary, record_index: int
) -> dict[str, Any] | None:
    if geojson is None:
        return None
    if not _geometry_has_z(geojson):
        summary.warnings.append(
            f"Record {record_index + 1} has geom3d without Z coordinates; geom3d was skipped."
        )
        return None

    geojson = geojson.copy()
    geojson["crs"] = {"type": "name", "properties": {"name": "EPSG:4979"}}
    return geojson


def _add_unknown_object_types(
    db: DBHandler,
    records: list[ImportObjectRecord],
    configuration: dict[str, Any],
    config_name: str,
    summary: ImportObjectSummary,
    dry_run: bool = False,
) -> None:
    object_types = configuration["meta_config"][config_name].setdefault(
        "object_types", {}
    )
    changed = False

    for record in records:
        object_type = record.object_type.strip()
        if not object_type:
            continue

        if object_type not in object_types:
            object_types[object_type] = []
            summary.unknown_object_types.setdefault(object_type, [])
            changed = True

        if record.subspecies and record.subspecies not in object_types[object_type]:
            object_types[object_type].append(record.subspecies)
            summary.unknown_object_types.setdefault(object_type, []).append(
                record.subspecies
            )
            changed = True

    if changed and not dry_run:
        db.store_object_types(object_types, config_name=config_name)


def _validate_metadata_against_config(
    records: list[ImportObjectRecord],
    configuration: dict[str, Any],
    summary: ImportObjectSummary,
) -> None:
    configured_metadata = _configured_metadata_keys(configuration)
    configured_environment = set(configuration.get("environment_data", {}).keys())

    imported_metadata = set()
    imported_environment = set()
    for record in records:
        imported_metadata.update(record.metadata.keys())
        imported_environment.update(record.environment_object.keys())

    summary.unknown_metadata_keys = sorted(imported_metadata - configured_metadata)
    summary.unknown_environment_keys = sorted(
        imported_environment - configured_environment
    )

    if imported_metadata and not imported_metadata.intersection(configured_metadata):
        summary.warnings.append(
            "Imported object metadata has no key overlap with the project metadata configuration."
        )


def _configured_metadata_keys(configuration: dict[str, Any]) -> set[str]:
    keys: set[str] = set()
    for meta_config in configuration.get("meta_config", {}).values():
        if meta_config.get("object_main_type", {}).get("naming"):
            keys.add(meta_config["object_main_type"]["naming"])
        if meta_config.get("object_sub_type", {}).get("naming"):
            keys.add(meta_config["object_sub_type"]["naming"])
        option = meta_config.get("object_sub_type", {}).get(
            "object_sub_type_option", {}
        )
        if option.get("name"):
            keys.add(option["name"])
        for value in meta_config.values():
            if isinstance(value, dict) and value.get("name"):
                keys.add(value["name"])
    return keys


def _load_existing_geometries(
    db: DBHandler,
) -> dict[int, list[geometry.base.BaseGeometry]]:
    existing: dict[int, list[geometry.base.BaseGeometry]] = {}
    for row in db.obj_load_for_ai_import_no_cropped_image():
        if row["geo2d"]:
            try:
                existing.setdefault(row["image"], []).append(
                    geometry.shape(json.loads(row["geo2d"]))
                )
            except (GEOSException, ValueError, TypeError, json.JSONDecodeError):
                logger.debug("Skipping existing object with invalid geometry: %s", row)
    return existing


def _is_duplicate(
    geom2d: dict[str, Any],
    existing_geometries: list[geometry.base.BaseGeometry],
    tolerance: float,
) -> bool:
    try:
        new_geometry = geometry.shape(geom2d)
    except (GEOSException, ValueError, TypeError):
        return False

    return any(
        equals_exact(new_geometry, existing, tolerance)
        for existing in existing_geometries
    )


def _load_image_for_record(
    db: DBHandler, record: ImportObjectRecord, image_base_path: Path | None = None
) -> dict[str, Any] | None:
    if record.image_path is None:
        return None

    candidates = _image_path_candidates(record.image_path, image_base_path)
    for candidate in candidates:
        image = db.load_image_by_path(candidate)
        if image is not None:
            return image

    for candidate in candidates:
        found = db.load_image_id_path_parts("%" + candidate.as_posix() + "%")
        if found and len(found) == 1:
            return db.load_image(found[0]["id"])

    found = db.load_image_id_path_parts("%" + record.image_path.name + "%")
    if found and len(found) == 1:
        return db.load_image(found[0]["id"])

    return None


def _image_path_candidates(
    path_value: Path, image_base_path: Path | None
) -> list[Path]:
    candidates = [path_value]
    if image_base_path is not None and not path_value.is_absolute():
        candidates.insert(0, image_base_path / path_value)
    return candidates


def _read_json_document(path_json: Path) -> dict[str, Any]:
    with path_json.open("r", encoding="utf-8") as fid:
        document = json.load(fid)
    if not isinstance(document, dict):
        raise ValueError("JSON object import expects a JSON object at document root")
    return document


def _metadata_version(document: dict[str, Any]) -> str | None:
    wisdam_block = document.get("wisdam")
    if isinstance(wisdam_block, dict) and wisdam_block.get("metadata_version"):
        return str(wisdam_block["metadata_version"])
    if document.get("metadata_version"):
        return str(document["metadata_version"])
    return None


def _check_metadata_version(
    summary: ImportObjectSummary, options: ImportObjectOptions
) -> None:
    if (
        options.metadata_version_expected
        and summary.metadata_version != options.metadata_version_expected
    ):
        summary.warnings.append(
            f"Metadata version mismatch: expected {options.metadata_version_expected}, "
            f"found {summary.metadata_version}"
        )


def _first_meta_config(configuration: dict[str, Any]) -> dict[str, Any]:
    config_name = _first_config_name(configuration)
    return configuration["meta_config"][config_name]


def _first_config_name(configuration: dict[str, Any]) -> str:
    try:
        return next(iter(configuration["meta_config"]))
    except (KeyError, StopIteration) as exc:
        raise ValueError("Project configuration has no meta_config entry") from exc


def _first_path(properties: dict[str, Any], keys: tuple[str, ...]) -> Path | None:
    value = _first_text(properties, keys)
    if value:
        return Path(value)
    return None


def _first_text(properties: dict[str, Any], keys: tuple[str, ...]) -> str:
    for key in keys:
        value = properties.get(key)
        if value is not None and str(value).strip():
            return str(value).strip()
    return ""


def _text_or_none(value: Any) -> str | None:
    if value is None:
        return None
    value = str(value).strip()
    return value or None


def _first_geometry(
    properties: dict[str, Any], keys: tuple[str, ...]
) -> dict[str, Any] | None:
    for key in keys:
        parsed = _parse_geometry(properties.get(key))
        if parsed is not None:
            return parsed
    return None


def _parse_geometry(value: Any) -> dict[str, Any] | None:
    if value in (None, "", {}):
        return None
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except json.JSONDecodeError:
            return None
    if not isinstance(value, dict):
        return None
    if value.get("type") and value.get("coordinates") is not None:
        return value
    return None


def _normalise_dict(value: Any) -> dict[str, Any]:
    if value in (None, ""):
        return {}
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except json.JSONDecodeError:
            return {}
    if isinstance(value, dict):
        return value.copy()
    return {}


def _normalise_environment(value: Any) -> dict[str, Any]:
    data = _normalise_dict(value)
    if not data:
        return {"propagation": 0, "data": {}}
    if "data" not in data:
        return {
            "propagation": _coerce_int(data.get("propagation"), default=0),
            "data": {k: v for k, v in data.items() if k != "propagation"},
        }
    return {
        "propagation": _coerce_int(data.get("propagation"), default=0),
        "data": _normalise_dict(data.get("data")),
    }


def _coerce_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def _geometry_has_z(geojson: dict[str, Any]) -> bool:
    def has_z(coordinates: Any) -> bool:
        if not isinstance(coordinates, list):
            return False
        if coordinates and all(isinstance(item, (int, float)) for item in coordinates):
            return len(coordinates) >= 3
        return any(has_z(item) for item in coordinates)

    return has_z(geojson.get("coordinates"))


def _emit_progress(progress_callback, maximum: int, value: int) -> None:
    if progress_callback is None:
        return
    if hasattr(progress_callback, "emit"):
        progress_callback.emit((maximum, value))
    elif hasattr(progress_callback, "put"):
        progress_callback.put(("progress", (maximum, value)))
