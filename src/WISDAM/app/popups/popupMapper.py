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


import logging
from pathlib import Path

import pyproj.exceptions as pyproj_exception
from pyproj import CRS

from PySide6.QtWidgets import QWidget, QFileDialog
from PySide6.QtCore import Qt, SignalInstance, Signal, QPointF

from app.utils_qt import change_led_color
from app.gui_design.ui_mapper import Ui_popup_mapper

from WISDAMcore.mapping.type_selector import mapper_load_from_dict
from WISDAMcore.mapping.base_class import MappingType, MappingBase
from WISDAMcore.mapping.plane import MappingPlane
from WISDAMcore.mapping.raster import MappingRaster
from WISDAMcore.exceptions import FileNotSupportedError, MappingError

logger = logging.getLogger(__name__)


class POPUPMapper(QWidget):

    send_mapper_dict: SignalInstance = Signal(dict, bool)

    def __init__(self):
        super().__init__()
        self.ui = Ui_popup_mapper()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        self.dragPos = QPointF(0, 0)

        self.ui.btn_save.clicked.connect(self.get_mapper_dict)
        self.ui.btn_close.clicked.connect(self.close_check)
        self.ui.btn_discard.clicked.connect(self.close_check)

        self.ui.rd_select_raster_mapper.clicked.connect(self.show_raster_mapper)
        self.ui.rd_select_plane_mapper.clicked.connect(self.show_plane_mapper)

        self.ui.btn_select_raster.clicked.connect(self.get_mapper_from_file)
        self.ui.btn_set_std_crs.clicked.connect(self.set_standard_crs)

        self.mapper: MappingBase | MappingRaster | MappingPlane | None = None

        # window drag mouse moving
        def move_window(event):
            if event.buttons() == Qt.LeftButton and not self.isMaximized():
                self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos.toPoint())
                self.dragPos = event.globalPosition()
                event.accept()

        # move by top frame and cropped image
        self.ui.frame_top.mouseMoveEvent = move_window

    def mousePressEvent(self, event):
        self.dragPos = event.globalPosition()

    def close_check(self):
        if self.mapper is not None:
            self.close()

    def set_standard_crs(self):
        self.ui.rd_crs_manual.setChecked(True)
        self.ui.le_manual_crs.setText("EPSG:4326+3855")

    def show_raster_mapper(self):
        self.clear_crs_fields()
        self.ui.frame_raster_mapper.setVisible(True)
        self.ui.frame_plane_mapper.setVisible(False)

    def show_plane_mapper(self):
        self.clear_crs_fields()
        self.ui.frame_raster_mapper.setVisible(False)
        self.ui.frame_plane_mapper.setVisible(True)

    def set_mapper(self, mapper_dict: dict | None):
        # Set data

        # Reset data before showing the window
        self.clear_plane_mapper_fields()
        self.clear_raster_mapper_fields()
        self.clear_crs_fields()
        self.mapper = None

        if mapper_dict is None:
            return

        try:
            self.mapper = mapper_load_from_dict(mapper_dict)
        except (ValueError, NotImplementedError, MappingError):
            logger.error("Stored Mapper is not possible to use")
            return

        if self.mapper is None:
            return

        if self.mapper.type.value == MappingType.HorizontalPlane.value:

            self.ui.rd_select_plane_mapper.setChecked(True)
            self.ui.frame_raster_mapper.setVisible(False)
            self.ui.frame_plane_mapper.setVisible(True)
            self.ui.le_plane_height.setText(str(self.mapper.plane_altitude))

            # Let Pyproj try to estimate a proper espg code
            # otherwise use the wkt string from the crs
            # at this stage the mapper.crs has to be set otherwise it would be a failure in the database
            plane_crs = self.mapper.crs.to_epsg(min_confidence=40)
            if plane_crs is not None:
                plane_crs = "EPSG:" + str(plane_crs)
            else:
                plane_crs = self.mapper.crs_wkt

            self.ui.pltext_plane_crs.setPlainText(plane_crs)

        elif self.mapper.type.value == MappingType.Raster.value:

            self.ui.rd_select_raster_mapper.setChecked(True)
            self.ui.frame_raster_mapper.setVisible(True)
            self.ui.frame_plane_mapper.setVisible(False)
            self.ui.pltext_raster_filepath.setPlainText(mapper_dict['type'])
            self.set_raster_mapper()

    def get_mapper_dict(self):

        recalculate = self.ui.rd_recalculate.isChecked()

        crs = None
        crs_text = ''
        if self.ui.rd_select_plane_mapper.isChecked():

            try:
                plane_height = float(self.ui.le_plane_height.text())
                crs_text = self.ui.pltext_plane_crs.toPlainText()
            except ValueError:
                logger.warning("Entered plane height is not a real number")
                return

            mapper = MappingPlane(None, plane_height)

        elif self.ui.rd_select_raster_mapper.isChecked():

            try:
                mapper = MappingRaster(Path(self.ui.pltext_raster_filepath.toPlainText()), None, allow_no_crs=True)
                crs_text = self.ui.pltext_raster_crs.toPlainText()

            except FileNotSupportedError:
                logger.error("Specified file can not be opened with rasterio")
                return

            if mapper.transform.is_identity:
                logger.warning("Raster has not geo transformation/World file")
                return

        else:
            logger.warning("No Mapper is selected")
            return

        if self.ui.rd_crs_manual.isChecked():

            crs_text = self.ui.le_manual_crs.text()

        if not crs_text:
            logger.warning("No coordinate system is specified")
            return

        try:
            crs = CRS(crs_text)
        except pyproj_exception.CRSError:
            logger.error("Specified coordinate system is not valid")
            return

        if crs is None:
            logger.warning("No coordinate system is specified")
            return

        if len(crs.axis_info) < 3:
            logger.warning("Coordinate System has not vertical axis")
            return

        mapper.crs = crs
        self.send_mapper_dict.emit(mapper.param_dict, recalculate)

        self.close()

        logger.info("Mapper was changed", extra={"finished": True})

    def clear_crs_fields(self):
        self.ui.le_manual_crs.clear()
        self.ui.rd_crs_manual.setChecked(False)

    def clear_plane_mapper_fields(self):
        self.ui.rd_select_plane_mapper.setChecked(False)
        self.ui.le_plane_height.clear()
        self.ui.pltext_plane_crs.clear()

    def clear_raster_mapper_fields(self):
        self.ui.rd_select_raster_mapper.setChecked(False)
        change_led_color(self.ui.led_rasterio_possible, on=False)
        change_led_color(self.ui.led_raster_geo_transform, on=False)
        change_led_color(self.ui.led_raster_crs, on=False)
        self.ui.pltext_raster_filepath.clear()
        self.ui.le_raster_pixel_size.clear()
        self.ui.pltext_raster_crs.clear()

    def get_mapper_from_file(self):

        self.clear_raster_mapper_fields()
        self.mapper = None

        raster_path, _ = QFileDialog.getOpenFileName(self, caption="Raster File for Mapping")
        if raster_path:

            try:
                self.mapper = MappingRaster(Path(raster_path), crs=None, allow_no_crs=True)
            except FileNotSupportedError:
                logger.error("Specified file can not be opened with rasterio")
                return

            self.set_raster_mapper()

    def set_raster_mapper(self):

        change_led_color(self.ui.led_rasterio_possible, on=True)
        self.ui.pltext_raster_filepath.setPlainText(self.mapper.path.as_posix())

        # rasterio returns identity if file has no geo-reference
        gt_flag = False
        if not self.mapper.transform.is_identity:
            gt_flag = True

        self.ui.le_raster_pixel_size.setText(str(self.mapper.resolution))
        change_led_color(self.ui.led_raster_geo_transform, on=gt_flag)

        if self.mapper.crs is not None:

            crs_has_z_axis = True if len(self.mapper.crs.axis_info) > 2 else False
            change_led_color(self.ui.led_raster_crs, on=True)
            change_led_color(self.ui.led_raster_is_vertical, on=crs_has_z_axis)
            rester_epsg = self.mapper.crs.to_epsg(min_confidence=40)
            if rester_epsg is not None:
                rester_crs = "EPSG:" + str(rester_epsg)
            else:
                rester_crs = self.mapper.crs_wkt

            self.ui.pltext_raster_crs.setPlainText(rester_crs)


