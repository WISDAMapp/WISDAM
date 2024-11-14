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

import numpy as np
import math

from PySide6.QtCore import (QPoint, Qt, Slot, Signal)
from PySide6.QtGui import (QKeySequence, QPainter, QShortcut, QTransform)
from PySide6.QtWidgets import (QGraphicsView, QApplication)


class ImageView(QGraphicsView):
    factor = 2.0

    place_nav_rect = Signal(tuple)
    send_text_label_walk_modus = Signal(str)

    def __init__(self, parent=None):
        super(ImageView, self).__init__(parent)
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.setMouseTracking(True)

        # self.setDragMode(QGraphicsView.ScrollHandDrag)
        QShortcut(QKeySequence.ZoomIn, self, activated=self.zoom_in)
        QShortcut(QKeySequence.ZoomOut, self, activated=self.zoom_out)

        # self.scene(): ImageScene() = None

        #self.rightPressed = False
        #self.middlePressed = False
        self.grid_navigation = False

        self._dragPos = QPoint()
        self.x_pos = 0
        self.y_pos = 0

        self.grid_width_index: int = 0
        self.grid_height_index: int = 0
        self.grid_walk_index: int = 0
        self.walk_grid_vector: np.ndarray | None = None
        self.nav_walk_flag_direction: bool = False
        self.nav_walk: bool = False
        self.grid_height: np.ndarray | None = None
        self.grid_height_number: int = 0
        self.grid_width: np.ndarray | None = None
        self.grid_width_number: int = 0
        self.grid_navigation: bool = False
        self.nav_current_scale = 1.0

    def set_drag_mode(self, activate: bool = False):
        if activate:
            self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        else:
            self.setDragMode(QGraphicsView.DragMode.NoDrag)

    def mousePressEvent(self, event):
        if not self.grid_navigation:
            self._dragPos = event.position()
            if event.button() == Qt.MiddleButton:
                QApplication.setOverrideCursor(Qt.ClosedHandCursor)
        super(ImageView, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            QApplication.restoreOverrideCursor()
        super(ImageView, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if not self.grid_navigation:
            new_pos = event.position()
            if event.buttons() == Qt.MiddleButton:
                diff = new_pos - self._dragPos
                self._dragPos = new_pos
                self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - diff.x())
                self.verticalScrollBar().setValue(self.verticalScrollBar().value() - diff.y())
                event.accept()
        super(ImageView, self).mouseMoveEvent(event)

    def wheelEvent(self, event):

        if not self.grid_navigation:
            num_degrees = event.angleDelta().y() / 10
            num_steps = num_degrees / 15.0
            # event.scenePos
            # self.centerOn(self.mapToScene(event.pos()))
            old_mouse_img_coo = self.mapToScene(event.position().toPoint())
            diff_vec = event.position() - QPoint(int(self.width() / 2), int(self.height() / 2))
            self.zoom(pow(0.8, num_steps))
            new_middle_map_pos = self.mapFromScene(old_mouse_img_coo).toPointF() - diff_vec
            self.centerOn(self.mapToScene(new_middle_map_pos.toPoint()))

    @Slot()
    def zoom_in(self):
        self.zoom(ImageView.factor)

    @Slot()
    def zoom_out(self):
        self.zoom(1 / ImageView.factor)

    def zoom(self, f):
        # print(self.transform(), f)
        if not self.grid_navigation:
            if self.transform().m11() < 60 and f > 1:
                self.scale(f, f)
            if self.transform().m11() > 0.01 and f < 1:
                self.scale(f, f)

    # EVENT Resize will call navigation class to change parameters as the view with or height was changed
    def resizeEvent(self, event):
        self.nav_scale(self.nav_current_scale)
        return super(ImageView, self).resizeEvent(event)

    @staticmethod
    def closest_grid_point(center: QPoint, grid_w: float, grid_h: float):

        diff_sort_w = np.argsort(np.abs(grid_w - center.x()))
        diff_sort_h = np.argsort(np.abs(grid_h - center.y()))

        return diff_sort_w[0], diff_sort_h[0]

    def set_navigation_mode(self, navigation_mode: bool):

        self.grid_navigation = navigation_mode
        if self.grid_navigation:
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.nav_scale(self.nav_current_scale)
        else:
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    def set_nav_walk(self, walk_mode: bool = False):
        self.nav_walk = walk_mode

        if self.grid_width is not None:

            if self.nav_walk:
                self.centerOn(self.grid_width[self.grid_width_index], self.grid_height[self.grid_height_index])
        return self.nav_walk

    def nav_scale(self, scale_input: float):

        self.nav_current_scale = scale_input
        if self.grid_navigation:
            if self.scene().items():

                if not scale_input == 1:
                    full_image_scale = self.height() / self.scene().height()

                    # Get the old center of view
                    view_center = self.mapToScene(QPoint(int(self.width() / 2.0), int(self.height() / 2.0)))

                    scale = scale_input * full_image_scale
                    self.setTransform(QTransform(scale, 0.0, 0.0, 0.0, scale, 0.0, 0.0, 0.0, 1.0))
                    # self.nav_top_left()

                    grid_height_single = self.mapToScene(QPoint(self.width(), self.height())) - self.mapToScene(
                        QPoint(0, 0))
                    grid_height_single = grid_height_single.y()
                    self.grid_height_number = round(self.scene().height() * 1.0 / grid_height_single)
                    grid_height_offset = self.scene().height() * 1.0 / self.grid_height_number
                    self.grid_height = np.array(
                        list(range(0, self.grid_height_number))) * grid_height_offset + grid_height_offset / 2.0

                    scale = scale_input * full_image_scale * 0.98
                    self.setTransform(QTransform(scale, 0.0, 0.0, 0.0, scale, 0.0, 0.0, 0.0, 1.0))

                    grid_width_single = self.mapToScene(QPoint(self.width(),
                                                               self.height())) - self.mapToScene(QPoint(0, 0))
                    grid_width_single = grid_width_single.x()

                    self.grid_width_number = math.ceil(self.scene().width() * 1.0 / grid_width_single)

                    grid_scale = round(self.scene().width() * 1.0 / grid_width_single)
                    missing_pixel = self.scene().width() - grid_width_single * grid_scale

                    # 1/100 th of the width of the image is allowed to miss
                    if 0 < missing_pixel < (self.scene().width() / 100.0):
                        self.grid_width_number = round(self.scene().width() * 1.0 / grid_width_single)

                    grid_width_offset = self.scene().width() * 1.0 / self.grid_width_number

                    self.grid_width = np.array(
                        list(range(0, self.grid_width_number))) * grid_width_offset + grid_width_offset / 2

                    self.grid_width_index, \
                        self.grid_height_index = self.closest_grid_point(view_center, self.grid_width, self.grid_height)
                    self.centerOn(self.grid_width[self.grid_width_index],
                                  self.grid_height[self.grid_height_index])

                    # Prepare vector which is used for walking through image

                    walk_grid = np.meshgrid(range(0, len(self.grid_width)), range(0, len(self.grid_height)))
                    for i, row in enumerate(walk_grid[0]):
                        if not i % 2 == 0:
                            walk_grid[0][i] = np.flip(walk_grid[0][i])

                    walk_grid = np.array(walk_grid)
                    self.walk_grid_vector = np.hstack(
                        (np.reshape(walk_grid[0], (walk_grid[0].shape[0] * walk_grid[0].shape[1], 1)),
                         np.reshape(walk_grid[1], (walk_grid[0].shape[0] * walk_grid[0].shape[1], 1))))

                    # find row which should be used
                    row = np.where(np.all(self.walk_grid_vector == [self.grid_width_index,
                                                                    self.grid_height_index], axis=1))[0]
                    self.grid_walk_index = row[0]

                else:
                    self.fitInView(self.scene().itemsBoundingRect(), Qt.KeepAspectRatio)
                    self.grid_walk_index = 0
                    self.walk_grid_vector = np.array([[0, 0]])
                    self.grid_width_index = 0
                    self.grid_height_index = 0

                self.nav_place_rect_overview()
                self.nav_get_center()

    def nav_reset(self):
        self.centerOn(0.0, 0.0)
        self.nav_get_center()
        if self.nav_walk:
            self.set_nav_walk()
        self.setTransform(QTransform(0.2, 0.0, 0.0, 0.0, 0.2, 0.0, 0.0, 0.0, 1.0))

    def nav_get_center(self):
        current_point = self.mapToScene(self.viewport().rect().center())
        self.x_pos = current_point.x()
        self.y_pos = current_point.y()

    def nav_place_rect_overview(self):
        if self.scene().items():
            current_point = self.mapToScene(self.viewport().rect().center())
            rect = self.mapToScene(self.viewport().rect())

            self.place_nav_rect.emit((self.scene().width(), self.scene().height(),
                                      rect.boundingRect().width(), rect.boundingRect().height(),
                                      current_point.x(), current_point.y()))

    def nav_top_left(self):
        if self.scene().items():
            if self.nav_current_scale == 1:
                self.centerOn(0, 0)
            else:
                self.centerOn(self.grid_width[0], self.grid_height[0])
            self.nav_get_center()
            self.nav_walk_flag_direction = False
            self.nav_place_rect_overview()
            self.grid_walk_index = 0
            self.grid_width_index = 0
            self.grid_height_index = 0

    def nav_walk_forward(self):
        if self.walk_grid_vector is not None:
            if self.grid_walk_index < self.walk_grid_vector.shape[0] - 1:
                self.grid_walk_index += 1
                self.centerOn(self.grid_width[self.walk_grid_vector[self.grid_walk_index, 0]],
                              self.grid_height[self.walk_grid_vector[self.grid_walk_index, 1]])
                self.grid_width_index = self.walk_grid_vector[self.grid_walk_index, 0]
                self.grid_height_index = self.walk_grid_vector[self.grid_walk_index, 1]

            if self.grid_walk_index == self.walk_grid_vector.shape[0] - 1:

                self.send_text_label_walk_modus.emit('END OF IMAGE')
            else:
                self.send_text_label_walk_modus.emit('WALK MODE ON')

    def nav_walk_backward(self):
        if self.walk_grid_vector is not None:
            if self.grid_walk_index > 0:
                self.grid_walk_index -= 1
                self.centerOn(self.grid_width[self.walk_grid_vector[self.grid_walk_index, 0]],
                              self.grid_height[self.walk_grid_vector[self.grid_walk_index, 1]])
                self.grid_width_index = self.walk_grid_vector[self.grid_walk_index, 0]
                self.grid_height_index = self.walk_grid_vector[self.grid_walk_index, 1]

            if self.grid_walk_index == 0:
                self.send_text_label_walk_modus.emit('END OF IMAGE')
            else:
                self.send_text_label_walk_modus.emit('WALK MODE ON')

    def nav_right(self):
        if self.nav_walk:
            self.nav_walk_forward()
        else:
            if self.grid_width_index < self.grid_width_number - 1:
                self.grid_width_index += 1
                self.centerOn(self.grid_width[self.grid_width_index], self.grid_height[self.grid_height_index])

        self.nav_place_rect_overview()

    def nav_left(self):
        if self.nav_walk:
            self.nav_walk_backward()
        else:
            if self.grid_width_index > 0:
                self.grid_width_index += -1
                self.centerOn(self.grid_width[self.grid_width_index], self.grid_height[self.grid_height_index])

        self.nav_place_rect_overview()

    def nav_up(self):
        if self.grid_height_index > 0:
            self.grid_height_index += -1
            self.centerOn(self.grid_width[self.grid_width_index], self.grid_height[self.grid_height_index])

        self.nav_place_rect_overview()

    def nav_down(self):
        if self.grid_height_index < self.grid_height_number - 1:
            self.grid_height_index += 1
            self.centerOn(self.grid_width[self.grid_width_index], self.grid_height[self.grid_height_index])

        self.nav_place_rect_overview()

    # fit image to screen
    def fit_view(self):
        scene_items = self.scene().items()
        if not self.grid_navigation and scene_items:
            self.fitInView(self.scene().itemsBoundingRect(), Qt.KeepAspectRatio)
