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


from app.var_classes import ColorGui

# TODO update config


# V1.0.4 and lower using color scheme
#           {"projection": {"attribute": "projection", "colors": {0: "#96ffaa00", 1: "#96ff007f"}}
# V1.05 using
# color_scheme_start = {"projection": {"attribute": "projection", "colors": {0: "#96ffaa00", 1: "#96ff007f"}},
#                      "reviewed": {"attribute": "reviewed", "colors": {0: "#fa6000", 1: "#53fa00"}},
#                      "inspected": {"attribute": "inspected", "colors": {0: "#fa6000", 1: "#53fa00"}}}

def check_update_color_config(color_scheme: dict) -> dict:
    color_config_default = ColorGui.color_scheme_start

    color_scheme_checked = {}
    if color_scheme.get('projection', None):
        color_scheme_checked['projection'] = color_scheme['projection']
        color_scheme_checked['projection']['colors'] = {0: color_scheme['projection']['colors']['0'],
                                                        1: color_scheme['projection']['colors']['1']}
    else:
        color_scheme_checked['projection'] = color_config_default['projection']

    if color_scheme.get('reviewed', None):
        color_scheme_checked['reviewed'] = color_scheme['reviewed']
        color_scheme_checked['reviewed']['colors'] = {0: color_scheme['reviewed']['colors']['0'],
                                                      1: color_scheme['reviewed']['colors']['1']}
    else:
        color_scheme_checked['reviewed'] = color_config_default['reviewed']

    if color_scheme.get('inspected', None):
        color_scheme_checked['inspected'] = color_scheme['inspected']
        color_scheme_checked['inspected']['colors'] = {0: color_scheme['inspected']['colors']['0'],
                                                       1: color_scheme['inspected']['colors']['1']}
    else:
        color_scheme_checked['inspected'] = color_config_default['inspected']

    return color_scheme_checked
