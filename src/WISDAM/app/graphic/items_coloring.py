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

import colorsys

from PySide6.QtGui import QColor

from app.var_classes import look_up_attribute_db_column, ColorGui

golden_ratio_conjugate = 0.618033988749895


# HSV values in [0..1[
# returns [r, g, b] values from 0 to 255
def hsv_to_rgb(h, s, v):
    h_i = int(h * 6)
    f = h * 6 - h_i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if h_i == 0:
        r, g, b = v, t, p
    if h_i == 1:
        r, g, b = q, v, p
    if h_i == 2:
        r, g, b = p, v, t
    if h_i == 3:
        r, g, b = p, q, v
    if h_i == 4:
        r, g, b = t, p, v
    if h_i == 5:
        r, g, b = v, p, q

    return [(r * 256), (g * 256), (b * 256)]


# http://devmag.org.za/2012/07/29/how-to-choose-colours-procedurally-algorithms/
def golden_colors(n, offset=0.3, saturation=0.85, value=0.99):
    # offset = 0.664  # random.random()
    color = []
    for i in range(n):
        color.append([int(x * 255) for x in colorsys.hsv_to_rgb((offset +
                                                                 (golden_ratio_conjugate * i)) % 1, saturation, value)])
    return color


def get_new_color_dict_objects(values_list: list[str | int]):
    """Get new dictionary with colors from golden colors by a value list"""
    color_dict = {}
    colors_sightings = golden_colors(len(values_list))
    for idx, value in enumerate(values_list):
        color = QColor.fromRgb(colors_sightings[idx][0], colors_sightings[idx][1], colors_sightings[idx][2],
                               200).name(QColor.HexArgb)
        color_dict[value] = color
    return color_dict


def update_color_dict_objects(color_dict: dict | None, value: str | int | None):
    """Update color dict with new value"""

    if value is None:
        return color_dict, False

    if value in color_dict['colors'].keys():
        return color_dict, False

    values_old = list(color_dict['colors'].keys())

    values_new = values_old + [value]
    values_new.sort()
    color_dict['colors'] = get_new_color_dict_objects(values_new)

    return color_dict, True


def color_objects_attribute(scene_items: list, attribute: str, color_dict: dict | None = None,
                            default_value: str | int | None = None, default_dict: dict | None = None):
    color_dict_new = None

    if scene_items:

        if default_value is None:
            if attribute in look_up_attribute_db_column.keys():
                default_value = look_up_attribute_db_column[attribute]['default']

        if default_dict is not None:
            if attribute in default_dict.keys():
                color_dict_new = default_dict[attribute]

        if color_dict is not None:
            color_dict_new = color_dict

        if color_dict_new is None:

            color_dict_new = {'attribute': attribute, 'colors': {}}

            values = []
            for item in scene_items:
                value = getattr(item, attribute)
                if value is None:
                    value = default_value

                if value not in values and value is not None:
                    values.append(value)

            values.sort()

            if default_value is not None:
                if default_value in values:
                    values.insert(0, values.pop(values.index(default_value)))
                else:
                    values.insert(0, default_value)

            colors = get_new_color_dict_objects(values)
            color_dict_new['colors'] = colors

        for item in scene_items:
            value = getattr(item, attribute)
            if value is not None and value in color_dict_new['colors'].keys():

                # It could be that default dict or passed color dict does not have this value
                item.set_color(color_dict_new['colors'].get(value, ColorGui.color_invalid_attribute_scenes))
            else:
                item.set_color(ColorGui.color_invalid_attribute_scenes)

    return color_dict_new
