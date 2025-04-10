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
import os
import time
import traceback
import json
import datetime
import logging
import sqlite3

from collections import Counter
import copy
from pathlib import Path
from collections import OrderedDict
import pyproj
from pyproj import CRS, datadir as pyproj_datadir
from multiprocessing import freeze_support

# PYSIDE imports
from PySide6.QtWidgets import (QMainWindow, QAbstractItemView, QApplication, QFileDialog, QMenu,
                               QGraphicsPixmapItem, QSizeGrip)
from PySide6.QtCore import (Slot, QSize, SignalInstance, QRunnable, Signal, QThreadPool, QEasingCurve,
                            QPropertyAnimation, QEvent, QObject, QRect, Qt, QModelIndex, QPersistentModelIndex, QPointF)
from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtGui import (QColor, QTransform, QIcon, QFontDatabase, QTextCursor, QAction, QCursor, QResizeEvent,
                           QDesktopServices, QPixmap, QKeyEvent)

# Functions and Classes from WISDAM
# GUI
from app.gui_design.ui_main import Ui_MainWindow
# Interaction Windows
from app.popups.popupMeta import POPUPMeta
from app.popups.popupUser import POPUPUser
from app.popups.popupChangePath import POPUPPathChange
from app.popups.popupConfig import POPUPConfiguration
from app.popups.popupGeoref import POPUPGeoref
from app.popups.infoOverlay import CtmWidget
from app.popups.popupConfigProject import POPUPConfigProject
from app.popups.popupImageMeta import POPUPImageMeta
from app.popups.popupMapper import POPUPMapper
from app.popups.popupAbout import POPUPAbout
from app.popups.popupTextInput import POPUPTextInput
from app.popups.popupConfirm import POPUPConfirm
# Model Views, List
from app.model_views.imageListView import (ImageListModel, digitizer_image_panel_assign_model,
                                           IconCenterDelegate, RolesImagePane)
from app.model_views.galleryView import (gallery_loader,
                                         GalleryIconDelegate,
                                         GalleryListModel,
                                         gallery_loader_single,
                                         CustomSortFilterProxyModel)
from app.model_views.aiView import ai_loader, AIListModel, AIDelegate, AICustomSortFilterProxyModel
from app.model_views.compareViews import (CompareListModel,
                                          RolesComparePane,
                                          compare_image_loader,
                                          CompareIconCenterDelegate, CompareIconDelegate)
from app.model_views.proxyFilters import (set_filter_value, set_filter_check_value,
                                          set_filter_boolean, set_filter_slider)
from app.model_views.groupArea import GroupAreaTable, loader_group_area

# Graphic Image, GIS
from app.graphic.imageScene import ImageScene
from app.graphic.gisScene import GISScene
from app.graphic.items_coloring import golden_colors

from app.custom_elements.pieChart import PieChartWisdam
from app.custom_elements.menu_left import MenuBar
from app.utils_qt import (image_thumb_grid_navigation_size, change_led_color, toggle_visible_frame)
from app.var_classes import (ColorGui,
                             ImageList, Instructions, is_number, GalleryIconSize, GroupAreaList,
                             point_size, ObjectSourceList,
                             GalleryRoles, url_wisdam, logging_style, Selection)
from compare.utils import CompareList, compare_list_header, CompareType
from compare.search import compare_searcher, compare_searcher_single_db_ai_to_ai_review
from db.environment import propagate_env_data_next_image
from importer.importerWisdam import IMAGEImporter
from importer.loaderImageBase import LoaderType
from WISDAM import software_version

# AI imports
from ai.wisdam_ai_wrapper import WISDAMAi, import_ai_detections_to_objects
from ai.import_objects import change_active_all
# from ai.wisdam_docker import docker_running
from ai.base_class import AILoaderType

# Interface to core module
from core_interface.loader_digitizer import loader_image_geom
from core_interface.image_loader import image_loader, image_loader_rasterio
from core_interface.wisdamIMAGE import WISDAMImage
from core_interface.store_images import process_folder
from core_interface.loader_gis import loader_gis_geom_objects_single, worker_heavy_loading
from core_interface.loader_gis import (loader_gis_geom_objects)
from core_interface.test_single_image import (meta_of_image, meta_of_ortho_image)
from core_interface.update_image_object_geometry import update_all_geoms

from statistic.process_group_area import group_area_multiprocess_start
from compare.export import compare_export

from db.dbHandler import DBHandler
from db.exporter.ai_wisdam import export_trainings_data_worker
from db.exporter.export import export_file
from db.release_value_changes import check_update_color_config

# WISDAMcore
from WISDAMcore.image.base_class import ImageType
from WISDAMcore.mapping.type_selector import mapper_load_from_dict
from WISDAMcore.mapping.base_class import MappingBase
from WISDAMcore.transform.coordinates import CoordinatesTransformer
from WISDAMcore.exceptions import MappingError

logger = logging.getLogger('main')
root = logging.getLogger()

# Data stored within application. see https://www.pyinstaller.org/en/stable/spec-files.html
# Seems also working in Nuitka
path_to_manual = Path(__file__).resolve().with_name("wisdam_manual.pdf")
if not path_to_manual.exists():
    path_to_manual = Path(__file__).resolve().parent.parent.parent / "docs" / "wisdam_manual.pdf"

path_to_shape = Path(__file__).resolve().parent / "data" / 'shapes' / "land_wgs84.shp"

path_to_bin = Path(__file__).resolve().with_name("bin")
if not path_to_bin.exists():
    path_to_bin = Path(__file__).resolve().parent.parent.parent / "bin"

path_to_exiftool = path_to_bin / 'exiftool.exe'
path_to_current_directory = Path(__file__).parent.resolve()
path_to_license_folder = Path(__file__).resolve().with_name("license")

path_to_proj_dir = Path(__file__).resolve().parent.with_name("proj_dir")
# print(path_to_proj_dir.as_posix(), Path(__file__).resolve().parent.parent / "proj_dir")
if not path_to_proj_dir.exists():
    path_to_proj_dir = Path(__file__).parent.parent.parent / "proj_dir"


# Signals need to be contained in a QObject or subclass in order to be correctly initialized.
class Signaller(QObject):
    signal = Signal(str, logging.LogRecord)


