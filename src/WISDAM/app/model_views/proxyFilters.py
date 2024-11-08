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


import re
from app.model_views.galleryView import CustomSortFilterProxyModel
from app.model_views.aiView import AICustomSortFilterProxyModel


def set_filter_boolean(proxy_model: CustomSortFilterProxyModel | AICustomSortFilterProxyModel,
                       filter_pass, caller, key):
    if caller.isChecked():
        filter_pass[key] = True
    else:
        filter_pass.pop(key, None)
    proxy_model.set_filter_data(filter_pass)


def set_filter_check_value(proxy_model: CustomSortFilterProxyModel | AICustomSortFilterProxyModel,
                           filter_pass, caller, key, value):
    if caller.isChecked():
        if key in filter_pass:
            filter_pass[key].append(value)
        else:
            filter_pass[key] = [value]
    else:
        if key in filter_pass:
            if value in filter_pass[key]:
                filter_pass[key].remove(value)
            if not filter_pass[key]:
                filter_pass.pop(key, None)
    proxy_model.set_filter_data(filter_pass)


def set_filter_value(proxy_model: CustomSortFilterProxyModel | AICustomSortFilterProxyModel, filter_pass, caller, key,
                     type_value):
    if caller.text():
        if type_value == 'int':
            if re.match(r"[-+]?\d+(\0*)?$", caller.text()) is not None:
                filter_pass[key] = int(caller.text())
            else:
                caller.setText("")
                if key in filter_pass:
                    filter_pass.pop(key, None)

        elif type_value == 'string':
            filter_pass[key] = caller.text()
    else:
        filter_pass.pop(key, None)
    proxy_model.set_filter_data(filter_pass)


def set_filter_slider(proxy_model: CustomSortFilterProxyModel | AICustomSortFilterProxyModel, filter_pass, caller, key,
                      scale=1):
    filter_pass[key] = float(caller.value()) / scale
    proxy_model.set_filter_data(filter_pass)
