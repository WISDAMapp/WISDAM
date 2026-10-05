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

import logging
from pathlib import Path


_warned_keys: set[str] = set()
_triggered_warnings: dict[str, str] = {}


def is_probable_proj_grid_error(error: BaseException | str | None) -> bool:
    if error is None:
        return False

    text = str(error).casefold()
    return any(
        marker in text
        for marker in (
            "proj",
            "coordinate transformation",
            "grid",
            "cdn.proj.org",
            "download",
            "network",
            "curl",
            ".tif",
            ".tiff",
            ".gtx",
            ".gsb",
        )
    )


def _message(
    action: str,
    error: BaseException | str | None = None,
    image_path: Path | None = None,
) -> str:
    image_info = f" for '{image_path.name}'" if image_path is not None else ""
    detail = f" Details: {error}" if error else ""
    return (
        f"{action} failed{image_info}. Required PROJ transformation grids may be missing locally "
        "and could not be downloaded. Check the internet connection or add the grid files to the "
        f"WISDAM proj_dir.{detail}"
    )


def log_proj_grid_warning_once(
    logger: logging.Logger,
    key: str,
    action: str,
    error: BaseException | str | None = None,
    image_path: Path | None = None,
) -> None:
    message = _message(action, error, image_path)
    _triggered_warnings.setdefault(key, message)

    if key in _warned_keys:
        return

    _warned_keys.add(key)
    logger.warning(message)


def collect_proj_grid_warnings() -> list[tuple[str, str]]:
    return list(_triggered_warnings.items())


def log_collected_proj_grid_warnings_once(
    logger: logging.Logger, warnings: list[tuple[str, str]] | None
) -> None:
    if not warnings:
        return

    for key, message in warnings:
        if key in _warned_keys:
            continue

        _warned_keys.add(key)
        _triggered_warnings.setdefault(key, message)
        logger.warning(message)
