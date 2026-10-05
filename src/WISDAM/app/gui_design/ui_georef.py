# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui_georef.ui'
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
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.custom_elements.spinningWaiter import QtWaitingSpinner
from . import files_rc


class Ui_popup_georef(object):
    def setupUi(self, popup_georef):
        if not popup_georef.objectName():
            popup_georef.setObjectName("popup_georef")
        popup_georef.resize(600, 500)
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(popup_georef.sizePolicy().hasHeightForWidth())
        popup_georef.setSizePolicy(sizePolicy)
        popup_georef.setMinimumSize(QSize(600, 500))
        popup_georef.setMaximumSize(QSize(600, 500))
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
        popup_georef.setPalette(palette)
        font = QFont()
        font.setFamilies(["Segoe UI"])
        font.setPointSize(9)
        popup_georef.setFont(font)
        popup_georef.setStyleSheet(
            "QWidget {background: transparent; color: rgb(210, 210, 210)}\n"
            "QToolTip {\n"
            "	color: #ffffff;\n"
            "	background-color: rgba(27, 29, 35, 160);\n"
            "	border: 1px solid rgb(40, 40, 40);\n"
            "	border-radius: 2px;\n"
            "}\n"
            ""
        )
        self.verticalLayout = QVBoxLayout(popup_georef)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_main = QFrame(popup_georef)
        self.frame_main.setObjectName("frame_main")
        sizePolicy.setHeightForWidth(self.frame_main.sizePolicy().hasHeightForWidth())
        self.frame_main.setSizePolicy(sizePolicy)
        self.frame_main.setMinimumSize(QSize(0, 0))
        self.frame_main.setMaximumSize(QSize(600, 500))
        font1 = QFont()
        font1.setFamilies(["Segoe UI"])
        self.frame_main.setFont(font1)
        self.frame_main.setStyleSheet(
            "/* LINE EDIT */\n"
            "QLineEdit {\n"
            "	background-color: rgb(27, 29, 35);\n"
            "	border-radius: 5px;\n"
            "	border: 2px solid rgb(27, 29, 35);\n"
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
            "	background: rgb(178, 186, 87);\n"
            "    min-width: 25px;\n"
            "	border-radius: 7px\n"
            "}\n"
            "QScrollBar::add-line:horizontal {\n"
            "    border: none;\n"
            "    background: rgb(55, 63, 77);\n"
            "    width: 20px;\n"
            "	border-top-right-radius: 7px;\n"
            "    border-bottom-right-radius: 7px;\n"
            "    subcontrol-position: right;\n"
            "    subcontrol-origin: margin;\n"
            "}\n"
            "QScrollBar::sub-line:horizontal {\n"
            "    border: none;\n"
            "    background: rgb(55, 63, 77);\n"
            "    width: 20px;\n"
            ""
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
            "	border-bottom-left-radius: 7px;\n"
            "    border-bottom-right-radius: 7px;\n"
            "     subcontrol-position: bottom;\n"
            "     subcontrol-origin: margin;\n"
            " }\n"
            " QScrollBar::sub-line:vertical {\n"
            "	border: none;\n"
            "    background: rgb(55, 63"
            ", 77);\n"
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
            "	border: 3px solid rgb(52, 59, 72);	\n"
            "}\n"
            "\n"
            "/* RADIO BUTTON */\n"
            "QRadioButton::indicator {\n"
            "    border: 3px solid rgb(52, 59, 72);\n"
            "	width: 15px;\n"
            "	height: 15px;\n"
            "	border-radius: 10px;\n"
            "    background: rgb(44, 49, 60);\n"
            "}\n"
            "QRadioButton"
            "::indicator:hover {\n"
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
            "	background-image: url(:/icons/icons/ico-arrow-bottom.png);\n"
            "	background-position: center;\n"
            "	background-repeat: no-reperat;\n"
            " }\n"
            "QComboBox QAbstractItemView {\n"
            "	color: rgb(85, 170, 255);	\n"
            "	background-color: rgb(27, 29, 35);\n"
            "	padding: 10p"
            "x;\n"
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
            "    background-color: rgb(85, 170, 255);\n"
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
            "	background-color: rgb(52, 59, 72);\n"
            "}\n"
            "QSlider::groove:vertical:hover {\n"
            "	background-color: rgb(55, 62, 76);\n"
            "}\n"
            "QSlider::handle:vertical {\n"
            "    background-color: rgb(85, 170, 255);\n"
            "	border: none;\n"
            ""
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
            "QPlainTextEdit {\n"
            "	background-color: rgb(92,99, 112);\n"
            "	border-radius: 5px;\n"
            "	border: 2px solid rgb(27, 29, 35);\n"
            "	padding-left: 10px;\n"
            "}\n"
            "QPlainTextEdit:hover {\n"
            "	border: 2px solid rgb(64, 71, 88);\n"
            "}\n"
            "QPlainTextEdit:focus {\n"
            "	border: 2px solid rgb(91, 101, 124);\n"
            "}\n"
            ""
        )
        self.frame_main.setFrameShape(QFrame.NoFrame)
        self.frame_main.setFrameShadow(QFrame.Raised)
        self.frame_main.setLineWidth(1)
        self.verticalLayout_4 = QVBoxLayout(self.frame_main)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frame_top = QFrame(self.frame_main)
        self.frame_top.setObjectName("frame_top")
        sizePolicy.setHeightForWidth(self.frame_top.sizePolicy().hasHeightForWidth())
        self.frame_top.setSizePolicy(sizePolicy)
        self.frame_top.setMinimumSize(QSize(0, 40))
        self.frame_top.setMaximumSize(QSize(16777215, 40))
        self.frame_top.setFont(font1)
        self.frame_top.setStyleSheet("background-color:rgb(127, 84, 0);\ncolor: white;")
        self.frame_top.setFrameShape(QFrame.NoFrame)
        self.frame_top.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_top)
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(10, 0, 0, 0)
        self.lbl_icon = QLabel(self.frame_top)
        self.lbl_icon.setObjectName("lbl_icon")
        self.lbl_icon.setMinimumSize(QSize(30, 30))
        self.lbl_icon.setMaximumSize(QSize(30, 30))
        self.lbl_icon.setPixmap(QPixmap(":/icons/icons/WISDAM_Icon_square_small.svg"))

        self.horizontalLayout_2.addWidget(self.lbl_icon)

        self.label_title = QLabel(self.frame_top)
        self.label_title.setObjectName("label_title")
        font2 = QFont()
        font2.setFamilies(["Segoe UI"])
        font2.setPointSize(10)
        font2.setBold(True)
        self.label_title.setFont(font2)
        self.label_title.setStyleSheet("background: transparent;\n")
        self.label_title.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_2.addWidget(self.label_title)

        self.label_info = QLabel(self.frame_top)
        self.label_info.setObjectName("label_info")
        font3 = QFont()
        font3.setPointSize(9)
        font3.setBold(True)
        self.label_info.setFont(font3)
        self.label_info.setLayoutDirection(Qt.RightToLeft)
        self.label_info.setStyleSheet("color: rgb(255, 85, 0)")
        self.label_info.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.label_info)

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
            "	background-color: rgb(103, 40, 23);\n"
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

        self.horizontalLayout_2.addWidget(self.btn_close)

        self.verticalLayout_4.addWidget(self.frame_top)

        self.frame = QFrame(self.frame_main)
        self.frame.setObjectName("frame")
        sizePolicy2 = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy2)
        self.frame.setMaximumSize(QSize(16777215, 16777215))
        self.frame.setFont(font1)
        self.frame.setStyleSheet("background-color: rgb(34, 36, 50);")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.input_height_above_ground = QLineEdit(self.frame)
        self.input_height_above_ground.setObjectName("input_height_above_ground")
        self.input_height_above_ground.setGeometry(QRect(30, 250, 151, 31))
        font4 = QFont()
        font4.setPointSize(10)
        self.input_height_above_ground.setFont(font4)
        self.input_height_above_ground.setStyleSheet(
            "background-color: rgb(52, 59, 72);"
        )
        self.input_sensor_width = QLineEdit(self.frame)
        self.input_sensor_width.setObjectName("input_sensor_width")
        self.input_sensor_width.setGeometry(QRect(160, 20, 111, 31))
        self.input_sensor_width.setFont(font4)
        self.input_sensor_width.setStyleSheet("background-color:rgb(255, 85, 0)")
        self.label_44 = QLabel(self.frame)
        self.label_44.setObjectName("label_44")
        self.label_44.setGeometry(QRect(20, 20, 121, 20))
        font5 = QFont()
        font5.setPointSize(10)
        font5.setBold(True)
        self.label_44.setFont(font5)
        self.input_latitude = QLineEdit(self.frame)
        self.input_latitude.setObjectName("input_latitude")
        self.input_latitude.setGeometry(QRect(30, 130, 151, 31))
        self.input_latitude.setFont(font4)
        self.input_latitude.setStyleSheet("background-color: rgb(52, 59, 72);")
        self.label_32 = QLabel(self.frame)
        self.label_32.setObjectName("label_32")
        self.label_32.setGeometry(QRect(30, 170, 101, 20))
        self.label_32.setFont(font5)
        self.input_longitude = QLineEdit(self.frame)
        self.input_longitude.setObjectName("input_longitude")
        self.input_longitude.setGeometry(QRect(30, 190, 151, 31))
        self.input_longitude.setFont(font4)
        self.input_longitude.setStyleSheet("background-color: rgb(52, 59, 72);")
        self.label_33 = QLabel(self.frame)
        self.label_33.setObjectName("label_33")
        self.label_33.setGeometry(QRect(30, 110, 81, 20))
        self.label_33.setFont(font5)
        self.btn_save = QPushButton(self.frame)
        self.btn_save.setObjectName("btn_save")
        self.btn_save.setGeometry(QRect(30, 390, 121, 41))
        self.btn_save.setFont(font2)
        self.btn_save.setStyleSheet(
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
        self.label_34 = QLabel(self.frame)
        self.label_34.setObjectName("label_34")
        self.label_34.setGeometry(QRect(30, 230, 171, 20))
        self.label_34.setFont(font5)
        self.stackedWidget = QStackedWidget(self.frame)
        self.stackedWidget.setObjectName("stackedWidget")
        self.stackedWidget.setGeometry(QRect(200, 110, 381, 271))
        self.stackedWidget.setFont(font3)
        self.stackedWidget.setStyleSheet(
            "QTabWidget::pane {\n"
            "  border: 0px solid lightgray;\n"
            "  top:-1px; \n"
            "} \n"
            "\n"
            "QTabBar::tab {\n"
            "  background: rgb(35, 40, 49); \n"
            "  border: 0px solid lightgray; \n"
            "  padding: 15px;\n"
            "} \n"
            "\n"
            "QTabBar::tab:selected { \n"
            "  background: rgb(92,99, 112); \n"
            "  margin-bottom: -1px; \n"
            "}"
        )
        self.heading_page = QWidget()
        self.heading_page.setObjectName("heading_page")
        self.label_36 = QLabel(self.heading_page)
        self.label_36.setObjectName("label_36")
        self.label_36.setGeometry(QRect(170, 30, 191, 31))
        self.label_36.setFont(font5)
        self.label_36.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.input_heading = QLineEdit(self.heading_page)
        self.input_heading.setObjectName("input_heading")
        self.input_heading.setGeometry(QRect(10, 30, 151, 31))
        self.input_heading.setFont(font4)
        self.input_heading.setStyleSheet("background-color: rgb(52, 59, 72);")
        self.widget = QWidget(self.heading_page)
        self.widget.setObjectName("widget")
        self.widget.setGeometry(QRect(50, 80, 251, 181))
        self.widget.setStyleSheet("image:url(:/icons/icons/heading_info.svg)")
        self.stackedWidget.addWidget(self.heading_page)
        self.opk_page = QWidget()
        self.opk_page.setObjectName("opk_page")
        self.label_37 = QLabel(self.opk_page)
        self.label_37.setObjectName("label_37")
        self.label_37.setGeometry(QRect(20, 20, 81, 20))
        self.label_37.setFont(font5)
        self.input_kappa = QLineEdit(self.opk_page)
        self.input_kappa.setObjectName("input_kappa")
        self.input_kappa.setGeometry(QRect(20, 160, 151, 31))
        self.input_kappa.setFont(font4)
        self.input_kappa.setStyleSheet("background-color: rgb(52, 59, 72);")
        self.label_38 = QLabel(self.opk_page)
        self.label_38.setObjectName("label_38")
        self.label_38.setGeometry(QRect(20, 80, 101, 20))
        self.label_38.setFont(font5)
        self.label_39 = QLabel(self.opk_page)
        self.label_39.setObjectName("label_39")
        self.label_39.setGeometry(QRect(20, 140, 101, 20))
        self.label_39.setFont(font5)
        self.input_phi = QLineEdit(self.opk_page)
        self.input_phi.setObjectName("input_phi")
        self.input_phi.setGeometry(QRect(20, 100, 151, 31))
        self.input_phi.setFont(font4)
        self.input_phi.setStyleSheet("background-color: rgb(52, 59, 72);")
        self.input_omega = QLineEdit(self.opk_page)
        self.input_omega.setObjectName("input_omega")
        self.input_omega.setGeometry(QRect(20, 40, 151, 31))
        self.input_omega.setFont(font4)
        self.input_omega.setStyleSheet("background-color: rgb(52, 59, 72);")
        self.stackedWidget.addWidget(self.opk_page)
        self.rpy_page = QWidget()
        self.rpy_page.setObjectName("rpy_page")
        self.label_40 = QLabel(self.rpy_page)
        self.label_40.setObjectName("label_40")
        self.label_40.setGeometry(QRect(20, 80, 101, 20))
        self.label_40.setFont(font5)
        self.label_41 = QLabel(self.rpy_page)
        self.label_41.setObjectName("label_41")
        self.label_41.setGeometry(QRect(20, 140, 101, 20))
        self.label_41.setFont(font5)
        self.input_pitch = QLineEdit(self.rpy_page)
        self.input_pitch.setObjectName("input_pitch")
        self.input_pitch.setGeometry(QRect(20, 100, 151, 31))
        self.input_pitch.setFont(font4)
        self.input_pitch.setStyleSheet("background-color: rgb(52, 59, 72);")
        self.input_yaw = QLineEdit(self.rpy_page)
        self.input_yaw.setObjectName("input_yaw")
        self.input_yaw.setGeometry(QRect(20, 160, 151, 31))
        self.input_yaw.setFont(font4)
        self.input_yaw.setStyleSheet("background-color: rgb(52, 59, 72);")
        self.label_42 = QLabel(self.rpy_page)
        self.label_42.setObjectName("label_42")
        self.label_42.setGeometry(QRect(20, 20, 81, 20))
        self.label_42.setFont(font5)
        self.input_roll = QLineEdit(self.rpy_page)
        self.input_roll.setObjectName("input_roll")
        self.input_roll.setGeometry(QRect(20, 40, 151, 31))
        self.input_roll.setFont(font4)
        self.input_roll.setStyleSheet("background-color: rgb(52, 59, 72);")
        self.stackedWidget.addWidget(self.rpy_page)
        self.frame_spinner = QFrame(self.frame)
        self.frame_spinner.setObjectName("frame_spinner")
        self.frame_spinner.setEnabled(True)
        self.frame_spinner.setGeometry(QRect(40, 350, 100, 100))
        self.frame_spinner.setMinimumSize(QSize(100, 100))
        self.frame_spinner.setMaximumSize(QSize(100, 100))
        self.frame_spinner.setFrameShape(QFrame.StyledPanel)
        self.frame_spinner.setFrameShadow(QFrame.Raised)
        self.waiting_spinner = QtWaitingSpinner(self.frame_spinner)
        self.waiting_spinner.setObjectName("waiting_spinner")
        self.waiting_spinner.setEnabled(True)
        self.waiting_spinner.setGeometry(QRect(5, 5, 90, 90))
        sizePolicy.setHeightForWidth(
            self.waiting_spinner.sizePolicy().hasHeightForWidth()
        )
        self.waiting_spinner.setSizePolicy(sizePolicy)
        self.waiting_spinner.setMinimumSize(QSize(90, 90))
        self.waiting_spinner.setMaximumSize(QSize(90, 90))
        self.waiting_spinner.setBaseSize(QSize(0, 50))
        self.cmb_angles = QComboBox(self.frame)
        self.cmb_angles.addItem("")
        self.cmb_angles.addItem("")
        self.cmb_angles.addItem("")
        self.cmb_angles.setObjectName("cmb_angles")
        self.cmb_angles.setGeometry(QRect(200, 70, 381, 41))
        self.cmb_angles.setFont(font5)
        self.cmb_angles.setStyleSheet(
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
        self.lbl_info = QLabel(self.frame)
        self.lbl_info.setObjectName("lbl_info")
        self.lbl_info.setGeometry(QRect(200, 390, 371, 61))
        font6 = QFont()
        font6.setPointSize(11)
        font6.setBold(True)
        self.lbl_info.setFont(font6)
        self.lbl_info.setStyleSheet("color: rgb(255, 85, 0)")
        self.input_focal_mm = QLineEdit(self.frame)
        self.input_focal_mm.setObjectName("input_focal_mm")
        self.input_focal_mm.setGeometry(QRect(430, 20, 111, 31))
        self.input_focal_mm.setFont(font4)
        self.input_focal_mm.setStyleSheet("background-color: rgb(52, 59, 72);")
        self.label_46 = QLabel(self.frame)
        self.label_46.setObjectName("label_46")
        self.label_46.setGeometry(QRect(300, 20, 121, 20))
        self.label_46.setFont(font5)

        self.verticalLayout_4.addWidget(self.frame)

        self.verticalLayout.addWidget(self.frame_main)

        self.retranslateUi(popup_georef)

        self.stackedWidget.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(popup_georef)

    # setupUi

    def retranslateUi(self, popup_georef):
        popup_georef.setWindowTitle(
            QCoreApplication.translate("popup_georef", "MainWindow", None)
        )
        self.lbl_icon.setText("")
        # if QT_CONFIG(tooltip)
        self.label_title.setToolTip(
            QCoreApplication.translate(
                "popup_georef",
                '<html><head/><body><p><span style=" font-size:8pt; font-weight:400;">Move window</span></p></body></html>',
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.label_title.setText(
            QCoreApplication.translate("popup_georef", "GEOREFERENCE", None)
        )
        self.label_info.setText(
            QCoreApplication.translate(
                "popup_georef", "Can not be used for Orthophotos.  ", None
            )
        )
        self.input_sensor_width.setText("")
        self.label_44.setText(
            QCoreApplication.translate("popup_georef", "Sensor width [mm]", None)
        )
        self.input_latitude.setText("")
        self.label_32.setText(
            QCoreApplication.translate("popup_georef", "Longitude [\u00b0]", None)
        )
        self.label_33.setText(
            QCoreApplication.translate("popup_georef", "Latitude [\u00b0]", None)
        )
        self.btn_save.setText(
            QCoreApplication.translate("popup_georef", "Save and\nRecalculate", None)
        )
        self.label_34.setText(
            QCoreApplication.translate("popup_georef", "Height above Ground [m]", None)
        )
        self.label_36.setText(
            QCoreApplication.translate(
                "popup_georef", "Heading [\u00b0]\nClassic Compass convention", None
            )
        )
        self.input_heading.setText(
            QCoreApplication.translate("popup_georef", "0.0", None)
        )
        self.label_37.setText(
            QCoreApplication.translate("popup_georef", "Omega [\u00b0]", None)
        )
        self.input_kappa.setText(
            QCoreApplication.translate("popup_georef", "0.0", None)
        )
        self.label_38.setText(
            QCoreApplication.translate("popup_georef", "Phi [\u00b0]", None)
        )
        self.label_39.setText(
            QCoreApplication.translate("popup_georef", "Kappa [\u00b0]", None)
        )
        self.input_phi.setText(QCoreApplication.translate("popup_georef", "0.0", None))
        self.input_omega.setText(
            QCoreApplication.translate("popup_georef", "0.0", None)
        )
        self.label_40.setText(
            QCoreApplication.translate("popup_georef", "Pitch [\u00b0]", None)
        )
        self.label_41.setText(
            QCoreApplication.translate("popup_georef", "Yaw [\u00b0]", None)
        )
        self.input_pitch.setText(
            QCoreApplication.translate("popup_georef", "0.0", None)
        )
        self.input_yaw.setText(QCoreApplication.translate("popup_georef", "0.0", None))
        self.label_42.setText(
            QCoreApplication.translate("popup_georef", "Roll [\u00b0]", None)
        )
        self.input_roll.setText(QCoreApplication.translate("popup_georef", "0.0", None))
        self.cmb_angles.setItemText(
            0, QCoreApplication.translate("popup_georef", "Heading only", None)
        )
        self.cmb_angles.setItemText(
            1, QCoreApplication.translate("popup_georef", "Omega - Phi - Kappa", None)
        )
        self.cmb_angles.setItemText(
            2, QCoreApplication.translate("popup_georef", "Roll - Pitch - Yaw", None)
        )

        self.lbl_info.setText("")
        self.input_focal_mm.setText("")
        self.label_46.setText(
            QCoreApplication.translate("popup_georef", "Focal length [mm]", None)
        )

    # retranslateUi
