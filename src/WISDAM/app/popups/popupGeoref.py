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


import sys
import traceback
import numpy as np
from numpy import cos, sin
from pathlib import Path
import logging
from pyproj import CRS

# Pyside imports
from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget

# Imports from our packages
from app.gui_design.ui_georef import Ui_popup_georef
from app.var_classes import is_number
from core_interface.wisdamIMAGE import WISDAMImage
from db.dbHandler import DBHandler
from core_interface.update_image_object_geometry import update_mapped_geom

from WISDAMcore.image.ortho import IMAGEOrtho
from WISDAMcore.mapping.base_class import MappingBase
from WISDAMcore.transform.rotation import Rotation
from WISDAMcore.image.perspective import IMAGEPerspective
from WISDAMcore.transform.utm_converter import point_convert_utm_wgs84_egm2008
from WISDAMcore.transform.coordinates import CoordinatesTransformer

logger = logging.getLogger(__name__)


class WorkerSignal(QtCore.QObject):
    finished: QtCore.SignalInstance = QtCore.Signal()
    error: QtCore.SignalInstance = QtCore.Signal(tuple)
    result: QtCore.SignalInstance = QtCore.Signal(tuple)
    # progress: QtCore.SignalInstance = QtCore.Signal(tuple)


def georef_recalculate(db_path: Path, user: str, image_ids: list, rot_cam: np.ndarray, position: list,
                       sensor_width_mm: float, focal_mm: float, mapping: MappingBase):
    numbers_all_geom_updated = 0
    number_images_updated = 0
    georef_success_number = 0
    number_all_objects = 0

    db = DBHandler.from_path(db_path, user)

    for image_id in image_ids:

        image = WISDAMImage.from_db(db.load_image(image_id), mapping)

        # TODO this should be done better
        if isinstance(image, IMAGEOrtho):
            continue

        result = point_convert_utm_wgs84_egm2008(CRS("EPSG:4326+3855"), position[0], position[1], position[2])

        if result is not None:
            x, y, z, crs = result
            position = np.array([x, y, z])

            orientation = Rotation(rot_cam)
            image_model = IMAGEPerspective(width=image.width, height=image.height, camera=image.image_model.camera,
                                           position=position, crs=crs, orientation=orientation, mapper=mapping)
            image.image_model = image_model
            gsd = 0.0
            area = 0.0
            footprint = None
            center = None
            if image_model.is_geo_referenced:
                # if the image is geo referenced try to calculate the footprint
                # as well estimate area and gsd
                res = image_model.map_footprint()
                if res is not None:
                    coordinates, gsd, area = res
                    coo_wgs84 = CoordinatesTransformer.from_crs(image.image_model.crs, CRS.from_epsg(4979),
                                                                coordinates)
                    footprint = coo_wgs84.geojson(geom_type='Polygon')
                res = image_model.map_center_point()
                if res is not None:
                    coordinates, gsd_center = res
                    point_mapped = CoordinatesTransformer.from_crs(image.image_model.crs,
                                                                   CRS.from_epsg(4979), coordinates)
                    center = point_mapped.geojson(geom_type='Point')

                if footprint is not None and center is not None:
                    georef_success_number += 1

                # We always will overwrite mapped attributes even if they None will override existing geometry
                db.image_update_georef(image=image, gsd=gsd, area=area,
                                       center_json=center, footprint_json=footprint)

                nr_of_objects, nr_of_objects_mapped, nr_of_objects_not_mapped = update_mapped_geom(db, image)

                number_images_updated += 1
                numbers_all_geom_updated += nr_of_objects_mapped
                number_all_objects += nr_of_objects

    changed_flag = True if number_images_updated > 0 else False
    return ('Images updated: ' + str(number_images_updated) + '\nGeometries updated: ' +
            str(numbers_all_geom_updated) + 'of ' + str(number_all_objects), changed_flag)


class Worker(QtCore.QRunnable):

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignal()
        # self.kwargs['progress_callback'] = self.signals.progress

    @QtCore.Slot()
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs, )
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()


