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
import json
from collections import OrderedDict

from PySide6 import QtCore
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QWidget, QFileDialog

from app.var_classes import object_name_file_header
from app.gui_design.ui_project_creator import Ui_popup_project_config

logger = logging.getLogger(__name__)


class POPUPConfigProject(QWidget):
    submit_config = Signal(object)

    def __init__(self):
        QWidget.__init__(self)

        self.ui = Ui_popup_project_config()
        self.ui.setupUi(self)
        self.dragPos = QtCore.QPointF(0, 0)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        self.ui.btn_close.clicked.connect(self.close)

        self.ui.btn_load_object_names.clicked.connect(self.load_object_names)
        self.ui.btn_save_object_names.clicked.connect(self.save_object_names)
        self.ui.btn_save_config.clicked.connect(self.save_config)
        self.ui.btn_load_config.clicked.connect(self.load_config)
        self.ui.btn_submit.clicked.connect(self.start_project)
        self.ui.btn_clear.clicked.connect(self.clear_config)

        self.ui.cmb_object_sub.add_signal.connect(self.add_new_subtype)
        self.ui.cmb_object_sub.delete_signal.connect(self.remove_new_subtype)

        self.ui.cmb_object_main.add_signal.connect(self.add_new_main_type)
        self.ui.cmb_object_main.delete_signal.connect(self.remove_new_main_type)
        self.ui.cmb_object_main.activated.connect(self.change_sub_items)

        self.ui.rd_sub_type_active.clicked.connect(self.sub_type_frame_visible)

        self.object_types = OrderedDict()
        self.config_name = "wisdam_default_012024"

        # move window
        def move_window(event):
            if event.buttons() == Qt.MouseButton.LeftButton and not self.isMaximized():
                self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos.toPoint())
                self.dragPos = event.globalPosition()
                event.accept()

        # WIDGET TO MOVE
        self.ui.frame_top.mouseMoveEvent = move_window

    def mousePressEvent(self, event):
        self.dragPos = event.globalPosition()

    def sub_type_frame_visible(self):
        self.ui.frame_object_sub_types.setVisible(self.ui.rd_sub_type_active.isChecked())

    def load_object_names(self):
        self.ui.cmb_object_main.clear()
        self.ui.cmb_object_sub.clear()
        self.object_types = OrderedDict()

        path_file, _ = QFileDialog.getOpenFileName(self, caption="Open object type names",
                                                   dir='.', filter='Text Files (*.txt)')
        if path_file:

            try:
                with open(path_file, 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        line = line.strip().lower()
                        if line[0] != '#':
                            object_import = line.split(';')
                            self.object_types[object_import[0]] = object_import[1:]
                if self.object_types:
                    main_names = list(self.object_types.keys())
                    self.ui.cmb_object_main.addItems(main_names)
                    self.ui.cmb_object_main.setCurrentIndex(0)
                    self.ui.cmb_object_sub.addItems(self.object_types[main_names[0]])
                    self.ui.cmb_object_sub.setCurrentIndex(0)
            except:
                logger.error("Object type name text file is not valid")

    def save_object_names(self):

        if self.object_types:

            path_file, _ = QFileDialog.getSaveFileName(self, caption="Save object type names",
                                                       dir='.', filter='Text Files (*.txt)')
            if path_file:

                with open(path_file, 'w') as f:

                    f.write(object_name_file_header)

                    for name, value in self.object_types.items():
                        f.write(';'.join([name] + value) + '\n')

    @Slot(str)
    def add_new_subtype(self, name: str):
        if len(self.object_types) > 0:
            self.object_types[self.ui.cmb_object_main.currentText()].append(name)
        else:
            self.ui.cmb_object_sub.clear()

    @Slot(str)
    def remove_new_subtype(self, name: str):

        if name in self.object_types[self.ui.cmb_object_main.currentText()]:
            self.object_types[self.ui.cmb_object_main.currentText()].remove(name)

    def change_sub_items(self):
        self.ui.cmb_object_sub.clear()
        self.ui.cmb_object_sub.addItems(self.object_types[self.ui.cmb_object_main.currentText()])
        self.ui.cmb_object_sub.setCurrentIndex(0)

    @Slot(str)
    def add_new_main_type(self, name: str):
        self.object_types[name] = []
        self.ui.cmb_object_sub.clear()

    @Slot(str)
    def remove_new_main_type(self, name: str):
        self.object_types.pop(name, None)
        self.ui.cmb_object_sub.clear()
        if len(self.object_types) > 0:
            self.ui.cmb_object_sub.addItems(self.object_types[self.ui.cmb_object_main.currentText()])

    def save_config(self):

        config = self.generate_config()

        if config is not None:

            path_file, _ = QFileDialog.getSaveFileName(self, caption="Save Configuration File",
                                                       dir='.', filter='Json Files (*.json)')
            if path_file:
                fid = open(path_file, 'w')
                json.dump(config, fid, indent=3)

    def load_config(self):
        path_file, _ = QFileDialog.getOpenFileName(self, caption="Load Configuration File",
                                                   dir='.', filter='Json Files (*.json)')
        if path_file:
            try:
                fid = open(path_file, 'r')
                config = json.load(fid)
                self.set_config(config)
            except json.decoder.JSONDecodeError:
                logger.error("Selected file is not a valid JSON")

    def start_project(self):

        config = self.generate_config()

        if config:
            self.close()
            self.submit_config.emit(config)
        return

    def clear_config(self):

        self.object_types = {}

        # clear main types
        self.ui.cmb_object_main.clear()
        self.ui.le_custom_object_naming.clear()
        self.ui.duo_main_type.setValue(0)
        self.ui.le_main_type_option_name.clear()
        self.ui.le_main_type_option_value_0.clear()
        self.ui.le_main_type_option_value_1.clear()

        # clear subtypes
        self.ui.rd_sub_type_active.setChecked(True)
        self.ui.frame_object_sub_types.show()
        self.ui.le_custom_object_sub_naming.clear()
        self.ui.cmb_object_sub.clear()
        self.ui.triple_sub_type.setValue(0)
        self.ui.le_sub_type_option_name.clear()
        self.ui.le_sub_type_option_value_0.clear()
        self.ui.le_sub_type_option_value_1.clear()
        self.ui.le_sub_type_option_value_2.clear()

        self.ui.rd_env_object_override.setChecked(False)
        self.ui.rd_env_object_override_propagate.setChecked(False)

        # Clear env data
        self.ui.le_custom_1.clear()
        self.ui.cmb_custom_1.clear()
        self.ui.le_custom_2.clear()
        self.ui.cmb_custom_2.clear()
        self.ui.le_custom_3.clear()
        self.ui.cmb_custom_3.clear()
        self.ui.le_custom_4.clear()
        self.ui.cmb_custom_4.clear()
        self.ui.le_custom_5.clear()
        self.ui.cmb_custom_5.clear()
        self.ui.le_custom_6.clear()
        self.ui.cmb_custom_6.clear()

        # Combo Meta
        self.ui.cmb_meta_1.clear()
        self.ui.le_meta_cmb_name_1.clear()

        self.ui.cmb_meta_2.clear()
        self.ui.le_meta_cmb_name_2.clear()

        self.ui.cmb_meta_3.clear()
        self.ui.le_meta_cmb_name_3.clear()

        # Text Input Fields
        self.ui.le_meta_input_txt_1.clear()
        self.ui.le_meta_input_txt_2.clear()
        self.ui.le_meta_input_txt_3.clear()

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

    @staticmethod
    def check_variable_names_duplicates(var_list: list, var_text: str):
        if var_text.lower() not in var_list:
            var_list.append(var_text.lower())
        else:
            logger.warning("Variable names must be unique")
            return False
        return True

    def set_config(self, config: dict):

        self.clear_config()
        env_data: dict | None = config.get('environment_data', None)
        env_propagate: dict | None = config.get('environment_propagation', None)
        self.config_name = list(config['meta_config'].keys())[0]
        config = config['meta_config'][self.config_name]

        object_type: dict | None = config.get('object_types', None)

        object_main_type_naming: dict | None = config["object_main_type"].get('naming', '')
        self.ui.le_custom_object_naming.setText(object_main_type_naming)

        main_names = []
        if object_type is not None:
            self.object_types = object_type
            main_names = list(self.object_types.keys())
            self.ui.cmb_object_main.addItems(main_names)
            self.ui.cmb_object_main.setCurrentIndex(0)

        # Main Type Option Slider
        if config["object_main_type"].get('object_main_type_option', False):
            duo_slider = config["object_main_type"]["object_main_type_option"]
            self.ui.le_main_type_option_name.setText(duo_slider['name'])
            self.ui.le_main_type_option_value_0.setText(duo_slider['value_0'])
            self.ui.le_main_type_option_value_1.setText(duo_slider['value_1'])
            self.ui.duo_main_type.setValue(duo_slider['start_value'])

        # Subtype Option Slider
        if config.get("object_sub_type", False):

            self.ui.rd_sub_type_active.setChecked(True)
            self.ui.frame_object_sub_types.show()

            if object_type is not None:
                if len(main_names) > 0:
                    self.ui.cmb_object_sub.addItems(self.object_types[main_names[0]])
                    self.ui.cmb_object_sub.setCurrentIndex(0)

            object_sub_type_naming: dict | None = config["object_sub_type"].get('naming', '')
            self.ui.le_custom_object_sub_naming.setText(object_sub_type_naming)

            if config["object_sub_type"].get("object_sub_type_option", False):
                triple_slider = config['object_sub_type']["object_sub_type_option"]
                self.ui.le_sub_type_option_name.setText(triple_slider['name'])
                self.ui.le_sub_type_option_value_0.setText(triple_slider['value_0'])
                self.ui.le_sub_type_option_value_1.setText(triple_slider['value_1'])
                self.ui.le_sub_type_option_value_2.setText(triple_slider['value_2'])
                self.ui.triple_sub_type.setValue(triple_slider['start_value'])
        else:
            self.ui.rd_sub_type_active.setChecked(False)
            self.ui.frame_object_sub_types.hide()
        if config.get('combo_meta_1', False):
            combo_meta = config['combo_meta_1']
            self.ui.cmb_meta_1.addItems(combo_meta['items'])
            self.ui.le_meta_cmb_name_1.setText(combo_meta['name'])
            self.ui.cmb_meta_1.setCurrentIndex(0)

        if config.get('combo_meta_2', False):
            combo_meta = config['combo_meta_2']
            self.ui.cmb_meta_2.addItems(combo_meta['items'])
            self.ui.le_meta_cmb_name_2.setText(combo_meta['name'])
            self.ui.cmb_meta_2.setCurrentIndex(0)

        if config.get('combo_meta_3', False):
            combo_meta = config['combo_meta_3']
            self.ui.cmb_meta_3.addItems(combo_meta['items'])
            self.ui.le_meta_cmb_name_3.setText(combo_meta['name'])
            self.ui.cmb_meta_3.setCurrentIndex(0)

        if config.get('input_text_1', False):
            self.ui.le_meta_input_txt_1.setText(config['input_text_1'])

        if config.get('input_text_2', False):
            self.ui.le_meta_input_txt_2.setText(config['input_text_2'])

        if config.get('input_text_3', False):
            self.ui.le_meta_input_txt_3.setText(config['input_text_3'])

        # DUO SLIDER
        if config.get('slider_duo1', False):
            duo_slider = config['slider_duo1']
            self.ui.le_meta_duo_name_1.setText(duo_slider['name'])
            self.ui.le_meta_duo_1_value_0.setText(duo_slider['value_0'])
            self.ui.le_meta_duo_1_value_1.setText(duo_slider['value_1'])
            self.ui.duo_meta_1.setValue(duo_slider['start_value'])

        if config.get('slider_duo2', False):
            duo_slider = config['slider_duo2']
            self.ui.le_meta_duo_name_2.setText(duo_slider['name'])
            self.ui.le_meta_duo_2_value_0.setText(duo_slider['value_0'])
            self.ui.le_meta_duo_2_value_1.setText(duo_slider['value_1'])
            self.ui.duo_meta_2.setValue(duo_slider['start_value'])

        if config.get('slider_duo3', False):
            duo_slider = config['slider_duo3']
            self.ui.le_meta_duo_name_3.setText(duo_slider['name'])
            self.ui.le_meta_duo_3_value_0.setText(duo_slider['value_0'])
            self.ui.le_meta_duo_3_value_1.setText(duo_slider['value_1'])
            self.ui.duo_meta_3.setValue(duo_slider['start_value'])

        # Triple Slider
        if config.get('slider_triple1', False):
            triple_slider = config['slider_triple1']
            self.ui.le_meta_triple_name_1.setText(triple_slider['name'])
            self.ui.le_meta_triple_1_value_0.setText(triple_slider['value_0'])
            self.ui.le_meta_triple_1_value_1.setText(triple_slider['value_1'])
            self.ui.le_meta_triple_1_value_2.setText(triple_slider['value_2'])
            self.ui.triple_meta_1.setValue(triple_slider['start_value'])

        if config.get('slider_triple2', False):
            triple_slider = config['slider_triple2']
            self.ui.le_meta_triple_name_2.setText(triple_slider['name'])
            self.ui.le_meta_triple_2_value_0.setText(triple_slider['value_0'])
            self.ui.le_meta_triple_2_value_1.setText(triple_slider['value_1'])
            self.ui.le_meta_triple_2_value_2.setText(triple_slider['value_2'])
            self.ui.triple_meta_2.setValue(triple_slider['start_value'])

        if config.get('slider_triple3', False):
            triple_slider = config['slider_triple3']
            self.ui.le_meta_triple_name_3.setText(triple_slider['name'])
            self.ui.le_meta_triple_3_value_0.setText(triple_slider['value_0'])
            self.ui.le_meta_triple_3_value_1.setText(triple_slider['value_1'])
            self.ui.le_meta_triple_3_value_2.setText(triple_slider['value_2'])
            self.ui.triple_meta_3.setValue(triple_slider['start_value'])

        if config.get('slider_triple4', False):
            triple_slider = config['slider_triple4']
            self.ui.le_meta_triple_name_4.setText(triple_slider['name'])
            self.ui.le_meta_triple_4_value_0.setText(triple_slider['value_0'])
            self.ui.le_meta_triple_4_value_1.setText(triple_slider['value_1'])
            self.ui.le_meta_triple_4_value_2.setText(triple_slider['value_2'])
            self.ui.triple_meta_4.setValue(triple_slider['start_value'])

        # Environment data loaded from a saved config file
        if env_propagate is not None:
            self.ui.rd_env_object_override.setChecked(env_propagate["first_object_set_override_none_image"])
            self.ui.rd_env_object_override_propagate.setChecked(env_propagate[
                                                                    "first_object_set_override_porpagated_image"])

        if env_data is not None:

            env_keys = list(env_data.keys())

            if len(env_keys) >= 1:
                self.ui.le_custom_1.setText(env_keys[0])
                self.ui.cmb_custom_1.addItems(env_data[env_keys[0]])
                self.ui.cmb_custom_1.setCurrentIndex(0)

            if len(env_keys) >= 2:
                self.ui.le_custom_2.setText(env_keys[1])
                self.ui.cmb_custom_2.addItems(env_data[env_keys[1]])
                self.ui.cmb_custom_2.setCurrentIndex(0)

            if len(env_keys) >= 3:
                self.ui.le_custom_3.setText(env_keys[2])
                self.ui.cmb_custom_3.addItems(env_data[env_keys[2]])
                self.ui.cmb_custom_3.setCurrentIndex(0)

            if len(env_keys) >= 4:
                self.ui.le_custom_4.setText(env_keys[3])
                self.ui.cmb_custom_4.addItems(env_data[env_keys[3]])
                self.ui.cmb_custom_4.setCurrentIndex(0)

            if len(env_keys) >= 5:
                self.ui.le_custom_5.setText(env_keys[4])
                self.ui.cmb_custom_5.addItems(env_data[env_keys[4]])
                self.ui.cmb_custom_5.setCurrentIndex(0)

            if len(env_keys) >= 6:
                self.ui.le_custom_6.setText(env_keys[5])
                self.ui.cmb_custom_6.addItems(env_data[env_keys[5]])
                self.ui.cmb_custom_6.setCurrentIndex(0)

    def generate_config(self) -> dict | None:

        if not self.object_types:
            logger.error("At least one object type must be specified")
            return None

        if not self.ui.le_custom_object_naming.text():
            logger.error("Object main type naming not specified")
            return None

        variable_names = ['certainty', 'firstcertain', 'resight']

        config_dict = {'meta_config': {self.config_name: {}}}
        config_specific_type = config_dict['meta_config']["wisdam_default_012024"]
        config_specific_type['object_types'] = self.object_types
        config_specific_type['object_main_type'] = {'naming': self.ui.le_custom_object_naming.text()}

        # Main type option
        if self.ui.le_main_type_option_name.text() and self.ui.le_main_type_option_value_0.text() and \
                self.ui.le_main_type_option_value_1.text():
            config_specific_type['object_main_type']['object_main_type_option'] = {
                'name': self.ui.le_main_type_option_name.text(),
                'value_0': self.ui.le_main_type_option_value_0.text(),
                'value_1': self.ui.le_main_type_option_value_1.text(),
                'start_value': self.ui.duo_main_type.value()}

            if not self.check_variable_names_duplicates(variable_names, self.ui.le_main_type_option_name.text()):
                return
        elif self.ui.le_main_type_option_name.text() or self.ui.le_main_type_option_value_0.text() or \
                self.ui.le_main_type_option_value_1.text():
            logger.warning("Object main type option not fully set")
            return

        if self.ui.rd_sub_type_active.isChecked():

            if not self.ui.le_custom_object_sub_naming.text():
                logger.error("Object sub type naming not specified")
                return None

            config_specific_type['object_sub_type'] = {'naming': self.ui.le_custom_object_sub_naming.text()}

            if not self.check_variable_names_duplicates(variable_names, self.ui.le_custom_object_sub_naming.text()):
                return

            if self.ui.le_sub_type_option_name.text() and self.ui.le_sub_type_option_value_0.text() and \
                    self.ui.le_sub_type_option_value_1.text() and self.ui.le_sub_type_option_value_2.text():
                dump = {'name': self.ui.le_sub_type_option_name.text(),
                        'value_0': self.ui.le_sub_type_option_value_0.text(),
                        'value_1': self.ui.le_sub_type_option_value_1.text(),
                        'value_2': self.ui.le_sub_type_option_value_2.text(),
                        'start_value': self.ui.triple_sub_type.value()}
                config_specific_type['object_sub_type']['object_sub_type_option'] = dump

                if not self.check_variable_names_duplicates(variable_names, self.ui.le_sub_type_option_name.text()):
                    return
            elif self.ui.le_sub_type_option_name.text() or self.ui.le_sub_type_option_value_0.text() or \
                    self.ui.le_sub_type_option_value_1.text() or self.ui.le_sub_type_option_value_2.text():
                logger.warning("Object sub type option not fully set")
                return

        if self.ui.le_meta_cmb_name_1.text() and self.ui.cmb_meta_1.count() > 0:
            items = [self.ui.cmb_meta_1.itemText(i) for i in range(self.ui.cmb_meta_1.count())]
            config_specific_type['combo_meta_1'] = {'name': self.ui.le_meta_cmb_name_1.text(),
                                                    'items': items}
            if not self.check_variable_names_duplicates(variable_names, self.ui.le_meta_cmb_name_1.text()):
                return
        elif self.ui.le_meta_cmb_name_1.text() or self.ui.cmb_meta_1.count() > 0:
            logger.warning("Some combo-box variable is not correct configured")
            return

        if self.ui.le_meta_cmb_name_2.text() and self.ui.cmb_meta_2.count() > 0:
            items = [self.ui.cmb_meta_2.itemText(i) for i in range(self.ui.cmb_meta_2.count())]
            config_specific_type['combo_meta_2'] = {'name': self.ui.le_meta_cmb_name_2.text(),
                                                    'items': items}
            if not self.check_variable_names_duplicates(variable_names, self.ui.le_meta_cmb_name_2.text()):
                return
        elif self.ui.le_meta_cmb_name_2.text() or self.ui.cmb_meta_2.count() > 0:
            logger.warning("Some combo-box variable is not correct configured")
            return

        if self.ui.le_meta_cmb_name_3.text() and self.ui.cmb_meta_3.count() > 0:
            items = [self.ui.cmb_meta_3.itemText(i) for i in range(self.ui.cmb_meta_3.count())]
            config_specific_type['combo_meta_3'] = {'name': self.ui.le_meta_cmb_name_3.text(),
                                                    'items': items}
            if not self.check_variable_names_duplicates(variable_names, self.ui.le_meta_cmb_name_3.text()):
                return
        elif self.ui.le_meta_cmb_name_3.text() or self.ui.cmb_meta_3.count() > 0:
            logger.warning("Some combo-box variable is not correct configured")
            return

        if self.ui.le_meta_input_txt_1.text():
            config_specific_type['input_text_1'] = self.ui.le_meta_input_txt_1.text()
            if not self.check_variable_names_duplicates(variable_names, self.ui.le_meta_input_txt_1.text()):
                return

        if self.ui.le_meta_input_txt_2.text():
            config_specific_type['input_text_2'] = self.ui.le_meta_input_txt_2.text()
            if not self.check_variable_names_duplicates(variable_names, self.ui.le_meta_input_txt_2.text()):
                return

            if self.ui.le_meta_input_txt_3.text():
                config_specific_type['input_text_3'] = self.ui.le_meta_input_txt_3.text()
                if not self.check_variable_names_duplicates(variable_names, self.ui.le_meta_input_txt_3.text()):
                    return

        # DUO SLIDER
        if self.ui.le_meta_duo_name_1.text() and self.ui.le_meta_duo_1_value_0.text() and \
                self.ui.le_meta_duo_1_value_1.text():
            config_specific_type['slider_duo1'] = {'name': self.ui.le_meta_duo_name_1.text(),
                                                   'value_0': self.ui.le_meta_duo_1_value_0.text(),
                                                   'value_1': self.ui.le_meta_duo_1_value_1.text(),
                                                   'start_value': self.ui.duo_meta_1.value()}
            if not self.check_variable_names_duplicates(variable_names, self.ui.le_meta_duo_name_1.text()):
                return
        elif self.ui.le_meta_duo_name_1.text() or self.ui.le_meta_duo_1_value_0.text() or \
                self.ui.le_meta_duo_1_value_1.text():
            logger.warning("Some double slider option not fully set")
            return

        if self.ui.le_meta_duo_name_2.text() and self.ui.le_meta_duo_2_value_0.text() and \
                self.ui.le_meta_duo_2_value_1.text():
            config_specific_type['slider_duo2'] = {'name': self.ui.le_meta_duo_name_2.text(),
                                                   'value_0': self.ui.le_meta_duo_2_value_0.text(),
                                                   'value_1': self.ui.le_meta_duo_2_value_1.text(),
                                                   'start_value': self.ui.duo_meta_2.value()}
            if not self.check_variable_names_duplicates(variable_names, self.ui.le_meta_duo_name_2.text()):
                return
        elif self.ui.le_meta_duo_name_2.text() or self.ui.le_meta_duo_2_value_0.text() or \
                self.ui.le_meta_duo_2_value_1.text():
            logger.warning("Some double slider option not fully set")
            return

        if self.ui.le_meta_duo_name_3.text() and self.ui.le_meta_duo_3_value_0.text() and \
                self.ui.le_meta_duo_3_value_1.text():
            config_specific_type['slider_duo3'] = {'name': self.ui.le_meta_duo_name_3.text(),
                                                   'value_0': self.ui.le_meta_duo_3_value_0.text(),
                                                   'value_1': self.ui.le_meta_duo_3_value_1.text(),
                                                   'start_value': self.ui.duo_meta_3.value()}
            if not self.check_variable_names_duplicates(variable_names, self.ui.le_meta_duo_name_3.text()):
                return
        elif self.ui.le_meta_duo_name_3.text() or self.ui.le_meta_duo_3_value_0.text() or \
                self.ui.le_meta_duo_3_value_1.text():
            logger.warning("Some double slider option not fully set")
            return

        # Triple Slider
        if self.ui.le_meta_triple_name_1.text() and self.ui.le_meta_triple_1_value_0.text() and \
                self.ui.le_meta_triple_1_value_1.text() and self.ui.le_meta_triple_1_value_2.text():
            config_specific_type['slider_triple1'] = {'name': self.ui.le_meta_triple_name_1.text(),
                                                      'value_0': self.ui.le_meta_triple_1_value_0.text(),
                                                      'value_1': self.ui.le_meta_triple_1_value_1.text(),
                                                      'value_2': self.ui.le_meta_triple_1_value_2.text(),
                                                      'start_value': self.ui.triple_meta_1.value()}
            if not self.check_variable_names_duplicates(variable_names, self.ui.le_meta_triple_name_1.text()):
                return
        elif self.ui.le_meta_triple_name_1.text() or self.ui.le_meta_triple_1_value_0.text() or \
                self.ui.le_meta_triple_1_value_1.text() or self.ui.le_meta_triple_1_value_2.text():
            logger.warning("Some triple slider option not fully set")
            return

        if self.ui.le_meta_triple_name_2.text() and self.ui.le_meta_triple_2_value_0.text() and \
                self.ui.le_meta_triple_2_value_1.text() and self.ui.le_meta_triple_2_value_2.text():
            config_specific_type['slider_triple2'] = {'name': self.ui.le_meta_triple_name_2.text(),
                                                      'value_0': self.ui.le_meta_triple_2_value_0.text(),
                                                      'value_1': self.ui.le_meta_triple_2_value_1.text(),
                                                      'value_2': self.ui.le_meta_triple_2_value_2.text(),
                                                      'start_value': self.ui.triple_meta_2.value()}
            if not self.check_variable_names_duplicates(variable_names, self.ui.le_meta_triple_name_2.text()):
                return
        elif self.ui.le_meta_triple_name_2.text() or self.ui.le_meta_triple_2_value_0.text() or \
                self.ui.le_meta_triple_2_value_1.text() or self.ui.le_meta_triple_2_value_2.text():
            logger.warning("Some triple slider option not fully set")
            return

        if self.ui.le_meta_triple_name_3.text() and self.ui.le_meta_triple_3_value_0.text() and \
                self.ui.le_meta_triple_3_value_1.text() and self.ui.le_meta_triple_3_value_2.text():
            config_specific_type['slider_triple3'] = {'name': self.ui.le_meta_triple_name_3.text(),
                                                      'value_0': self.ui.le_meta_triple_3_value_0.text(),
                                                      'value_1': self.ui.le_meta_triple_3_value_1.text(),
                                                      'value_2': self.ui.le_meta_triple_3_value_2.text(),
                                                      'start_value': self.ui.triple_meta_3.value()}
            if not self.check_variable_names_duplicates(variable_names, self.ui.le_meta_triple_name_3.text()):
                return
        elif self.ui.le_meta_triple_name_3.text() or self.ui.le_meta_triple_3_value_0.text() or \
                self.ui.le_meta_triple_3_value_1.text() or self.ui.le_meta_triple_3_value_2.text():
            logger.warning("Some triple slider option not fully set")
            return

        if self.ui.le_meta_triple_name_4.text() and self.ui.le_meta_triple_4_value_0.text() and \
                self.ui.le_meta_triple_4_value_1.text() and self.ui.le_meta_triple_4_value_2.text():
            config_specific_type['slider_triple4'] = {'name': self.ui.le_meta_triple_name_4.text(),
                                                      'value_0': self.ui.le_meta_triple_4_value_0.text(),
                                                      'value_1': self.ui.le_meta_triple_4_value_1.text(),
                                                      'value_2': self.ui.le_meta_triple_4_value_2.text(),
                                                      'start_value': self.ui.triple_meta_4.value()}
            if not self.check_variable_names_duplicates(variable_names, self.ui.le_meta_triple_name_4.text()):
                return
        elif self.ui.le_meta_triple_name_4.text() or self.ui.le_meta_triple_4_value_0.text() or \
                self.ui.le_meta_triple_4_value_1.text() or self.ui.le_meta_triple_4_value_2.text():
            logger.warning("Some triple slider option not fully set")
            return

        env_config = {}
        # Environment data
        if self.ui.le_custom_1.text() and self.ui.cmb_custom_1.count() > 0:
            items = [self.ui.cmb_custom_1.itemText(i) for i in range(self.ui.cmb_custom_1.count())]
            env_config[self.ui.le_custom_1.text()] = items

        if self.ui.le_custom_2.text() and self.ui.cmb_custom_2.count() > 0:
            items = [self.ui.cmb_custom_2.itemText(i) for i in range(self.ui.cmb_custom_2.count())]
            env_config[self.ui.le_custom_2.text()] = items

        if self.ui.le_custom_3.text() and self.ui.cmb_custom_3.count() > 0:
            items = [self.ui.cmb_custom_3.itemText(i) for i in range(self.ui.cmb_custom_3.count())]
            env_config[self.ui.le_custom_3.text()] = items

        if self.ui.le_custom_4.text() and self.ui.cmb_custom_4.count() > 0:
            items = [self.ui.cmb_custom_4.itemText(i) for i in range(self.ui.cmb_custom_4.count())]
            env_config[self.ui.le_custom_4.text()] = items

        if self.ui.le_custom_5.text() and self.ui.cmb_custom_5.count() > 0:
            items = [self.ui.cmb_custom_5.itemText(i) for i in range(self.ui.cmb_custom_5.count())]
            env_config[self.ui.le_custom_5.text()] = items

        if self.ui.le_custom_6.text() and self.ui.cmb_custom_6.count() > 0:
            items = [self.ui.cmb_custom_6.itemText(i) for i in range(self.ui.cmb_custom_6.count())]
            env_config[self.ui.le_custom_6.text()] = items

        if not env_config:
            logger.error("At least one environment data must be specified")
            return None

        config_dict['environment_data'] = env_config

        config_dict["environment_propagation"] = {}
        config_dict["environment_propagation"][
            "first_object_set_override_none_image"] = self.ui.rd_env_object_override.isChecked()
        config_dict["environment_propagation"][
            "first_object_set_override_porpagated_image"] = self.ui.rd_env_object_override_propagate.isChecked()

        return config_dict