# Handler for SLOT in QT for logging
class QtHandler(logging.Handler):
    def __init__(self, slot_func, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.signaller = Signaller()
        self.signaller.signal.connect(slot_func)

    def emit(self, record):
        s = self.format(record)
        print(s)
        self.signaller.signal.emit(s, record)


# Core Wrapper for stdout, stderr
class OutputWrapper(QObject):
    outputWritten: SignalInstance = Signal(object, object)

    def __init__(self, parent, stdout=True):
        QObject.__init__(self, parent)
        if stdout:
            self._stream = sys.stdout
            sys.stdout = self
        else:
            self._stream = sys.stderr
            sys.stderr = self
        self._stdout = stdout

    def write(self, text):
        if self._stream is not None:
            self._stream.write(text)
        self.outputWritten.emit(text, self._stdout)

    def __getattr__(self, name):
        return getattr(self._stream, name)

    def __del__(self):
        try:
            if self._stdout:
                sys.stdout = self._stream
            else:
                sys.stderr = self._stream
        except AttributeError:
            pass


# Signals of worker
class WorkerSignal(QObject):
    finished: SignalInstance = Signal()
    error: SignalInstance = Signal(tuple)
    result: SignalInstance = Signal(object)
    progress: SignalInstance = Signal(tuple)


class Worker(QRunnable):

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignal()
        if kwargs.get('progress_callback'):
            self.kwargs['progress_callback'] = self.signals.progress

    @Slot()
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs, )
        except Exception:
            # traceback.print_exc()
            exc_type, value = sys.exc_info()[:2]
            self.signals.error.emit((exc_type, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()


class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.label_version.setText(str(software_version))

        self.handler = h = QtHandler(self.handle_output_logging)
        fs = '%(levelname)s:%(name)s:  %(message)s'
        formatter = logging.Formatter(fs)
        h.setFormatter(formatter)
        root.addHandler(h)
        root.setLevel(logging.INFO)

        # stdout = OutputWrapper(self, True)
        # stdout.outputWritten.connect(self.handle_output)
        stderr = OutputWrapper(self, False)
        stderr.outputWritten.connect(self.handle_output)

        # MultiThread
        self.threadpool = QThreadPool()

        # Classes for pup up windows
        self.popup_meta = POPUPMeta()
        self.pop_user = POPUPUser()
        self.popup_config = POPUPConfiguration()
        self.popup_path = POPUPPathChange()
        self.popup_georef = POPUPGeoref()
        self.popup_info = CtmWidget(parent=self)
        self.popup_config_project = POPUPConfigProject()
        self.popup_mapper = POPUPMapper()
        self.popup_info.close()
        self.popup_about = POPUPAbout(path_to_license_folder)

        self.pop_user.got_user.connect(self.user_save)
        self.popup_georef.georef_updated.connect(self.georef_finished)
        self.popup_georef.closed.connect(self.popup_georef_closed)
        self.popup_config.config_send.connect(self.config_changed)

        self.popup_meta.object_change.connect(self.object_type_change)
        self.popup_meta.object_delete.connect(self.object_deleting)
        self.popup_meta.emit_object_types.connect(self.save_object_types_to_db)

        self.popup_config_project.submit_config.connect(self.create_new_db_start)

        self.popup_mapper.send_mapper_dict.connect(self.change_mapper)

        self.popup_path.windowClosed.connect(self.change_path_db_finished)
        self.ui.btn_info_popup.clicked.connect(self.show_info_popup)

        # Classes
        self.db: DBHandler | None = None
        self.input_data_types = IMAGEImporter()
        self.ai_workflow_types = WISDAMAi()

        self.mapper: MappingBase | None = None

        self.gallery_proxyModel = CustomSortFilterProxyModel(self)
        self.thumbnail_model: GalleryListModel | None = None
        self.image_panel_model: ImageListModel | None = None
        self.persistent_model_indexes_images: QPersistentModelIndex | None = None

        self.ai_model: None | AIListModel = None
        self.ai_proxyModel = AICustomSortFilterProxyModel(self)
        self.group_area_model = GroupAreaTable

        # compare
        self.compare1: CompareType | None = None
        self.compare2: CompareType | None = None
        self.cmp_model: CompareListModel | None = None

        # Graphic View classes
        self.image_view = self.ui.qgraphic_digitizer
        self.image_scene = ImageScene(self)
        self.fist_click_digitizer_page = True
        self.image_view.setScene(self.image_scene)
        self.image_view.grid_navigation = False
        self.gis_view = self.ui.gis_view
        self.gis_scene = GISScene(self)
        self.gis_view.setScene(self.gis_scene)
        self.gis_view.draw_map(path_to_data=path_to_shape)
        self.image_scene.db = self.db
        self.gis_scene.db = self.db

        # Connect signals
        self.image_scene.show_popup.connect(self.show_meta_popup)
        self.image_scene.resight_set.connect(self.resight_set)
        self.image_scene.element_created.connect(self.add_object)
        self.image_view.place_nav_rect.connect(self.set_rect)

        self.gis_scene.show_popup.connect(self.show_meta_popup)
        self.gis_scene.resight_set.connect(self.resight_set)
        self.gis_scene.group_images.connect(self.group_images)
        self.gis_scene.goto_image.connect(self.goto_image)
        self.gis_scene.selected_images.connect(self.select_images_in_pane)
        self.gis_scene.deselect_images.connect(self.deselect_images_in_pane)
        self.gis_scene.change_image_meta_list.connect(self.change_image_meta)
        self.gis_scene.change_image_block_list.connect(self.change_image_block)
        self.gis_scene.change_image_transect_list.connect(self.change_image_transect)

        self.ui.digitizer_image_panel.georef_signal.connect(self.show_popup_georef)
        self.ui.gis_image_panel.georef_signal.connect(self.show_popup_georef)
        self.ui.digitizer_image_panel.delete_images.connect(self.delete_images)
        self.ui.gis_image_panel.delete_images.connect(self.delete_images)

        self.ui.digitizer_image_panel.assign_environment.connect(self.assign_environment)
        self.ui.gis_image_panel.assign_environment.connect(self.assign_environment)

        self.ui.digitizer_image_panel.delete_folder.connect(self.delete_images_folder)
        self.ui.gis_image_panel.delete_folder.connect(self.delete_images_folder)

        self.ui.digitizer_image_panel.change_image_meta_list.connect(self.change_image_meta)
        self.ui.digitizer_image_panel.change_image_meta_folder.connect(self.change_image_meta_folder)
        self.ui.gis_image_panel.change_image_meta_list.connect(self.change_image_meta)
        self.ui.gis_image_panel.change_image_meta_folder.connect(self.change_image_meta_folder)

        self.ui.gallery_listview.goto_image.connect(self.goto_image)
        self.ui.gallery_listview.open_meta.connect(self.show_meta_popup)
        self.ui.gallery_listview.object_delete.connect(self.object_deleting)
        self.ui.gallery_listview.resight_set.connect(self.resight_set)

        # Assign variables to objects
        self.ui.gallery_listview.set_db(self.db)
        self.ui.ai_listview.set_db(self.db)

        # Variables
        self.dragPos = QPointF()
        self.user = 'user'
        self.logging_current_level = logging.INFO
        self.image: WISDAMImage | None = None
        self.current_index_persistent_index = QModelIndex()
        self.current_image_id = -1
        self.log_file: Path | None = None
        self.db_is_locked = ''
        self.gallery_filter = {}
        self.ai_filter = {}
        self.color_scheme = {}
        self.config = {}
        self.data_environment: dict | None = None

        # Color dicts for gis and digitizer page
        self.color_dict_gis_objects = None
        self.gis_color_attribute_images = 'folder'
        self.gis_color_attribute_objects = 'object_type'
        self.image_color_attribute_objects = 'projection'

        self.ai_path_input = ''
        self.ai_orig_path = ''
        self.ai_path_results = ''
        self.ai_time_processing = 0.0
        self.image_folders: list[Path] = []

        # Input data types
        input_data_names = self.input_data_types.get_input_names()
        self.ui.imp_cmb_input_type.addItems(input_data_names)
        self.input_data_types.set_input_class(self.ui.imp_cmb_input_type.currentText())
        self.ext_data_img_folder = ''

        # AI workflows
        ai_names = self.ai_workflow_types.get_input_names()
        self.ui.ai_cmb_input_type.addItems(ai_names)
        self.ai_workflow_types.set_ai_class(self.ui.imp_cmb_input_type.currentText())

        # ------------------------------------------------------------------------------------------------------------
        # Side menu
        self.ui.btn_toggle_menu.clicked.connect(self.menu_main_animation)

        # ------------------------------------------------------------------------------------------------------------
        # Toolbar MENU
        main_menu_new_db = QAction("Create New Project", self)
        main_menu_new_db.triggered.connect(self.create_new_db)

        main_menu_load_db = QAction("Load Project", self)
        main_menu_load_db.triggered.connect(self.load_existing_db)

        # Change paths
        main_menu_path_changing = QAction("Configure Image Paths", self)
        main_menu_path_changing.triggered.connect(self.show_change_path_db)

        # Change paths
        main_menu_mapper_config = QAction("Configure Mapper", self)
        main_menu_mapper_config.triggered.connect(self.show_mapper_configurator)

        # Change config
        main_menu_configure = QAction("Configure Colours", self)
        main_menu_configure.triggered.connect(self.show_config)

        align_menu = QMenu(self)
        align_menu.addAction(main_menu_new_db)
        align_menu.addAction(main_menu_load_db)
        align_menu.addSeparator()
        align_menu.addAction(main_menu_mapper_config)
        align_menu.addAction(main_menu_path_changing)
        align_menu.addAction(main_menu_configure)

        align_menu.setStyleSheet("background: rgb(130, 130, 130);font: 10pt;\n")

        help_menu_about = QAction("About WISDAM", self)
        help_menu_about.triggered.connect(self.popup_about.show)
        help_menu = QMenu(self)
        help_menu.addAction(help_menu_about)
        help_menu.addSeparator()
        help_menu.setStyleSheet("background: rgb(130, 130, 130);font: 10pt;\n")

        self.ui.toolButton_main.setMenu(align_menu)
        self.ui.toolButton_help.setMenu(help_menu)

        # ------------------------------------------------------------------------------------------------------------
        # Gallery PAGE
        # Gallery View hide sidebar
        self.ui.buttonGroup_gallery_order.buttonClicked.connect(self.show_thumbnails)
        self.ui.gallery_slider_thumb_size.valueChanged.connect(self.gallery_icon_size)

        self.ui.btn_gallery_filter_reset.clicked.connect(self.clear_gallery_filter)
        self.ui.btn_gallery_toggle_props.clicked.connect(
            lambda: toggle_visible_frame(self.ui.btn_gallery_toggle_props,
                                         self.ui.frame_gallery_properties))
        self.ui.gallery_fast_activate.clicked.connect(self.set_gallery_fast_activate)
        self.ui.gallery_filter_starred.clicked.connect(lambda: set_filter_boolean(self.gallery_proxyModel,
                                                                                  self.gallery_filter,
                                                                                  self.ui.gallery_filter_starred,
                                                                                  'highlighted'))

        self.ui.gallery_filter_reviewed.clicked.connect(lambda: set_filter_boolean(self.gallery_proxyModel,
                                                                                   self.gallery_filter,
                                                                                   self.ui.gallery_filter_reviewed,
                                                                                   'reviewed'))
        self.ui.gallery_filter_perspective_image.clicked.connect(
            lambda: set_filter_check_value(self.gallery_proxyModel, self.gallery_filter,
                                           self.ui.gallery_filter_perspective_image, 'image_type',
                                           ImageType.Perspective.fullname))
        self.ui.gallery_filter_ortho_image.clicked.connect(
            lambda: set_filter_check_value(self.gallery_proxyModel, self.gallery_filter,
                                           self.ui.gallery_filter_ortho_image, 'image_type',
                                           ImageType.Orthophoto.fullname))
        self.ui.gallery_filter_manual.clicked.connect(
            lambda: set_filter_check_value(self.gallery_proxyModel, self.gallery_filter,
                                           self.ui.gallery_filter_manual, 'source', 0))
        self.ui.gallery_filter_ai.clicked.connect(
            lambda: set_filter_check_value(self.gallery_proxyModel, self.gallery_filter, self.ui.gallery_filter_ai,
                                           'source', 1))

        self.ui.gallery_filter_external.clicked.connect(
            lambda: set_filter_check_value(self.gallery_proxyModel, self.gallery_filter,
                                           self.ui.gallery_filter_external, 'source', 2))

        self.ui.gallery_filter_group_area.textEdited.connect(
            lambda: set_filter_value(self.gallery_proxyModel, self.gallery_filter,
                                     self.ui.gallery_filter_group_area, 'group_area', 'int'))
        self.ui.gallery_filter_resight_set.textEdited.connect(
            lambda: set_filter_value(self.gallery_proxyModel, self.gallery_filter,
                                     self.ui.gallery_filter_resight_set, 'resight_set', 'int'))
        self.ui.gallery_filter_object.textEdited.connect(
            lambda: set_filter_value(self.gallery_proxyModel, self.gallery_filter, self.ui.gallery_filter_object,
                                     'object_type', 'string'))
        self.ui.gallery_filter_deactivated.clicked.connect(
            lambda: set_filter_check_value(self.gallery_proxyModel, self.gallery_filter,
                                           self.ui.gallery_filter_deactivated, 'active', 0))
        self.ui.gallery_filter_activated.clicked.connect(
            lambda: set_filter_check_value(self.gallery_proxyModel, self.gallery_filter,
                                           self.ui.gallery_filter_activated, 'active', 1))

        # ------------------------------------------------------------------------------------------------------------
        # GIS PAGE
        # Hide picks and images on gis page

        self.ui.gis_slider_area_distance.valueChanged.connect(self.group_area_distance_changed)
        self.group_area_distance_changed()
        self.ui.gis_btn_calc_group_area.clicked.connect(self.run_group_area)

        self.ui.btn_selection_rectangle.clicked.connect(
            lambda: self.set_instruction_selection(Selection.Rectangle))
        self.ui.btn_selection_lasso.clicked.connect(
            lambda: self.set_instruction_selection(Selection.Lasso))
        self.ui.gis_hide_images.clicked.connect(
            lambda: self.gis_scene.hide_images(self.ui.gis_hide_images.isChecked()))
        self.ui.gis_hide_image_centers.clicked.connect(
            lambda: self.gis_scene.hide_centerpoints(self.ui.gis_hide_image_centers.isChecked()))
        self.ui.gis_show_image_center_footprints.clicked.connect(
            lambda: self.gis_scene.show_footprints_on_hover(self.ui.gis_show_image_center_footprints.isChecked()))
        self.ui.gis_hide_objects.clicked.connect(
            lambda: self.gis_scene.hide_objects(self.ui.gis_hide_objects.isChecked()))

        self.ui.gis_color_objects_image.clicked.connect(
            lambda: self.gis_change_object_colors('image_id'))
        self.ui.gis_color_objects_resight_set.clicked.connect(
            lambda: self.gis_change_object_colors('resight_set'))
        self.ui.gis_color_objects_group_area.clicked.connect(
            lambda: self.gis_change_object_colors('group_area'))
        self.ui.gis_color_objects_type.clicked.connect(lambda: self.gis_change_object_colors('object_type'))
        self.ui.gis_color_objects_source.clicked.connect(lambda: self.gis_change_object_colors('source'))
        self.ui.gis_color_objects_reviewed.clicked.connect(lambda: self.gis_change_object_colors('reviewed'))

        self.ui.gis_color_image_folder.clicked.connect(
            lambda: self.gis_change_image_colors('folder'))
        self.ui.gis_color_image_group.clicked.connect(
            lambda: self.gis_change_image_colors('group_image'))
        self.ui.gis_color_image_transect.clicked.connect(
            lambda: self.gis_change_image_colors('transect'))
        self.ui.gis_color_image_refid.clicked.connect(
            lambda: self.gis_change_image_colors('flight_ref'))
        self.ui.gis_color_image_block.clicked.connect(
            lambda: self.gis_change_image_colors('block'))
        self.ui.gis_color_image_inspected.clicked.connect(
            lambda: self.gis_change_image_colors('inspected'))

        # GIS View double Click on image
        self.ui.gis_image_panel.doubleClicked.connect(self.gis_image_list_double_click)
        self.ui.gis_group_area_panel.doubleClicked.connect(self.gis_group_area_double_click)
        # Picking View hide sidebars
        self.ui.btn_gis_toggle_list.clicked.connect(
            lambda: toggle_visible_frame(self.ui.btn_gis_toggle_list, self.ui.frame_gis_object_list))
        self.ui.btn_gis_toggle_props.clicked.connect(
            lambda: toggle_visible_frame(self.ui.btn_gis_toggle_props, self.ui.frame_gis_properties))

        # ------------------------------------------------------------------------------------------------------------
        # Digitizer PAGE

        # Picking View hide sidebars
        self.ui.btn_picking_toggle_list.clicked.connect(
            lambda: toggle_visible_frame(self.ui.btn_picking_toggle_list, self.ui.frame_picking_image_list))
        self.ui.btn_picking_toggle_props.clicked.connect(
            lambda: toggle_visible_frame(self.ui.btn_picking_toggle_props, self.ui.frame_picking_properties))
        # Draw Instruction

        # Geometry Creation
        self.ui.btn_create_rectangle.clicked.connect(lambda: self.set_instruction(Instructions.Rectangle_Instruction))
        self.ui.btn_create_polygon.clicked.connect(lambda: self.set_instruction(Instructions.Polygon_Instruction))
        self.ui.btn_create_point.clicked.connect(lambda: self.set_instruction(Instructions.Point_Instruction))
        self.ui.btn_create_line.clicked.connect(lambda: self.set_instruction(Instructions.LineString_Instruction))
        # self.ui.btn_geometry_move.clicked.connect(lambda: self.set_instruction('move_geometry'))
        # self.ui.btn_geometry_resize.clicked.connect(lambda: self.set_instruction('change_geometry'))

        # Hide picks and Projections
        self.ui.picking_hide_projections.clicked.connect(self.pick_hide_projections)
        self.ui.picking_hide.clicked.connect(self.pick_hide)
        # Picking View double Click on image
        self.ui.digitizer_image_panel.doubleClicked.connect(self.load_image)

        self.ui.digitizing_color_reprojection.clicked.connect(
            lambda: self.digitizer_change_object_colors('projection'))
        self.ui.digitizing_color_image.clicked.connect(
            lambda: self.digitizer_change_object_colors('image_id', default_value=self.current_image_id))
        self.ui.digitizing_color_resight_set.clicked.connect(
            lambda: self.digitizer_change_object_colors('resight_set'))
        self.ui.digitizing_color_object_type.clicked.connect(
            lambda: self.digitizer_change_object_colors('object_type'))
        self.ui.digitizing_color_source.clicked.connect(
            lambda: self.digitizer_change_object_colors('source'))

        # Environment data
        self.ui.environment_image.value_changed.connect(self.set_environment)

        # Fit View
        self.ui.btn_fit_view.clicked.connect(self.image_view.fit_view)
        # Navigation Modus
        self.ui.stack_navigation.setCurrentWidget(self.ui.nav_page_free)
        self.ui.btn_navigation_chg_to_grid.clicked.connect(lambda: self.set_navigation_mode(grid_navigation=True))
        self.ui.btn_navigation_chg_to_free.clicked.connect(lambda: self.set_navigation_mode(grid_navigation=False))

        self.ui.btn_navigation_r.clicked.connect(self.image_view.nav_right)
        self.ui.btn_navigation_l.clicked.connect(self.image_view.nav_left)
        self.ui.btn_navigation_u.clicked.connect(self.image_view.nav_up)
        self.ui.btn_navigation_d.clicked.connect(self.image_view.nav_down)
        self.ui.btn_navigation_topleft.clicked.connect(self.image_view.nav_top_left)
        self.ui.dial_image_scale.valueChanged.connect(
            lambda: self.image_view.nav_scale(self.ui.dial_image_scale.value()))
        self.ui.btn_navigation_startwalk.clicked.connect(lambda:
                                                         self.nav_walk_modus(walk_modus=not self.image_view.nav_walk))
        self.ui.label_walk_modus.setHidden(True)

        self.image_view.send_text_label_walk_modus.connect(self.set_walk_label)

        # ------------------------------------------------------------------------------------------------------------
        # Project Cockpit PAGE

        self.ui.gauge_images_inspected.set_initial(gauge_name_1='IMAGES', gauge_name_2='inspected',
                                                   color_progres=ColorGui.color_gauge_img_inspected_progress,
                                                   color_inner=ColorGui.color_gauge_img_inspected_inner,
                                                   color_outer=ColorGui.color_gauge_img_inspected_outer)

        self.ui.gauge_images_georef.set_initial(gauge_name_1='IMAGES', gauge_name_2='georeferenced',
                                                color_progres=ColorGui.color_gauge_img_georef_percent,
                                                color_inner=ColorGui.color_gauge_img_georef_inner,
                                                color_outer=ColorGui.color_gauge_img_georef_outer)

        self.ui.gauge_ai_reviewed.set_initial(gauge_name_1='AI Imports', gauge_name_2='reviewed',
                                              color_progres=ColorGui.color_gauge_ai_reviewed_percent,
                                              color_inner=ColorGui.color_gauge_ai_reviewed_inner,
                                              color_outer=ColorGui.color_gauge_ai_reviewed_outer)

        self.ui.gauge_ai_imported.set_initial(gauge_name_1='AI Objects', gauge_name_2='imported',
                                              color_progres=ColorGui.color_gauge_ai_imported_percent,
                                              color_inner=ColorGui.color_gauge_ai_imported_inner,
                                              color_outer=ColorGui.color_gauge_ai_imported_outer)

        self.chart_obj_types = PieChartWisdam()
        self.ui.chart_view_obj_type.setChart(self.chart_obj_types)

        # ------------------------------------------------------------------------------------------------------------
        # Import PAGE
        # Load Data
        self.ui.imp_rd_logfile_image_folders.clicked.connect(self.hide_log_import_buttons)
        self.ui.imp_btn_logfile.clicked.connect(self.logfile_chooser)
        self.ui.imp_btn_logfile_folder.clicked.connect(self.logfile_path_chooser)
        self.ui.imp_btn_image_folder.clicked.connect(self.import_image_folder)
        # Change Input Data Type
        self.ui.imp_cmb_input_type.currentIndexChanged.connect(self.image_input_chooser)
        # self.ui.combo_external_type.currentIndexChanged.connect(self.external_chooser)
        # Import external Data
        # self.ui.btn_import_external_data.clicked.connect(self.import_external_data_caller)
        # self.ui.btn_select_img_folder_external_data.clicked.connect(self.ext_image_folder_chooser)
        self.ui.btn_test_image_exif.clicked.connect(self.get_meta_single_image)
        self.ui.btn_test_image_ortho.clicked.connect(self.get_meta_single_ortho)
        # ------------------------------------------------------------------------------------------------------------
        # Export PAGE
        # Export Buttons

        self.ui.btn_exp_footprint_kml.clicked.connect(lambda: self.export('footprint_kml.kml'))
        self.ui.btn_exp_footprint_shp.clicked.connect(lambda: self.export('footprint_shp.shp'))
        self.ui.btn_exp_footprint_csv.clicked.connect(lambda: self.export('footprint_csv.csv'))
        self.ui.btn_exp_footprint_json.clicked.connect(lambda: self.export('footprint_json.json'))

        self.ui.btn_exp_obj_shp.clicked.connect(lambda: self.export('object_shp.shp'))
        self.ui.btn_exp_obj_csv.clicked.connect(lambda: self.export('object_csv.csv'))
        self.ui.btn_exp_obj_kml.clicked.connect(lambda: self.export('object_kml.kml'))
        self.ui.btn_exp_obj_json.clicked.connect(lambda: self.export('object_json.json'))
        self.ui.btn_exp_obj_poin_shp.clicked.connect(lambda: self.export('object_point_shp.shp'))
        self.ui.btn_exp_obj_point_kml.clicked.connect(lambda: self.export('object_point_kml.kml'))
        self.ui.btn_exp_obj_point_json.clicked.connect(lambda: self.export('object_point_json.json'))
        # Export Trainings Data
        self.ui.db_export_trainingsdata.clicked.connect(self.export_trainings_data)
        # Export Project information
        self.ui.epxort_project_information.clicked.connect(lambda: self.export('project_information.txt'))

        # ------------------------------------------------------------------------------------------------------------
        # AI PAGE

        self.ui.ai_slider_thumb_size.valueChanged.connect(self.ai_change_icon_size)
        self.ui.rd_ai_all_follders.clicked.connect(self.ai_toggle_all_folders)
        self.ui.rd_toggle_labels.clicked.connect(self.toggle_ai_label)
        self.ui.ai_cmb_input_type.currentIndexChanged.connect(self.ai_input_chooser)
        self.ui.btn_load_ai_res_filesystem.clicked.connect(self.load_ai_results_filesystem)

        self.ui.btn_ai_activate_all.clicked.connect(lambda: self.ai_change_active_all(activate=True))
        self.ui.btn_ai_deactivate_all.clicked.connect(lambda: self.ai_change_active_all(activate=False))

        self.ui.btn_ai_toggle_props.clicked.connect(lambda: toggle_visible_frame(self.ui.btn_ai_toggle_props,
                                                                                 self.ui.frame_ai_properties))

        self.ui.btn_start_ai.clicked.connect(self.run_ai)
        self.ui.btn_import_ai.clicked.connect(self.import_ai)
        self.ui.btn_ai_filter_reset.clicked.connect(self.clear_ai_filter)
        self.ui.ai_filter_probability_slider.valueChanged.connect(self.set_ai_slider_label)
        self.ui.ai_filter_deactivated.clicked.connect(
            lambda: set_filter_check_value(self.ai_proxyModel, self.ai_filter, self.ui.ai_filter_deactivated,
                                           'active', 0))
        self.ui.ai_filter_activated.clicked.connect(
            lambda: set_filter_check_value(self.ai_proxyModel, self.ai_filter, self.ui.ai_filter_activated,
                                           'active', 1))
        self.ui.ai_filter_ai_run.textEdited.connect(
            lambda: set_filter_value(self.ai_proxyModel, self.ai_filter, self.ui.ai_filter_ai_run, 'ai_run',
                                     'int'))
        self.ui.ai_filter_object.textEdited.connect(
            lambda: set_filter_value(self.ai_proxyModel, self.ai_filter, self.ui.ai_filter_object,
                                     'object_type', 'string'))
        self.ui.ai_filter_probability_slider.sliderReleased.connect(
            lambda: set_filter_slider(self.ai_proxyModel, self.ai_filter, self.ui.ai_filter_probability_slider,
                                      'probability', scale=100))
        self.ui.ai_filter_prob_lower.clicked.connect(
            lambda: set_filter_boolean(self.ai_proxyModel, self.ai_filter, self.ui.ai_filter_prob_lower,
                                       'prob_lower'))
        # ------------------------------------------------------------------------------------------------------------
        # COMPARE PAGE
        # Picking View double Click on image
        self.ui.compare_tableView.doubleClicked.connect(self.compare_page_load_images)
        self.ui.btn_cmp_start.clicked.connect(self.compare_run)
        self.ui.btn_cmp_accept.clicked.connect(self.compare_accept)
        self.ui.btn_cmp_reject.clicked.connect(self.compare_reject)
        self.ui.btn_cmp_export.clicked.connect(self.compare_export)
        self.ui.btn_cmp_load.clicked.connect(self.compare_load)
        self.ui.btn_cmp_save.clicked.connect(self.compare_save)

        self.ui.compare_thumbs1.change_valid.connect(self.cmp_table_row_change_valid_cs1)
        self.ui.compare_thumbs1.valid_all_no.connect(self.cmp_table_row_all_no_cs1)
        self.ui.compare_thumbs2.change_valid.connect(self.cmp_table_row_change_valid_cs2)
        self.ui.compare_thumbs2.valid_all_no.connect(self.cmp_table_row_all_no_cs2)
        self.ui.btn_cmp_split.clicked.connect(self.compare_split)
        self.ui.btn_cmp_merge.clicked.connect(self.compare_merge)
        self.ui.compare_slider_size.valueChanged.connect(self.compare_icon_lists_icon_size)

        # ------------------------------------------------------------------------------------------------------------
        # Help PAGE
        #
        self.ui.btn_wisdam_homepage.clicked.connect(lambda: QDesktopServices.openUrl(url_wisdam))
        self.ui.btn_open_manual.clicked.connect(lambda: QDesktopServices.openUrl(path_to_manual.as_posix()))
        self.m_document = QPdfDocument(self)
        self.m_document.load(path_to_manual.as_posix())
        self.ui.pdf_viewer.setDocument(self.m_document)
        self.ui.pdf_viewer.setPageMode(QPdfView.PageMode.MultiPage)

        # ------------------------------------------------------------------------------------------------------------
        # window basic attributes

        # Add Menus
        self.ui.page_stack.setMinimumWidth(20)
        self.animation: QPropertyAnimation | None = None
        self.menu_buttons = MenuBar(top_widget=self.ui.layout_menus,
                                    bottom_widget=self.ui.layout_menu_bottom,
                                    action=self.menu_set)
        self.menu_buttons.add_button("PROJECT Cockpit", "url(:/icons/icons/menu-home.svg)", True)
        self.menu_buttons.add_button("IMPORT", "url(:/icons/icons/menu-import.svg)", True)
        self.menu_buttons.add_button("MAP", "url(:/icons/icons/menu-map.svg)", True)
        self.menu_buttons.add_button("OBJECT Digitiser", "url(:/icons/icons/menu-image.svg)", True)
        self.menu_buttons.add_button("GALLERY", "url(:/icons/icons/menu-gallery.svg)", True)
        self.menu_buttons.add_button("EXPORT", "url(:/icons/icons/menu-save.svg)", True)
        self.menu_buttons.add_button("AI", "url(:/icons/icons/menu-ai.svg)", False)
        self.menu_buttons.add_button("COMPARE Projects", "url(:/icons/icons/menu-compare.svg)", False)
        self.menu_buttons.add_button(" ", "", False)
        self.menu_buttons.add_button("MANUAL", "url(:/icons/icons/menu-mug-tea.svg)", False)

        # Start Page
        self.menu_set("PROJECT Cockpit")

        # frame, shadow
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.image_input_chooser()
        self.ai_input_chooser()

        self.ui.frame_top_middle.mouseDoubleClickEvent = self.double_click_maximize_restore

        # Move Window with top Frame
        self.ui.frame_top_middle.mouseMoveEvent = self.drag_window

        # Resize options
        sizegrip = QSizeGrip(self.ui.frame_size_grip)
        sizegrip.setStyleSheet("width: 20px; height: 20px; margin 0px; padding: 0px;")

        # Buttons for Windows
        self.ui.btn_minimize.clicked.connect(lambda: self.showMinimized())
        self.ui.btn_maximize_restore.clicked.connect(lambda: self.maximize_restore())
        self.ui.btn_close.clicked.connect(lambda: self.close())

        # Set Splitter parameters
        self.ui.picking_splitter.setSizes([100, 600])
        self.ui.picking_splitter.setCollapsible(0, False)
        self.ui.picking_splitter.setCollapsible(1, False)

        self.ui.splitter_gis.setSizes([100, 600])
        self.ui.splitter_gis.setCollapsible(0, False)
        self.ui.splitter_gis.setCollapsible(1, False)

        # ------------------------------------------------------------------------------------------------------------
        self.installEventFilter(self)

        # ------------------------------------------------------------------------------------------------------------
        # SHOW WINDOW
        # ------------------------------------------------------------------------------------------------------------
        # show window
        # First user window will be shown
        self.pop_user.show()

        # Test if docker is running
        # change_led_color(self.ui.led_docker_service, on=docker_running())
        # self.ui.led_docker_service.clicked.connect(self.led_docker_check)

    # ------------------------------------------------------------------------------------------------------------
    # Change menu action
    # ------------------------------------------------------------------------------------------------------------

    def menu_set(self, button_text: str):

        if self.popup_meta.isEnabled():
            self.popup_meta.close()

        self.menu_buttons.set_active(button_text)
        # Home Page
        if button_text == "PROJECT Cockpit":
            self.ui.page_stack.setCurrentWidget(self.ui.page_home)
            self.update_info()
        # IMPORT Page
        if button_text == "IMPORT":
            self.ui.page_stack.setCurrentWidget(self.ui.page_import)
        # GIS Page
        if button_text == "MAP":
            self.ui.page_stack.setCurrentWidget(self.ui.page_gis)
        # Picking Page
        if button_text == "OBJECT Digitiser":
            self.ui.page_stack.setCurrentWidget(self.ui.page_digitizer)
            if self.fist_click_digitizer_page:
                self.image_view.fit_view()
                self.fist_click_digitizer_page = False
        # Gallery Page
        if button_text == "GALLERY":
            self.ui.page_stack.setCurrentWidget(self.ui.page_gallery)
            self.ui.gallery_listview.setFocus()
        # AI Page
        if button_text == "AI":
            self.ui.page_stack.setCurrentWidget(self.ui.page_ai)
        # Export Page
        if button_text == "EXPORT":
            self.ui.page_stack.setCurrentWidget(self.ui.page_export)
        # Compare Page
        if button_text == "COMPARE Projects":
            self.ui.page_stack.setCurrentWidget(self.ui.page_compare)
        # Help Page
        if button_text == "MANUAL":
            self.ui.page_stack.setCurrentWidget(self.ui.page_help)

    # ------------------------------------------------------------------------------------------------------------
    # EVENTS MAIN WINDOW
    # ------------------------------------------------------------------------------------------------------------

    # move window
    def double_click_maximize_restore(self, event):
        # IF DOUBLE CLICK CHANGE STATUS
        if event.type() == QEvent.Type.MouseButtonDblClick:
            self.maximize_restore()

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def drag_window(self, event):
        # MOVE WINDOW
        if event.buttons() == Qt.MouseButton.LeftButton and not self.isMaximized():
            if event.globalPosition().y() < self.screen().size().height() - 50:
                self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos.toPoint())
                self.dragPos = event.globalPosition()
                event.accept()

    def eventFilter(self, source, event: QEvent | QKeyEvent):

        if event.type() == QEvent.Type.KeyRelease:
            if event.key() == Qt.Key.Key_Control:
                self.image_view.set_drag_mode(False)
                return True

        if event.type() == QEvent.Type.KeyPress:

            if not self.isActiveWindow():
                return False
            if self.ui.page_digitizer.isVisible():

                if self.image is not None:
                    # if self.image_scene.width() != 0.0 and \
                    #        not (self.popup_meta.isVisible() or self.popup_georef.isVisible() or
                    #             self.pop_path.isVisible()):

                    hard_propagate = self.ui.btn_propagate_always.isChecked()

                    if event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
                        next_index = self.image_panel_model.next_index(self.current_index_persistent_index)

                        if next_index.isValid():
                            self.load_image(next_index, propagate_environment=True,
                                            hard_propagate=hard_propagate)
                            # self.ui.digitizer_image_panel.scrollTo(next_index)
                            # self.ui.gis_image_panel.scrollTo(next_index)
                            return True

                    if event.key() == Qt.Key.Key_Backspace:
                        next_index = self.image_panel_model.previous_index(self.current_index_persistent_index)

                        if next_index.isValid():
                            self.load_image(next_index, propagate_environment=True,
                                            hard_propagate=hard_propagate)
                            # self.ui.digitizer_image_panel.scrollTo(next_index)
                            # self.ui.gis_image_panel.scrollTo(next_index)
                            return True

                    if event.key() == Qt.Key.Key_Space:
                        self.set_navigation_mode(not self.image_view.grid_navigation)
                        return True

                    if event.key() == Qt.Key.Key_Right:
                        self.image_view.nav_right()
                        return True
                    if event.key() == Qt.Key.Key_Left:
                        self.image_view.nav_left()
                        return True
                    if event.key() == Qt.Key.Key_Up:
                        self.image_view.nav_up()
                        return True
                    if event.key() == Qt.Key.Key_Down:
                        self.image_view.nav_down()
                        return True
                    if event.key() == Qt.Key.Key_Control:
                        self.image_view.set_drag_mode(True)
                        return True

        return False

    def mousePressEvent(self, event):
        self.dragPos = event.globalPosition()
        super(MainWindow, self).mousePressEvent(event)

    def resizeEvent(self, event: QResizeEvent) -> None:
        if self.popup_info.isVisible():
            frame_y = self.ui.frame_low.y()
            self.popup_info.move(0, frame_y - self.popup_info.height())
        super(MainWindow, self).resizeEvent(event)

    # --------------------------------------------------------------
    # Window
    # --------------------------------------------------------------

    def menu_main_animation(self):

        # get current width of the button frame
        width = self.ui.frame_left_menu.width()
        max_width = 220
        min_width = 60

        # set width depending on current width
        if width < max_width:
            width_extended = max_width
        else:
            width_extended = min_width

        # animation of the frame with buttons
        self.animation = QPropertyAnimation(self.ui.frame_left_menu, b"minimumWidth")
        self.animation.setDuration(300)
        self.animation.setStartValue(width)
        self.animation.setEndValue(width_extended)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuart)
        self.animation.start()

    def maximize_restore(self):
        if not self.isMaximized():
            self.showMaximized()
            self.ui.horizontalLayout.setContentsMargins(0, 0, 0, 0)
            self.ui.btn_maximize_restore.setToolTip("Restore")
            self.ui.btn_maximize_restore.setIcon(QIcon(u":/icons/icons/ico-window-restore.png"))
            self.ui.frame_size_grip.hide()
        else:
            self.showNormal()
            self.resize(self.width(), self.height())
            self.ui.btn_maximize_restore.setToolTip("Maximize")
            self.ui.btn_maximize_restore.setIcon(QIcon(u":/icons/icons/ico-window-maximize.png"))
            self.ui.frame_size_grip.show()

    # --------------------------------------------------------------
    # LOGGING PLOTTER
    # --------------------------------------------------------------
    # Handler for standard output
    def handle_output(self, text, stdout):

        frame_y = self.ui.frame_low.y()
        self.popup_info.move(0, frame_y - self.popup_info.height())
        self.popup_info.ui.info_screen.moveCursor(QTextCursor.MoveOperation.End)
        if not stdout:
            log_style = logging_style.get(logging.ERROR, '')
            self.logging_current_level = logging.ERROR
        else:
            log_style = logging_style.get(logging.INFO, '')
            self.logging_current_level = logging.ERROR

        self.ui.btn_info_popup.setIcon(QIcon(log_style['icon']))
        self.popup_info.ui.frame_info.setStyleSheet(log_style['frame'])
        self.popup_info.ui.info_screen.setTextColor(log_style['txt'])
        self.popup_info.show()
        self.popup_info.ui.info_screen.insertPlainText(text)
        self.popup_info.ui.info_screen.setTextColor(QColor(255, 255, 255))

    # Handler for logging class
    @Slot(str, logging.LogRecord)
    def handle_output_logging(self, status, record: logging.LogRecord):

        frame_y = self.ui.frame_low.y()
        self.popup_info.move(0, frame_y - self.popup_info.height())

        if record.levelno is logging.INFO and hasattr(record, 'finished'):
            log_style = logging_style.get("finished", '')
        else:
            log_style = logging_style.get(record.levelno, '')

        if record.levelno > self.logging_current_level or hasattr(record, 'finished'):
            # Only set the info page if current is higher as the actually shown one
            # Therefore a normal info will not change the error screen if immediately followed
            self.ui.btn_info_popup.setIcon(QIcon(log_style['icon']))
            self.popup_info.ui.frame_info.setStyleSheet(log_style['frame'])
        self.logging_current_level = record.levelno

        # This can be set for every type of logging
        self.popup_info.ui.info_screen.moveCursor(QTextCursor.MoveOperation.End)
        self.popup_info.ui.info_screen.setTextColor(log_style['txt'])
        self.popup_info.ui.info_screen.insertPlainText(status + '\n')
        if record.levelno > logging.INFO or hasattr(record, 'finished'):
            self.popup_info.show()

        scroll = self.popup_info.ui.info_screen.verticalScrollBar()
        scroll.setValue(scroll.maximum())

    # --------------------------------------------------------------
    # COMMON SLOTS
    # --------------------------------------------------------------
    @Slot(object)
    def delete_images_folder(self, folder: Path):
        """Delete images from database and geometries
        Make sure that also the groups are updated
        There are references to image db in Ai detections, configuration and
        on geometries. So that must be changed first"""

        images_id = self.db.get_image_id_by_folder(folder)
        if images_id is not None:
            self.db.delete_images(images_id)
            self.reload_database()

    @Slot(list)
    def delete_images(self, images_id: list):
        """Delete images from database and geometries
        Make sure that also the groups are updated
        There are references to image db in Ai detections, configuration and
        on geometries. So that must be changed first"""

        self.db.delete_images(images_id)
        self.reload_database()

    @Slot(object)
    def change_image_meta_folder(self, folder: Path):
        """Change the image metadata for a complete folder"""

        images_ids = self.db.get_image_id_by_folder(folder)
        if images_ids is not None:
            self.change_image_meta(images_ids)

    @Slot(list)
    def change_image_block(self, images_ids: list):
        v = POPUPTextInput()
        if v.exec():
            value = v.get_data()

            if value:
                if not value.isspace():
                    self.db.update_image_meta(images_ids, block=value)
                    self.gis_scene.change_survey_data(images_ids, block=value)
                    self.gis_scene.color_images(attribute=self.gis_color_attribute_images)

    @Slot(list)
    def change_image_transect(self, images_ids: list):
        v = POPUPTextInput()
        if v.exec():
            value = v.get_data()

            if value:
                if not value.isspace():
                    self.db.update_image_meta(images_ids, transect=value)
                    self.gis_scene.change_survey_data(images_ids, transect=value)
                    self.gis_scene.color_images(attribute=self.gis_color_attribute_images)

    @Slot(list)
    def change_image_meta(self, images_ids: list):

        v = POPUPImageMeta()
        update_all = False

        if len(images_ids) == 1:

            # If single image is updated, the data can be loaded
            # and everything will be updated
            update_all = True
            data = self.db.load_image(images_ids[0])

            meta = {}
            if data['meta_user']:
                meta = json.loads(data['meta_user'])

            v.set_data(transect=data['transect'], flight_ref=data['flight_ref'], block=data['block'], meta_user=meta)

        if v.exec():
            data = v.get_data()
            flight_ref, transect, block, meta_user_input = data

            # if meta_user is deleted for single image displayed it should be written standard emtpy
            if not meta_user_input and update_all:
                meta_user_input = {'operator': '', 'camera_ref': '', 'conditions': '', 'comments': ''}
            self.db.update_image_meta(images_ids, flight_ref, transect, block, meta_user_input, update_all)

            if flight_ref or transect or block or update_all:
                self.gis_scene.change_survey_data(images_ids, transect=transect, flight_ref=flight_ref,
                                                  block=block, update_all=False)
                self.gis_scene.color_images(attribute=self.gis_color_attribute_images)

    @Slot(int, list)
    def assign_environment(self, image_ref: int, image_list: list, change_objects: bool):
        """Assign environment data to images from image reference"""
        if not self.db_is_locked:

            env_data = self.db.load_image_environment_data(image_ref)
            if env_data:

                # Change image env data.
                self.db.update_multiple_image_environment_data(env_data, image_list)

                if change_objects:
                    self.db.update_multiple_objects_environment_data(env_data, image_list)

                # Update the env of current image if in image list
                if self.image_scene.image_id_db in image_list:
                    self.ui.environment_image.data = env_data
            else:
                logger.warning("Reference image - environment data is not set")

    @Slot(list)
    def select_images_in_pane(self, persistent_indexes: list):

        if self.image_panel_model.image_count() < 5000:
            selection_model = self.image_panel_model.select_images(persistent_indexes)
            self.ui.digitizer_image_panel.setSelectionModel(selection_model)
            self.ui.gis_image_panel.setSelectionModel(selection_model)

        # old version
        # self.ui.digitizer_image_panel.select_images(persistent_indexes)
        # self.ui.gis_image_panel.select_images(persistent_indexes)

    @Slot()
    def deselect_images_in_pane(self):
        self.ui.digitizer_image_panel.clearSelection()
        self.ui.gis_image_panel.clearSelection()

    @Slot(int)
    def goto_image(self, image_id: int):

        index = self.image_panel_model.match(self.image_panel_model.index(0, 0),
                                             RolesImagePane.id, image_id, -1, Qt.MatchFlag.MatchRecursive)[0]
        item = self.image_panel_model.get_item(index)

        if Path(item.data(ImageList.path)).exists():
            if self.current_index_persistent_index.data(RolesImagePane.id) != index.data(RolesImagePane.id):

                self.load_image(index)

            else:
                self.menu_set("OBJECT Digitiser")
        else:
            logger.warning('Images does not exist: ' + Path(item.data(ImageList.path)).name +
                           '\nPlease use "Change PATHS" to locate these images')

            # Prevent if on GIS view to recenter
            if self.sender() == self.ui.gallery_listview:
                self.gis_image_list_double_click(index)

    @Slot(list, bool)
    def resight_set(self, item_list: list, clear_group=False):
        item_list_left = []
        item_list_mew = item_list

        # Get ids and all group ids of all members in the groups of the objects in item_list
        objs_in_groups = self.db.get_group_ids_by_object_ids(item_list)
        objects_id_with_group = [x['id'] for x in objs_in_groups if x['resight_set'] > 0]
        groups_found = list(set([x['resight_set'] for x in objs_in_groups if x['resight_set'] > 0]))
        images_found = [x['image'] for x in objs_in_groups if x['id'] in item_list or x['resight_set'] > 0]
        obj_types_found = [x['object_type'] for x in objs_in_groups if x['id'] in item_list or x['resight_set'] > 0]
        meta_types_found = [x['meta_type'] for x in objs_in_groups if x['id'] in item_list or x['resight_set'] > 0]

        if clear_group:
            # Seems none of the items is in a group
            if len(objects_id_with_group) == 0:
                return

            # As only one element can be cleared by this function it should only be one group here after all
            # So if in a group only 2 elements than for both objects the group will be cleared
            if len(objects_id_with_group) < 3:
                item_list_mew = objects_id_with_group

            # The items which will be left in the group
            if len(objects_id_with_group) >= 3:
                # This will be needed for the first certain
                item_list_left = [x for x in objects_id_with_group if x not in item_list]

            # To clear group set index to 0
            group_index = 0

        else:
            # Set groups

            if len(images_found) > len(set(images_found)):
                logger.warning("Can not set resight set within the same image")
                return

            if len(set(obj_types_found)) > 1:
                logger.warning("Can not set resight for objets of different object types")
                return

            if len(set(meta_types_found)) > 1:
                logger.warning("Can not set resight for of different meta types")
                return

            # check if some selected objects have already a resight set id
            if len(groups_found) == 0:
                group_index = self.db.get_next_resight_set() + 1
            elif len(groups_found) == 1:
                group_index = groups_found[0]
                item_list_mew = list(set(objects_id_with_group + item_list))
            else:
                logger.warning("Can not merge items of more than one resight set")
                return

        # Set Resight Set of new objects or adapt other
        self.db.set_resight_set(item_list_mew, group_index)

        # Certainty handling
        # This sets the dependencies of first certain if cleared or newly groups are formed
        if clear_group:
            self.db.clear_resight_data(item_list_mew)
            if len(item_list_left) > 0:
                self.db.set_resight_data(item_list_left)
        else:
            self.db.set_resight_data(item_list_mew)

        # Update Thumbnail values
        for item in item_list_mew:
            index_thumb = self.thumbnail_model.match(self.thumbnail_model.index(0, 0), GalleryRoles.id, item)
            self.thumbnail_model.set_resight_set(index_thumb[0].row(), group_index)

        # Update GIS objects
        self.gis_scene.change_resight_set(item_list_mew, group_index)
        # self.gis_scene.change_tooltip(item_list_mew, resight_set=group_index)
        if self.ui.gis_color_objects_resight_set.isChecked():
            self.gis_change_object_colors(attribute='resight_set')

        # Update image objects
        self.image_scene.change_resight_set(item_list_mew, group_index)
        # self.image_scene.change_tooltip(item_list_mew, resight_set=group_index)
        if self.ui.digitizing_color_resight_set.isChecked():
            self.digitizer_change_object_colors(attribute='resight_set')

    @Slot(list)
    def group_images(self, item_list):

        group_index = self.db.get_next_images_group() + 1
        self.db.set_group_images(item_list, group_index)
        self.gis_scene.change_image_group(item_list, group_index)
        if self.ui.gis_color_image_group.isChecked():
            self.gis_change_image_colors(attribute='group_image')

    # --------------------------------------------------------------
    # Popup Handling
    # --------------------------------------------------------------
    def show_info_popup(self):

        if self.popup_info.isVisible():
            self.popup_info.hide()
            self.ui.btn_info_popup.setIcon(QIcon(u":/icons/icons/info-40.svg"))
            log_style = logging_style.get(logging.INFO, '')
            self.popup_info.ui.frame_info.setStyleSheet(log_style['frame'])
            self.logging_current_level = logging.INFO
        else:
            frame_y = self.ui.frame_low.y()
            self.popup_info.move(0, frame_y - self.popup_info.height())
            self.popup_info.show()

    @Slot(str)
    def user_save(self, user):
        self.user = user
        logger.info('Welcome ' + self.user.upper() + '. Enjoy working')
        self.show()

    @Slot(tuple)
    def thread_update_geom_result(self, result: tuple[int, int, int, int]):

        self.ui.waiting_spinner_main.stop()
        info_text = "Update geometries finished\n\t\tImages mapped: %i, Images not mapped: %i\n" \
                    "\t\tObjects mapped: %i, Objects not mapped %i\nReloading GIS geometries" % result
        logger.info(info_text, extra={"finished": True})
        self.gis_scene.clear()
        # persistent_index_dict is a dictionary with path as posix and the
        # persistent model index from image pane model
        worker = Worker(worker_heavy_loading, None, self.db.path,
                        self.persistent_model_indexes_images,
                        True, self.gis_color_attribute_objects, self.color_scheme)
        worker.signals.result.connect(self.thread_result_heavy_worker)
        worker.signals.finished.connect(self.thread_finished_heavy_worker)
        worker.signals.error.connect(self.thread_error)
        self.threadpool.start(worker)
        self.ui.waiting_spinner_main.start()

    @Slot(dict, bool)
    def change_mapper(self, mapper_config: dict | None, recalculate_geometries: bool = False):

        self.mapper = mapper_load_from_dict(mapper_config)
        # The mapper should not be None because we just got a valid mapper
        change_led_color(self.ui.led_elevation_service, on=True)

        # Set mapper to DB
        self.db.mapper = mapper_config

        # Change the mapper of the current image
        if self.image is not None:
            self.image.mapper = self.mapper

        if recalculate_geometries:
            logger.info("Start updating image and objects coordinates")
            self.db_is_locked = 'Database locked for recalculating geometries'
            worker = Worker(update_all_geoms, self.db.path, self.mapper)
            worker.signals.result.connect(self.thread_update_geom_result)
            worker.signals.error.connect(self.thread_error)
            self.threadpool.start(worker)
            self.ui.waiting_spinner_main.start()

    def show_mapper_configurator(self):

        if self.db is not None:
            config_mapper = None
            config = self.db.load_config()
            if config['mapper'] is not None:
                config_mapper = json.loads(config['mapper'])
            self.popup_mapper.set_mapper(config_mapper)
            self.popup_mapper.show()

    @Slot(int)
    def show_meta_popup(self, obj_id):
        self.popup_meta.set_db(self.db)
        self.popup_meta.load_values(obj_id)
        self.popup_meta.show()
        self.popup_meta.activateWindow()

    @Slot(list)
    def show_popup_georef(self, image_ids: list):

        if self.image_scene.working_instruction:
            return
        if not self.db_is_locked:
            self.db_is_locked = 'Database locked for georef update'

            if self.popup_meta.isEnabled():
                self.popup_meta.close()

            self.popup_georef.db = self.db
            self.popup_georef.image_ids = image_ids
            self.popup_georef.user = self.user
            self.popup_georef.mapper = self.mapper
            self.popup_georef.show()
            self.popup_georef.activateWindow()
        else:
            logger.warning(self.db_is_locked)

    def show_config(self):
        if self.db is not None:
            self.popup_config.show()
            self.popup_config.activateWindow()

    @Slot(object)
    def config_changed(self, color: dict):

        if self.db is not None:
            self.color_scheme['projection']['colors'] = color
            self.image_scene.standard_color = color[0]

            self.db.color_scheme = self.color_scheme

            if self.ui.digitizing_color_reprojection.isChecked():
                self.digitizer_change_object_colors('projection')

    def show_change_path_db(self):
        if not self.db_is_locked and self.ui.digitizer_image_panel.model():
            self.db_is_locked = 'Database locked for path mounting'
            self.popup_path.set_db(self.db)
            self.popup_path.get_values()
            self.popup_path.show()
            self.popup_path.activateWindow()

    @Slot(bool)
    def change_path_db_finished(self, changed: bool):
        self.db_is_locked = ''
        if changed:
            images = self.db.load_images_list()
            if images:
                self.image_scene.clear()

                # Update path and in image pane
                self.persistent_model_indexes_images = self.show_image_list(images)
                # self.show_image_list(images)
                last_used_image = self.db.last_image
                if last_used_image:
                    index = self.image_panel_model.match(self.image_panel_model.index(0, 0),
                                                         RolesImagePane.id, last_used_image, -1,
                                                         Qt.MatchFlag.MatchRecursive)[0]

                    self.load_image(index, change_to_digitizer_page=False)

            self.update_info()
        logger.info('Path window closed')

    @Slot()
    def popup_georef_closed(self):
        self.db_is_locked = ''

    @Slot(bool)
    def georef_finished(self, updated):
        self.db_is_locked = ''
        if updated:
            self.reload_database()

    # --------------------------------------------------------------
    # Object Handling
    # --------------------------------------------------------------
    @Slot(OrderedDict, str)
    def save_object_types_to_db(self, object_types: OrderedDict, config_name: str | None = None):

        self.db.store_object_types(object_types, config_name)

    @Slot()
    def thread_mapping_finished(self):
        pass

    @Slot(object)
    def thread_mapping_result(self, return_tuple: tuple[int, str, CoordinatesTransformer | None, float, float] | None):

        if return_tuple is None:
            logger.warning("Mapping not possible")
            return

        obj_id, geom_type, coordinates_wgs84, gsd, area = return_tuple

        if self.popup_meta.isVisible():

            if gsd is not None:
                if gsd > 0.0:
                    self.popup_meta.set_scale(gsd)

        # We do not need to check if Object ID exists, sqlite update will simply find not the ID
        geojson = coordinates_wgs84.geojson(geom_type=geom_type)
        self.db.update_object_mapping(obj_id, geojson=geojson, gsd=gsd, area=area)

        # At this stage it is actually possible that the type is not yet assigned
        # Therefore if object type is emtpy it will be plotted black
        self.color_dict_gis_objects = loader_gis_geom_objects_single(self.db, self.gis_scene, obj_id,
                                                                     self.color_dict_gis_objects,
                                                                     self.gis_color_attribute_objects,
                                                                     default_dict=self.color_scheme)

    @Slot(int, str, list)
    def add_object(self, obj_id: int, geom_type: str, pixel_coordinates: list):

        index_image = self.image_panel_model.match(self.image_panel_model.index(0, 0),
                                                   RolesImagePane.id, self.current_image_id, -1,
                                                   Qt.MatchFlag.MatchRecursive)[0]

        # Add thumbnail to gallery
        data = gallery_loader_single(self.db, obj_id)
        self.thumbnail_model.append_data(data)
        self.image_panel_model.add_object(index_image)

        self.show_meta_popup(obj_id)

        if self.image.is_geo_referenced:
            worker = Worker(self.image.map_geometry_to_epsg4979, obj_id, geom_type, pixel_coordinates)
            worker.signals.finished.connect(self.thread_mapping_finished)
            worker.signals.result.connect(self.thread_mapping_result)
            worker.signals.error.connect(self.thread_error)
            self.threadpool.start(worker)

    @Slot(int, int)
    def object_deleting(self, obj_id: int, image_id: int):

        index_thumb = self.thumbnail_model.match(self.thumbnail_model.index(0, 0), GalleryRoles.id, obj_id)

        index_image = self.image_panel_model.match(self.image_panel_model.index(0, 0),
                                                   RolesImagePane.id, image_id, -1,
                                                   Qt.MatchFlag.MatchRecursive)[0]

        # Before deleting we perform a clear of the resight set
        # Thus if after deleting an object would be left as single resight is prevented
        self.resight_set([obj_id], clear_group=True)

        index_thumb[0].model().removeRows(index_thumb[0].row(), 1)

        self.image_panel_model.remove_object(index_image)
        self.gis_scene.delete_object(obj_id)
        self.image_scene.delete_object(obj_id)
        self.db.obj_delete(obj_id)

        # If resight coloring is checked it would be already redrawn in resight_set
        # Just to avoid spending time, probably not necessary
        if not self.ui.gis_color_objects_resight_set.isChecked():
            self.gis_change_object_colors()

        if not self.ui.digitizing_color_resight_set.isChecked():
            self.digitizer_change_object_colors()

    @Slot(int, int)
    def object_type_change(self, obj_id: int, image_id: int):

        # save changes to Database
        index_thumb = self.thumbnail_model.match(self.thumbnail_model.index(0, 0), GalleryRoles.id, obj_id)
        data = gallery_loader_single(self.db, obj_id)
        self.thumbnail_model.change_object_tag_reviewed(index_thumb[0], data)

        # self.image_scene.change_tooltip([obj_id], data.object_type, reviewed=1)
        self.image_scene.change_object_type([obj_id], data.object_type)
        # self.gis_scene.change_tooltip([obj_id], data.object_type, reviewed=1)
        self.gis_scene.change_object_type([obj_id], data.object_type)

        if self.ui.gis_color_objects_type.isChecked():
            self.gis_change_object_colors(attribute='object_type')

        # TODO Actually that could be only done for that specific object
        # No function currently to update single element
        if self.ui.gis_color_objects_reviewed.isChecked():
            self.gis_change_object_colors(attribute='reviewed')

        # The image scene should always be updated
        self.digitizer_change_object_colors()

        # We update the env data for that image if the object changed it because it was not set
        if image_id == self.current_image_id:

            env_data = self.db.load_image_environment_data(self.current_image_id)
            if env_data:
                self.data_environment = env_data
                self.ui.environment_image.data = self.data_environment

    # --------------------------------------------------------------
    # STANDARD THREAD signals - outputs and progress handling
    # --------------------------------------------------------------
    @Slot(tuple)
    def progress_fn(self, value):
        self.ui.progressBar_importer.setMaximum(value[0])
        self.ui.progressBar_importer.setValue(value[1])
        self.ui.progressBar_importer.update()

    @Slot(str)
    def thread_output(self, s):
        pass

    @Slot(object)
    def thread_output_image_import(self, res_dict: dict | None):

        if res_dict is not None:

            if res_dict['log_fail']:
                logger.warning("Import aborted. Logfile problem")
                return

            # this key is only set if using logfile importer
            success_logfiles = res_dict.get('log_success', None)
            if success_logfiles is not None:
                # logfiles importer was used but not logfile found
                if success_logfiles == 0:
                    logger.warning("No logfiles found")

            if not res_dict['img_nr']:

                logger.warning("No images found")
            else:

                if success_logfiles is not None:

                    msg = ("\nImage import finished: "
                           "\n\tfound %i logfiles,"
                           "\n\tfound %i images,"
                           "\n\t%i re-imported; %i georeferenced; %i can not be imported\n") % (res_dict['log_success'],
                                                                                                res_dict['img_nr'],
                                                                                                res_dict['exist_nr'],
                                                                                                res_dict['geo_nr'],
                                                                                                res_dict['fail_nr'])
                else:
                    msg = ("\nImage import finished: "
                           "\n\tfound %i images,"
                           "\n\t%i re-imported; %i georeferenced; %i can not be imported\n") % (res_dict['img_nr'],
                                                                                                res_dict['exist_nr'],
                                                                                                res_dict['geo_nr'],
                                                                                                res_dict['fail_nr'])
                logger.info(msg, extra={"finished": True})

    @Slot(tuple)
    def thread_error(self, t):
        exc_type, value, text = t
        logger.error(text)
        self.ui.waiting_spinner_main.stop()
        self.ui.ai_waiting_spinner.stop()
        self.ui.gis_group_waiting_spinner.stop()
        self.db_is_locked = ''

    # --------------------------------------------------------------
    # AI
    # --------------------------------------------------------------

    def ai_change_icon_size(self):
        thumb_size_user = GalleryIconSize()
        thumb_size_user.width = self.ui.ai_slider_thumb_size.value()
        thumb_size_user.height = thumb_size_user.width
        self.ui.ai_listview.setIconSize(QSize(thumb_size_user.width, thumb_size_user.height))
        self.ui.ai_listview.setItemDelegate(AIDelegate(icon_size=thumb_size_user, db=self.db))

    def ai_toggle_all_folders(self):
        """If all folders radio button is checked than single folder combo box is not visible and
        also the different image folder is not visible because that only works for single folders"""
        if self.sender().isChecked():
            self.ui.ai_folder_chooser.setVisible(False)
            self.ui.ai_radio_different_image_folder.setVisible(False)
        else:
            self.ui.ai_folder_chooser.setVisible(True)
            self.ui.ai_radio_different_image_folder.setVisible(True)

    def toggle_ai_label(self):
        self.ui.ai_listview.itemDelegate().toggle_labels()
        self.ui.ai_listview.repaint()

    @Slot(bool)
    def thread_output_ai(self, s):

        elapsed = time.time() - self.ai_time_processing
        time_string = 'Time elapsed[min]: ' + str(int(elapsed / 60))

        if s:
            logger.info(time_string + " - AI run finished", extra={"finished": True})
        else:
            logger.error(time_string + " - AI run failed.")

    @Slot(tuple)
    def progress_fn_ai(self, value):
        self.ui.progressBar_ai.setMaximum(value[0])
        self.ui.progressBar_ai.setValue(value[1])
        self.ui.progressBar_ai.update()

    @Slot()
    def thread_complete_ai_import(self):

        config = json.loads(self.db.load_config()['configuration'], object_pairs_hook=OrderedDict)
        first_key = list(config['meta_config'].keys())[0]
        config = config['meta_config'][first_key]
        self.popup_meta.configure_object_types(config)

        self.update_table_views()
        self.ui.ai_waiting_spinner.stop()

    @Slot()
    def thread_complete_ai_run(self):
        self.db_is_locked = ''
        self.show_ai()
        self.ui.ai_waiting_spinner.stop()

    @Slot()
    def thread_complete_export_ai(self):
        self.db_is_locked = ''
        self.ui.waiting_spinner_main.stop()

    def ai_input_chooser(self):
        self.ai_workflow_types.set_ai_class(self.ui.ai_cmb_input_type.currentText())
        if self.ai_workflow_types.ai_type_current.is_runnable:
            self.ui.ai_frame_start.show()
        else:
            self.ui.ai_frame_start.hide()
        logger.info('Set current ai workflow to: ' + self.ai_workflow_types.ai_type_current.name)

    def set_ai_slider_label(self, value):
        self.ui.ai_prob_slider_value.setText("%2i" % value + '%')

    def show_ai(self):

        if self.db is not None:

            self.ui.ai_listview.setModel(None)
            if self.ai_model is not None:
                self.ai_model.deleteLater()
            self.ai_model = None
            self.ai_proxyModel.setSourceModel(None)
            thumb_size_user = GalleryIconSize()
            thumb_size_user.width = self.ui.ai_slider_thumb_size.value()
            thumb_size_user.height = thumb_size_user.width
            self.ui.ai_listview.setIconSize(QSize(thumb_size_user.width, thumb_size_user.height))
            self.ai_model = ai_loader(self.db)
            self.ai_proxyModel.setSourceModel(self.ai_model)
            self.ui.ai_listview.setModel(self.ai_proxyModel)
            self.ui.ai_listview.setItemDelegate(AIDelegate(icon_size=thumb_size_user, db=self.db))

    def run_ai(self):

        if not self.ai_workflow_types.ai_type_current.is_runnable:
            logger.warning("That AI workflow has no running option")
            return

        if self.db is not None:
            if not self.db_is_locked:
                self.ai_path_input = self.ui.ai_folder_chooser.currentText()
                self.ai_orig_path = None

                if self.ai_path_input:

                    if self.ui.ai_radio_different_image_folder.isChecked():
                        image_path = QFileDialog.getExistingDirectory(self,
                                                                      caption="Image folder to be used for AI",
                                                                      dir=self.ai_path_input)
                        if image_path:
                            self.ai_orig_path = self.ai_path_input
                            self.ai_path_input = image_path

                        else:
                            return

                    self.db_is_locked = "DB locked for running AI"

                    self.ai_path_results = Path.joinpath(Path(self.db.path.parent), self.db.path.stem + '_export')
                    if not self.ai_path_results.exists():
                        self.ai_path_results.mkdir()
                    str_day = datetime.datetime.now().strftime("run-%Y_%d_%m-%H_%M")
                    self.ai_path_results = Path.joinpath(Path(self.db.path.parent),
                                                         self.db.path.stem + '_export', str_day)
                    if not self.ai_path_results.exists():
                        self.ai_path_results.mkdir()

                    self.ai_path_input = Path(self.ai_path_input)
                    if self.ui.rd_ai_all_follders.isChecked():
                        worker = Worker(self.ai_workflow_types.run_ai_all_folders,
                                        self.db.path, self.image_folders,
                                        self.ai_path_results, self.user, progress_callback=True)

                    else:
                        worker = Worker(self.ai_workflow_types.run_ai_single_folder,
                                        self.db.path, self.ai_path_input, self.ai_orig_path,
                                        self.ai_path_results, self.user, progress_callback=True)
                    worker.signals.result.connect(self.thread_output_ai)
                    worker.signals.finished.connect(self.thread_complete_ai_run)
                    worker.signals.progress.connect(self.progress_fn_ai)
                    worker.signals.error.connect(self.thread_error)
                    logger.info('AI Started at: ' + time.asctime())
                    self.ai_time_processing = time.time()
                    self.threadpool.start(worker)
                    self.ui.ai_waiting_spinner.start()
            else:
                logger.warning(self.db_is_locked)

    def load_ai_results_filesystem(self):

        if not self.ai_workflow_types.ai_type_current.is_filesystem_loadable:
            logger.warning("That AI workflow has no filesystem load implemented")
            return

        if self.db is not None:
            if not self.db_is_locked:

                if self.ai_workflow_types.ai_type_current.loader == AILoaderType.Folder:
                    ai_import_path = QFileDialog.getExistingDirectory(self, caption="AI Folder or root Folder",
                                                                      dir=self.db.path.parent.as_posix())
                elif self.ai_workflow_types.ai_type_current.loader == AILoaderType.LogFile:
                    ai_import_path, _ = QFileDialog.getOpenFileName(self, caption="AI import file",
                                                                    dir=self.db.path.parent.as_posix())

                else:
                    logger.error("AI Loader Type not implemented")
                    return

                if ai_import_path:
                    worker = Worker(self.ai_workflow_types.load_ai_result_filesystem,
                                    self.db.path, Path(ai_import_path), self.user,
                                    progress_callback=True)
                    worker.signals.result.connect(self.thread_output_ai)
                    worker.signals.finished.connect(self.thread_complete_ai_run)
                    worker.signals.progress.connect(self.progress_fn_ai)
                    worker.signals.error.connect(self.thread_error)

                    self.ai_time_processing = time.time()
                    logger.info('AI file system import start at: ' + time.asctime())
                    self.threadpool.start(worker)
                    self.db_is_locked = 'DB locked for MAD import'
                    self.ui.ai_waiting_spinner.start()
            else:
                logger.warning(self.db_is_locked)

    def import_ai(self):
        if self.db is not None:
            if not self.db_is_locked:
                self.db_is_locked = "Locked for importing AI"
                worker = Worker(import_ai_detections_to_objects, self.db.path, self.user, self.mapper,
                                path_to_proj_dir, progress_callback=True)
                worker.signals.result.connect(self.thread_output_ai)
                worker.signals.finished.connect(self.thread_complete_ai_import)
                worker.signals.progress.connect(self.progress_fn_ai)
                worker.signals.error.connect(self.thread_error)
                self.threadpool.start(worker)
                self.ai_time_processing = time.time()
                self.ui.ai_waiting_spinner.start()
            else:
                logger.warning(self.db_is_locked)

    def ai_change_active_all(self, activate: bool = False):
        if self.db is not None:
            if not self.db_is_locked:

                v = POPUPConfirm("Are you sure about that operation?")
                if v.exec():
                    self.db_is_locked = "Locked for change active Status of all Detections"
                    worker = Worker(change_active_all, self.db.path, activate)
                    worker.signals.finished.connect(self.thread_complete_ai_run)
                    worker.signals.error.connect(self.thread_error)
                    self.threadpool.start(worker)
                    self.ui.ai_waiting_spinner.start()
            else:
                logger.warning(self.db_is_locked)

    # --------------------------------------------------------------
    # LISTVIEW, TABLEVIEWS, FILTER
    # --------------------------------------------------------------

    def reload_database(self):
        if not self.db_is_locked:

            # clear all possible widgets and model
            self.clean_all_views_and_tables()

            # self reload config
            # Load the configured object types
            config = json.loads(self.db.load_config()['configuration'], object_pairs_hook=OrderedDict)

            self.popup_meta.configure(config)
            self.ui.environment_image.set_config(config['environment_data'])

            self.db = DBHandler.from_path(Path(self.db.path), self.user)

            images = self.db.load_images_list()
            if not images:
                return

            self.image_scene.db = self.db
            self.gis_scene.db = self.db
            self.ui.gallery_listview.set_db(self.db)
            self.ui.ai_listview.set_db(self.db)

            self.update_table_views(images)

            self.show_group_area_list()

            last_used_image = self.db.last_image
            if last_used_image:
                index = self.image_panel_model.match(self.image_panel_model.index(0, 0),
                                                     RolesImagePane.id, last_used_image, -1,
                                                     Qt.MatchFlag.MatchRecursive)[0]

                self.load_image(index, change_to_digitizer_page=False)

    def thread_finished_heavy_worker(self):
        self.db_is_locked = ''
        self.ui.waiting_spinner_main.stop()

    def thread_result_heavy_worker(self, return_object: object):

        union_area, img_gsd, gis_objects, node_list, gis_geom, self.color_dict_gis_objects = return_object

        # There have been cases where img_gsd became none because it was not set in DB and calculation crashed
        # because all GSD was 0.0 due to bug.
        # Just to be sure if that happens set to 0.0
        if img_gsd is None:
            img_gsd = 0.0

        if union_area is None:
            union_area = 0.0

        self.ui.prj_label_image_union_area.setText('%3.1e' % union_area + 'm²')
        self.ui.prj_label_image_gsd.setText('%2.1f' % (img_gsd * 100) + 'cm')

        for item in gis_objects:
            self.gis_scene.addItem(item)

        if node_list:
            self.gis_view.item_group_node = self.gis_scene.createItemGroup(node_list)

        for item in gis_geom:
            self.gis_scene.addItem(item)

        # Update coloring now
        self.gis_scene.color_images(attribute=self.gis_color_attribute_images,
                                    default_dict=self.color_scheme)

    def update_table_views(self, images: list = None, recalculate_area_gsd: bool = False):

        if images is None:
            images = self.db.load_images_list()

        if images is not None:

            img_georef = 0
            img_importer = []
            img_folder = []
            for rows in images:

                # the widgets and self.image_folder are cleared by clean_all_views_and_tables
                if Path(rows['path']).parent not in self.image_folders:
                    self.image_folders.append(Path(rows['path']).parent)
                    self.ui.ai_folder_chooser.addItem(Path(rows['path']).parent.as_posix())

                img_importer.append(rows['importer'])

                if rows['geom']:
                    img_georef += 1

            img_importer = len(set(img_importer))
            img_folder = len(set(img_folder))
            self.ui.prj_label_image_number.setText(str(len(images)))
            self.ui.gauge_images_georef.change_value(img_georef, len(images))
            self.ui.prj_label_image_folder.setText(str(img_folder))
            self.ui.prj_label_image_types.setText(str(img_importer))

            self.persistent_model_indexes_images = self.show_image_list(images)

            self.gis_scene.clear()
            self.gis_view.draw_map(path_to_data=path_to_shape)

            self.show_thumbnails()
            self.show_ai()
            self.update_info()

            # persistent_index_dict is a dictionary with path as posix and the
            # persistent model index from image pane model
            worker = Worker(worker_heavy_loading, images, self.db.path,
                            self.persistent_model_indexes_images,
                            recalculate_area_gsd, self.gis_color_attribute_objects, self.color_scheme)
            worker.signals.result.connect(self.thread_result_heavy_worker)
            worker.signals.finished.connect(self.thread_finished_heavy_worker)
            worker.signals.error.connect(self.thread_error)
            self.threadpool.start(worker)
            self.ui.waiting_spinner_main.start()

    def show_image_list(self, images) -> dict:
        self.image_panel_model, list_persistent_images = digitizer_image_panel_assign_model(images)

        self.ui.digitizer_image_panel.setModel(self.image_panel_model)
        self.ui.digitizer_image_panel.setColumnHidden(ImageList.path, True)
        self.ui.digitizer_image_panel.setColumnHidden(ImageList.active, True)
        self.ui.digitizer_image_panel.setColumnHidden(ImageList.path_exists, True)
        self.ui.digitizer_image_panel.setColumnWidth(0, 130)
        self.ui.digitizer_image_panel.setColumnWidth(1, 20)
        self.ui.digitizer_image_panel.setColumnWidth(2, 20)
        self.ui.digitizer_image_panel.setColumnWidth(3, 20)
        self.ui.digitizer_image_panel.setColumnWidth(4, 20)
        self.ui.digitizer_image_panel.setColumnWidth(5, 60)
        self.ui.digitizer_image_panel.setColumnWidth(6, 40)
        self.ui.digitizer_image_panel.setColumnWidth(7, 60)
        self.ui.digitizer_image_panel.setColumnWidth(8, 60)

        self.ui.gis_image_panel.setModel(self.image_panel_model)
        self.ui.gis_image_panel.setColumnHidden(ImageList.path, True)
        self.ui.gis_image_panel.setColumnHidden(ImageList.active, True)
        self.ui.gis_image_panel.setColumnHidden(ImageList.path_exists, True)
        self.ui.gis_image_panel.setColumnWidth(0, 130)
        self.ui.gis_image_panel.setColumnWidth(1, 20)
        self.ui.gis_image_panel.setColumnWidth(2, 20)
        self.ui.gis_image_panel.setColumnWidth(3, 20)
        self.ui.gis_image_panel.setColumnWidth(4, 20)
        self.ui.gis_image_panel.setColumnWidth(5, 60)
        self.ui.gis_image_panel.setColumnWidth(6, 40)
        self.ui.gis_image_panel.setColumnWidth(7, 60)
        self.ui.gis_image_panel.setColumnWidth(8, 60)

        delegate = IconCenterDelegate(self.ui.digitizer_image_panel)
        self.ui.digitizer_image_panel.setItemDelegateForColumn(4, delegate)
        self.ui.digitizer_image_panel.setItemDelegateForColumn(2, delegate)
        self.ui.gis_image_panel.setItemDelegateForColumn(4, delegate)
        self.ui.gis_image_panel.setItemDelegateForColumn(2, delegate)

        self.ui.digitizer_image_panel.horizontalScrollBar().setValue(0)
        self.ui.gis_image_panel.horizontalScrollBar().setValue(0)

        return list_persistent_images

    # --------------------------------------------------------------
    # CLEARING
    # --------------------------------------------------------------
    def clear_image_view_scene(self):
        self.image_view.nav_reset()
        self.nav_walk_modus(walk_modus=False)
        self.image_scene.clear()
        self.image_scene.working_instruction = False
        self.image_scene.image_id_db = None

    def clean_all_views_and_tables(self, close_db=False):
        self.image_scene.working_instruction = False
        self.ui.btn_create_rectangle.setIcon(QIcon(u":/icons/icons/rectangle.svg"))
        self.ui.btn_create_polygon.setIcon(QIcon(u":/icons/icons/polygon.svg"))
        self.ui.btn_create_point.setIcon(QIcon(u":/icons/icons/point.svg"))
        self.ui.btn_create_line.setIcon(QIcon(u":/icons/icons/linestring.svg"))

        self.set_instruction_selection(Selection.Rectangle)

        self.ui.gis_show_image_center_footprints.setChecked(True)
        self.ui.gis_hide_images.setChecked(True)
        self.ui.gis_hide_objects.setChecked(False)
        self.ui.gis_hide_image_centers.setChecked(False)

        self.gis_scene.show_footprints_on_hover(True)
        self.gis_scene.hide_images(True)

        self.ui.picking_hide.setChecked(False)
        self.ui.picking_hide_projections.setChecked(False)
        self.gis_scene.clear()
        self.gis_view.draw_map(path_to_data=path_to_shape)
        self.ui.gis_image_panel.setModel(None)
        self.ui.gis_group_area_panel.setModel(None)

        self.image_scene.clear()
        self.ui.dial_image_scale.setValue(1.0)
        self.image_view.nav_reset()
        self.ui.digitizer_image_panel.setModel(None)

        self.ui.ai_listview.setModel(None)
        self.ai_proxyModel.setSourceModel(None)
        if self.ai_model is not None:
            self.ai_model.deleteLater()
        self.ai_model = None

        self.ui.gallery_listview.setModel(None)

        self.ui.compare_tableView.setModel(None)
        self.ui.compare_thumbs1.setModel(None)
        self.ui.compare_thumbs2.setModel(None)
        self.image_folders: list[Path] = []
        self.image_panel_model = None
        self.thumbnail_model = None
        self.ui.ai_folder_chooser.clear()

        self.ui.prj_label_object_ai_import_nr.setText('0')
        self.ui.prj_label_object_manual_nr.setText('0')
        self.ui.prj_label_object_external_nr.setText('0')
        self.ui.prj_label_image_gsd.setText('0')
        self.ui.prj_label_image_union_area.setText('0')
        self.ui.prj_label_image_types.setText('0')
        self.ui.prj_label_image_folder.setText('0')
        self.ui.prj_label_image_number.setText('0')
        self.ui.prj_label_object_ai_detection_nr.setText('0')
        self.ui.prj_label_object_ai_processes.setText('0')

        self.ui.gauge_images_inspected.change_value(0, 0)
        self.ui.gauge_images_georef.change_value(0, 0)
        self.ui.gauge_ai_reviewed.change_value(0, 0)
        self.ui.gauge_ai_imported.change_value(0, 0)
        self.chart_obj_types.clear()

        self.ui.lbl_database_name.clear()
        self.ui.lbl_database_name.setStyleSheet('')

        self.popup_meta.configure(None)
        self.ui.environment_image.set_config(None)

        if close_db:
            if self.db is not None and not self.db_is_locked:
                self.db.close()
                self.db = None

    def clear_gallery_filter(self):

        self.gallery_filter = {}
        self.gallery_proxyModel.set_filter_data(self.gallery_filter)
        self.ui.gallery_filter_starred.setChecked(False)
        self.ui.gallery_filter_perspective_image.setChecked(False)
        self.ui.gallery_filter_ortho_image.setChecked(False)
        self.ui.gallery_filter_manual.setChecked(False)
        self.ui.gallery_filter_ai.setChecked(False)
        self.ui.gallery_filter_external.setChecked(False)
        self.ui.gallery_filter_group_area.clear()
        self.ui.gallery_filter_resight_set.clear()
        self.ui.gallery_filter_object.clear()
        self.ui.gallery_filter_deactivated.setChecked(False)
        self.ui.gallery_filter_activated.setChecked(False)
        self.ui.gallery_filter_reviewed.setChecked(False)

    def clear_ai_filter(self):
        self.ai_filter = {}
        self.ai_proxyModel.set_filter_data(self.ai_filter)
        self.ui.gallery_filter_external.setChecked(False)
        self.ui.ai_filter_ai_run.clear()
        self.ui.ai_filter_object.clear()
        self.ui.ai_filter_deactivated.setChecked(False)
        self.ui.ai_filter_activated.setChecked(False)
        self.ui.ai_filter_prob_lower.setChecked(False)
        self.ui.ai_filter_probability_slider.setValue(0)

    # --------------------------------------------------------------
    # LOAD IMAGE AND GEOMETRIES
    # --------------------------------------------------------------
    @Slot()
    def thread_image_loading_finished(self):
        """Function which will be called once the image loading is finished"""
        self.ui.waiting_spinner_main.stop()
        return

    @Slot(object)
    def thread_data_image(self, q_pixmap: QPixmap):
        """Pass image to image scene and set visual changes in lists and view
        :param q_pixmap: Pixmap with the image data"""

        self.ui.waiting_spinner_main.stop()

        if q_pixmap is None:
            logger.warning("Image could not be loaded")
            # set for self.image all indices and set the model to active
            self.current_index_persistent_index = None
            self.current_image_id = None
            return

        self.image_panel_model.setData(self.current_index_persistent_index, ImageList.active, True)

        # Load image class and geometries to be shown
        self.image = WISDAMImage.from_db(self.db.load_image(self.current_image_id), self.mapper)
        if self.image is None:
            return

        # Not sure why this is done, maybe in previous times image.shape had not always values?
        if not self.image.shape[0]:
            pixmap_size = q_pixmap.size()
            self.image.width = pixmap_size.width()
            self.image.height = pixmap_size.height()

        default_value = None
        if self.image_color_attribute_objects == 'image_id':
            default_value = self.current_image_id

        # Put image to Scene. Thread will be started for reading the image content
        # Once this is done all the navigation and stuff will be set in the thread result function
        self.image_scene.image_id_db = self.current_image_id

        self.image_scene.image_item = QGraphicsPixmapItem()
        self.image_scene.addItem(self.image_scene.image_item)
        self.image_scene.image_item.setPixmap(q_pixmap)
        self.image_scene.image_item.setCursor(QCursor(Qt.CursorShape.CrossCursor))

        # set the overview rectangle to the image size
        w, h = image_thumb_grid_navigation_size(self.image.shape)
        self.ui.rect_nav_overview.resize(w, h)

        self.image_scene.setSceneRect(self.image_scene.itemsBoundingRect())

        loader_image_geom(self.db, self.image_scene, self.image, point_size, self.image_color_attribute_objects,
                          default_dict=self.color_scheme, default_value=default_value)

        if self.image_view.grid_navigation:
            self.image_view.nav_scale(self.ui.dial_image_scale.value())
            self.image_view.nav_top_left()
            if self.ui.btn_walkmodus_alway_on.isChecked():
                self.nav_walk_modus(walk_modus=True)
        else:
            self.ui.dial_image_scale.setValue(1.0)
            self.image_view.fitInView(self.image_scene.itemsBoundingRect(), Qt.AspectRatioMode.KeepAspectRatio)
            self.image_view.centerOn(self.image_scene.image_item)

        if self.image.is_geo_referenced:
            # Center gis view on that image
            # TODO that should not be the image position also check other gis_view_centerON
            self.gis_view.centerOn(self.image.position_wgs84[0], -self.image.position_wgs84[1])

        self.image_panel_model.setData(self.current_index_persistent_index, ImageList.inspected, 1)

        # Set new image as inspected, maybe better if it was really loaded
        if not self.image.inspected:
            self.db.set_image_as_inspected(self.current_image_id)
            self.gis_scene.change_image_inspected([self.current_image_id])
            if self.ui.gis_color_image_inspected.isChecked():
                self.gis_scene.color_images(attribute='inspected', default_dict=self.color_scheme)
        # Set new image as current image in DB
        self.db.last_image = self.current_image_id

        self.ui.waiting_spinner_main.stop()

    def load_image(self, index: QModelIndex, propagate_environment=False, hard_propagate=False,
                   change_to_digitizer_page=True):
        """Load image and objects to image scene"""

        # Visible appearance of list to scroll to new image
        self.ui.digitizer_image_panel.scrollTo(index, hint=QAbstractItemView.ScrollHint.PositionAtCenter)
        self.ui.gis_image_panel.scrollTo(index, hint=QAbstractItemView.ScrollHint.PositionAtCenter)
        item = self.image_panel_model.get_item(index)
        if item.child_count() > 0:
            return
        # If the meta popup is open for some reason, close it now
        if self.popup_meta.isEnabled():
            self.popup_meta.close()

        # reset some states of digitizer page
        self.ui.picking_hide_projections.setChecked(False)
        self.ui.picking_hide.setChecked(False)
        self.image_scene.working_instruction = False

        # set current image to not active color
        if self.current_index_persistent_index is not None:
            self.image_panel_model.setData(self.current_index_persistent_index, ImageList.active, False)
        self.clear_image_view_scene()

        # Image loading and passing to scene
        # Test if image actually exists
        if Path(item.data(ImageList.path)).exists():

            # set for self.image all indices and set the model to active
            self.current_index_persistent_index = QPersistentModelIndex(index)
            self.current_image_id = item.data(ImageList.id)
            path = Path(item.data(ImageList.path))

            # Todo: Better to use rasterio to load ortho-photos?

            if item.data(ImageList.importers) == 'Orthoimagery using Rasterio':
                worker = Worker(image_loader_rasterio, path)
            else:
                worker = Worker(image_loader, path)

            worker.signals.finished.connect(self.thread_image_loading_finished)
            worker.signals.result.connect(self.thread_data_image)
            worker.signals.error.connect(self.thread_error)
            self.threadpool.start(worker)

            self.ui.waiting_spinner_main.start()

        else:
            # Image does not exist - Path is not valid
            # Clear digitizer screen, reset navigation in view
            logger.warning('Images does not exist: ' + Path(item.data(ImageList.path)).name +
                           '\nPlease use "Change PATHS" to locate these images')
            self.image = None
            return

        if change_to_digitizer_page:
            self.menu_set("OBJECT Digitiser")

        # Environmental data of image
        # The propagation of env variables will also be done if image could not be loaded
        # That propagation is still be set if image will be available again

        if self.current_image_id is not None:

            if hard_propagate:
                if self.data_environment is not None:
                    self.data_environment = propagate_env_data_next_image(self.data_environment)

                    self.db.store_image_environment_data(self.data_environment, self.current_image_id)
                    self.ui.environment_image.data = self.data_environment

            # Get environmental data if present in image Database
            env_data = self.db.load_image_environment_data(self.current_image_id)

            # If present set the environment data already as this is the section without hard propagation
            if env_data:
                self.data_environment = env_data
                self.ui.environment_image.data = self.data_environment

            else:
                if propagate_environment:

                    # Propagation is only possible if the current image's env is not already set
                    if self.data_environment:
                        self.data_environment = propagate_env_data_next_image(self.data_environment)

                        self.db.store_image_environment_data(self.data_environment, self.current_image_id)
                        self.ui.environment_image.data = self.data_environment
                else:
                    self.data_environment = None
                    self.ui.environment_image.data = self.data_environment

    # --------------------------------------------------------------
    # GIS page functions
    # --------------------------------------------------------------
    def gis_image_list_double_click(self, index):
        item = self.image_panel_model.get_item(index)
        if item.child_count():
            return
        center = self.db.load_image_center(item.data(ImageList.id))
        if center:
            if self.gis_view.transform().m11() < 100000:
                self.gis_view.setTransform(QTransform(100000, 0.0, 0.0, 0.0, 100000, 0.0, 0.0, 0.0, 1.0))
            self.gis_view.centerOn(center[0], -center[1])
            self.ui.gis_view.scene().clearSelection()

    def group_area_distance_changed(self):
        self.ui.gis_btn_calc_group_area.setText("Calculate %i m" % self.ui.gis_slider_area_distance.value())

    def gis_group_area_double_click(self, index):
        center = index.model().index(index.row(), GroupAreaList.position).data()
        if center:
            if self.gis_view.transform().m11() < 100000:
                self.gis_view.setTransform(QTransform(100000, 0.0, 0.0, 0.0, 100000, 0.0, 0.0, 0.0, 1.0))
            self.gis_view.centerOn(center[0], -center[1])
            self.ui.gis_view.scene().clearSelection()

    @Slot(object)
    def thread_complete_group_area_load_geom(self, result: object):

        # In the thread complete group area run we clear all objects from the GIS scene and add them new
        geom_items, self.color_dict_gis_objects = result
        for item in geom_items:
            self.gis_scene.addItem(item)

        self.show_group_area_list()
        self.show_thumbnails()
        self.db_is_locked = ''
        self.ui.gis_group_waiting_spinner.stop()

    @Slot()
    def thread_complete_group_area_run(self):
        # self.db.load(self.db.path)

        self.gis_scene.clear_objects()

        worker = Worker(loader_gis_geom_objects, self.db.path, self.gis_color_attribute_objects, self.color_scheme)
        worker.signals.result.connect(self.thread_complete_group_area_load_geom)
        worker.signals.error.connect(self.thread_error)

        self.threadpool.start(worker)

    def run_group_area(self):
        if self.db is not None:
            if not self.db_is_locked:
                self.db_is_locked = 'Database locked for creating area groups'
                worker = Worker(group_area_multiprocess_start, self.db.path, self.ui.gis_slider_area_distance.value())
                worker.signals.finished.connect(self.thread_complete_group_area_run)
                worker.signals.result.connect(self.thread_output)
                worker.signals.error.connect(self.thread_error)

                self.threadpool.start(worker)
                self.ui.gis_group_waiting_spinner.start()
            else:
                logger.warning(self.db_is_locked)

    def show_group_area_list(self):
        self.group_area_model = loader_group_area(self.db)
        if self.group_area_model:
            self.ui.gis_group_area_panel.setModel(self.group_area_model)
        self.ui.gis_group_area_panel.setColumnHidden(GroupAreaList.position, True)

    def gis_change_image_colors(self, attribute: str | None = None, default_value=None):
        if attribute is not None:
            self.gis_color_attribute_images = attribute
        self.gis_scene.color_images(self.gis_color_attribute_images,
                                    default_value=default_value,
                                    default_dict=self.color_scheme)

    def gis_change_object_colors(self, attribute: str | None = None):

        if attribute is not None:
            self.gis_color_attribute_objects = attribute
        self.color_dict_gis_objects = self.gis_scene.color_objects(self.gis_color_attribute_objects,
                                                                   default_dict=self.color_scheme)

    # --------------------------------------------------------------
    # COMPARE page functions
    # --------------------------------------------------------------
    def compare_load(self):
        self.ui.compare_tableView.setModel(None)
        self.ui.compare_thumbs1.setModel(None)
        self.ui.compare_thumbs2.setModel(None)
        cmp_load_path, _ = QFileDialog.getOpenFileName(self, caption="Load Comparison",
                                                       dir='.', filter='Json Files (*.json)')
        if cmp_load_path:

            try:
                fid = open(cmp_load_path, 'rb')
                stored_data = json.load(fid)
                fid.close()
            except json.decoder.JSONDecodeError:
                self.ui.compare_label_info.setText('File seems not working')
                return

            try:
                model_data = stored_data[0]
                self.compare1.db = Path(stored_data[1])
                self.compare1.ai = stored_data[2]
                self.compare2.db = Path(stored_data[3])
                self.compare2.ai = stored_data[4]
            except IndexError:
                self.ui.compare_label_info.setText('File seems not working')
                return

            if model_data:
                self.cmp_model = CompareListModel(model_data, compare_list_header)
                self.ui.compare_label_info.setText('Results loaded: ' + str(len(model_data)))
                self.cmp_view_model()
            else:
                self.ui.compare_label_info.setText('File seems empty')
                return

        else:
            self.ui.compare_label_info.setText('No file chosen')
            return

    def compare_save(self):

        if self.ui.compare_tableView.model() is not None:

            cmp_store_path, _ = QFileDialog.getSaveFileName(self, caption="Save Compare as JSON",
                                                            dir='.', filter='Json Files (*.json)')

            if cmp_store_path:

                if self.cmp_model:
                    fid = open(cmp_store_path, 'w')
                    stored_data = [self.cmp_model.get_data(), self.compare1.db.as_posix(), self.compare1.ai,
                                   self.compare2.db.as_posix(), self.compare2.ai]
                    json.dump(stored_data, fid, indent=1)
                    fid.close()
            else:
                self.ui.compare_label_info.setText('No file chosen')
                return
        else:
            self.ui.compare_label_info.setText('No comparison present')
            return

    def compare_run(self):

        self.ui.compare_tableView.setModel(None)
        self.ui.compare_thumbs1.setModel(None)
        self.ui.compare_thumbs2.setModel(None)
        compare_modus = self.ui.compare_modus_combobox.currentText()

        compare_individuals = self.ui.compare_individual_check.isChecked()

        if "1)" in compare_modus:
            if self.db is not None:
                source_list1 = [0, 2]
                source_list2 = [1]
                self.compare1 = CompareType(ai=False, path=self.db.path)
                self.compare2 = CompareType(ai=False, path=self.db.path)

                self.cmp_model, output = compare_searcher(self.compare1.db,
                                                          self.compare2.db, self.user, source1=source_list1,
                                                          source2=source_list2, non_grouping=compare_individuals)
                if not self.cmp_model:
                    self.ui.compare_label_info.setText('Seems no data is present')
                    return
                self.ui.compare_label_info.setText('Matching loaded')

            else:
                self.ui.compare_label_info.setText('For this modus database must be loaded')
                return

        elif "2)" in compare_modus:
            if self.db is not None:

                self.compare1 = CompareType(ai=True, path=self.db.path)
                self.compare2 = CompareType(ai=True, path=self.db.path)

                self.cmp_model, output = compare_searcher_single_db_ai_to_ai_review(self.db)
                if not self.cmp_model:
                    self.ui.compare_label_info.setText('Seems not Data is present')
                    return
                self.ui.compare_label_info.setText(output)
            else:
                self.ui.compare_label_info.setText('For this mode Database must be loaded')
                return
        else:
            self.ui.compare_tableView.setModel(None)
            db_path, _ = QFileDialog.getOpenFileName(self, caption="Load Database 1",
                                                     dir='.', filter='SQLITE Files (*.sqlite)')
            if db_path:
                self.compare1 = CompareType(ai=False, path=Path(db_path))
            else:
                self.ui.compare_label_info.setText('No Database chosen')
                return

            db_path2, _ = QFileDialog.getOpenFileName(self, caption="Load Database 2",
                                                      dir=db_path, filter='SQLITE Files (*.sqlite)')

            if db_path2:
                self.compare2 = CompareType(ai=False, path=Path(db_path2))
            else:
                self.ui.compare_label_info.setText('No Database chosen')
                return

            self.ui.compare_label_info.setText('Matching loaded')

            if "4)" in compare_modus:
                source_list = [0, 1, 2]
            elif "3)" in compare_modus:
                source_list = [0, 2]
            else:
                source_list = []
            self.cmp_model, text = compare_searcher(self.compare1.db,
                                                    self.compare2.db, self.user, source1=source_list,
                                                    source2=source_list, non_grouping=compare_individuals)

        self.cmp_view_model()

    def cmp_view_model(self):
        self.ui.compare_tableView.setModel(self.cmp_model)
        self.ui.compare_tableView.setColumnHidden(CompareList.db, True)
        self.ui.compare_tableView.setColumnHidden(CompareList.c1_ids, True)
        self.ui.compare_tableView.setColumnHidden(CompareList.c2_ids, True)
        self.ui.compare_tableView.setColumnHidden(CompareList.flag_valid, True)
        self.ui.compare_tableView.setColumnHidden(CompareList.type_other, True)
        self.ui.compare_tableView.setColumnHidden(CompareList.c1_valid, True)
        self.ui.compare_tableView.setColumnHidden(CompareList.c2_valid, True)
        self.ui.compare_tableView.setColumnHidden(CompareList.c1_group, True)
        self.ui.compare_tableView.setColumnHidden(CompareList.c2_group, True)
        self.ui.compare_tableView.setColumnHidden(CompareList.c1_image, True)
        self.ui.compare_tableView.setColumnHidden(CompareList.c2_image, True)
        self.ui.compare_tableView.setColumnHidden(CompareList.c1_data, True)
        self.ui.compare_tableView.setColumnHidden(CompareList.c2_data, True)
        self.ui.compare_tableView.setColumnHidden(CompareList.c2_data_env, True)
        self.ui.compare_tableView.setColumnHidden(CompareList.c1_data_env, True)
        self.ui.compare_tableView.setColumnWidth(CompareList.type, 120)
        self.ui.compare_tableView.setColumnWidth(CompareList.id, 70)
        self.ui.compare_tableView.setColumnWidth(CompareList.groups_involved, 60)
        self.ui.compare_tableView.setColumnWidth(CompareList.nrs_db1, 80)
        self.ui.compare_tableView.setColumnWidth(CompareList.nrs_db2, 80)
        self.ui.compare_tableView.setColumnWidth(CompareList.db, 20)
        self.ui.compare_tableView.setColumnWidth(CompareList.seen, 40)
        delegate = CompareIconCenterDelegate(self.ui.compare_tableView)
        self.ui.compare_tableView.setItemDelegateForColumn(CompareList.seen, delegate)
        self.ui.compare_tableView.setItemDelegateForColumn(CompareList.nrs_db1, delegate)
        self.ui.compare_tableView.setItemDelegateForColumn(CompareList.nrs_db2, delegate)

    def compare_icon_lists_icon_size(self):
        thumb_size_user = GalleryIconSize()
        thumb_size_user.width = self.ui.compare_slider_size.value()
        thumb_size_user.height = thumb_size_user.width
        self.ui.compare_thumbs1.setItemDelegate(CompareIconDelegate(thumb_size=thumb_size_user))
        self.ui.compare_thumbs2.setItemDelegate(CompareIconDelegate(thumb_size=thumb_size_user))

    def compare_merge(self):
        """Merge rows of the compare table"""

        if self.cmp_model is None:
            return

        if len(self.ui.compare_tableView.selectionModel().selectedRows()) < 2:
            logger.warning("Can not merge if not multiple rows selected")
            return

        # Rows selected by the user
        rows_index = self.ui.compare_tableView.selectionModel().selectedRows()

        rows = [QPersistentModelIndex(x) for x in rows_index]

        # Data of all rows will be merged to the updated data (e.g. first selected index)
        first_index = rows[0]
        cmo_model_data = self.cmp_model.get_data()

        updated_data = copy.deepcopy(cmo_model_data[rows[0].row()])

        # ids of objects of the first row selected
        orig_c1_ids = first_index.data(RolesComparePane.c1_ids)
        orig_c2_ids = first_index.data(RolesComparePane.c2_ids)

        # check if a group is involved in the rows to be merged
        flag_group_found = updated_data[CompareList.groups_involved]

        for row_index in rows[1:]:
            data = cmo_model_data[row_index.row()]

            # check if a group is involved in the rows to be merged
            if data[CompareList.groups_involved] == 'yes':
                flag_group_found = data[CompareList.groups_involved]

            # append data for all rows selected to updated_data
            for idx, elements in enumerate(data):
                updated_data[idx] += elements

        updated_data[CompareList.groups_involved] = flag_group_found

        # reset the newest data row
        updated_data[CompareList.seen] = 0
        updated_data[CompareList.flag_valid] = 0

        if len(updated_data[CompareList.c1_ids]) > 0:
            updated_data[CompareList.db] = 1
            updated_data[CompareList.id] = updated_data[CompareList.c1_ids][0]
        else:
            updated_data[CompareList.db] = 2
            updated_data[CompareList.id] = updated_data[CompareList.c2_ids][0]

        updated_data[CompareList.nrs_db1] = len(updated_data[CompareList.c1_ids])
        updated_data[CompareList.nrs_db2] = len(updated_data[CompareList.c2_ids])

        # First remove the rows which have been merged into first row selected
        # ID can not be used because first and second data to compare can have the same id
        # Grab the c1 and c2 ids to use for search before deleting row
        c_ids = []
        for row in rows[1:]:
            c_ids.append([row.data(RolesComparePane.c1_ids), row.data(RolesComparePane.c2_ids)])
        for row in c_ids:
            if row[0]:
                index_delete = self.cmp_model.match(self.cmp_model.index(0, 0),
                                                    RolesComparePane.c1_ids,
                                                    row[0], hits=-1,
                                                    flags=Qt.MatchFlag.MatchExactly)
            else:
                index_delete = self.cmp_model.match(self.cmp_model.index(0, 0),
                                                    RolesComparePane.c2_ids,
                                                    row[1], hits=-1,
                                                    flags=Qt.MatchFlag.MatchExactly)

            # remove the row
            self.cmp_model.removeRows(index_delete[0].row(), 1, index_delete[0])

        # Now get the index of the first row: Could also first_index be used?
        if orig_c1_ids:
            index_first = self.cmp_model.match(self.cmp_model.index(0, 0),
                                               RolesComparePane.c1_ids, orig_c1_ids, hits=-1,
                                               flags=Qt.MatchFlag.MatchExactly)
        else:
            index_first = self.cmp_model.match(self.cmp_model.index(0, 0),
                                               RolesComparePane.c2_ids, orig_c2_ids, hits=-1,
                                               flags=Qt.MatchFlag.MatchExactly)

        self.cmp_model.change_row(index_first[0], updated_data)
        self.compare_page_load_images(index_first[0])
        self.ui.compare_tableView.selectRow(index_first[0].row())

    def compare_split(self):

        if self.cmp_model is None:
            return

        obj_count = 0
        obj_count_2 = 0
        model_thumbs_1 = self.ui.compare_thumbs1.model()
        model_thumbs_2 = self.ui.compare_thumbs2.model()

        if model_thumbs_1 is None and model_thumbs_2 is None:
            return

        index = QModelIndex()
        if model_thumbs_1 is not None:
            index = model_thumbs_1.row(0).index
            obj_count = model_thumbs_1.rowCount()
        if model_thumbs_2 is not None:
            index = model_thumbs_2.row(0).index
            obj_count_2 = model_thumbs_2.rowCount()

        if obj_count + obj_count_2 < 2:
            return

        if index.isValid():

            # get the valid ids of all elements
            valids_c1 = index.data(RolesComparePane.c1_valid)
            valids_c2 = index.data(RolesComparePane.c2_valid)

            data_row = self.cmp_model.get_data()[index.row()]

            # if one of the elements has -1 than we split it under certain conditions
            if -1 in valids_c1 or -1 in valids_c2:

                old_c1 = [i for i, j in enumerate(valids_c1) if j > -1]
                old_c2 = [i for i, j in enumerate(valids_c2) if j > -1]
                new_c1 = [i for i, j in enumerate(valids_c1) if j == -1]
                new_c2 = [i for i, j in enumerate(valids_c2) if j == -1]

                new_c1_group = [data_row[CompareList.c1_group][i] for i in new_c1]
                new_c2_group = [data_row[CompareList.c2_group][i] for i in new_c2]

                if len(set(new_c1_group)) > 1 or len(set(new_c2_group)) > 1:
                    logger.warning(
                        "Can not split if:\n"
                        "either db1 or db2 more groups are selected or single and group is selected")
                    return

                # check if all items of group are selected
                items_with_selected_group_c1 = [i for i in new_c1_group if i > 0]
                items_with_selected_group_c2 = [i for i in new_c2_group if i > 0]

                len_item_with_group = len(
                    [i for i in data_row[CompareList.c1_group] if i in items_with_selected_group_c1])
                if len(new_c1) != len_item_with_group and len(items_with_selected_group_c1) > 0:
                    logger.warning("Splitting only if all items of group are selected")
                    return

                len_item_with_group = len(
                    [i for i in data_row[CompareList.c2_group] if i in items_with_selected_group_c2])
                if len(new_c2) != len_item_with_group and len(items_with_selected_group_c2) > 0:
                    logger.warning("Splitting only if all items of group are selected")
                    return

                flag_group_found = 'yes' if (len(set([data_row[CompareList.c1_group][i] for i in new_c1])) > 1) or (
                        len(set([data_row[CompareList.c2_group][i] for i in new_c2])) > 1) else 'no'

                if len(new_c1) > 0:
                    db_used = 1
                    id_new = [data_row[CompareList.c1_ids][i] for i in new_c1]
                    nr_source = len(new_c1)
                    nr_compare = len(new_c2)
                else:
                    db_used = 2
                    id_new = [data_row[CompareList.c2_ids][i] for i in new_c2]
                    nr_source = len(new_c1)
                    nr_compare = len(new_c2)

                new_data = [id_new[0],
                            [data_row[1][i] for i in new_c1],
                            db_used,
                            0,  # set seen to 0
                            nr_source,
                            nr_compare,
                            flag_group_found,
                            [data_row[7][i] for i in new_c1],
                            [data_row[8][i] for i in new_c2],
                            0,  # flag valid
                            [data_row[10][i] for i in new_c2],
                            [1 for _ in new_c1],  # valids of c1
                            [1 for _ in new_c2],  # valids of c2
                            [data_row[13][i] for i in new_c1],
                            [data_row[14][i] for i in new_c2],
                            [data_row[15][i] for i in new_c1],
                            [data_row[16][i] for i in new_c2],
                            [data_row[17][i] for i in new_c1],
                            [data_row[18][i] for i in new_c2],
                            [data_row[CompareList.c1_data_env][i] for i in new_c1],
                            [data_row[CompareList.c2_data_env][i] for i in new_c2]]

                flag_group_found = 'yes' if (len(set([data_row[CompareList.c1_group][i] for i in old_c1])) > 1) or (
                        len(set([data_row[CompareList.c2_group][i] for i in old_c2])) > 1) else 'no'

                if len(old_c1) > 0:
                    db_used = 1
                    id_new = [data_row[CompareList.c1_ids][i] for i in old_c1]
                    nr_source = len(old_c1)
                    nr_compare = len(old_c2)
                else:
                    db_used = 2
                    id_new = [data_row[CompareList.c2_ids][i] for i in old_c2]
                    nr_source = len(old_c1)
                    nr_compare = len(old_c2)

                updated_data = [id_new[0],
                                [data_row[1][i] for i in old_c1],
                                db_used,
                                0,  # set seen to 0
                                nr_source,
                                nr_compare,
                                flag_group_found,
                                [data_row[7][i] for i in old_c1],
                                [data_row[8][i] for i in old_c2],
                                0,  # flag valid
                                [data_row[10][i] for i in old_c2],
                                [data_row[11][i] for i in old_c1],
                                [data_row[12][i] for i in old_c2],
                                [data_row[13][i] for i in old_c1],
                                [data_row[14][i] for i in old_c2],
                                [data_row[15][i] for i in old_c1],
                                [data_row[16][i] for i in old_c2],
                                [data_row[17][i] for i in old_c1],
                                [data_row[18][i] for i in old_c2],
                                [data_row[CompareList.c1_data_env][i] for i in old_c1],
                                [data_row[CompareList.c2_data_env][i] for i in old_c2]]

                self.cmp_model.change_row(index, updated_data)

                self.cmp_model.append_data(new_data)

                self.compare_page_load_images(index)

    def compare_accept(self):
        index = self.ui.compare_tableView.currentIndex()
        if index.isValid():
            self.cmp_model.change_value(self.cmp_model.index(index.row(), CompareList.seen), 1)
            self.cmp_model.change_value(self.cmp_model.index(index.row(), CompareList.flag_valid), 1)
            next_index = self.cmp_model.index(index.row() + 1, 0)
            if next_index.isValid():
                self.ui.compare_tableView.scrollTo(next_index)
                self.ui.compare_tableView.setCurrentIndex(next_index)
                self.compare_page_load_images(next_index)

    def compare_reject(self):
        index = self.ui.compare_tableView.currentIndex()
        if index.isValid():
            self.cmp_model.change_value(self.cmp_model.index(index.row(), CompareList.seen), 1)
            self.cmp_model.change_value(self.cmp_model.index(index.row(), CompareList.flag_valid), 0)
            next_index = self.cmp_model.index(index.row() + 1, 0)
            if next_index.isValid():
                self.ui.compare_tableView.scrollTo(next_index)
                self.ui.compare_tableView.setCurrentIndex(next_index)
                self.compare_page_load_images(next_index)

    def compare_export(self):

        if self.cmp_model is not None:

            cmp_store_path, _ = QFileDialog.getSaveFileName(self, caption="Save Compare as CSV",
                                                            dir='.', filter='Comma Separated  (*.CSV)')

            if not cmp_store_path:
                self.ui.compare_label_info.setText('No filename specified')
                return

            db1 = self.compare1.db.as_posix()
            db2 = self.compare2.db.as_posix()
            data = self.cmp_model.get_data()
            compare_export(Path(cmp_store_path), db1, db2, data)
            logger.info('Comparison exported to: ' + cmp_store_path, extra={"finished": True})

    @Slot(object, int, int)
    def cmp_table_row_change_valid_cs1(self, persistent_index: QPersistentModelIndex, id_obj, valid):
        self.cmp_model.change_valid(persistent_index, id_obj, valid, compare_source=0)

    @Slot(object)
    def cmp_table_row_all_no_cs1(self, persistent_index: QPersistentModelIndex):
        self.cmp_model.set_all_no_valid(persistent_index, compare_source=0)

    @Slot(object, int, int)
    def cmp_table_row_change_valid_cs2(self, persistent_index: QPersistentModelIndex, id_obj, valid):
        self.cmp_model.change_valid(persistent_index, id_obj, valid, compare_source=1)

    @Slot(object)
    def cmp_table_row_all_no_cs2(self, persistent_index: QPersistentModelIndex):
        self.cmp_model.set_all_no_valid(persistent_index, compare_source=1)

    def compare_page_load_images(self, index):

        cs1_ids = index.data(RolesComparePane.c1_ids)
        cs2_ids = index.data(RolesComparePane.c2_ids)
        cs1_valids = index.data(RolesComparePane.c1_valid)
        cs2_valids = index.data(RolesComparePane.c2_valid)

        thumb_size_user = GalleryIconSize()
        thumb_size_user.width = self.ui.compare_slider_size.value()
        thumb_size_user.height = thumb_size_user.width

        persistent_index = QPersistentModelIndex(index)

        if cs1_ids:
            cs1_model = compare_image_loader(self.compare1.db, index=persistent_index,
                                             ids=cs1_ids, valids=cs1_valids,
                                             table_ai=self.compare1.ai)
            self.ui.compare_thumbs1.setModel(cs1_model)
            self.ui.compare_thumbs1.setItemDelegate(CompareIconDelegate(thumb_size=thumb_size_user))
        else:
            self.ui.compare_thumbs1.setModel(None)
        if cs2_ids:
            cs2_model = compare_image_loader(self.compare2.db, index=persistent_index,
                                             ids=cs2_ids, valids=cs2_valids,
                                             table_ai=self.compare2.ai)
            self.ui.compare_thumbs2.setModel(cs2_model)
            self.ui.compare_thumbs2.setItemDelegate(CompareIconDelegate(thumb_size=thumb_size_user))
        else:
            self.ui.compare_thumbs2.setModel(None)

    # --------------------------------------------------------------
    # Digitizing PAGE
    # --------------------------------------------------------------
    def nav_walk_modus(self, walk_modus: bool = False):

        self.image_view.set_nav_walk(walk_modus)
        if self.image_view.nav_walk:
            self.ui.btn_navigation_startwalk.setText('STOP WALK')
            self.ui.label_walk_modus.setHidden(False)
            select = self.ui.btn_navigation_startwalk.styleSheet().replace("background-color: rgb(72, 100, 92);",
                                                                           "background-color: rgb(100, 72, 92);")
            self.ui.btn_navigation_startwalk.setStyleSheet(select)
            self.ui.btn_navigation_d.setHidden(True)
            self.ui.btn_navigation_u.setHidden(True)

            self.ui.label_walk_modus.setText('WALK MODE ON')

        else:
            self.ui.btn_navigation_startwalk.setText('START WALK')
            self.ui.label_walk_modus.setHidden(True)
            self.ui.btn_navigation_d.setHidden(False)
            self.ui.btn_navigation_u.setHidden(False)
            self.image_view.nav_walk_flag_direction = False
            select = self.ui.btn_navigation_startwalk.styleSheet().replace("background-color: rgb(100, 72, 92);",
                                                                           "background-color: rgb(72, 100, 92);")
            self.ui.btn_navigation_startwalk.setStyleSheet(select)

    def set_navigation_mode(self, grid_navigation: bool = False):

        self.image_view.grid_navigation = grid_navigation
        self.image_view.set_navigation_mode(grid_navigation)
        if self.image_view.grid_navigation:
            self.ui.stack_navigation.setCurrentWidget(self.ui.nav_page_grid)
            self.nav_walk_modus(walk_modus=False)
        else:
            self.ui.stack_navigation.setCurrentWidget(self.ui.nav_page_free)
            self.nav_walk_modus(walk_modus=False)

    @Slot(tuple)
    def set_rect(self, param: tuple):

        img_width, img_height, view_rect_width, view_rect_height, px, py = param
        scale_w = self.ui.rect_nav_overview.width() / img_width
        scale_h = self.ui.rect_nav_overview.height() / img_height
        w = int(scale_w * view_rect_width)
        h = int(scale_h * view_rect_height) + 1
        x = int(scale_w * px - w / 2.0)
        y = int(scale_h * py - h / 2.0)

        self.ui.rect_nav_grid.setGeometry(QRect(x, y, w, h))

    @Slot(str)
    def set_walk_label(self, text: str):

        self.ui.label_walk_modus.setText(text)

    @Slot(object)
    def set_environment(self, env_dict):
        if self.current_image_id > -1:
            self.data_environment = env_dict
            self.db.store_image_environment_data(env_dict, self.current_image_id)

    def set_instruction_selection(self, selection: Selection):

        self.ui.btn_selection_rectangle.setIcon(QIcon(u":/icons/icons/rectangle.svg"))
        self.ui.btn_selection_lasso.setIcon(QIcon(u":/icons/icons/lasso.svg"))

        if selection == Selection.Rectangle:
            self.gis_scene.set_selection_mode(Selection.Rectangle)
            self.ui.btn_selection_rectangle.setIcon(QIcon(u":/icons/icons/rectangle_active_selection.svg"))
        elif selection == Selection.Lasso:
            self.gis_scene.set_selection_mode(Selection.Lasso)
            self.ui.btn_selection_lasso.setIcon(QIcon(u":/icons/icons/lasso_active_selection.svg"))
        else:
            self.gis_scene.set_selection_mode(Selection.Rectangle)
            self.ui.btn_selection_rectangle.setIcon(QIcon(u":/icons/icons/rectangle_active_selection.svg"))

    def set_instruction(self, action: Instructions):

        if not self.image_scene.working_instruction:
            self.ui.btn_create_rectangle.setIcon(QIcon(u":/icons/icons/rectangle.svg"))
            self.ui.btn_create_polygon.setIcon(QIcon(u":/icons/icons/polygon.svg"))
            self.ui.btn_create_point.setIcon(QIcon(u":/icons/icons/point.svg"))
            self.ui.btn_create_line.setIcon(QIcon(u":/icons/icons/linestring.svg"))
            # self.ui.btn_geometry_move.setIcon(QtGui.QIcon(u":/icons/icons/move.svg"))
            # self.ui.btn_geometry_resize.setIcon(QtGui.QIcon(u":/icons/icons/resize.svg"))

            if self.image_scene.current_instruction == action:
                self.image_scene.current_instruction = Instructions.No_Instruction
                return

            if action == Instructions.Rectangle_Instruction:
                self.image_scene.current_instruction = Instructions.Rectangle_Instruction
                self.ui.btn_create_rectangle.setIcon(QIcon(u":/icons/icons/rectangle_active.svg"))
            elif action == Instructions.Polygon_Instruction:
                self.image_scene.current_instruction = Instructions.Polygon_Instruction
                self.ui.btn_create_polygon.setIcon(QIcon(u":/icons/icons/polygon_active.svg"))
            elif action == Instructions.Point_Instruction:
                self.image_scene.current_instruction = Instructions.Point_Instruction
                self.ui.btn_create_point.setIcon(QIcon(u":/icons/icons/point_active.svg"))
            elif action == Instructions.LineString_Instruction:
                self.image_scene.current_instruction = Instructions.LineString_Instruction
                self.ui.btn_create_line.setIcon(QIcon(u":/icons/icons/linestring_active.svg"))

            # elif action == 'move_geometry':
            #    self.m_scene2.current_instruction = Instructions.Move_Instruction
            #    self.ui.btn_geometry_move.setIcon(QtGui.QIcon(u":/icons/icons/move_active.svg"))
            # elif action == 'change_geometry':
            #    self.m_scene2.current_instruction = Instructions.Change_Instruction
            #    self.ui.btn_geometry_resize.setIcon(QtGui.QIcon(u":/icons/icons/resize_active.svg"))

    def digitizer_change_object_colors(self, attribute: str | None = None, default_value=None):
        if attribute is not None:
            self.image_color_attribute_objects = attribute

        if self.image_color_attribute_objects == 'image_id':
            default_value = self.current_image_id
        self.image_scene.color_objects(self.image_color_attribute_objects,
                                       default_value=default_value,
                                       default_dict=self.color_scheme)

    def pick_hide_projections(self):
        scene_items = self.image_scene.items()
        if scene_items:
            for obj in scene_items:
                if hasattr(obj, 'projection'):
                    if obj.projection:
                        obj.setVisible(not obj.isVisible())

    def pick_hide(self):
        scene_items = self.image_scene.items()
        if scene_items:
            for obj in scene_items:
                if hasattr(obj, 'projection'):
                    if not obj.projection:
                        if self.ui.picking_hide.isChecked():
                            obj.setVisible(False)
                        else:
                            obj.setVisible(True)

    # --------------------------------------------------------------
    # Project page
    # --------------------------------------------------------------
    # def led_docker_check(self):
    #    change_led_color(self.ui.led_docker_service, on=docker_running())

    def update_info(self):

        change_led_color(self.ui.led_elevation_service, on=self.mapper is not None)
        # It is called each time we change to the project page. Thus, the GUI could freeze
        # Tested with 7k images 6k objects and takes like 0.03 seconds
        if self.db is not None:

            if self.image_panel_model is not None:
                img_missing = self.image_panel_model.nr_images_missing()
                img_nr = self.image_panel_model.image_count()
                img_inspected = self.image_panel_model.nr_images_inspected()

                self.ui.gauge_images_inspected.change_value(img_inspected, img_nr)
                change_led_color(self.ui.led_image_path, on=not img_missing)

            if self.thumbnail_model is not None:
                nr_objects = len(self.thumbnail_model.get_data())
                obj_source = dict(Counter(sub.source for sub in self.thumbnail_model.get_data()))
                if ObjectSourceList.manual in obj_source:
                    self.ui.prj_label_object_manual_nr.setText(str(obj_source[ObjectSourceList.manual]))
                else:
                    self.ui.prj_label_object_manual_nr.setText('0')

                if ObjectSourceList.ai in obj_source:
                    self.ui.prj_label_object_ai_import_nr.setText(str(obj_source[ObjectSourceList.ai]))
                else:
                    self.ui.prj_label_object_ai_import_nr.setText('0')

                if ObjectSourceList.external in obj_source:
                    self.ui.prj_label_object_external_nr.setText(str(obj_source[ObjectSourceList.external]))
                else:
                    self.ui.prj_label_object_external_nr.setText('0')

                reviewed = len([1 for sub in self.thumbnail_model.get_data() if
                                sub.source == ObjectSourceList.ai and sub.reviewed])
                ai_objects = len([1 for sub in self.thumbnail_model.get_data() if sub.source == ObjectSourceList.ai])
                self.ui.gauge_ai_reviewed.change_value(reviewed, ai_objects)

                obj_types = dict(Counter(sub.object_type for sub in self.thumbnail_model.get_data()))
                self.chart_obj_types.clear()

                color = golden_colors(len(obj_types), offset=0.1, saturation=0.3, value=0.4)
                for idx, (label, value) in enumerate(obj_types.items()):
                    self.chart_obj_types.add_slice(label, value, color[idx], values_max=nr_objects)

            if self.ai_model is not None:
                ai_detections = self.ai_model.rowCount()
                ai_runs = self.ai_model.get_nr_ai_runs()
                ai_imported = self.ai_model.nr_imported()

                self.ui.prj_label_object_ai_detection_nr.setText(str(ai_detections))
                self.ui.prj_label_object_ai_processes.setText(str(ai_runs))
                self.ui.gauge_ai_imported.change_value(ai_imported, ai_detections)

    # --------------------------------------------------------------
    # Import page
    # --------------------------------------------------------------

    #        logger.info("%i of %i total images could be geo-referenced" % (georef_success_number,
    #                                                                      len(folder_image_list)),
    #                    extra={"finished": True})

    def get_meta_single_image(self):

        file_to_test, _ = QFileDialog.getOpenFileName(self, caption="Choose Image File to test", dir='.')
        if file_to_test:
            if Path(file_to_test).is_file():
                worker = Worker(meta_of_image, image_path=Path(file_to_test), path_to_exiftool=path_to_exiftool)
                worker.signals.result.connect(self.thread_output_image_exif_test)
                worker.signals.finished.connect(self.thread_complete_image_test)
                worker.signals.error.connect(self.thread_error)
                self.ui.waiting_spinner_main.start()
                self.threadpool.start(worker)

    def get_meta_single_ortho(self):

        file_to_test, _ = QFileDialog.getOpenFileName(self, caption="Choose Ortho Image File to test", dir='.')
        if file_to_test:
            if Path(file_to_test).is_file():
                worker = Worker(meta_of_ortho_image, image_path=Path(file_to_test))
                worker.signals.result.connect(self.thread_output_image_ortho_test)
                worker.signals.finished.connect(self.thread_complete_image_test)
                worker.signals.error.connect(self.thread_error)
                self.ui.waiting_spinner_main.start()
                self.threadpool.start(worker)

    @Slot(object)
    def thread_output_image_exif_test(self, meta_values: tuple | None = None):
        if meta_values is None:
            change_led_color(self.ui.led_focal_length, on=False)
            change_led_color(self.ui.led_gnss_data, on=False)
            change_led_color(self.ui.led_crs_data, on=False)
            change_led_color(self.ui.led_crs_vertical, on=False)
            change_led_color(self.ui.led_image_pose, on=False)
        else:
            focal, gnss, crs_hor_exif, crs_vert_exif, pose = meta_values

            change_led_color(self.ui.led_focal_length, on=focal)
            change_led_color(self.ui.led_gnss_data, on=gnss)
            change_led_color(self.ui.led_crs_data, on=crs_hor_exif)
            change_led_color(self.ui.led_crs_vertical, on=crs_vert_exif)
            change_led_color(self.ui.led_image_pose, on=pose)

    @Slot(object)
    def thread_output_image_ortho_test(self, meta_values: tuple | None = None):
        if meta_values is None:
            change_led_color(self.ui.led_rasterio_possible, on=False)
            change_led_color(self.ui.led_ortho_coordinates, on=False)
            change_led_color(self.ui.led_ortho_crs, on=False)
        else:
            rasterio_flag, coordinates_flag, crs_flag = meta_values

            change_led_color(self.ui.led_rasterio_possible, on=rasterio_flag)
            change_led_color(self.ui.led_ortho_coordinates, on=coordinates_flag)
            change_led_color(self.ui.led_ortho_crs, on=crs_flag)

    @Slot()
    def thread_complete_image_test(self):
        self.ui.waiting_spinner_main.stop()

    @Slot()
    def thread_complete_image_import(self):

        self.ui.waiting_spinner_main.stop()
        images = self.db.load_images_list()

        self.image_folders: list[Path] = []
        self.ui.ai_folder_chooser.clear()
        if images:
            self.update_table_views(images=images, recalculate_area_gsd=True)
        else:
            self.db_is_locked = ''

    def hide_log_import_buttons(self):
        self.ui.frame_logfile_buttons.setVisible(not self.ui.imp_rd_logfile_image_folders.isChecked())
        self.log_file = None

        if self.input_data_types.input_type_current.log_file_contains_image_path and \
                not self.ui.imp_rd_logfile_image_folders.isChecked():
            self.ui.imp_rd_recursive.hide()
        else:
            self.ui.imp_rd_recursive.show()

    def logfile_chooser(self):
        self.log_file = None
        self.ui.imp_rd_recursive_logfiles_folder.setChecked(False)
        logfile, _ = QFileDialog.getOpenFileName(self, caption="Choose Logfile", dir=self.db.path.parent.as_posix())
        if logfile:
            if Path(logfile).is_file():
                self.log_file = Path(logfile)

    def logfile_path_chooser(self):
        self.log_file = None
        logfile_path = QFileDialog.getExistingDirectory(self, caption="Choose Logfile Folder", dir=self.db.path.parent.as_posix())
        if logfile_path:
            self.log_file = Path(logfile_path)

    def image_input_chooser(self):
        self.input_data_types.set_input_class(self.ui.imp_cmb_input_type.currentText())
        self.ui.imp_rd_recursive.setChecked(False)

        self.log_file = None

        self.hide_log_import_buttons()

        self.ui.imp_stack_type.setCurrentWidget(self.ui.imp_stack_empty)
        self.ui.imp_epsg_input.setText(None)

        if self.ui.imp_cmb_input_type.currentText() == 'Simple Image':
            self.ui.imp_stack_type.setCurrentWidget(self.ui.imp_stack_georef)

        if self.input_data_types.input_type_current.loader_type == LoaderType.Logfile_Loader:
            self.ui.imp_stack_type.setCurrentWidget(self.ui.imp_stack_logFile)

        if self.input_data_types.input_type_current.loader_type == LoaderType.EXIF_Loader:
            self.ui.imp_stack_type.setCurrentWidget(self.ui.imp_stack_vert_ref)
            self.ui.imp_rd_ortho_heights.setChecked(True)

        if self.input_data_types.input_type_current.crs_input_show:
            self.ui.frame_imp_epsg.show()
        else:
            self.ui.frame_imp_epsg.hide()

        if self.input_data_types.input_type_current.loader_type == LoaderType.Ortho_Loader:
            # Reset Leds
            self.thread_output_image_ortho_test()
            self.ui.stack_image_test.setCurrentWidget(self.ui.page_ortho_test)
        else:
            # Reset Leds
            self.thread_output_image_exif_test()
            self.ui.stack_image_test.setCurrentWidget(self.ui.page_exif_test)

        self.ui.progressBar_importer.setValue(0)
        self.ui.import_image_reference.setText('')
        self.ui.import_image_block.setText('')
        self.ui.import_image_transect.setText('')

        self.ui.import_image_meta_operator.setText('')
        self.ui.import_image_meta_camera.setText('')
        self.ui.import_image_conditions.setText('')
        self.ui.import_image_meta_comment.setPlainText('')

        self.ui.input_adj_rel_height.setText("0.0")
        logger.info('Set current input format for import to: ' + self.input_data_types.input_type_current.name)

    def import_image_folder(self):

        if self.db is None:
            logger.error("No database is connected")
            return

        flag_recursive_image = self.ui.imp_rd_recursive.isChecked()
        flag_log_fom_image_folder = self.ui.imp_rd_logfile_image_folders.isChecked()
        flag_recursive_log = self.ui.imp_rd_recursive_logfiles_folder.isChecked()

        # check overriding CRS
        crs_manual = None  # CRS("EPSG:4326+3855")
        crs_text = self.ui.imp_epsg_input.text()
        if self.input_data_types.input_type_current.crs_input_mandatory:
            if not crs_text:
                logger.error("This importer rquires CRS to be specified")
                return

        if crs_text:
            try:
                crs_manual = CRS(crs_text)
            except pyproj.exceptions.CRSError:
                logger.error("Specified CRS not working")
                return

        if not self.db_is_locked:
            self.image_scene.working_instruction = False
            self.image_scene.current_instruction = Instructions.No_Instruction
            self.ui.btn_create_rectangle.setIcon(QIcon(u":/icons/icons/rectangle.svg"))
            self.ui.btn_create_polygon.setIcon(QIcon(u":/icons/icons/polygon.svg"))
            self.ui.btn_create_point.setIcon(QIcon(u":/icons/icons/point.svg"))

            if self.input_data_types.input_type_current.loader_type == LoaderType.Logfile_Loader:

                if not flag_log_fom_image_folder:
                    if self.log_file is None:
                        logger.error('No Logfile specified')
                        return

            if self.log_file is not None:
                folder = self.log_file.parent.as_posix()
            else:
                folder = self.db.path.parent.as_posix()

            manual_georef = None

            vertical_ref = ''
            if self.ui.imp_stack_vert_ref.isVisible():

                if self.ui.imp_rd_ortho_heights.isChecked():
                    vertical_ref = 'orthometric'

                # The button is currently exclusive and we will check if text is orthometric in DJI end EXIF importer
                #elif self.ui.imp_rd_ell_heights.isChecked():
                #    vertical_ref = 'ellipsoid'

            if self.ui.imp_stack_georef.isVisible():

                if (self.ui.imp_georef_latitude.text() or
                        self.ui.imp_georef_longitude.text() or
                        self.ui.imp_georef_heading.text() or
                        self.ui.imp_georef_height.text() or
                        self.ui.imp_georef_sensor_width.text() or
                        self.ui.imp_georef_focal_mm.text()):

                    if (is_number(self.ui.imp_georef_latitude.text()) and
                            is_number(self.ui.imp_georef_longitude.text()) and
                            is_number(self.ui.imp_georef_heading.text()) and
                            is_number(self.ui.imp_georef_height.text()) and
                            is_number(self.ui.imp_georef_sensor_width.text()) and
                            is_number(self.ui.imp_georef_focal_mm.text())):

                        latitude = float(self.ui.imp_georef_latitude.text())
                        longitude = float(self.ui.imp_georef_longitude.text())
                        height = float(self.ui.imp_georef_height.text())

                        if abs(latitude) < 90 and 360 > longitude > 0 or height < 0.1:

                            heading = float(self.ui.imp_georef_heading.text())
                            sensor_width_mm = float(self.ui.imp_georef_sensor_width.text())
                            focal_mm = float(self.ui.imp_georef_focal_mm.text())

                            manual_georef = [longitude, latitude, height, heading, focal_mm, sensor_width_mm]
                        else:
                            self.ui.imp_georef_status.setText(
                                'Some input is set - maybe no numbers or not valid (check Lat, Long)')
                            return

                    else:
                        self.ui.imp_georef_status.setText(
                            'Some input is set - maybe no numbers or not valid (check Lat, Long)')
                        return

            # Check if we need to open Dialogue for image folders
            image_path = ''
            if (not self.input_data_types.input_type_current.log_file_contains_image_path) or (
                    self.ui.imp_rd_logfile_image_folders.isChecked()):
                image_path = QFileDialog.getExistingDirectory(self, caption="Load Images", dir=folder)
                if not image_path:
                    return

            self.db_is_locked = 'Database locked for image loading'
            self.ui.progressBar_importer.setValue(0)

            # Survey information entered by user
            flight_ref = self.ui.import_image_reference.text()
            survey_block = self.ui.import_image_block.text()
            transect = self.ui.import_image_transect.text()

            # Meta data entered by user
            operator = self.ui.import_image_meta_operator.text()
            camera_ref = self.ui.import_image_meta_camera.text()
            conditions = self.ui.import_image_conditions.text()
            comments = self.ui.import_image_meta_comment.toPlainText()
            meta_user = {'operator': operator, 'camera_ref': camera_ref, 'conditions': conditions,
                         'comments': comments}

            # if self.ui.input_adj_rel_height.text() == "0.0":
            #     rel_h = 0
            # else:
            #     rel_h = float(self.ui.input_adj_rel_height.text())

            self.ui.imp_georef_status.setText('')

            worker = Worker(process_folder, input_path=Path(image_path), db_path=self.db.path, user=self.user,
                            mapper=self.mapper, input_data_class=self.input_data_types, logfile_path=self.log_file,
                            meta_user=meta_user,
                            flight_ref=flight_ref, survey_block=survey_block, transect=transect,
                            crs_manual=crs_manual,
                            georef_input=manual_georef,
                            flag_recursive_image=flag_recursive_image,
                            flag_recursive_log=flag_recursive_log,
                            flag_log_fom_image_folder=flag_log_fom_image_folder,
                            vertical_ref=vertical_ref,
                            path_to_exiftool=path_to_exiftool, progress_callback=True)
            worker.signals.result.connect(self.thread_output_image_import)
            worker.signals.finished.connect(self.thread_complete_image_import)
            worker.signals.progress.connect(self.progress_fn)
            worker.signals.error.connect(self.thread_error)
            self.ui.waiting_spinner_main.start()
            self.threadpool.start(worker)
        else:
            logger.warning(self.db_is_locked)

    # --------------------------------------------------------------
    # Standard menu functions
    # --------------------------------------------------------------
    def create_new_db(self):
        if not self.db_is_locked:
            self.clean_all_views_and_tables(close_db=True)
            self.popup_config_project.clear_config()
            self.popup_config_project.show()
        else:
            logger.warning(self.db_is_locked)

    @Slot(object)
    def create_new_db_start(self, config: dict):

        db_path, _ = QFileDialog.getSaveFileName(self, caption="Create Database",
                                                 dir='.', filter='SQLITE Files (*.sqlite)')

        if db_path:
            path_db = Path(db_path)
            if path_db.exists():
                try:
                    path_db.unlink()
                    logger.info('DB File was overwritten!')
                except PermissionError:
                    logger.error('DB File seems to be locked! Maybe opened by program. Otherwise try restart of '
                                 'computer')

                    self.popup_config_project.show()
                    return

            # Create Database
            self.db = DBHandler.create(path_db, self.user, time.asctime(), config)
            if self.db is not None:
                self.image_scene.db = self.db
                self.gis_scene.db = self.db
                self.ui.gallery_listview.set_db(self.db)
                self.ui.ai_listview.set_db(self.db)
                self.db.color_scheme = ColorGui.color_scheme_start
                self.color_scheme = ColorGui.color_scheme_start
                self.popup_config.set_color_widget(self.color_scheme['projection']['colors'])
                self.show_thumbnails()
                logger.info('New database was created: ' + path_db.name)
                self.ui.lbl_database_name.setText(path_db.name)
                self.ui.lbl_database_name.setStyleSheet(r"""border: 3px solid rgb(187, 184, 87);border-radius:15px;""")

                # Load the configured object types
                self.popup_meta.configure(config)
                self.ui.environment_image.set_config(config['environment_data'])

                self.show_mapper_configurator()

            else:
                logger.error('Database can not be created: Probably locked')

        else:
            self.popup_config_project.show()

    def load_existing_db(self):
        if not self.db_is_locked:

            db_path, _ = QFileDialog.getOpenFileName(self, caption="Load Database",
                                                     dir='.', filter='SQLITE Files (*.sqlite)')

            if db_path:

                self.clean_all_views_and_tables(close_db=True)

                self.db = DBHandler.from_path(Path(db_path), self.user)
                if self.db is None:
                    logger.error("Not able to load database")
                    return

                try:
                    project_config = self.db.load_config()
                except sqlite3.OperationalError:
                    logger.error("Not able to load database. Maybe version not supported")
                    return

                try:
                    config_mapper = None
                    if project_config['mapper'] is not None:
                        config_mapper = json.loads(project_config['mapper'])
                except KeyError:
                    logger.error("Not able to load database. Maybe version not supported")
                    return

                try:
                    self.mapper = mapper_load_from_dict(config_mapper)
                except MappingError:
                    logger.error("Mapper can not be loaded. Please change mapper")
                    self.mapper = None

                self.image_scene.db = self.db
                self.gis_scene.db = self.db
                self.ui.gallery_listview.set_db(self.db)
                self.ui.ai_listview.set_db(self.db)

                # load color config
                # Check for existing entries as older Version have not saved everything
                # also json dump will convert integer keys to string. will be reparsed at check_update_color_config
                self.color_scheme = check_update_color_config(json.loads(project_config['color_scheme']))
                self.db.color_scheme = self.color_scheme

                self.popup_config.set_color_widget(self.color_scheme['projection']['colors'])

                config = json.loads(project_config['configuration'], object_pairs_hook=OrderedDict)
                self.popup_meta.configure(config)
                self.ui.environment_image.set_config(config['environment_data'])

                logger.info('Existing database was loaded: ' + Path(db_path).name)
                self.ui.lbl_database_name.setText(Path(db_path).name)

                # Color project name in top frame
                # Yellow border -  border: 3px solid rgb(187, 184, 87);border-radius:15px
                # Main color as background #2c313c
                self.ui.lbl_database_name.setStyleSheet(r"""background-color:#476647; border-radius:8px""")

                images = self.db.load_images_list()

                if not images:
                    return
                self.update_table_views(images)
                self.show_group_area_list()

                last_used_image = self.db.last_image

                # Show last used image on image screen
                if last_used_image:
                    index = self.image_panel_model.match(self.image_panel_model.index(0, ImageList.id),
                                                         RolesImagePane.id, last_used_image, -1,
                                                         Qt.MatchFlag.MatchRecursive)
                    if index is None:
                        return
                    index = index[0]
                    self.load_image(index, change_to_digitizer_page=False)

        else:
            logger.warning(self.db_is_locked)

    # --------------------------------------------------------------------------------------------------
    # GALLERY PAGE
    # --------------------------------------------------------------------------------------------------

    def gallery_icon_size(self):
        thumb_size_user = GalleryIconSize()
        thumb_size_user.width = self.ui.gallery_slider_thumb_size.value()
        thumb_size_user.height = thumb_size_user.width
        self.ui.gallery_listview.setItemDelegate(GalleryIconDelegate(thumb_size=thumb_size_user, db=self.db))

    def set_gallery_fast_activate(self):
        self.ui.gallery_listview.fast_activate = self.sender().isChecked()

    def show_thumbnails(self):

        if self.db is not None:
            thumb_size_user = GalleryIconSize()
            thumb_size_user.width = self.ui.gallery_slider_thumb_size.value()
            thumb_size_user.height = thumb_size_user.width
            self.ui.gallery_listview.setIconSize(QSize(thumb_size_user.width, thumb_size_user.height))

            if self.ui.gallery_btn_order_object_type.isChecked():
                order_value = 'object_type'
            elif self.ui.gallery_btn_order_area.isChecked():
                order_value = 'group_area'
            elif self.ui.gallery_btn_order_resight.isChecked():
                order_value = 'resight_set'
            else:
                order_value = 'id'

            self.thumbnail_model = gallery_loader(self.db, order_value=order_value)
            self.gallery_proxyModel.setSourceModel(self.thumbnail_model)
            self.ui.gallery_listview.setModel(self.gallery_proxyModel)
            # self.proxy_filter.setFilterRole(self.thumbnail_model.)

            self.ui.gallery_listview.setItemDelegate(GalleryIconDelegate(thumb_size=thumb_size_user, db=self.db))

    # --------------------------------------------------------------------------------------------------
    # EXPORT PAGE
    # --------------------------------------------------------------------------------------------------
    def export_trainings_data(self):

        if self.db is not None:
            if not self.db_is_locked:
                self.db_is_locked = "DB Locked for export trainings data"

                export_folder = QFileDialog.getExistingDirectory(self, caption="Choose Folder for export")

                if export_folder:

                    exclude_ai = self.ui.db_check_export_ai_detections.isChecked()

                    # Thread for running the export
                    worker = Worker(export_trainings_data_worker, self.db.path,
                                    self.ui.db_check_export_ai_full_images.isChecked(), export_folder, exclude_ai,
                                    progress_callback=True)
                    worker.signals.result.connect(self.thread_output)
                    worker.signals.finished.connect(self.thread_complete_export_ai)
                    worker.signals.error.connect(self.thread_error)
                    # worker.signals.progress.connect(self.progress_fn)
                    self.threadpool.start(worker)
                    self.ui.waiting_spinner_main.start()
                else:
                    self.db_is_locked = ''
            else:
                logger.warning(self.db_is_locked)

    def thread_complete_export(self):
        self.ui.waiting_spinner_main.stop()

    def export(self, format_export):

        if self.db is not None:
            worker = Worker(export_file, self.db.path,
                            format_export, self.ui.rd_export_first_certain.isChecked())
            worker.signals.finished.connect(self.thread_complete_export)
            worker.signals.error.connect(self.thread_error)
            self.threadpool.start(worker)
            self.ui.waiting_spinner_main.start()


# ----------------------------------------------------------------------------------------------------------
# main function also called by entry point
def main():
    # add Path to spatialite package and to exiftool
    sqlite_extension = path_to_bin / 'spatialite-loadable-modules-5.0.0-win-amd64'
    os.environ['PATH'] = ';'.join([path_to_bin.as_posix(), sqlite_extension.as_posix(),
                                   path_to_current_directory.as_posix(), os.environ['PATH']])

    # enable pyproj network capabilities for downloading raster and transformation grids
    pyproj.network.set_network_enabled(active=True)
    pyproj_datadir.append_data_dir(path_to_proj_dir.as_posix())
    # Nuitka and PyInstaller already  bundling now the libraries in the correct place
    # pyproj.datadir.set_data_dir((path_to_datadir / "proj").as_posix())

    freeze_support()
    app = QApplication()
    QFontDatabase.addApplicationFont('app/gui_design/fonts/segoeui.ttf')
    QFontDatabase.addApplicationFont('app/gui_design/fonts/segoeuib.ttf')
    window = MainWindow()
    app.installEventFilter(window)
    app.setWindowIcon(QIcon(u":/icons/icons/WISDAM_Icon_square.png"))
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
