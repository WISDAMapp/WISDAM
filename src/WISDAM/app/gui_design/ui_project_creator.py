# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui_project_creator.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QSizePolicy,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from app.custom_elements.comboInteractive import InteractiveCombo
from . import files_rc


class Ui_popup_project_config(object):
    def setupUi(self, popup_project_config):
        if not popup_project_config.objectName():
            popup_project_config.setObjectName("popup_project_config")
        popup_project_config.resize(1000, 797)
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            popup_project_config.sizePolicy().hasHeightForWidth()
        )
        popup_project_config.setSizePolicy(sizePolicy)
        popup_project_config.setMinimumSize(QSize(1000, 600))
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush
        )
        brush1 = QBrush(QColor(0, 0, 0, 0))
        brush1.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, brush1)
        brush2 = QBrush(QColor(66, 73, 90, 255))
        brush2.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Light, brush2)
        brush3 = QBrush(QColor(55, 61, 75, 255))
        brush3.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QPalette.ColorGroup.Active, QPalette.ColorRole.Midlight, brush3
        )
        brush4 = QBrush(QColor(22, 24, 30, 255))
        brush4.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Dark, brush4)
        brush5 = QBrush(QColor(29, 32, 40, 255))
        brush5.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Mid, brush5)
        brush6 = QBrush(QColor(210, 210, 210, 255))
        brush6.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush6)
        palette.setBrush(
            QPalette.ColorGroup.Active, QPalette.ColorRole.BrightText, brush
        )
        palette.setBrush(
            QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush
        )
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush1)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush1)
        brush7 = QBrush(QColor(0, 0, 0, 255))
        brush7.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Shadow, brush7)
        brush8 = QBrush(QColor(85, 170, 255, 255))
        brush8.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QPalette.ColorGroup.Active, QPalette.ColorRole.Highlight, brush8
        )
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Link, brush8)
        brush9 = QBrush(QColor(255, 0, 127, 255))
        brush9.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QPalette.ColorGroup.Active, QPalette.ColorRole.LinkVisited, brush9
        )
        palette.setBrush(
            QPalette.ColorGroup.Active, QPalette.ColorRole.AlternateBase, brush4
        )
        brush10 = QBrush(QColor(44, 49, 60, 255))
        brush10.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QPalette.ColorGroup.Active, QPalette.ColorRole.ToolTipBase, brush10
        )
        palette.setBrush(
            QPalette.ColorGroup.Active, QPalette.ColorRole.ToolTipText, brush6
        )
        brush11 = QBrush(QColor(210, 210, 210, 128))
        brush11.setStyle(Qt.BrushStyle.SolidPattern)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(
            QPalette.ColorGroup.Active, QPalette.ColorRole.PlaceholderText, brush11
        )
        # endif
        palette.setBrush(
            QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush
        )
        palette.setBrush(
            QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, brush1
        )
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Light, brush2)
        palette.setBrush(
            QPalette.ColorGroup.Inactive, QPalette.ColorRole.Midlight, brush3
        )
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Dark, brush4)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Mid, brush5)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush6)
        palette.setBrush(
            QPalette.ColorGroup.Inactive, QPalette.ColorRole.BrightText, brush
        )
        palette.setBrush(
            QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush
        )
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush1)
        palette.setBrush(
            QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush1
        )
        palette.setBrush(
            QPalette.ColorGroup.Inactive, QPalette.ColorRole.Shadow, brush7
        )
        palette.setBrush(
            QPalette.ColorGroup.Inactive, QPalette.ColorRole.Highlight, brush8
        )
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Link, brush8)
        palette.setBrush(
            QPalette.ColorGroup.Inactive, QPalette.ColorRole.LinkVisited, brush9
        )
        palette.setBrush(
            QPalette.ColorGroup.Inactive, QPalette.ColorRole.AlternateBase, brush4
        )
        palette.setBrush(
            QPalette.ColorGroup.Inactive, QPalette.ColorRole.ToolTipBase, brush10
        )
        palette.setBrush(
            QPalette.ColorGroup.Inactive, QPalette.ColorRole.ToolTipText, brush6
        )
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(
            QPalette.ColorGroup.Inactive, QPalette.ColorRole.PlaceholderText, brush11
        )
        # endif
        palette.setBrush(
            QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush4
        )
        palette.setBrush(
            QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, brush1
        )
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Light, brush2)
        palette.setBrush(
            QPalette.ColorGroup.Disabled, QPalette.ColorRole.Midlight, brush3
        )
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Dark, brush4)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Mid, brush5)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush4)
        palette.setBrush(
            QPalette.ColorGroup.Disabled, QPalette.ColorRole.BrightText, brush
        )
        palette.setBrush(
            QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush4
        )
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush1)
        palette.setBrush(
            QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush1
        )
        palette.setBrush(
            QPalette.ColorGroup.Disabled, QPalette.ColorRole.Shadow, brush7
        )
        brush12 = QBrush(QColor(51, 153, 255, 255))
        brush12.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QPalette.ColorGroup.Disabled, QPalette.ColorRole.Highlight, brush12
        )
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Link, brush8)
        palette.setBrush(
            QPalette.ColorGroup.Disabled, QPalette.ColorRole.LinkVisited, brush9
        )
        palette.setBrush(
            QPalette.ColorGroup.Disabled, QPalette.ColorRole.AlternateBase, brush10
        )
        palette.setBrush(
            QPalette.ColorGroup.Disabled, QPalette.ColorRole.ToolTipBase, brush10
        )
        palette.setBrush(
            QPalette.ColorGroup.Disabled, QPalette.ColorRole.ToolTipText, brush6
        )
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(
            QPalette.ColorGroup.Disabled, QPalette.ColorRole.PlaceholderText, brush11
        )
        # endif
        popup_project_config.setPalette(palette)
        font = QFont()
        font.setFamilies(["Segoe UI"])
        font.setPointSize(10)
        popup_project_config.setFont(font)
        popup_project_config.setStyleSheet(
            "QWidget {background: transparent; color: rgb(210, 210, 210)}\n"
            "QToolTip {\n"
            "	color: #ffffff;\n"
            "	background-color: rgba(27, 29, 35, 160);\n"
            "	border: 1px solid rgb(40, 40, 40);\n"
            "	border-radius: 2px;\n"
            "}\n"
            "/* LINE EDIT */\n"
            "QLineEdit {\n"
            "	background-color: rgb(27, 29, 35);\n"
            "	border-radius: 5px;\n"
            "	border: 2px solid rgb(57, 59, 65);\n"
            "	padding-left: 10px;\n"
            "}\n"
            "QLineEdit:hover {\n"
            "	border: 2px solid rgb(64, 71, 88);\n"
            "}\n"
            "QLineEdit:focus {\n"
            "	border: 2px solid rgb(91, 101, 124);\n"
            "}\n"
            "\n"
            "/* SCROLL BARS */\n"
            "QScrollBar:horizontal {\n"
            "    border: none;\n"
            "    background: rgb(52, 59, 72);\n"
            "    height: 14px;\n"
            "    margin: 0px 21px 0 21px;\n"
            "	border-radius: 0px;\n"
            "}\n"
            "QScrollBar::handle:horizontal {\n"
            "    background: rgb(178, 186, 87);\n"
            "    min-width: 25px;\n"
            "	border-radius: 7px\n"
            "}\n"
            "QScrollBar::add-line:horizontal {\n"
            "    border: none;\n"
            "    background: rgb(55, 63, 77);\n"
            "    width: 20px;\n"
            "	border-top-right-radius: 7px;\n"
            "    border-bot"
            "tom-right-radius: 7px;\n"
            "    subcontrol-position: right;\n"
            "    subcontrol-origin: margin;\n"
            "}\n"
            "QScrollBar::sub-line:horizontal {\n"
            "    border: none;\n"
            "    background: rgb(55, 63, 77);\n"
            "    width: 20px;\n"
            "	border-top-left-radius: 7px;\n"
            "    border-bottom-left-radius: 7px;\n"
            "    subcontrol-position: left;\n"
            "    subcontrol-origin: margin;\n"
            "}\n"
            "QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal\n"
            "{\n"
            "     background: none;\n"
            "}\n"
            "QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
            "{\n"
            "     background: none;\n"
            "}\n"
            " QScrollBar:vertical {\n"
            "	border: none;\n"
            "    background: rgb(52, 59, 72);\n"
            "    width: 14px;\n"
            "    margin: 21px 0 21px 0;\n"
            "	border-radius: 0px;\n"
            " }\n"
            " QScrollBar::handle:vertical {	\n"
            "	background: rgb(178, 186, 87);\n"
            "    min-height: 25px;\n"
            "	border-radius: 7px\n"
            " }\n"
            " QScrollBar::add-line:vertical {\n"
            "     border: none;\n"
            "    background: rgb(55, 63, 77);\n"
            "     height: 20px;\n"
            "	border-bottom-left"
            "-radius: 7px;\n"
            "    border-bottom-right-radius: 7px;\n"
            "     subcontrol-position: bottom;\n"
            "     subcontrol-origin: margin;\n"
            " }\n"
            " QScrollBar::sub-line:vertical {\n"
            "	border: none;\n"
            "    background: rgb(55, 63, 77);\n"
            "     height: 20px;\n"
            "	border-top-left-radius: 7px;\n"
            "    border-top-right-radius: 7px;\n"
            "     subcontrol-position: top;\n"
            "     subcontrol-origin: margin;\n"
            " }\n"
            " QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
            "     background: none;\n"
            " }\n"
            "\n"
            " QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
            "     background: none;\n"
            " }\n"
            "\n"
            "/* CHECKBOX */\n"
            "QCheckBox::indicator {\n"
            "    border: 3px solid rgb(52, 59, 72);\n"
            "	width: 15px;\n"
            "	height: 15px;\n"
            "	border-radius: 10px;\n"
            "    background: rgb(44, 49, 60);\n"
            "}\n"
            "QCheckBox::indicator:hover {\n"
            "    border: 3px solid rgb(58, 66, 81);\n"
            "}\n"
            "QCheckBox::indicator:checked {\n"
            "    background: 3px solid rgb(52, 59, 72);\n"
            "	border: 3px solid rgb(52, 59, 72);\n"
            "}\n"
            ""
            "\n"
            "/* RADIO BUTTON */\n"
            "QRadioButton::indicator {\n"
            "    border: 3px solid rgb(52, 59, 72);\n"
            "	width: 15px;\n"
            "	height: 15px;\n"
            "	border-radius: 10px;\n"
            "    background: rgb(44, 49, 60);\n"
            "}\n"
            "QRadioButton::indicator:hover {\n"
            "    border: 3px solid rgb(58, 66, 81);\n"
            "}\n"
            "QRadioButton::indicator:checked {\n"
            "    background: 3px solid rgb(94, 106, 130);\n"
            "	border: 3px solid rgb(52, 59, 72);	\n"
            "}\n"
            "\n"
            "/* COMBOBOX */\n"
            "QComboBox{\n"
            "	background-color: rgb(27, 29, 35);\n"
            "	border-radius: 5px;\n"
            "	border: 2px solid rgb(27, 29, 35);\n"
            "	padding: 5px;\n"
            "	padding-left: 10px;\n"
            "}\n"
            "QComboBox:hover{\n"
            "	border: 2px solid rgb(64, 71, 88);\n"
            "}\n"
            "QComboBox::drop-down {\n"
            "	subcontrol-origin: padding;\n"
            "	subcontrol-position: top right;\n"
            "	width: 25px; \n"
            "	border-left-width: 3px;\n"
            "	border-left-color: rgba(39, 44, 54, 150);\n"
            "	border-left-style: solid;\n"
            "	border-top-right-radius: 3px;\n"
            "	border-bottom-right-radius: 3px;	\n"
            "	background-image: url(:/icons/icons/ico-"
            "arrow-bottom.png);\n"
            "	background-position: center;\n"
            "	background-repeat: no-reperat;\n"
            " }\n"
            "QComboBox QAbstractItemView {\n"
            "	color: rgb(85, 170, 255);	\n"
            "	background-color: rgb(27, 29, 35);\n"
            "	padding: 10px;\n"
            "	selection-background-color: rgb(39, 44, 54);\n"
            "}\n"
            "\n"
            "/* SLIDERS */\n"
            "QSlider::groove:horizontal {\n"
            "    border-radius: 9px;\n"
            "    height: 18px;\n"
            "	margin: 0px;\n"
            "	background-color: rgb(52, 59, 72);\n"
            "}\n"
            "QSlider::groove:horizontal:hover {\n"
            "	background-color: rgb(55, 62, 76);\n"
            "}\n"
            "QSlider::handle:horizontal {\n"
            "    background-color: rgb(178, 186, 87);\n"
            "    border: none;\n"
            "    height: 18px;\n"
            "    width: 18px;\n"
            "    margin: 0px;\n"
            "	border-radius: 9px;\n"
            "}\n"
            "QSlider::handle:horizontal:hover {\n"
            "    background-color: rgb(105, 180, 255);\n"
            "}\n"
            "QSlider::handle:horizontal:pressed {\n"
            "    background-color: rgb(65, 130, 195);\n"
            "}\n"
            "\n"
            "QSlider::groove:vertical {\n"
            "    border-radius: 9px;\n"
            "    width: 18px;\n"
            "    margin: 0px;\n"
            "	bac"
            "kground-color: rgb(52, 59, 72);\n"
            "}\n"
            "QSlider::groove:vertical:hover {\n"
            "	background-color: rgb(55, 62, 76);\n"
            "}\n"
            "QSlider::handle:vertical {\n"
            "    background-color: rgb(85, 170, 255);\n"
            "	border: none;\n"
            "    height: 18px;\n"
            "    width: 18px;\n"
            "    margin: 0px;\n"
            "	border-radius: 9px;\n"
            "}\n"
            "QSlider::handle:vertical:hover {\n"
            "    background-color: rgb(105, 180, 255);\n"
            "}\n"
            "QSlider::handle:vertical:pressed {\n"
            "    background-color: rgb(65, 130, 195);\n"
            "}\n"
            "\n"
            ""
        )
        self.verticalLayout = QVBoxLayout(popup_project_config)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_top = QFrame(popup_project_config)
        self.frame_top.setObjectName("frame_top")
        self.frame_top.setMinimumSize(QSize(0, 40))
        self.frame_top.setMaximumSize(QSize(16777215, 40))
        font1 = QFont()
        font1.setFamilies(["Segoe UI"])
        self.frame_top.setFont(font1)
        self.frame_top.setStyleSheet("background-color:rgb(127, 84, 0);\ncolor: white;")
        self.frame_top.setFrameShape(QFrame.NoFrame)
        self.frame_top.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_top)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(10, 0, 0, 0)
        self.lbl_icon = QLabel(self.frame_top)
        self.lbl_icon.setObjectName("lbl_icon")
        self.lbl_icon.setMinimumSize(QSize(30, 30))
        self.lbl_icon.setMaximumSize(QSize(30, 30))
        self.lbl_icon.setPixmap(QPixmap(":/icons/icons/WISDAM_Icon_square_small.svg"))

        self.horizontalLayout.addWidget(self.lbl_icon)

        self.label_title = QLabel(self.frame_top)
        self.label_title.setObjectName("label_title")
        font2 = QFont()
        font2.setFamilies(["Segoe UI"])
        font2.setPointSize(10)
        font2.setBold(True)
        self.label_title.setFont(font2)
        self.label_title.setStyleSheet("background: transparent;\n")
        self.label_title.setFrameShadow(QFrame.Raised)

        self.horizontalLayout.addWidget(self.label_title)

        self.btn_close = QPushButton(self.frame_top)
        self.btn_close.setObjectName("btn_close")
        self.btn_close.setEnabled(True)
        sizePolicy1 = QSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.btn_close.sizePolicy().hasHeightForWidth())
        self.btn_close.setSizePolicy(sizePolicy1)
        self.btn_close.setMinimumSize(QSize(40, 0))
        self.btn_close.setMaximumSize(QSize(40, 16777215))
        self.btn_close.setFont(font1)
        # if QT_CONFIG(tooltip)
        self.btn_close.setToolTip("Close")
        # endif // QT_CONFIG(tooltip)
        self.btn_close.setStyleSheet(
            "QPushButton {	\n"
            "	border: none;\n"
            "	background-color: transparent;\n"
            "}\n"
            "QPushButton:hover {\n"
            "	background-color: rgb(150, 40, 23);\n"
            "}\n"
            "QPushButton:pressed {	\n"
            "	background-color: rgb(250, 39, 10);\n"
            "}"
        )
        self.btn_close.setText("")
        icon = QIcon()
        icon.addFile(
            ":/icons/icons/ico-x.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.btn_close.setIcon(icon)

        self.horizontalLayout.addWidget(self.btn_close)

        self.verticalLayout.addWidget(self.frame_top)

        self.frame_center = QFrame(popup_project_config)
        self.frame_center.setObjectName("frame_center")
        sizePolicy2 = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(
            self.frame_center.sizePolicy().hasHeightForWidth()
        )
        self.frame_center.setSizePolicy(sizePolicy2)
        self.frame_center.setFont(font1)
        self.frame_center.setStyleSheet("background-color: rgb(34, 36, 50);")
        self.frame_center.setFrameShape(QFrame.NoFrame)
        self.frame_center.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_center)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.frame_center)
        self.frame.setObjectName("frame")
        self.frame.setFont(font1)
        self.frame.setStyleSheet("")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame_environment = QFrame(self.frame)
        self.frame_environment.setObjectName("frame_environment")
        self.frame_environment.setGeometry(QRect(5, 320, 461, 301))
        self.frame_environment.setAutoFillBackground(False)
        self.frame_environment.setStyleSheet(
            "#frame_environment{\n"
            "border: 1px solid rgb(170, 170, 255);\n"
            "border-radius:15px;}\n"
            ""
        )
        self.frame_environment.setFrameShape(QFrame.NoFrame)
        self.frame_environment.setFrameShadow(QFrame.Plain)
        self.frame_environment.setLineWidth(1)
        self.cmb_custom_2 = InteractiveCombo(self.frame_environment)
        self.cmb_custom_2.setObjectName("cmb_custom_2")
        self.cmb_custom_2.setGeometry(QRect(160, 110, 141, 31))
        self.cmb_custom_2.setFont(font)
        self.cmb_custom_2.setStyleSheet(
            "QComboBox { color: white;background-color: rgb(27, 29, 35);}\n"
            "QComboBox QAbstractItemView {\n"
            "  color: white;background-color: rgb(27, 29, 35);\n"
            "}"
        )
        self.cmb_custom_2.setCurrentText("")
        self.cmb_custom_1 = InteractiveCombo(self.frame_environment)
        self.cmb_custom_1.setObjectName("cmb_custom_1")
        self.cmb_custom_1.setGeometry(QRect(10, 110, 141, 31))
        font3 = QFont()
        font3.setFamilies(["Segoe UI"])
        font3.setPointSize(10)
        font3.setBold(False)
        self.cmb_custom_1.setFont(font3)
        # if QT_CONFIG(tooltip)
        self.cmb_custom_1.setToolTip("")
        # endif // QT_CONFIG(tooltip)
        self.cmb_custom_1.setStyleSheet(
            "QComboBox { color: white;background-color: rgb(27, 29, 35);}\n"
            "QComboBox QAbstractItemView {\n"
            "  color: white;background-color: rgb(27, 29, 35);\n"
            "}"
        )
        self.cmb_custom_1.setEditable(False)
        self.cmb_custom_1.setCurrentText("")
        self.cmb_custom_1.setFrame(True)
        self.cmb_custom_3 = InteractiveCombo(self.frame_environment)
        self.cmb_custom_3.setObjectName("cmb_custom_3")
        self.cmb_custom_3.setGeometry(QRect(310, 110, 141, 31))
        self.cmb_custom_3.setFont(font)
        self.cmb_custom_3.setStyleSheet(
            "QComboBox { color: white;background-color: rgb(27, 29, 35);}\n"
            "QComboBox QAbstractItemView {\n"
            "  color: white;background-color: rgb(27, 29, 35);\n"
            "}"
        )
        self.cmb_custom_3.setCurrentText("")
        self.cmb_custom_5 = InteractiveCombo(self.frame_environment)
        self.cmb_custom_5.setObjectName("cmb_custom_5")
        self.cmb_custom_5.setGeometry(QRect(160, 200, 141, 31))
        self.cmb_custom_5.setFont(font)
        self.cmb_custom_5.setStyleSheet(
            "QComboBox { color: white;background-color: rgb(27, 29, 35);}\n"
            "QComboBox QAbstractItemView {\n"
            "  color: white;background-color: rgb(27, 29, 35);\n"
            "}"
        )
        self.cmb_custom_5.setCurrentText("")
        self.cmb_custom_4 = InteractiveCombo(self.frame_environment)
        self.cmb_custom_4.setObjectName("cmb_custom_4")
        self.cmb_custom_4.setGeometry(QRect(10, 200, 141, 31))
        self.cmb_custom_4.setFont(font3)
        self.cmb_custom_4.setStyleSheet(
            "QComboBox { color: white;background-color: rgb(27, 29, 35);}\n"
            "QComboBox QAbstractItemView {\n"
            "  color: white;background-color: rgb(27, 29, 35);\n"
            "}"
        )
        self.cmb_custom_4.setEditable(False)
        self.cmb_custom_4.setCurrentText("")
        self.cmb_custom_6 = InteractiveCombo(self.frame_environment)
        self.cmb_custom_6.setObjectName("cmb_custom_6")
        self.cmb_custom_6.setGeometry(QRect(310, 200, 141, 31))
        self.cmb_custom_6.setFont(font)
        self.cmb_custom_6.setStyleSheet(
            "QComboBox { color: white;background-color: rgb(27, 29, 35);}\n"
            "QComboBox QAbstractItemView {\n"
            "  color: white;background-color: rgb(27, 29, 35);\n"
            "}"
        )
        self.cmb_custom_6.setCurrentText("")
        self.le_custom_1 = QLineEdit(self.frame_environment)
        self.le_custom_1.setObjectName("le_custom_1")
        self.le_custom_1.setGeometry(QRect(12, 80, 131, 22))
        font4 = QFont()
        font4.setPointSize(10)
        font4.setBold(True)
        self.le_custom_1.setFont(font4)
        self.le_custom_2 = QLineEdit(self.frame_environment)
        self.le_custom_2.setObjectName("le_custom_2")
        self.le_custom_2.setGeometry(QRect(168, 80, 131, 22))
        self.le_custom_2.setFont(font4)
        self.le_custom_4 = QLineEdit(self.frame_environment)
        self.le_custom_4.setObjectName("le_custom_4")
        self.le_custom_4.setGeometry(QRect(12, 170, 131, 22))
        self.le_custom_4.setFont(font4)
        self.le_custom_5 = QLineEdit(self.frame_environment)
        self.le_custom_5.setObjectName("le_custom_5")
        self.le_custom_5.setGeometry(QRect(158, 170, 141, 22))
        self.le_custom_5.setFont(font4)
        self.le_custom_6 = QLineEdit(self.frame_environment)
        self.le_custom_6.setObjectName("le_custom_6")
        self.le_custom_6.setGeometry(QRect(312, 170, 131, 22))
        self.le_custom_6.setFont(font4)
        self.label_7 = QLabel(self.frame_environment)
        self.label_7.setObjectName("label_7")
        self.label_7.setGeometry(QRect(20, 10, 411, 61))
        font5 = QFont()
        font5.setPointSize(10)
        self.label_7.setFont(font5)
        self.le_custom_3 = QLineEdit(self.frame_environment)
        self.le_custom_3.setObjectName("le_custom_3")
        self.le_custom_3.setGeometry(QRect(312, 80, 131, 22))
        self.le_custom_3.setFont(font4)
        self.rd_env_object_override = QRadioButton(self.frame_environment)
        self.rd_env_object_override.setObjectName("rd_env_object_override")
        self.rd_env_object_override.setGeometry(QRect(20, 250, 231, 41))
        font6 = QFont()
        font6.setPointSize(11)
        self.rd_env_object_override.setFont(font6)
        self.rd_env_object_override.setText(
            "First object to set image\nenv data if not present"
        )
        self.rd_env_object_override.setChecked(False)
        self.rd_env_object_override.setAutoExclusive(False)
        self.rd_env_object_override_propagate = QRadioButton(self.frame_environment)
        self.rd_env_object_override_propagate.setObjectName(
            "rd_env_object_override_propagate"
        )
        self.rd_env_object_override_propagate.setGeometry(QRect(230, 250, 211, 41))
        self.rd_env_object_override_propagate.setFont(font6)
        self.rd_env_object_override_propagate.setText(
            "First object to set image\nenv data if only propagated"
        )
        self.rd_env_object_override_propagate.setChecked(False)
        self.rd_env_object_override_propagate.setAutoExclusive(False)
        self.btn_save_config = QPushButton(self.frame)
        self.btn_save_config.setObjectName("btn_save_config")
        self.btn_save_config.setGeometry(QRect(180, 640, 141, 41))
        self.btn_save_config.setFont(font2)
        self.btn_save_config.setStyleSheet(
            "QPushButton {\n"
            "	border: 2px solid rgb(52, 59, 72);\n"
            "	border-radius: 5px;	\n"
            "	background-color: rgb(52, 59, 72);\n"
            "}\n"
            "QPushButton:hover {\n"
            "	background-color: rgb(57, 65, 80);\n"
            "	border: 2px solid rgb(61, 70, 86);\n"
            "}\n"
            "QPushButton:pressed {	\n"
            "	background-color: rgb(35, 40, 49);\n"
            "	border: 2px solid rgb(43, 50, 61);\n"
            "}"
        )
        self.btn_submit = QPushButton(self.frame)
        self.btn_submit.setObjectName("btn_submit")
        self.btn_submit.setGeometry(QRect(230, 700, 141, 41))
        self.btn_submit.setFont(font2)
        self.btn_submit.setStyleSheet(
            "QPushButton {\n"
            "	border: 2px solid rgb(52, 59, 72);\n"
            "	border-radius: 5px;	\n"
            "	background-color: rgb(52, 59, 72);\n"
            "}\n"
            "QPushButton:hover {\n"
            "	background-color: rgb(57, 65, 80);\n"
            "	border: 2px solid rgb(61, 70, 86);\n"
            "}\n"
            "QPushButton:pressed {	\n"
            "	background-color: rgb(35, 40, 49);\n"
            "	border: 2px solid rgb(43, 50, 61);\n"
            "}"
        )
        self.btn_load_config = QPushButton(self.frame)
        self.btn_load_config.setObjectName("btn_load_config")
        self.btn_load_config.setGeometry(QRect(20, 640, 151, 41))
        self.btn_load_config.setFont(font2)
        self.btn_load_config.setStyleSheet(
            "QPushButton {\n"
            "	border: 2px solid rgb(52, 59, 72);\n"
            "	border-radius: 5px;	\n"
            "	background-color: rgb(52, 59, 72);\n"
            "}\n"
            "QPushButton:hover {\n"
            "	background-color: rgb(57, 65, 80);\n"
            "	border: 2px solid rgb(61, 70, 86);\n"
            "}\n"
            "QPushButton:pressed {	\n"
            "	background-color: rgb(35, 40, 49);\n"
            "	border: 2px solid rgb(43, 50, 61);\n"
            "}"
        )
        self.frame_object_main_type = QFrame(self.frame)
        self.frame_object_main_type.setObjectName("frame_object_main_type")
        self.frame_object_main_type.setGeometry(QRect(10, 30, 601, 111))
        self.frame_object_main_type.setStyleSheet(
            "#frame_object_names{\n"
            "border: 1px solid rgb(170, 170, 255);\n"
            "border-radius:15px;}\n"
            ""
        )
        self.frame_object_main_type.setFrameShape(QFrame.StyledPanel)
        self.frame_object_main_type.setFrameShadow(QFrame.Raised)
        self.le_custom_object_naming = QLineEdit(self.frame_object_main_type)
        self.le_custom_object_naming.setObjectName("le_custom_object_naming")
        self.le_custom_object_naming.setGeometry(QRect(10, 10, 321, 31))
        font7 = QFont()
        font7.setPointSize(11)
        font7.setBold(True)
        self.le_custom_object_naming.setFont(font7)
        self.cmb_object_main = InteractiveCombo(self.frame_object_main_type)
        self.cmb_object_main.setObjectName("cmb_object_main")
        self.cmb_object_main.setGeometry(QRect(10, 52, 301, 41))
        font8 = QFont()
        font8.setFamilies(["Segoe UI"])
        font8.setPointSize(12)
        self.cmb_object_main.setFont(font8)
        self.cmb_object_main.setStyleSheet(
            "QComboBox{\n"
            "	background-color: rgb(27, 29, 35);\n"
            "	border-radius: 5px;\n"
            "	border: 2px solid rgb(27, 29, 35);\n"
            "	padding: 5px;\n"
            "	padding-left: 10px;\n"
            "}\n"
            "QComboBox:hover{\n"
            "	border: 2px solid rgb(64, 71, 88);\n"
            "}\n"
            "QComboBox QAbstractItemView {\n"
            "	color: rgb(85, 170, 255);	\n"
            "	background-color: rgb(27, 29, 35);\n"
            "	padding: 10px;\n"
            "	selection-background-color: rgb(39, 44, 54);\n"
            "}"
        )
        self.cmb_object_main.setEditable(False)
        self.cmb_object_main.setInsertPolicy(QComboBox.InsertAlphabetically)
        self.frame_16 = QFrame(self.frame_object_main_type)
        self.frame_16.setObjectName("frame_16")
        self.frame_16.setGeometry(QRect(400, 10, 190, 91))
        self.frame_16.setFont(font1)
        # if QT_CONFIG(tooltip)
        self.frame_16.setToolTip("")
        # endif // QT_CONFIG(tooltip)
        self.frame_16.setStyleSheet("")
        self.frame_16.setFrameShape(QFrame.NoFrame)
        self.frame_16.setFrameShadow(QFrame.Raised)
        self.duo_main_type = QSlider(self.frame_16)
        self.duo_main_type.setObjectName("duo_main_type")
        self.duo_main_type.setGeometry(QRect(25, 30, 140, 22))
        self.duo_main_type.setFont(font1)
        self.duo_main_type.setMaximum(1)
        self.duo_main_type.setPageStep(1)
        self.duo_main_type.setOrientation(Qt.Horizontal)
        self.le_main_type_option_name = QLineEdit(self.frame_16)
        self.le_main_type_option_name.setObjectName("le_main_type_option_name")
        self.le_main_type_option_name.setGeometry(QRect(25, 5, 140, 22))
        self.le_main_type_option_name.setFont(font4)
        self.le_main_type_option_name.setAlignment(Qt.AlignCenter)
        self.le_main_type_option_value_0 = QLineEdit(self.frame_16)
        self.le_main_type_option_value_0.setObjectName("le_main_type_option_value_0")
        self.le_main_type_option_value_0.setGeometry(QRect(0, 60, 85, 22))
        self.le_main_type_option_value_0.setFont(font4)
        self.le_main_type_option_value_0.setFrame(True)
        self.le_main_type_option_value_0.setAlignment(Qt.AlignCenter)
        self.le_main_type_option_value_1 = QLineEdit(self.frame_16)
        self.le_main_type_option_value_1.setObjectName("le_main_type_option_value_1")
        self.le_main_type_option_value_1.setGeometry(QRect(90, 60, 85, 22))
        self.le_main_type_option_value_1.setFont(font4)
        self.le_main_type_option_value_1.setAlignment(Qt.AlignCenter)
        self.frame_meta_object = QFrame(self.frame)
        self.frame_meta_object.setObjectName("frame_meta_object")
        self.frame_meta_object.setGeometry(QRect(474, 320, 521, 421))
        self.frame_meta_object.setStyleSheet(
            "#frame_meta_object{\n"
            "border: 1px solid rgb(170, 170, 255);\n"
            "border-radius:15px;}\n"
            ""
        )
        self.frame_meta_object.setFrameShape(QFrame.StyledPanel)
        self.frame_meta_object.setFrameShadow(QFrame.Raised)
        self.frame_11 = QFrame(self.frame_meta_object)
        self.frame_11.setObjectName("frame_11")
        self.frame_11.setGeometry(QRect(265, 100, 250, 91))
        self.frame_11.setFont(font1)
        self.frame_11.setStyleSheet("")
        self.frame_11.setFrameShape(QFrame.NoFrame)
        self.frame_11.setFrameShadow(QFrame.Raised)
        self.triple_meta_4 = QSlider(self.frame_11)
        self.triple_meta_4.setObjectName("triple_meta_4")
        self.triple_meta_4.setGeometry(QRect(10, 30, 220, 22))
        self.triple_meta_4.setFont(font1)
        self.triple_meta_4.setMaximum(2)
        self.triple_meta_4.setPageStep(1)
        self.triple_meta_4.setOrientation(Qt.Horizontal)
        self.le_meta_triple_name_4 = QLineEdit(self.frame_11)
        self.le_meta_triple_name_4.setObjectName("le_meta_triple_name_4")
        self.le_meta_triple_name_4.setGeometry(QRect(50, 5, 150, 22))
        self.le_meta_triple_name_4.setFont(font4)
        self.le_meta_triple_4_value_0 = QLineEdit(self.frame_11)
        self.le_meta_triple_4_value_0.setObjectName("le_meta_triple_4_value_0")
        self.le_meta_triple_4_value_0.setGeometry(QRect(0, 60, 80, 22))
        self.le_meta_triple_4_value_0.setFont(font4)
        self.le_meta_triple_4_value_0.setAlignment(Qt.AlignCenter)
        self.le_meta_triple_4_value_1 = QLineEdit(self.frame_11)
        self.le_meta_triple_4_value_1.setObjectName("le_meta_triple_4_value_1")
        self.le_meta_triple_4_value_1.setGeometry(QRect(85, 60, 80, 22))
        self.le_meta_triple_4_value_1.setFont(font4)
        self.le_meta_triple_4_value_1.setAlignment(Qt.AlignCenter)
        self.le_meta_triple_4_value_2 = QLineEdit(self.frame_11)
        self.le_meta_triple_4_value_2.setObjectName("le_meta_triple_4_value_2")
        self.le_meta_triple_4_value_2.setGeometry(QRect(170, 60, 80, 22))
        self.le_meta_triple_4_value_2.setFont(font4)
        self.le_meta_triple_4_value_2.setAlignment(Qt.AlignCenter)
        self.cmb_meta_1 = InteractiveCombo(self.frame_meta_object)
        self.cmb_meta_1.setObjectName("cmb_meta_1")
        self.cmb_meta_1.setGeometry(QRect(10, 320, 155, 31))
        self.cmb_meta_1.setFont(font)
        self.cmb_meta_1.setStyleSheet(
            "QComboBox { color: white;background-color: rgb(27, 29, 35);}\n"
            "QComboBox QAbstractItemView {\n"
            "  color: white;background-color: rgb(27, 29, 35);\n"
            "}"
        )
        self.cmb_meta_1.setCurrentText("")
        self.le_meta_cmb_name_1 = QLineEdit(self.frame_meta_object)
        self.le_meta_cmb_name_1.setObjectName("le_meta_cmb_name_1")
        self.le_meta_cmb_name_1.setGeometry(QRect(10, 290, 155, 31))
        self.le_meta_cmb_name_1.setFont(font4)
        self.le_meta_cmb_name_1.setAlignment(Qt.AlignCenter)
        self.cmb_meta_2 = InteractiveCombo(self.frame_meta_object)
        self.cmb_meta_2.setObjectName("cmb_meta_2")
        self.cmb_meta_2.setGeometry(QRect(180, 320, 155, 31))
        self.cmb_meta_2.setFont(font)
        self.cmb_meta_2.setStyleSheet(
            "QComboBox { color: white;background-color: rgb(27, 29, 35);}\n"
            "QComboBox QAbstractItemView {\n"
            "  color: white;background-color: rgb(27, 29, 35);\n"
            "}"
        )
        self.cmb_meta_2.setCurrentText("")
        self.le_meta_cmb_name_2 = QLineEdit(self.frame_meta_object)
        self.le_meta_cmb_name_2.setObjectName("le_meta_cmb_name_2")
        self.le_meta_cmb_name_2.setGeometry(QRect(180, 290, 155, 31))
        self.le_meta_cmb_name_2.setFont(font4)
        self.le_meta_cmb_name_2.setAlignment(Qt.AlignCenter)
        self.cmb_meta_3 = InteractiveCombo(self.frame_meta_object)
        self.cmb_meta_3.setObjectName("cmb_meta_3")
        self.cmb_meta_3.setGeometry(QRect(350, 320, 155, 31))
        self.cmb_meta_3.setFont(font)
        self.cmb_meta_3.setStyleSheet(
            "QComboBox { color: white;background-color: rgb(27, 29, 35);}\n"
            "QComboBox QAbstractItemView {\n"
            "  color: white;background-color: rgb(27, 29, 35);\n"
            "}"
        )
        self.cmb_meta_3.setCurrentText("")
        self.le_meta_cmb_name_3 = QLineEdit(self.frame_meta_object)
        self.le_meta_cmb_name_3.setObjectName("le_meta_cmb_name_3")
        self.le_meta_cmb_name_3.setGeometry(QRect(350, 290, 155, 31))
        self.le_meta_cmb_name_3.setFont(font4)
        self.le_meta_cmb_name_3.setAlignment(Qt.AlignCenter)
        self.le_meta_input_txt_1 = QLineEdit(self.frame_meta_object)
        self.le_meta_input_txt_1.setObjectName("le_meta_input_txt_1")
        self.le_meta_input_txt_1.setGeometry(QRect(10, 370, 155, 31))
        self.le_meta_input_txt_1.setStyleSheet(
            "color: white;background-color: rgb(27, 29, 35);"
        )
        self.frame_12 = QFrame(self.frame_meta_object)
        self.frame_12.setObjectName("frame_12")
        self.frame_12.setGeometry(QRect(5, 100, 250, 91))
        self.frame_12.setFont(font1)
        self.frame_12.setStyleSheet("")
        self.frame_12.setFrameShape(QFrame.NoFrame)
        self.frame_12.setFrameShadow(QFrame.Raised)
        self.triple_meta_3 = QSlider(self.frame_12)
        self.triple_meta_3.setObjectName("triple_meta_3")
        self.triple_meta_3.setGeometry(QRect(15, 30, 220, 22))
        self.triple_meta_3.setFont(font1)
        self.triple_meta_3.setMaximum(2)
        self.triple_meta_3.setPageStep(1)
        self.triple_meta_3.setOrientation(Qt.Horizontal)
        self.le_meta_triple_name_3 = QLineEdit(self.frame_12)
        self.le_meta_triple_name_3.setObjectName("le_meta_triple_name_3")
        self.le_meta_triple_name_3.setGeometry(QRect(50, 5, 150, 22))
        self.le_meta_triple_name_3.setFont(font4)
        self.le_meta_triple_3_value_0 = QLineEdit(self.frame_12)
        self.le_meta_triple_3_value_0.setObjectName("le_meta_triple_3_value_0")
        self.le_meta_triple_3_value_0.setGeometry(QRect(0, 60, 80, 22))
        self.le_meta_triple_3_value_0.setFont(font4)
        self.le_meta_triple_3_value_0.setAlignment(Qt.AlignCenter)
        self.le_meta_triple_3_value_1 = QLineEdit(self.frame_12)
        self.le_meta_triple_3_value_1.setObjectName("le_meta_triple_3_value_1")
        self.le_meta_triple_3_value_1.setGeometry(QRect(85, 60, 80, 22))
        self.le_meta_triple_3_value_1.setFont(font4)
        self.le_meta_triple_3_value_1.setAlignment(Qt.AlignCenter)
        self.le_meta_triple_3_value_2 = QLineEdit(self.frame_12)
        self.le_meta_triple_3_value_2.setObjectName("le_meta_triple_3_value_2")
        self.le_meta_triple_3_value_2.setGeometry(QRect(170, 60, 80, 22))
        self.le_meta_triple_3_value_2.setFont(font4)
        self.le_meta_triple_3_value_2.setAlignment(Qt.AlignCenter)
        self.le_meta_input_txt_2 = QLineEdit(self.frame_meta_object)
        self.le_meta_input_txt_2.setObjectName("le_meta_input_txt_2")
        self.le_meta_input_txt_2.setGeometry(QRect(180, 370, 155, 31))
        self.le_meta_input_txt_2.setStyleSheet(
            "color: white;background-color: rgb(27, 29, 35);"
        )
        self.le_meta_input_txt_3 = QLineEdit(self.frame_meta_object)
        self.le_meta_input_txt_3.setObjectName("le_meta_input_txt_3")
        self.le_meta_input_txt_3.setGeometry(QRect(350, 370, 155, 31))
        self.le_meta_input_txt_3.setStyleSheet(
            "color: white;background-color: rgb(27, 29, 35);"
        )
        self.frame_8 = QFrame(self.frame_meta_object)
        self.frame_8.setObjectName("frame_8")
        self.frame_8.setGeometry(QRect(5, 200, 170, 81))
        self.frame_8.setFont(font1)
        self.frame_8.setStyleSheet("")
        self.frame_8.setFrameShape(QFrame.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.duo_meta_1 = QSlider(self.frame_8)
        self.duo_meta_1.setObjectName("duo_meta_1")
        self.duo_meta_1.setGeometry(QRect(20, 27, 130, 22))
        self.duo_meta_1.setFont(font1)
        self.duo_meta_1.setMaximum(1)
        self.duo_meta_1.setOrientation(Qt.Horizontal)
        self.le_meta_duo_name_1 = QLineEdit(self.frame_8)
        self.le_meta_duo_name_1.setObjectName("le_meta_duo_name_1")
        self.le_meta_duo_name_1.setGeometry(QRect(15, 0, 140, 22))
        self.le_meta_duo_name_1.setFont(font4)
        self.le_meta_duo_1_value_0 = QLineEdit(self.frame_8)
        self.le_meta_duo_1_value_0.setObjectName("le_meta_duo_1_value_0")
        self.le_meta_duo_1_value_0.setGeometry(QRect(0, 55, 80, 22))
        self.le_meta_duo_1_value_0.setFont(font4)
        self.le_meta_duo_1_value_1 = QLineEdit(self.frame_8)
        self.le_meta_duo_1_value_1.setObjectName("le_meta_duo_1_value_1")
        self.le_meta_duo_1_value_1.setGeometry(QRect(85, 55, 80, 22))
        self.le_meta_duo_1_value_1.setFont(font4)
        self.frame_9 = QFrame(self.frame_meta_object)
        self.frame_9.setObjectName("frame_9")
        self.frame_9.setGeometry(QRect(177, 200, 170, 81))
        self.frame_9.setFont(font1)
        self.frame_9.setStyleSheet("")
        self.frame_9.setFrameShape(QFrame.NoFrame)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.duo_meta_2 = QSlider(self.frame_9)
        self.duo_meta_2.setObjectName("duo_meta_2")
        self.duo_meta_2.setGeometry(QRect(20, 27, 130, 22))
        self.duo_meta_2.setFont(font1)
        self.duo_meta_2.setMaximum(1)
        self.duo_meta_2.setOrientation(Qt.Horizontal)
        self.le_meta_duo_name_2 = QLineEdit(self.frame_9)
        self.le_meta_duo_name_2.setObjectName("le_meta_duo_name_2")
        self.le_meta_duo_name_2.setGeometry(QRect(15, 0, 140, 22))
        self.le_meta_duo_name_2.setFont(font4)
        self.le_meta_duo_2_value_0 = QLineEdit(self.frame_9)
        self.le_meta_duo_2_value_0.setObjectName("le_meta_duo_2_value_0")
        self.le_meta_duo_2_value_0.setGeometry(QRect(0, 55, 80, 22))
        self.le_meta_duo_2_value_0.setFont(font4)
        self.le_meta_duo_2_value_1 = QLineEdit(self.frame_9)
        self.le_meta_duo_2_value_1.setObjectName("le_meta_duo_2_value_1")
        self.le_meta_duo_2_value_1.setGeometry(QRect(85, 55, 80, 22))
        self.le_meta_duo_2_value_1.setFont(font4)
        self.frame_13 = QFrame(self.frame_meta_object)
        self.frame_13.setObjectName("frame_13")
        self.frame_13.setGeometry(QRect(350, 200, 165, 81))
        self.frame_13.setFont(font1)
        self.frame_13.setStyleSheet("")
        self.frame_13.setFrameShape(QFrame.NoFrame)
        self.frame_13.setFrameShadow(QFrame.Raised)
        self.duo_meta_3 = QSlider(self.frame_13)
        self.duo_meta_3.setObjectName("duo_meta_3")
        self.duo_meta_3.setGeometry(QRect(20, 27, 130, 22))
        self.duo_meta_3.setFont(font1)
        self.duo_meta_3.setMaximum(1)
        self.duo_meta_3.setOrientation(Qt.Horizontal)
        self.le_meta_duo_name_3 = QLineEdit(self.frame_13)
        self.le_meta_duo_name_3.setObjectName("le_meta_duo_name_3")
        self.le_meta_duo_name_3.setGeometry(QRect(15, 0, 140, 22))
        self.le_meta_duo_name_3.setFont(font4)
        self.le_meta_duo_3_value_0 = QLineEdit(self.frame_13)
        self.le_meta_duo_3_value_0.setObjectName("le_meta_duo_3_value_0")
        self.le_meta_duo_3_value_0.setGeometry(QRect(0, 55, 80, 22))
        self.le_meta_duo_3_value_0.setFont(font4)
        self.le_meta_duo_3_value_1 = QLineEdit(self.frame_13)
        self.le_meta_duo_3_value_1.setObjectName("le_meta_duo_3_value_1")
        self.le_meta_duo_3_value_1.setGeometry(QRect(85, 55, 80, 22))
        self.le_meta_duo_3_value_1.setFont(font4)
        self.frame_14 = QFrame(self.frame_meta_object)
        self.frame_14.setObjectName("frame_14")
        self.frame_14.setGeometry(QRect(265, 5, 250, 91))
        self.frame_14.setFont(font1)
        self.frame_14.setStyleSheet("")
        self.frame_14.setFrameShape(QFrame.NoFrame)
        self.frame_14.setFrameShadow(QFrame.Raised)
        self.triple_meta_2 = QSlider(self.frame_14)
        self.triple_meta_2.setObjectName("triple_meta_2")
        self.triple_meta_2.setGeometry(QRect(15, 30, 220, 22))
        self.triple_meta_2.setFont(font1)
        self.triple_meta_2.setMaximum(2)
        self.triple_meta_2.setPageStep(1)
        self.triple_meta_2.setOrientation(Qt.Horizontal)
        self.le_meta_triple_name_2 = QLineEdit(self.frame_14)
        self.le_meta_triple_name_2.setObjectName("le_meta_triple_name_2")
        self.le_meta_triple_name_2.setGeometry(QRect(50, 5, 150, 22))
        self.le_meta_triple_name_2.setFont(font4)
        self.le_meta_triple_name_2.setAlignment(Qt.AlignCenter)
        self.le_meta_triple_2_value_0 = QLineEdit(self.frame_14)
        self.le_meta_triple_2_value_0.setObjectName("le_meta_triple_2_value_0")
        self.le_meta_triple_2_value_0.setGeometry(QRect(0, 60, 80, 22))
        self.le_meta_triple_2_value_0.setFont(font4)
        self.le_meta_triple_2_value_0.setAlignment(Qt.AlignCenter)
        self.le_meta_triple_2_value_1 = QLineEdit(self.frame_14)
        self.le_meta_triple_2_value_1.setObjectName("le_meta_triple_2_value_1")
        self.le_meta_triple_2_value_1.setGeometry(QRect(85, 60, 80, 22))
        self.le_meta_triple_2_value_1.setFont(font4)
        self.le_meta_triple_2_value_1.setAlignment(Qt.AlignCenter)
        self.le_meta_triple_2_value_2 = QLineEdit(self.frame_14)
        self.le_meta_triple_2_value_2.setObjectName("le_meta_triple_2_value_2")
        self.le_meta_triple_2_value_2.setGeometry(QRect(170, 60, 80, 22))
        self.le_meta_triple_2_value_2.setFont(font4)
        self.le_meta_triple_2_value_2.setAlignment(Qt.AlignCenter)
        self.frame_15 = QFrame(self.frame_meta_object)
        self.frame_15.setObjectName("frame_15")
        self.frame_15.setGeometry(QRect(5, 5, 250, 91))
        self.frame_15.setFont(font1)
        self.frame_15.setStyleSheet("")
        self.frame_15.setFrameShape(QFrame.NoFrame)
        self.frame_15.setFrameShadow(QFrame.Raised)
        self.triple_meta_1 = QSlider(self.frame_15)
        self.triple_meta_1.setObjectName("triple_meta_1")
        self.triple_meta_1.setGeometry(QRect(15, 30, 220, 22))
        self.triple_meta_1.setFont(font1)
        self.triple_meta_1.setMaximum(2)
        self.triple_meta_1.setPageStep(1)
        self.triple_meta_1.setOrientation(Qt.Horizontal)
        self.le_meta_triple_name_1 = QLineEdit(self.frame_15)
        self.le_meta_triple_name_1.setObjectName("le_meta_triple_name_1")
        self.le_meta_triple_name_1.setGeometry(QRect(50, 5, 150, 22))
        self.le_meta_triple_name_1.setFont(font4)
        self.le_meta_triple_name_1.setAlignment(Qt.AlignCenter)
        self.le_meta_triple_1_value_0 = QLineEdit(self.frame_15)
        self.le_meta_triple_1_value_0.setObjectName("le_meta_triple_1_value_0")
        self.le_meta_triple_1_value_0.setGeometry(QRect(0, 60, 80, 22))
        self.le_meta_triple_1_value_0.setFont(font4)
        self.le_meta_triple_1_value_0.setAlignment(Qt.AlignCenter)
        self.le_meta_triple_1_value_1 = QLineEdit(self.frame_15)
        self.le_meta_triple_1_value_1.setObjectName("le_meta_triple_1_value_1")
        self.le_meta_triple_1_value_1.setGeometry(QRect(85, 60, 80, 22))
        self.le_meta_triple_1_value_1.setFont(font4)
        self.le_meta_triple_1_value_1.setAlignment(Qt.AlignCenter)
        self.le_meta_triple_1_value_2 = QLineEdit(self.frame_15)
        self.le_meta_triple_1_value_2.setObjectName("le_meta_triple_1_value_2")
        self.le_meta_triple_1_value_2.setGeometry(QRect(170, 60, 80, 22))
        self.le_meta_triple_1_value_2.setFont(font4)
        self.le_meta_triple_1_value_2.setAlignment(Qt.AlignCenter)
        self.btn_clear = QPushButton(self.frame)
        self.btn_clear.setObjectName("btn_clear")
        self.btn_clear.setGeometry(QRect(20, 690, 151, 41))
        self.btn_clear.setFont(font2)
        self.btn_clear.setStyleSheet(
            "QPushButton {\n"
            "	border: 2px solid rgb(52, 59, 72);\n"
            "	border-radius: 5px;	\n"
            "	background-color: rgb(52, 59, 72);\n"
            "}\n"
            "QPushButton:hover {\n"
            "	background-color: rgb(57, 65, 80);\n"
            "	border: 2px solid rgb(61, 70, 86);\n"
            "}\n"
            "QPushButton:pressed {	\n"
            "	background-color: rgb(35, 40, 49);\n"
            "	border: 2px solid rgb(43, 50, 61);\n"
            "}"
        )
        self.rd_sub_type_active = QRadioButton(self.frame)
        self.rd_sub_type_active.setObjectName("rd_sub_type_active")
        self.rd_sub_type_active.setGeometry(QRect(590, 150, 161, 21))
        self.rd_sub_type_active.setFont(font6)
        self.rd_sub_type_active.setChecked(True)
        self.rd_sub_type_active.setAutoExclusive(False)
        self.btn_save_object_names = QPushButton(self.frame)
        self.btn_save_object_names.setObjectName("btn_save_object_names")
        self.btn_save_object_names.setGeometry(QRect(820, 50, 141, 41))
        self.btn_save_object_names.setFont(font2)
        self.btn_save_object_names.setStyleSheet(
            "QPushButton {\n"
            "	border: 2px solid rgb(52, 59, 72);\n"
            "	border-radius: 5px;	\n"
            "	background-color: rgb(52, 59, 72);\n"
            "}\n"
            "QPushButton:hover {\n"
            "	background-color: rgb(57, 65, 80);\n"
            "	border: 2px solid rgb(61, 70, 86);\n"
            "}\n"
            "QPushButton:pressed {	\n"
            "	background-color: rgb(35, 40, 49);\n"
            "	border: 2px solid rgb(43, 50, 61);\n"
            "}"
        )
        self.btn_load_object_names = QPushButton(self.frame)
        self.btn_load_object_names.setObjectName("btn_load_object_names")
        self.btn_load_object_names.setGeometry(QRect(650, 50, 161, 41))
        self.btn_load_object_names.setFont(font2)
        self.btn_load_object_names.setStyleSheet(
            "QPushButton {\n"
            "	border: 2px solid rgb(52, 59, 72);\n"
            "	border-radius: 5px;	\n"
            "	background-color: rgb(52, 59, 72);\n"
            "}\n"
            "QPushButton:hover {\n"
            "	background-color: rgb(57, 65, 80);\n"
            "	border: 2px solid rgb(61, 70, 86);\n"
            "}\n"
            "QPushButton:pressed {	\n"
            "	background-color: rgb(35, 40, 49);\n"
            "	border: 2px solid rgb(43, 50, 61);\n"
            "}"
        )
        self.frame_object_sub_types = QFrame(self.frame)
        self.frame_object_sub_types.setObjectName("frame_object_sub_types")
        self.frame_object_sub_types.setGeometry(QRect(385, 170, 611, 111))
        self.frame_object_sub_types.setStyleSheet(
            "#frame_object_sub_types{\n"
            "border: 1px solid rgb(170, 170, 255);\n"
            "border-radius:15px;}\n"
            ""
        )
        self.frame_object_sub_types.setFrameShape(QFrame.StyledPanel)
        self.frame_object_sub_types.setFrameShadow(QFrame.Raised)
        self.cmb_object_sub = InteractiveCombo(self.frame_object_sub_types)
        self.cmb_object_sub.setObjectName("cmb_object_sub")
        self.cmb_object_sub.setGeometry(QRect(10, 60, 301, 41))
        self.cmb_object_sub.setFont(font8)
        self.cmb_object_sub.setStyleSheet(
            "QComboBox{\n"
            "	background-color: rgb(27, 29, 35);\n"
            "	border-radius: 5px;\n"
            "	border: 2px solid rgb(27, 29, 35);\n"
            "	padding: 5px;\n"
            "	padding-left: 10px;\n"
            "}\n"
            "QComboBox:hover{\n"
            "	border: 2px solid rgb(64, 71, 88);\n"
            "}\n"
            "QComboBox QAbstractItemView {\n"
            "	color: rgb(85, 170, 255);	\n"
            "	background-color: rgb(27, 29, 35);\n"
            "	padding: 10px;\n"
            "	selection-background-color: rgb(39, 44, 54);\n"
            "}"
        )
        self.le_custom_object_sub_naming = QLineEdit(self.frame_object_sub_types)
        self.le_custom_object_sub_naming.setObjectName("le_custom_object_sub_naming")
        self.le_custom_object_sub_naming.setGeometry(QRect(10, 20, 321, 31))
        self.le_custom_object_sub_naming.setFont(font7)
        self.frame_17 = QFrame(self.frame_object_sub_types)
        self.frame_17.setObjectName("frame_17")
        self.frame_17.setGeometry(QRect(350, 10, 250, 83))
        self.frame_17.setFont(font1)
        self.frame_17.setStyleSheet("")
        self.frame_17.setFrameShape(QFrame.NoFrame)
        self.frame_17.setFrameShadow(QFrame.Raised)
        self.triple_sub_type = QSlider(self.frame_17)
        self.triple_sub_type.setObjectName("triple_sub_type")
        self.triple_sub_type.setGeometry(QRect(25, 30, 200, 22))
        self.triple_sub_type.setFont(font1)
        self.triple_sub_type.setMaximum(2)
        self.triple_sub_type.setPageStep(1)
        self.triple_sub_type.setOrientation(Qt.Horizontal)
        self.le_sub_type_option_name = QLineEdit(self.frame_17)
        self.le_sub_type_option_name.setObjectName("le_sub_type_option_name")
        self.le_sub_type_option_name.setGeometry(QRect(50, 5, 150, 22))
        self.le_sub_type_option_name.setFont(font4)
        self.le_sub_type_option_name.setAlignment(Qt.AlignCenter)
        self.le_sub_type_option_value_0 = QLineEdit(self.frame_17)
        self.le_sub_type_option_value_0.setObjectName("le_sub_type_option_value_0")
        self.le_sub_type_option_value_0.setGeometry(QRect(0, 60, 80, 22))
        self.le_sub_type_option_value_0.setFont(font4)
        self.le_sub_type_option_value_0.setAlignment(Qt.AlignCenter)
        self.le_sub_type_option_value_1 = QLineEdit(self.frame_17)
        self.le_sub_type_option_value_1.setObjectName("le_sub_type_option_value_1")
        self.le_sub_type_option_value_1.setGeometry(QRect(85, 60, 80, 22))
        self.le_sub_type_option_value_1.setFont(font4)
        self.le_sub_type_option_value_1.setAlignment(Qt.AlignCenter)
        self.le_sub_type_option_value_2 = QLineEdit(self.frame_17)
        self.le_sub_type_option_value_2.setObjectName("le_sub_type_option_value_2")
        self.le_sub_type_option_value_2.setGeometry(QRect(170, 60, 80, 22))
        self.le_sub_type_option_value_2.setFont(font4)
        self.le_sub_type_option_value_2.setAlignment(Qt.AlignCenter)
        self.frame_7 = QFrame(self.frame)
        self.frame_7.setObjectName("frame_7")
        self.frame_7.setGeometry(QRect(20, 190, 131, 61))
        self.frame_7.setFont(font1)
        self.frame_7.setStyleSheet("")
        self.frame_7.setFrameShape(QFrame.NoFrame)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.slider_certainty = QSlider(self.frame_7)
        self.slider_certainty.setObjectName("slider_certainty")
        self.slider_certainty.setEnabled(False)
        self.slider_certainty.setGeometry(QRect(10, 20, 111, 22))
        self.slider_certainty.setFont(font1)
        self.slider_certainty.setMaximum(1)
        self.slider_certainty.setValue(1)
        self.slider_certainty.setOrientation(Qt.Horizontal)
        self.label_19 = QLabel(self.frame_7)
        self.label_19.setObjectName("label_19")
        self.label_19.setGeometry(QRect(30, 0, 71, 16))
        font9 = QFont()
        font9.setFamilies(["Segoe UI"])
        font9.setPointSize(11)
        font9.setBold(True)
        self.label_19.setFont(font9)
        self.label_20 = QLabel(self.frame_7)
        self.label_20.setObjectName("label_20")
        self.label_20.setGeometry(QRect(10, 40, 31, 21))
        self.label_20.setFont(font9)
        self.label_21 = QLabel(self.frame_7)
        self.label_21.setObjectName("label_21")
        self.label_21.setGeometry(QRect(100, 40, 31, 21))
        self.label_21.setFont(font9)
        self.frame_5 = QFrame(self.frame)
        self.frame_5.setObjectName("frame_5")
        self.frame_5.setGeometry(QRect(170, 190, 91, 61))
        self.frame_5.setFont(font1)
        self.frame_5.setStyleSheet("")
        self.frame_5.setFrameShape(QFrame.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.slider_first_certain = QSlider(self.frame_5)
        self.slider_first_certain.setObjectName("slider_first_certain")
        self.slider_first_certain.setEnabled(False)
        self.slider_first_certain.setGeometry(QRect(10, 20, 81, 22))
        self.slider_first_certain.setFont(font1)
        self.slider_first_certain.setMaximum(1)
        self.slider_first_certain.setValue(1)
        self.slider_first_certain.setOrientation(Qt.Horizontal)
        self.label_10 = QLabel(self.frame_5)
        self.label_10.setObjectName("label_10")
        self.label_10.setGeometry(QRect(20, 0, 71, 16))
        self.label_10.setFont(font)
        self.label_11 = QLabel(self.frame_5)
        self.label_11.setObjectName("label_11")
        self.label_11.setGeometry(QRect(10, 40, 31, 21))
        self.label_11.setFont(font)
        self.label_12 = QLabel(self.frame_5)
        self.label_12.setObjectName("label_12")
        self.label_12.setGeometry(QRect(70, 40, 31, 21))
        self.label_12.setFont(font)
        self.frame_6 = QFrame(self.frame)
        self.frame_6.setObjectName("frame_6")
        self.frame_6.setGeometry(QRect(270, 190, 81, 61))
        self.frame_6.setFont(font1)
        self.frame_6.setStyleSheet("")
        self.frame_6.setFrameShape(QFrame.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.slider_resight = QSlider(self.frame_6)
        self.slider_resight.setObjectName("slider_resight")
        self.slider_resight.setEnabled(False)
        self.slider_resight.setGeometry(QRect(10, 20, 70, 22))
        self.slider_resight.setFont(font1)
        self.slider_resight.setMaximum(1)
        self.slider_resight.setOrientation(Qt.Horizontal)
        self.label_13 = QLabel(self.frame_6)
        self.label_13.setObjectName("label_13")
        self.label_13.setGeometry(QRect(20, 0, 51, 16))
        self.label_13.setFont(font)
        self.label_14 = QLabel(self.frame_6)
        self.label_14.setObjectName("label_14")
        self.label_14.setGeometry(QRect(10, 40, 31, 21))
        self.label_14.setFont(font)
        self.label_15 = QLabel(self.frame_6)
        self.label_15.setObjectName("label_15")
        self.label_15.setGeometry(QRect(60, 40, 21, 21))
        self.label_15.setFont(font)
        self.frame_certainty_show = QFrame(self.frame)
        self.frame_certainty_show.setObjectName("frame_certainty_show")
        self.frame_certainty_show.setGeometry(QRect(20, 170, 341, 111))
        self.frame_certainty_show.setStyleSheet(
            "#frame_certainty_show{\n"
            "border: 0px solid rgb(170, 170, 255);\n"
            "background: rgba(34, 36, 50,150);\n"
            "border-radius:15px;}\n"
            ""
        )
        self.frame_certainty_show.setFrameShape(QFrame.StyledPanel)
        self.frame_certainty_show.setFrameShadow(QFrame.Raised)
        self.label_9 = QLabel(self.frame)
        self.label_9.setObjectName("label_9")
        self.label_9.setGeometry(QRect(130, 160, 121, 16))
        self.label_9.setStyleSheet(
            "border: 1px solid rgba(170, 170, 255,100);\nborder-radius:15px;"
        )
        self.label_9.setAlignment(Qt.AlignCenter)
        self.frame_object_sub_types.raise_()
        self.frame_environment.raise_()
        self.btn_save_config.raise_()
        self.btn_submit.raise_()
        self.btn_load_config.raise_()
        self.frame_object_main_type.raise_()
        self.frame_meta_object.raise_()
        self.btn_clear.raise_()
        self.rd_sub_type_active.raise_()
        self.btn_save_object_names.raise_()
        self.btn_load_object_names.raise_()
        self.frame_7.raise_()
        self.frame_5.raise_()
        self.frame_6.raise_()
        self.frame_certainty_show.raise_()
        self.label_9.raise_()

        self.horizontalLayout_2.addWidget(self.frame)

        self.verticalLayout.addWidget(self.frame_center)

        QWidget.setTabOrder(self.btn_load_object_names, self.btn_save_object_names)
        QWidget.setTabOrder(self.btn_save_object_names, self.le_custom_object_naming)
        QWidget.setTabOrder(self.le_custom_object_naming, self.cmb_object_main)
        QWidget.setTabOrder(self.cmb_object_main, self.le_custom_1)
        QWidget.setTabOrder(self.le_custom_1, self.cmb_custom_1)
        QWidget.setTabOrder(self.cmb_custom_1, self.le_custom_2)
        QWidget.setTabOrder(self.le_custom_2, self.cmb_custom_2)
        QWidget.setTabOrder(self.cmb_custom_2, self.cmb_custom_3)
        QWidget.setTabOrder(self.cmb_custom_3, self.le_custom_4)
        QWidget.setTabOrder(self.le_custom_4, self.cmb_custom_4)
        QWidget.setTabOrder(self.cmb_custom_4, self.le_custom_5)
        QWidget.setTabOrder(self.le_custom_5, self.cmb_custom_5)
        QWidget.setTabOrder(self.cmb_custom_5, self.le_custom_6)
        QWidget.setTabOrder(self.le_custom_6, self.cmb_custom_6)
        QWidget.setTabOrder(self.cmb_custom_6, self.btn_load_config)
        QWidget.setTabOrder(self.btn_load_config, self.btn_save_config)
        QWidget.setTabOrder(self.btn_save_config, self.btn_submit)
        QWidget.setTabOrder(self.btn_submit, self.btn_close)
        QWidget.setTabOrder(self.btn_close, self.triple_meta_4)

        self.retranslateUi(popup_project_config)

        QMetaObject.connectSlotsByName(popup_project_config)

    # setupUi

    def retranslateUi(self, popup_project_config):
        popup_project_config.setWindowTitle(
            QCoreApplication.translate("popup_project_config", "MainWindow", None)
        )
        self.lbl_icon.setText("")
        # if QT_CONFIG(tooltip)
        self.label_title.setToolTip(
            QCoreApplication.translate(
                "popup_project_config",
                '<html><head/><body><p><span style=" font-size:8pt; font-weight:400;">Move window</span></p></body></html>',
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.label_title.setText(
            QCoreApplication.translate("popup_project_config", "CREATE PROJECT", None)
        )
        self.cmb_custom_2.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "right click edit", None)
        )
        self.cmb_custom_1.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "right click edit", None)
        )
        self.cmb_custom_3.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "right click edit", None)
        )
        self.cmb_custom_5.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "right click edit", None)
        )
        self.cmb_custom_4.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "right click edit", None)
        )
        self.cmb_custom_6.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "right click edit", None)
        )
        self.le_custom_1.setText("")
        self.le_custom_1.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "Enter Field Name", None)
        )
        self.le_custom_2.setText("")
        self.le_custom_2.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "Enter Field Name", None)
        )
        self.le_custom_4.setText("")
        self.le_custom_4.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "Enter Field Name", None)
        )
        self.le_custom_5.setText("")
        self.le_custom_5.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "Enter Field Name", None)
        )
        self.le_custom_6.setText("")
        self.le_custom_6.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "Enter Field Name", None)
        )
        self.label_7.setText(
            QCoreApplication.translate(
                "popup_project_config",
                "ENVIRONMENT\n"
                "Enter Name for image variables (e.g. turbidity, cloudy).\n"
                "With right click you can edit members",
                None,
            )
        )
        self.le_custom_3.setText("")
        self.le_custom_3.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "Enter Field Name", None)
        )
        self.btn_save_config.setText(
            QCoreApplication.translate(
                "popup_project_config", "Save Project File", None
            )
        )
        self.btn_submit.setText(
            QCoreApplication.translate("popup_project_config", "Start Project", None)
        )
        self.btn_load_config.setText(
            QCoreApplication.translate(
                "popup_project_config", "Load Project File", None
            )
        )
        self.le_custom_object_naming.setText("")
        self.le_custom_object_naming.setPlaceholderText(
            QCoreApplication.translate(
                "popup_project_config",
                "Enter Obejct Main Type Naming (e.g. Taxa)",
                None,
            )
        )
        self.cmb_object_main.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "right click edit", None)
        )
        self.le_main_type_option_name.setText("")
        self.le_main_type_option_name.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "Enter Field Name", None)
        )
        self.le_main_type_option_value_0.setText("")
        self.le_main_type_option_value_0.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "Value", None)
        )
        self.le_main_type_option_value_1.setText("")
        self.le_main_type_option_value_1.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "Value", None)
        )
        self.le_meta_triple_name_4.setText("")
        self.le_meta_triple_name_4.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "Enter Field Name", None)
        )
        self.le_meta_triple_4_value_0.setText("")
        self.le_meta_triple_4_value_0.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "Value", None)
        )
        self.le_meta_triple_4_value_1.setText("")
        self.le_meta_triple_4_value_1.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "Value", None)
        )
        self.le_meta_triple_4_value_2.setText("")
        self.le_meta_triple_4_value_2.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "Value", None)
        )
        self.cmb_meta_1.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "right click edit", None)
        )
        self.le_meta_cmb_name_1.setText("")
        self.le_meta_cmb_name_1.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "Enter Field Name", None)
        )
        self.cmb_meta_2.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "right click edit", None)
        )
        self.le_meta_cmb_name_2.setText("")
        self.le_meta_cmb_name_2.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "Enter Field Name", None)
        )
        self.cmb_meta_3.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "right click edit", None)
        )
        self.le_meta_cmb_name_3.setText("")
        self.le_meta_cmb_name_3.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "Enter Field Name", None)
        )
        self.le_meta_input_txt_1.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "Variable Name", None)
        )
        self.le_meta_triple_name_3.setText("")
        self.le_meta_triple_name_3.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "Enter Field Name", None)
        )
        self.le_meta_triple_3_value_0.setText("")
        self.le_meta_triple_3_value_0.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "Value", None)
        )
        self.le_meta_triple_3_value_1.setText("")
        self.le_meta_triple_3_value_1.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "Value", None)
        )
        self.le_meta_triple_3_value_2.setText("")
        self.le_meta_triple_3_value_2.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "Value", None)
        )
        self.le_meta_input_txt_2.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "Variable Name", None)
        )
        self.le_meta_input_txt_3.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "Variable Name", None)
        )
        self.le_meta_duo_name_1.setText("")
        self.le_meta_duo_name_1.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "Enter Field Name", None)
        )
        self.le_meta_duo_1_value_0.setText("")
        self.le_meta_duo_1_value_0.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "Value", None)
        )
        self.le_meta_duo_1_value_1.setText("")
        self.le_meta_duo_1_value_1.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "Value", None)
        )
        self.le_meta_duo_name_2.setText("")
        self.le_meta_duo_name_2.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "Enter Field Name", None)
        )
        self.le_meta_duo_2_value_0.setText("")
        self.le_meta_duo_2_value_0.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "Value", None)
        )
        self.le_meta_duo_2_value_1.setText("")
        self.le_meta_duo_2_value_1.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "Value", None)
        )
        self.le_meta_duo_name_3.setText("")
        self.le_meta_duo_name_3.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "Enter Field Name", None)
        )
        self.le_meta_duo_3_value_0.setText("")
        self.le_meta_duo_3_value_0.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "Value", None)
        )
        self.le_meta_duo_3_value_1.setText("")
        self.le_meta_duo_3_value_1.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "Value", None)
        )
        self.le_meta_triple_name_2.setText("")
        self.le_meta_triple_name_2.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "Enter Field Name", None)
        )
        self.le_meta_triple_2_value_0.setText("")
        self.le_meta_triple_2_value_0.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "Value", None)
        )
        self.le_meta_triple_2_value_1.setText("")
        self.le_meta_triple_2_value_1.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "Value", None)
        )
        self.le_meta_triple_2_value_2.setText("")
        self.le_meta_triple_2_value_2.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "Value", None)
        )
        self.le_meta_triple_name_1.setText("")
        self.le_meta_triple_name_1.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "Enter Field Name", None)
        )
        self.le_meta_triple_1_value_0.setText("")
        self.le_meta_triple_1_value_0.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "Value", None)
        )
        self.le_meta_triple_1_value_1.setText("")
        self.le_meta_triple_1_value_1.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "Value", None)
        )
        self.le_meta_triple_1_value_2.setText("")
        self.le_meta_triple_1_value_2.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "Value", None)
        )
        self.btn_clear.setText(
            QCoreApplication.translate("popup_project_config", "Clear Everything", None)
        )
        self.rd_sub_type_active.setText(
            QCoreApplication.translate(
                "popup_project_config", "Activate Sub-Types", None
            )
        )
        self.btn_save_object_names.setText(
            QCoreApplication.translate(
                "popup_project_config", "Save Object Types", None
            )
        )
        self.btn_load_object_names.setText(
            QCoreApplication.translate(
                "popup_project_config", "Load Object Types", None
            )
        )
        self.cmb_object_sub.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "right click edit", None)
        )
        self.le_custom_object_sub_naming.setText("")
        self.le_custom_object_sub_naming.setPlaceholderText(
            QCoreApplication.translate(
                "popup_project_config", "Enter Obejct Sub Naming (e.g. Species)", None
            )
        )
        self.le_sub_type_option_name.setText("")
        self.le_sub_type_option_name.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "Enter Field Name", None)
        )
        self.le_sub_type_option_value_0.setText("")
        self.le_sub_type_option_value_0.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "Value", None)
        )
        self.le_sub_type_option_value_1.setText("")
        self.le_sub_type_option_value_1.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "Value", None)
        )
        self.le_sub_type_option_value_2.setText("")
        self.le_sub_type_option_value_2.setPlaceholderText(
            QCoreApplication.translate("popup_project_config", "Value", None)
        )
        self.label_19.setText(
            QCoreApplication.translate("popup_project_config", "Certainty", None)
        )
        self.label_20.setText(
            QCoreApplication.translate("popup_project_config", "no", None)
        )
        self.label_21.setText(
            QCoreApplication.translate("popup_project_config", "yes", None)
        )
        self.label_10.setText(
            QCoreApplication.translate("popup_project_config", "First Certain", None)
        )
        self.label_11.setText(
            QCoreApplication.translate("popup_project_config", "no", None)
        )
        self.label_12.setText(
            QCoreApplication.translate("popup_project_config", "yes", None)
        )
        self.label_13.setText(
            QCoreApplication.translate("popup_project_config", "Resight", None)
        )
        self.label_14.setText(
            QCoreApplication.translate("popup_project_config", "no", None)
        )
        self.label_15.setText(
            QCoreApplication.translate("popup_project_config", "yes", None)
        )
        self.label_9.setText(
            QCoreApplication.translate(
                "popup_project_config", "Standard Parameter", None
            )
        )

    # retranslateUi