class POPUPGeoref(QWidget):
    georef_updated: QtCore.SignalInstance = QtCore.Signal(bool)
    closed: QtCore.SignalInstance = QtCore.Signal(bool)

    def __init__(self):
        QWidget.__init__(self, parent=None)

        self.ui = Ui_popup_georef()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.ui.btn_save.clicked.connect(self.start_recalculate)
        self.ui.btn_close.clicked.connect(self.close_ui)
        self.ui.cmb_angles.currentIndexChanged.connect(self.angle_selector)

        self._db: DBHandler | None = None
        self.threadpool = QtCore.QThreadPool()
        self._image_ids = []
        self._user = ''
        self.mapper: MappingBase | None = None

        self.updated_flag = False

        self.ui.frame_spinner.hide()

    @property
    def db(self):
        return self._db

    @db.setter
    def db(self, db_input: DBHandler):
        self._db = db_input

    @property
    def image_ids(self):
        return self._image_ids

    @image_ids.setter
    def image_ids(self, image_ids: list):
        self._image_ids = image_ids

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user: str):
        self._user = user

    def thread_output(self, s):
        text, changed_flag = s
        self.ui.lbl_info.setText(text)
        self.updated_flag = changed_flag
        self.georef_updated.emit(changed_flag)

    def thread_complete(self):
        self.ui.waiting_spinner.stop()

    def close_ui(self):

        if not self.threadpool.activeThreadCount():
            self.ui.lbl_info.setText('')

            self.ui.input_yaw.setText('')
            self.ui.input_roll.setText('')
            self.ui.input_pitch.setText('')
            self.ui.input_phi.setText('')
            self.ui.input_kappa.setText('')
            self.ui.input_omega.setText('')
            self.ui.input_heading.setText('')
            self.ui.input_longitude.setText('')
            self.ui.input_latitude.setText('')
            self.ui.input_height_above_ground.setText('')
            self.ui.input_focal_mm.setText('')
            self.ui.input_sensor_width.setText('')

            self.ui.btn_save.show()
            self.ui.frame_spinner.hide()

            self.closed.emit(True) if self.updated_flag else self.closed.emit(False)
            self.close()

    def angle_selector(self):
        """change the angle sector page and delete all contents"""

        self.ui.lbl_info.setText('')

        self.ui.input_yaw.setText('')
        self.ui.input_roll.setText('')
        self.ui.input_pitch.setText('')
        self.ui.input_phi.setText('')
        self.ui.input_kappa.setText('')
        self.ui.input_omega.setText('')
        self.ui.input_heading.setText('')

        self.ui.stackedWidget.setCurrentIndex(self.ui.cmb_angles.currentIndex())

    def check_input(self):
        """check input"""

        # if not is_number(self.ui.input_sensor_width.text()):
        #    return False

        # if not is_number(self.ui.input_focal_mm.text()):
        #    return False

        if not (is_number(self.ui.input_latitude.text()) and
                is_number(self.ui.input_longitude.text()) and
                is_number(self.ui.input_height_above_ground.text())):
            return False

        latitude = float(self.ui.input_latitude.text())
        if abs(latitude) > 90:
            return False

        longitude = float(self.ui.input_longitude.text())
        if longitude > 360 or longitude < 0:
            return False

        height = float(self.ui.input_height_above_ground.text())
        if height > 8000 or height < 0.1:
            return False

        if self.ui.cmb_angles.currentIndex() == 0:
            if not is_number(self.ui.input_heading.text()):
                return False

        elif self.ui.cmb_angles.currentIndex() == 1:
            if not (is_number(self.ui.input_omega.text()) and
                    is_number(self.ui.input_phi.text()) and
                    is_number(self.ui.input_kappa.text())):
                return False

        elif self.ui.cmb_angles.currentIndex() == 2:
            if not (is_number(self.ui.input_roll.text()) and
                    is_number(self.ui.input_pitch.text()) and
                    is_number(self.ui.input_yaw.text())):
                return False

        return True

    def start_recalculate(self):

        if not self.check_input():
            self.ui.lbl_info.setText('Inputs are not valid numbers or exceeds limits')
            return

        sensor_width_mm = 0  # float(self.ui.input_sensor_width.text())
        focal_mm = 0  # float(self.ui.input_focal_mm.text())
        pos = [float(self.ui.input_longitude.text()),
               float(self.ui.input_latitude.text()),
               float(self.ui.input_height_above_ground.text())]

        if self.ui.cmb_angles.currentIndex() == 0:
            heading = -np.deg2rad(float(self.ui.input_heading.text()))
            r = np.array([[cos(heading), -sin(heading), 0], [sin(heading), cos(heading), 0], [0, 0, 1]])

        elif self.ui.cmb_angles.currentIndex() == 1:
            omega = float(self.ui.input_omega.text())
            phi = float(self.ui.input_phi.text())
            kappa = float(self.ui.input_kappa.text())
            r = Rotation.from_opk_degree(omega, phi, kappa)

        else:
            roll = float(self.ui.input_roll.text())
            pitch = float(self.ui.input_pitch.text())
            yaw = float(self.ui.input_yaw.text())
            r = np.array([[cos(pitch) * cos(yaw), sin(roll) * sin(pitch) * cos(yaw) - cos(roll) * sin(yaw),
                           cos(roll) * sin(pitch) * cos(yaw) + sin(roll) * sin(yaw)],
                          [cos(pitch) * sin(yaw), sin(roll) * sin(pitch) * sin(yaw) + cos(roll) * cos(yaw),
                           cos(roll) * sin(pitch) * sin(yaw) - sin(roll) * cos(yaw)],
                          [-sin(pitch), sin(roll) * cos(pitch), cos(roll) * cos(pitch)]])

        worker = Worker(georef_recalculate, self._db.path, self._user, self._image_ids, r, pos,
                        sensor_width_mm, focal_mm, mapping=self.mapper)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.result.connect(self.thread_output)

        self.threadpool.start(worker)
        self.ui.btn_save.hide()
        self.ui.frame_spinner.show()
        self.ui.waiting_spinner.start()
