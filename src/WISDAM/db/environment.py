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


from enum import IntEnum


class EnvSource(IntEnum):
    direct = 0
    from_image_propagation = 1
    from_object = 2
    from_object_propagation = 3


def propagate_env_data_next_image(env_data: dict):

    # If the original env data is from an object, we will set as propagated from object
    if env_data["propagation"] == EnvSource.from_object:
        env_data["propagation"] = EnvSource.from_object_propagation

    # If propagation is no, this means it is from a user input directly
    elif env_data["propagation"] == EnvSource.direct:

        env_data["propagation"] = EnvSource.from_image_propagation

    else:
        # If env data is already from image propagation or object propagation
        # Do not change the propagation value
        pass

    return env_data

