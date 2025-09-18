# ==============================================================================
# This file is part of the WISDAM distribution
# https://github.com/WISDAMapp/WISDAM
# Copyright (C) 2025 Martin Wieser.
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


import json
from collections import OrderedDict
import logging

from PySide6 import QtCore
from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtGui import (QPixmap, QPainter)
from PySide6.QtCore import Qt, Signal, Slot, QSize

from app.gui_design.ui_meta import Ui_popup_meta
from app.popups.popupConfirm import POPUPConfirm

from db.dbHandler import DBHandler

logger = logging.getLogger(__name__)


class POPUPMeta(QWidget):
    """Window for showing and manipulating metadata"""

    # Signals
    object_change = Signal(int, int)
    object_delete = Signal(int, int)
    emit_object_types = Signal(OrderedDict, str)

    def __init__(self):
        QWidget.__init__(self)

        self.ui = Ui_popup_meta()
        self.ui.setupUi(self)
        self.dragPos = QtCore.QPointF(0, 0)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        # Connect Buttons
        self.ui.btn_save.clicked.connect(self.send_values)
        self.ui.btn_delete.clicked.connect(self.delete_item)
        self.ui.btn_close.clicked.connect(self.close_check)

        # Connect Custom Combo Class right click events
        self.ui.cmb_obejcet_types_sub.add_signal.connect(self.add_new_subtype)
        self.ui.cmb_obejcet_types_sub.delete_signal.connect(self.remove_new_subtype)
        self.ui.cmb_obejcet_types_main.add_signal.connect(self.add_new_main_type)
        self.ui.cmb_obejcet_types_main.delete_signal.connect(self.remove_new_main_type)
        self.ui.cmb_obejcet_types_main.activated.connect(self.object_type_main_changed)

        # Connect env frame actions
        self.ui.custom_env_layout.value_changed.connect(self.env_changed)

        self.ui.slider_certainty.valueChanged.connect(self.certainty_change)

        self.data_env: dict | None = None
        self.db: DBHandler | None = None
        self.object_id = 0
        self.image_id = 0
        self.config: OrderedDict = OrderedDict()
        self.config_meta_type = ''
        self.mapping_table = {}
        self.object_types = OrderedDict()
        self.pixmap_orig_size = (0, 0)

        self.change_image_env_none = False
        self.change_image_env_propagate = False

        # Set while loading data if image has no env data or if only propagated
        self.image_env_data_type: bool = False

        # window drag mouse moving
        def move_window(event):
            if event.buttons() == Qt.LeftButton and not self.isMaximized():
                self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos.toPoint())
                self.dragPos = event.globalPosition()
                event.accept()

        # move by top frame and cropped image
        self.ui.frame_top.mouseMoveEvent = move_window
        self.ui.cropped_image.mouseMoveEvent = move_window

    def mousePressEvent(self, event):
        self.dragPos = event.globalPosition()

    def set_db(self, db):
        self.db = db

    def set_scale(self, gsd: float):
        unit = "m"
        unit_scale = 1
        length_v = gsd * self.pixmap_orig_size[1]
        length_h = gsd * self.pixmap_orig_size[0]

        if length_v < 0.50 or length_h < 0.50:
            unit = "cm"
            unit_scale = 100
        self.ui.le_scale_vertical.setText("%3.2f %s" % (length_v * unit_scale, unit))
        self.ui.le_scale_horizontal.setText("%3.2f %s" % (length_h * unit_scale, unit))

    @Slot(object)
    def env_changed(self, config: dict):
        self.data_env = config

    # Environment data
    def configure_environment(self, config: dict | None):
        self.ui.custom_env_layout.set_config(config)

    def configure_object_types(self, config: dict | None):
        self.ui.cmb_obejcet_types_main.clear()
        self.ui.cmb_obejcet_types_sub.clear()

        # Objects Types
        object_types = config['object_types']
        if object_types:
            self.object_types = object_types
            main_names = list(self.object_types.keys())
            self.ui.cmb_obejcet_types_main.addItems(main_names)

    def configure(self, config: dict | None):

        # Clear all settings beforehand
        self.clear_all()

        if config is not None:

            # Set the environment widget/frame
            self.configure_environment(config["environment_data"])

            if config.get("environment_propagation", False):
                self.change_image_env_none = config["environment_propagation"]["first_object_set_override_none_image"]
                self.change_image_env_propagate = config["environment_propagation"][
                    "first_object_set_override_porpagated_image"]

            first_key = list(config['meta_config'].keys())[0]
            self.config_meta_type = first_key
            self.config = config['meta_config'][first_key]

            # Objects Types
            self.configure_object_types(self.config)

            # Main Type Naming
            self.ui.le_object_main_naming.setText(self.config["object_main_type"]["naming"])

            # Show main type option
            if self.config['object_main_type'].get('object_main_type_option', False):
                self.ui.frame_main_type_option.show()
                duo_slider = self.config['object_main_type']["object_main_type_option"]
                self.ui.le_main_type_option_name.setText(duo_slider['name'])
                self.ui.le_main_type_option_value_0.setText(duo_slider['value_0'])
                self.ui.le_main_type_option_value_1.setText(duo_slider['value_1'])
                self.ui.duo_main_type_option.setValue(duo_slider['start_value'])

            # Show subtype
            if self.config.get('object_sub_type', False):

                self.ui.frame_subtype.show()
                self.ui.le_object_sub_naming.setText(self.config['object_sub_type']["naming"])

                # show subtype option
                if self.config['object_sub_type'].get('object_sub_type_option', False):
                    self.ui.frame_sub_type_option.show()
                    triple_slider = self.config['object_sub_type']["object_sub_type_option"]
                    self.ui.le_sub_type_option_name.setText(triple_slider['name'])
                    self.ui.le_sub_type_option_value_0.setText(triple_slider['value_0'])
                    self.ui.le_sub_type_option_value_1.setText(triple_slider['value_1'])
                    self.ui.le_sub_type_option_value_2.setText(triple_slider['value_2'])
                    self.ui.triple_sub_type_option.setValue(triple_slider['start_value'])

            # Combo Items
            if self.config.get('combo_meta_1', False):
                combo_meta = self.config['combo_meta_1']
                self.ui.cmb_meta_1.addItems(combo_meta['items'])
                self.ui.le_meta_cmb_name_1.setText(combo_meta['name'])
                self.ui.cmb_meta_1.setCurrentIndex(0)
                self.ui.frame_cmb_meta_1.show()

            if self.config.get('combo_meta_2', False):
                combo_meta = self.config['combo_meta_2']
                self.ui.cmb_meta_2.addItems(combo_meta['items'])
                self.ui.le_meta_cmb_name_2.setText(combo_meta['name'])
                self.ui.cmb_meta_2.setCurrentIndex(0)
                self.ui.frame_cmb_meta_2.show()

            if self.config.get('combo_meta_3', False):
                combo_meta = self.config['combo_meta_3']
                self.ui.cmb_meta_3.addItems(combo_meta['items'])
                self.ui.le_meta_cmb_name_3.setText(combo_meta['name'])
                self.ui.cmb_meta_3.setCurrentIndex(0)
                self.ui.frame_cmb_meta_3.show()

            # Text inputs
            if self.config.get('input_text_1', False):
                self.ui.le_meta_input_txt_name_1.setText(self.config['input_text_1'])
                self.ui.frame_txt_1.show()

            if self.config.get('input_text_2', False):
                self.ui.le_meta_input_txt_name_2.setText(self.config['input_text_2'])
                self.ui.frame_txt_2.show()

            if self.config.get('input_text_3', False):
                self.ui.le_meta_input_txt_name_3.setText(self.config['input_text_3'])
                self.ui.frame_txt_3.show()

            # DUO SLIDER
            if self.config.get('slider_duo1', False):
                duo_slider = self.config['slider_duo1']
                self.ui.le_meta_duo_name_1.setText(duo_slider['name'])
                self.ui.le_meta_duo_1_value_0.setText(duo_slider['value_0'])
                self.ui.le_meta_duo_1_value_1.setText(duo_slider['value_1'])
                self.ui.duo_meta_1.setValue(duo_slider['start_value'])
                self.ui.frame_duo_1.show()

            if self.config.get('slider_duo2', False):
                duo_slider = self.config['slider_duo2']
                self.ui.le_meta_duo_name_2.setText(duo_slider['name'])
                self.ui.le_meta_duo_2_value_0.setText(duo_slider['value_0'])
                self.ui.le_meta_duo_2_value_1.setText(duo_slider['value_1'])
                self.ui.duo_meta_2.setValue(duo_slider['start_value'])
                self.ui.frame_duo_2.show()

            if self.config.get('slider_duo3', False):
                duo_slider = self.config['slider_duo3']
                self.ui.le_meta_duo_name_3.setText(duo_slider['name'])
                self.ui.le_meta_duo_3_value_0.setText(duo_slider['value_0'])
                self.ui.le_meta_duo_3_value_1.setText(duo_slider['value_1'])
                self.ui.duo_meta_3.setValue(duo_slider['start_value'])
                self.ui.frame_duo_3.show()

            # Triple Slider
            if self.config.get('slider_triple1', False):
                triple_slider = self.config['slider_triple1']
                self.ui.le_meta_triple_name_1.setText(triple_slider['name'])
                self.ui.le_meta_triple_1_value_0.setText(triple_slider['value_0'])
                self.ui.le_meta_triple_1_value_1.setText(triple_slider['value_1'])
                self.ui.le_meta_triple_1_value_2.setText(triple_slider['value_2'])
                self.ui.triple_meta_1.setValue(triple_slider['start_value'])
                self.ui.frame_triple_1.show()

            if self.config.get('slider_triple2', False):
                triple_slider = self.config['slider_triple2']
                self.ui.le_meta_triple_name_2.setText(triple_slider['name'])
                self.ui.le_meta_triple_2_value_0.setText(triple_slider['value_0'])
                self.ui.le_meta_triple_2_value_1.setText(triple_slider['value_1'])
                self.ui.le_meta_triple_2_value_2.setText(triple_slider['value_2'])
                self.ui.triple_meta_2.setValue(triple_slider['start_value'])
                self.ui.frame_triple_2.show()

            if self.config.get('slider_triple3', False):
                triple_slider = self.config['slider_triple3']
                self.ui.le_meta_triple_name_3.setText(triple_slider['name'])
                self.ui.le_meta_triple_3_value_0.setText(triple_slider['value_0'])
                self.ui.le_meta_triple_3_value_1.setText(triple_slider['value_1'])
                self.ui.le_meta_triple_3_value_2.setText(triple_slider['value_2'])
                self.ui.triple_meta_3.setValue(triple_slider['start_value'])
                self.ui.frame_triple_3.show()

            if self.config.get('slider_triple4', False):
                triple_slider = self.config['slider_triple4']
                self.ui.le_meta_triple_name_4.setText(triple_slider['name'])
                self.ui.le_meta_triple_4_value_0.setText(triple_slider['value_0'])
                self.ui.le_meta_triple_4_value_1.setText(triple_slider['value_1'])
                self.ui.le_meta_triple_4_value_2.setText(triple_slider['value_2'])
                self.ui.triple_meta_4.setValue(triple_slider['start_value'])
                self.ui.frame_triple_4.show()

            # Build up the mapping table
            self.mapping_table = {}

            # mapping table main option
            if self.config["object_main_type"].get('object_main_type_option', ''):
                value = self.config["object_main_type"]['object_main_type_option']['name']
                self.mapping_table['object_main_type_option'] = value

            # mapping table sub type
            if self.config.get("object_sub_type"):
                self.mapping_table['object_sub_type'] = self.config['object_sub_type']['naming']

                # mapping table subtype option
                if self.config["object_sub_type"].get('object_sub_type_option', ''):
                    value = self.config["object_sub_type"]['object_sub_type_option']['name']
                    self.mapping_table['object_sub_type_option'] = value

            # mapping table Triple Sliders
            if self.config.get('slider_triple1', ''):
                value = self.config['slider_triple1']['name']
                self.mapping_table['triple_1'] = value

            if self.config.get('slider_triple2', ''):
                value = self.config['slider_triple2']['name']
                self.mapping_table['triple_2'] = value

            if self.config.get('slider_triple3', ''):
                value = self.config['slider_triple3']['name']
                self.mapping_table['triple_3'] = value

            if self.config.get('slider_triple4', ''):
                value = self.config['slider_triple4']['name']
                self.mapping_table['triple_4'] = value

            # mapping table text input
            if self.config.get('input_text_1', ''):
                value = self.config['input_text_1']
                self.mapping_table['txt_1'] = value

            if self.config.get('input_text_2', ''):
                value = self.config['input_text_2']
                self.mapping_table['txt_2'] = value

            if self.config.get('input_text_3', ''):
                value = self.config['input_text_3']
                self.mapping_table['txt_3'] = value

            # mapping table slider duo
            if self.config.get('slider_duo1', ''):
                value = self.config['slider_duo1']['name']
                self.mapping_table['duo_1'] = value

            if self.config.get('slider_duo2', ''):
                value = self.config['slider_duo2']['name']
                self.mapping_table['duo_2'] = value

            if self.config.get('slider_duo3', ''):
                value = self.config['slider_duo3']['name']
                self.mapping_table['duo_3'] = value

            # mapping table combos
            if self.config.get('combo_meta_1', ''):
                value = self.config['combo_meta_1']['name']
                self.mapping_table['cmb_1'] = value

            if self.config.get('combo_meta_2', ''):
                value = self.config['combo_meta_2']['name']
                self.mapping_table['cmb_2'] = value

            if self.config.get('combo_meta_3', ''):
                value = self.config['combo_meta_3']['name']
                self.mapping_table['cmb_3'] = value

    def reset_values_from_config(self):
        """Reset the already configured items. Set slider values, set combo to index 0, clear text fields"""

        self.ui.cmb_obejcet_types_main.setCurrentIndex(-1)
        self.ui.cmb_obejcet_types_sub.clear()

        # reset main type option
        if self.config['object_main_type'].get('object_main_type_option', False):
            self.ui.duo_main_type_option.setValue(self.config['object_main_type']
                                                  ['object_main_type_option']['start_value'])

        # reset subtype option
        if self.config.get('object_sub_type', False):
            if self.config['object_sub_type'].get('object_sub_type_option', False):
                self.ui.triple_sub_type_option.setValue(self.config['object_sub_type']
                                                        ['object_sub_type_option']['start_value'])

        self.ui.slider_certainty.setValue(1)
        self.ui.slider_first_certain.setValue(1)
        self.ui.slider_resight.setValue(0)

        # Combo
        self.ui.cmb_meta_1.setCurrentIndex(0)
        self.ui.cmb_meta_2.setCurrentIndex(0)
        self.ui.cmb_meta_3.setCurrentIndex(0)

        # Text Input Fields
        self.ui.le_meta_input_txt_1.clear()
        self.ui.le_meta_input_txt_2.clear()
        self.ui.le_meta_input_txt_3.clear()
        self.ui.txt_notes.clear()

        # Slider Triple
        if self.config.get('slider_triple1', ''):
            self.ui.triple_meta_1.setValue(self.config['slider_triple1']['start_value'])
        if self.config.get('slider_triple2', ''):
            self.ui.triple_meta_2.setValue(self.config['slider_triple2']['start_value'])
        if self.config.get('slider_triple3', ''):
            self.ui.triple_meta_3.setValue(self.config['slider_triple3']['start_value'])
        if self.config.get('slider_triple4', ''):
            self.ui.triple_meta_4.setValue(self.config['slider_triple4']['start_value'])

        # Slider Duo
        if self.config.get('slider_duo1', ''):
            self.ui.duo_meta_1.setValue(self.config['slider_duo1']['start_value'])
        if self.config.get('slider_duo2', ''):
            self.ui.duo_meta_2.setValue(self.config['slider_duo2']['start_value'])
        if self.config.get('slider_duo3', ''):
            self.ui.duo_meta_3.setValue(self.config['slider_duo3']['start_value'])

    def clear_all(self):

        # clear environment config
        self.configure_environment(config=None)
        self.change_image_env_none = False
        self.change_image_env_propagate = False

        # main types
        self.ui.le_object_main_naming.clear()
        self.ui.cmb_obejcet_types_main.clear()
        self.ui.le_main_type_option_name.clear()
        self.ui.le_main_type_option_value_0.clear()
        self.ui.le_main_type_option_value_1.clear()
        self.ui.duo_main_type_option.setValue(0)

        # subtypes
        self.ui.le_object_sub_naming.clear()
        self.ui.cmb_obejcet_types_sub.clear()
        self.ui.le_sub_type_option_name.clear()
        self.ui.le_sub_type_option_value_0.clear()
        self.ui.le_sub_type_option_value_1.clear()
        self.ui.le_sub_type_option_value_2.clear()
        self.ui.triple_sub_type_option.setValue(0)

        # Comments field
        self.ui.txt_notes.clear()

        # Text Box
        self.ui.le_meta_input_txt_name_1.clear()
        self.ui.le_meta_input_txt_1.clear()
        self.ui.le_meta_input_txt_name_2.clear()
        self.ui.le_meta_input_txt_2.clear()
        self.ui.le_meta_input_txt_name_3.clear()
        self.ui.le_meta_input_txt_3.clear()

        # Combo Meta
        self.ui.le_meta_cmb_name_1.clear()
        self.ui.le_meta_cmb_name_2.clear()
        self.ui.le_meta_cmb_name_3.clear()
        self.ui.cmb_meta_1.clear()
        self.ui.cmb_meta_2.clear()
        self.ui.cmb_meta_3.clear()

        # Duo Slider
        self.ui.le_meta_duo_name_1.clear()
        self.ui.le_meta_duo_1_value_0.clear()
        self.ui.le_meta_duo_1_value_1.clear()
        self.ui.duo_meta_1.setValue(0)

        self.ui.le_meta_duo_name_2.clear()
        self.ui.le_meta_duo_2_value_0.clear()
        self.ui.le_meta_duo_2_value_1.clear()
        self.ui.duo_meta_2.setValue(0)

        self.ui.le_meta_duo_name_3.clear()
        self.ui.le_meta_duo_3_value_0.clear()
        self.ui.le_meta_duo_3_value_1.clear()
        self.ui.duo_meta_3.setValue(0)

        # Triple Slider
        self.ui.le_meta_triple_name_1.clear()
        self.ui.le_meta_triple_1_value_0.clear()
        self.ui.le_meta_triple_1_value_1.clear()
        self.ui.le_meta_triple_1_value_2.clear()
        self.ui.triple_meta_1.setValue(0)

        self.ui.le_meta_triple_name_2.clear()
        self.ui.le_meta_triple_2_value_0.clear()
        self.ui.le_meta_triple_2_value_1.clear()
        self.ui.le_meta_triple_2_value_2.clear()
        self.ui.triple_meta_2.setValue(0)

        self.ui.le_meta_triple_name_3.clear()
        self.ui.le_meta_triple_3_value_0.clear()
        self.ui.le_meta_triple_3_value_1.clear()
        self.ui.le_meta_triple_3_value_2.clear()
        self.ui.triple_meta_3.setValue(0)

        self.ui.le_meta_triple_name_4.clear()
        self.ui.le_meta_triple_4_value_0.clear()
        self.ui.le_meta_triple_4_value_1.clear()
        self.ui.le_meta_triple_4_value_2.clear()
        self.ui.triple_meta_4.setValue(0)

        # Meta widgets hide initial while configuration while be set shown again
        self.ui.frame_main_type_option.hide()
        self.ui.frame_subtype.hide()
        self.ui.frame_sub_type_option.hide()
        self.ui.frame_txt_1.hide()
        self.ui.frame_txt_2.hide()
        self.ui.frame_txt_3.hide()
        self.ui.frame_cmb_meta_1.hide()
        self.ui.frame_cmb_meta_2.hide()
        self.ui.frame_cmb_meta_3.hide()
        self.ui.frame_duo_1.hide()
        self.ui.frame_duo_2.hide()
        self.ui.frame_duo_3.hide()
        self.ui.frame_triple_1.hide()
        self.ui.frame_triple_2.hide()
        self.ui.frame_triple_3.hide()
        self.ui.frame_triple_4.hide()

    # ---------------------------------------------------
    # Object Type System
    @Slot(str)
    def add_new_subtype(self, name: str):

        # If main object type is not set, do not store the entered subtype
        if self.ui.cmb_obejcet_types_main.currentText():

            self.object_types[self.ui.cmb_obejcet_types_main.currentText()].append(name)
            self.emit_object_types.emit(self.object_types, self.config_meta_type)

        else:
            self.ui.cmb_obejcet_types_sub.clear()

    @Slot(str)
    def remove_new_subtype(self, name: str):
        if self.ui.cmb_obejcet_types_main.currentText():
            if name in self.object_types[self.ui.cmb_obejcet_types_main.currentText()]:
                self.object_types[self.ui.cmb_obejcet_types_main.currentText()].remove(name)
                self.emit_object_types.emit(self.object_types, self.config_meta_type)

    def object_type_main_changed(self):
        self.ui.cmb_obejcet_types_main.setStyleSheet("")
        self.ui.cmb_obejcet_types_sub.clear()
        if self.ui.cmb_obejcet_types_main.currentText():
            if self.object_types[self.ui.cmb_obejcet_types_main.currentText()]:
                self.ui.cmb_obejcet_types_sub.addItems(self.object_types[self.ui.cmb_obejcet_types_main.currentText()])

    @Slot(str)
    def add_new_main_type(self, name: str):
        self.object_types[name] = []
        self.ui.cmb_obejcet_types_sub.clear()
        self.emit_object_types.emit(self.object_types, self.config_meta_type)

    @Slot(str)
    def remove_new_main_type(self, name: str):

        if name:
            self.object_types.pop(name, None)
            self.ui.cmb_obejcet_types_sub.clear()
            if len(self.object_types) > 0:
                self.ui.cmb_obejcet_types_sub.addItems(self.object_types[self.ui.cmb_obejcet_types_main.currentText()])

            self.emit_object_types.emit(self.object_types, self.config_meta_type)
        else:
            self.ui.cmb_obejcet_types_main.insertItem(0, '')
            self.ui.cmb_obejcet_types_main.setCurrentIndex(0)

    def certainty_change(self):
        if self.sender().value() == 0:
            self.ui.slider_first_certain.setValue(0)

    def load_values(self, object_id: int):

        self.reset_values_from_config()
        self.object_id = object_id

        data = self.db.load_objects_single(self.object_id)
        self.image_id = data["image"]

        self.pixmap_orig_size = (0, 0)
        self.ui.le_scale_vertical.setText(None)
        self.ui.le_scale_horizontal.setText(None)

        # Environment data
        # Get environment data from image
        # If the object has stored as well environment data it will be preferred
        # This is the same for all. Not depending on meta configuration
        # If the object has no env data but the image has one-> immediately store
        # because otherwise it could be that if image env is changed afterwards
        # and object has no env data it will show env data but is not saved if
        # closed without saving
        self.data_env = None

        self.image_env_data_type = None
        if data["data_env_image"] is not None:
            self.data_env = json.loads(data["data_env_image"])
            self.image_env_data_type = self.data_env["propagation"]

            # Set to image propagation because we got it from image
            self.data_env['propagation'] = 1

        if data["data_env"] is not None:
            self.data_env = json.loads(data["data_env"])
        else:
            if data["data_env_image"] is not None:
                self.db.store_objects_env_data(self.object_id, self.data_env)

        # sets the env layout
        self.ui.custom_env_layout.data = self.data_env

        # Cropped image
        # Load the sub image of the object which is stored as blob binary in jpg
        pixmap = QPixmap()
        pixmap.loadFromData(data['cropped_image'], "JPG")
        self.pixmap_orig_size = (pixmap.width(), pixmap.height())
        # Scale to the size of widget to draw in
        w = self.ui.cropped_image.width()
        h = self.ui.cropped_image.height()
        self.ui.cropped_image.setPixmap(pixmap.scaled(w, h, Qt.KeepAspectRatio))

        if data["gsd"]:
            if data["gsd"] > 0.0:
                self.set_scale(data["gsd"])

        meta_data = {}
        if data['data']:
            meta_data = json.loads(data['data'])
        self.set_fields(data['object_type'], meta_data)

    def set_fields(self, object_type: str, data_meta: dict | None):

        # Set Object Type
        if object_type:
            # It could be that object type was deleted from the list but is still in some objects.
            # Therefore, we need to add that object type again
            index_main_type = self.ui.cmb_obejcet_types_main.findText(object_type,
                                                                      flags=Qt.MatchFixedString)
            if index_main_type >= 0:
                self.ui.cmb_obejcet_types_main.setCurrentIndex(index_main_type)
            else:
                self.add_new_main_type(object_type)
                self.ui.cmb_obejcet_types_main.addItem(object_type)
                #  Actually this can only happen by external import, or it was deleted
                self.ui.cmb_obejcet_types_main.setCurrentText(object_type)

        self.object_type_main_changed()

        if data_meta:

            if data_meta.get("firstcertain", ''):
                first_certain = 1 if data_meta["firstcertain"] == "yes" else 0
                self.ui.slider_first_certain.setValue(first_certain)
            if data_meta.get("resight", ''):
                resight = 1 if data_meta["resight"] == "yes" else 0
                self.ui.slider_resight.setValue(resight)

            if data_meta.get("certainty", ''):
                certainty = 1 if data_meta["certainty"] == "yes" else 0
                self.ui.slider_certainty.setValue(certainty)

            # Main Type Option
            if self.config['object_main_type'].get('object_main_type_option', ''):
                if data_meta.get(self.mapping_table.get('object_main_type_option', ''), 0):
                    value = map_text_to_slider(data_meta.get(self.mapping_table.get('object_main_type_option', ''), 0),
                                               self.config['object_main_type']['object_main_type_option'])
                    self.ui.duo_main_type_option.setValue(value)

            # Sub Type
            if self.config.get('object_sub_type', False):

                # Sub Type data
                object_subtype_name = self.mapping_table.get('object_sub_type', '')

                sub_type_name = data_meta.get(object_subtype_name, '')
                if sub_type_name:
                    index_sub_type = self.ui.cmb_obejcet_types_sub.findText(sub_type_name, flags=Qt.MatchFixedString)
                    if index_sub_type >= 0:
                        self.ui.cmb_obejcet_types_sub.setCurrentIndex(index_sub_type)
                    else:
                        self.add_new_subtype(sub_type_name)
                        self.ui.cmb_obejcet_types_sub.addItem(sub_type_name)
                        #  Actually this can only happen by external import, or it was deleted
                        self.ui.cmb_obejcet_types_sub.setCurrentText(sub_type_name)

                # Sub Option
                if self.config['object_sub_type'].get('object_sub_type_option', ''):
                    if data_meta.get(self.mapping_table.get('object_sub_type_option', ''), 0):
                        value = map_text_to_slider(data_meta[self.mapping_table['object_sub_type_option']],
                                                   self.config['object_sub_type']['object_sub_type_option'])
                        self.ui.triple_sub_type_option.setValue(value)

            # Comments
            self.ui.txt_notes.setPlainText(data_meta.get('comments', ''))

            # Combo Widgets
            if self.mapping_table.get('cmb_1', ''):
                if data_meta.get(self.mapping_table.get('cmb_1', ''), ''):
                    self.ui.cmb_meta_1.setCurrentText(data_meta.get(self.mapping_table.get('cmb_1', '')))

            if self.mapping_table.get('cmb_2', ''):
                if data_meta.get(self.mapping_table.get('cmb_2', ''), ''):
                    self.ui.cmb_meta_2.setCurrentText(data_meta.get(self.mapping_table.get('cmb_2', '')))

            if self.mapping_table.get('cmb_3', ''):
                if data_meta.get(self.mapping_table.get('cmb_3', ''), ''):
                    self.ui.cmb_meta_3.setCurrentText(data_meta.get(self.mapping_table.get('cmb_3', '')))

            # Text fields
            self.ui.le_meta_input_txt_1.setText(data_meta.get(self.mapping_table.get('txt_1', ''), ''))
            self.ui.le_meta_input_txt_2.setText(data_meta.get(self.mapping_table.get('txt_2', ''), ''))
            self.ui.le_meta_input_txt_3.setText(data_meta.get(self.mapping_table.get('txt_3', ''), ''))

            # Slider
            if self.config.get('slider_triple1', ''):
                if data_meta.get(self.mapping_table.get('triple_1', ''), 0):
                    value = map_text_to_slider(data_meta.get(self.mapping_table.get('triple_1', ''), 0),
                                               self.config['slider_triple1'])
                    self.ui.triple_meta_1.setValue(value)

            if self.config.get('slider_triple2', ''):
                if data_meta.get(self.mapping_table.get('triple_2', ''), 0):
                    value = map_text_to_slider(data_meta.get(self.mapping_table.get('triple_2', ''), 0),
                                               self.config['slider_triple2'])
                    self.ui.triple_meta_2.setValue(value)

            if self.config.get('slider_triple3', ''):
                if data_meta.get(self.mapping_table.get('triple_3', ''), 0):
                    value = map_text_to_slider(data_meta.get(self.mapping_table.get('triple_3', ''), 0),
                                               self.config['slider_triple3'])
                    self.ui.triple_meta_3.setValue(value)

            if self.config.get('slider_triple4', ''):
                if data_meta.get(self.mapping_table.get('triple_4', ''), 0):
                    value = map_text_to_slider(data_meta.get(self.mapping_table.get('triple_4', ''), 0),
                                               self.config['slider_triple4'])
                    self.ui.triple_meta_4.setValue(value)

            if self.config.get('slider_duo1', ''):
                if data_meta.get(self.mapping_table.get('duo_1', ''), 0):
                    value = map_text_to_slider(data_meta.get(self.mapping_table.get('duo_1', ''), 0),
                                               self.config['slider_duo1'])
                    self.ui.duo_meta_1.setValue(value)

            if self.config.get('slider_duo2', ''):
                if data_meta.get(self.mapping_table.get('duo_2', ''), 0):
                    value = map_text_to_slider(data_meta.get(self.mapping_table.get('duo_2', ''), 0),
                                               self.config['slider_duo2'])
                    self.ui.duo_meta_2.setValue(value)

            if self.config.get('slider_duo3', ''):
                if data_meta.get(self.mapping_table.get('duo_3', ''), 0):
                    value = map_text_to_slider(data_meta.get(self.mapping_table.get('duo_3', ''), 0),
                                               self.config['slider_duo3'])
                    self.ui.duo_meta_3.setValue(value)

    def get_object_data(self):

        # TODO this is only temporary implemented to provide functionality for different meta types
        meta_type = self.config_meta_type
        data = {}
        object_type = self.ui.cmb_obejcet_types_main.currentText()

        # Main Type option
        if self.config['object_main_type'].get('object_main_type_option', False):
            name, value = map_slider_to_text(self.ui.duo_main_type_option.value(),
                                             self.config['object_main_type']['object_main_type_option'])
            data[self.mapping_table['object_main_type_option']] = value

        # Sub Type
        if self.config.get('object_sub_type', False):

            data[self.mapping_table['object_sub_type']] = self.ui.cmb_obejcet_types_sub.currentText()

            # subtype option
            if self.config['object_sub_type'].get('object_sub_type_option', False):
                name, value = map_slider_to_text(self.ui.triple_sub_type_option.value(),
                                                 self.config['object_sub_type']['object_sub_type_option'])
                data[self.mapping_table['object_sub_type_option']] = value

        # Comments
        if self.ui.txt_notes.toPlainText():
            data['comments'] = self.ui.txt_notes.toPlainText()

        # Text Fields
        if self.mapping_table.get('cmb_1', ''):
            data[self.mapping_table['cmb_1']] = self.ui.cmb_meta_1.currentText()

        if self.mapping_table.get('cmb_2', ''):
            data[self.mapping_table['cmb_2']] = self.ui.cmb_meta_2.currentText()

        if self.mapping_table.get('cmb_3', ''):
            data[self.mapping_table['cmb_3']] = self.ui.cmb_meta_3.currentText()

        # Text fields can be empty
        if self.mapping_table.get('txt_1', '') and self.ui.le_meta_input_txt_1.text():
            data[self.mapping_table['txt_1']] = self.ui.le_meta_input_txt_1.text()
        if self.mapping_table.get('txt_2', '') and self.ui.le_meta_input_txt_2.text():
            data[self.mapping_table['txt_2']] = self.ui.le_meta_input_txt_2.text()
        if self.mapping_table.get('txt_3', '') and self.ui.le_meta_input_txt_3.text():
            data[self.mapping_table['txt_3']] = self.ui.le_meta_input_txt_3.text()

        if self.mapping_table.get('triple_1', ''):
            name, value = map_slider_to_text(self.ui.triple_meta_1.value(), self.config['slider_triple1'])
            data[self.mapping_table['triple_1']] = value

        if self.mapping_table.get('triple_2', ''):
            name, value = map_slider_to_text(self.ui.triple_meta_2.value(), self.config['slider_triple2'])
            data[self.mapping_table['triple_2']] = value

        if self.mapping_table.get('triple_3', ''):
            name, value = map_slider_to_text(self.ui.triple_meta_3.value(), self.config['slider_triple3'])
            data[self.mapping_table['triple_3']] = value

        if self.mapping_table.get('triple_4', ''):
            name, value = map_slider_to_text(self.ui.triple_meta_4.value(), self.config['slider_triple4'])
            data[self.mapping_table['triple_4']] = value

        if self.mapping_table.get('duo_1', ''):
            name, value = map_slider_to_text(self.ui.duo_meta_1.value(), self.config['slider_duo1'])
            data[self.mapping_table['duo_1']] = value

        if self.mapping_table.get('duo_2', ''):
            name, value = map_slider_to_text(self.ui.duo_meta_2.value(), self.config['slider_duo2'])
            data[self.mapping_table['duo_2']] = value

        if self.mapping_table.get('duo_3', ''):
            name, value = map_slider_to_text(self.ui.duo_meta_3.value(), self.config['slider_duo3'])
            data[self.mapping_table['duo_3']] = value

        first_certain = "yes" if self.ui.slider_first_certain.value() else "no"
        resight = "yes" if self.ui.slider_resight.value() else "no"
        certainty = "yes" if self.ui.slider_certainty.value() else "no"
        data["certainty"] = certainty
        data["firstcertain"] = first_certain
        data["resight"] = resight

        return object_type.lower(), json.dumps(data), meta_type

    @QtCore.Slot()
    def close_check(self):
        # Need to check if loaded object type is already set, otherwise this object was probably just created and
        # closing would force an emtpy object type
        if self.ui.cmb_obejcet_types_main.currentText():
            self.close()
        else:
            self.ui.cmb_obejcet_types_main.setStyleSheet("QComboBox{background-color: #c63d0e;}")

    @QtCore.Slot()
    def send_values(self):

        if not self.ui.cmb_obejcet_types_main.currentText():
            self.ui.cmb_obejcet_types_main.setStyleSheet("QComboBox{background-color: #c63d0e;}")
            return

        object_type, data, meta_type = self.get_object_data()
        if object_type:
            self.db.store_objects_meta(self.object_id, object_type, meta_type, data)

            if self.data_env is not None:
                self.db.store_objects_env_data(self.object_id, self.data_env)

                # If image has no env data or only propagated than assign env if data is set here to image
                if ((self.image_env_data_type is None and self.change_image_env_none) or
                        (self.image_env_data_type in [1, 3] and self.change_image_env_propagate)):
                    self.db.store_image_environment_data(self.data_env, self.image_id)

            self.object_change.emit(self.object_id, self.image_id)
            self.close()

    @QtCore.Slot()
    def delete_item(self):

        v = POPUPConfirm("Are you sure about removing object?")
        if v.exec():

            self.object_delete.emit(self.object_id, self.image_id)
            self.close()


def map_slider_to_text(value, slider_config):
    if value == 0:
        value_mapped = slider_config['value_0']
    elif value == 1:
        value_mapped = slider_config['value_1']
    else:
        value_mapped = slider_config['value_2']

    return slider_config['name'], value_mapped


def map_text_to_slider(value, slider_config):
    if value == slider_config['value_0']:
        return 0
    if value == slider_config['value_1']:
        return 1
    if value == slider_config['value_2']:
        return 2
