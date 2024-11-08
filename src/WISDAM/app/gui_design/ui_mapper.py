# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui_mapper.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QPlainTextEdit, QPushButton, QRadioButton,
    QSizePolicy, QVBoxLayout, QWidget)
from . import files_rc

class Ui_popup_mapper(object):
    def setupUi(self, popup_mapper):
        if not popup_mapper.objectName():
            popup_mapper.setObjectName(u"popup_mapper")
        popup_mapper.resize(950, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(popup_mapper.sizePolicy().hasHeightForWidth())
        popup_mapper.setSizePolicy(sizePolicy)
        popup_mapper.setMinimumSize(QSize(950, 600))
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(0, 0, 0, 0))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush1)
        brush2 = QBrush(QColor(66, 73, 90, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Light, brush2)
        brush3 = QBrush(QColor(55, 61, 75, 255))
        brush3.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Midlight, brush3)
        brush4 = QBrush(QColor(22, 24, 30, 255))
        brush4.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Dark, brush4)
        brush5 = QBrush(QColor(29, 32, 40, 255))
        brush5.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Mid, brush5)
        brush6 = QBrush(QColor(210, 210, 210, 255))
        brush6.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Text, brush6)
        palette.setBrush(QPalette.Active, QPalette.BrightText, brush)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette.setBrush(QPalette.Active, QPalette.Window, brush1)
        brush7 = QBrush(QColor(0, 0, 0, 255))
        brush7.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Shadow, brush7)
        brush8 = QBrush(QColor(85, 170, 255, 255))
        brush8.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Highlight, brush8)
        palette.setBrush(QPalette.Active, QPalette.Link, brush8)
        brush9 = QBrush(QColor(255, 0, 127, 255))
        brush9.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.LinkVisited, brush9)
        palette.setBrush(QPalette.Active, QPalette.AlternateBase, brush4)
        brush10 = QBrush(QColor(44, 49, 60, 255))
        brush10.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.ToolTipBase, brush10)
        palette.setBrush(QPalette.Active, QPalette.ToolTipText, brush6)
        brush11 = QBrush(QColor(210, 210, 210, 128))
        brush11.setStyle(Qt.SolidPattern)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Active, QPalette.PlaceholderText, brush11)
#endif
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Light, brush2)
        palette.setBrush(QPalette.Inactive, QPalette.Midlight, brush3)
        palette.setBrush(QPalette.Inactive, QPalette.Dark, brush4)
        palette.setBrush(QPalette.Inactive, QPalette.Mid, brush5)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush6)
        palette.setBrush(QPalette.Inactive, QPalette.BrightText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Shadow, brush7)
        palette.setBrush(QPalette.Inactive, QPalette.Highlight, brush8)
        palette.setBrush(QPalette.Inactive, QPalette.Link, brush8)
        palette.setBrush(QPalette.Inactive, QPalette.LinkVisited, brush9)
        palette.setBrush(QPalette.Inactive, QPalette.AlternateBase, brush4)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush10)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipText, brush6)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush11)
#endif
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Light, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.Midlight, brush3)
        palette.setBrush(QPalette.Disabled, QPalette.Dark, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Mid, brush5)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.BrightText, brush)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Shadow, brush7)
        brush12 = QBrush(QColor(51, 153, 255, 255))
        brush12.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Highlight, brush12)
        palette.setBrush(QPalette.Disabled, QPalette.Link, brush8)
        palette.setBrush(QPalette.Disabled, QPalette.LinkVisited, brush9)
        palette.setBrush(QPalette.Disabled, QPalette.AlternateBase, brush10)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush10)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipText, brush6)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush11)
#endif
        popup_mapper.setPalette(palette)
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(10)
        popup_mapper.setFont(font)
        popup_mapper.setStyleSheet(u"QWidget {background: transparent; color: rgb(210, 210, 210)}\n"
"QToolTip {\n"
"	color: #ffffff;\n"
"	background-color: rgba(27, 29, 35, 160);\n"
"	border: 1px solid rgb(40, 40, 40);\n"
"	border-radius: 2px;\n"
"}")
        self.verticalLayout = QVBoxLayout(popup_mapper)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_main = QFrame(popup_mapper)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setStyleSheet(u"/* LINE EDIT */\n"
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
"QPlainTextEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"\n"
"QPlainTextEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding-left: 10px;\n"
"}\n"
"\n"
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
"    background: rgb(85, 170, 255);\n"
"    min-width: 25px;\n"
"	border-radius: 7px\n"
"}\n"
"QScrollBar::add-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"	border-top-right-radi"
                        "us: 7px;\n"
"    border-bottom-right-radius: 7px;\n"
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
"	background: rgb(85, 170, 255);\n"
"    min-height: 25px;\n"
"	border-radius: 7px\n"
" }\n"
" QScrollBar::add-line:vertical {\n"
"     border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20"
                        "px;\n"
"	border-bottom-left-radius: 7px;\n"
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
"	border: 3px soli"
                        "d rgb(52, 59, 72);\n"
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
"	background-"
                        "image: url(:/icons/icons/ico-arrow-bottom.png);\n"
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
""
                        "    margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
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
"")
        self.frame_main.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_main.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_main)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_top = QFrame(self.frame_main)
        self.frame_top.setObjectName(u"frame_top")
        self.frame_top.setMinimumSize(QSize(0, 40))
        self.frame_top.setMaximumSize(QSize(16777215, 40))
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        self.frame_top.setFont(font1)
        self.frame_top.setStyleSheet(u"background-color:rgb(127, 84, 0);\n"
"color: white;")
        self.frame_top.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_top.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_top)
        self.horizontalLayout_4.setSpacing(10)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(10, 0, 0, 0)
        self.lbl_icon = QLabel(self.frame_top)
        self.lbl_icon.setObjectName(u"lbl_icon")
        self.lbl_icon.setMinimumSize(QSize(30, 30))
        self.lbl_icon.setMaximumSize(QSize(30, 30))
        self.lbl_icon.setPixmap(QPixmap(u":/icons/icons/WISDAM_Icon_square_small.svg"))

        self.horizontalLayout_4.addWidget(self.lbl_icon)

        self.label_title = QLabel(self.frame_top)
        self.label_title.setObjectName(u"label_title")
        font2 = QFont()
        font2.setFamilies([u"Segoe UI"])
        font2.setPointSize(10)
        font2.setBold(True)
        self.label_title.setFont(font2)
        self.label_title.setStyleSheet(u"background: transparent;\n"
"")
        self.label_title.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_4.addWidget(self.label_title)

        self.btn_close = QPushButton(self.frame_top)
        self.btn_close.setObjectName(u"btn_close")
        self.btn_close.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.btn_close.sizePolicy().hasHeightForWidth())
        self.btn_close.setSizePolicy(sizePolicy1)
        self.btn_close.setMinimumSize(QSize(40, 0))
        self.btn_close.setMaximumSize(QSize(40, 16777215))
        self.btn_close.setFont(font1)
#if QT_CONFIG(tooltip)
        self.btn_close.setToolTip(u"Close")
#endif // QT_CONFIG(tooltip)
        self.btn_close.setStyleSheet(u"QPushButton {	\n"
"	border: none;\n"
"	background-color: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(150, 40, 23);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(250, 39, 10);\n"
"}")
        self.btn_close.setText(u"")
        icon = QIcon()
        icon.addFile(u":/icons/icons/ico-x.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_close.setIcon(icon)

        self.horizontalLayout_4.addWidget(self.btn_close)


        self.verticalLayout_2.addWidget(self.frame_top)

        self.frame_center = QFrame(self.frame_main)
        self.frame_center.setObjectName(u"frame_center")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.frame_center.sizePolicy().hasHeightForWidth())
        self.frame_center.setSizePolicy(sizePolicy2)
        self.frame_center.setFont(font1)
        self.frame_center.setStyleSheet(u"background-color: rgb(34, 36, 50);")
        self.frame_center.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_center.setFrameShadow(QFrame.Shadow.Raised)
        self.btn_save = QPushButton(self.frame_center)
        self.btn_save.setObjectName(u"btn_save")
        self.btn_save.setGeometry(QRect(80, 500, 131, 31))
        self.btn_save.setFont(font2)
        self.btn_save.setStyleSheet(u"QPushButton {\n"
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
"}")
        self.btn_discard = QPushButton(self.frame_center)
        self.btn_discard.setObjectName(u"btn_discard")
        self.btn_discard.setGeometry(QRect(240, 500, 141, 31))
        self.btn_discard.setFont(font2)
        self.btn_discard.setStyleSheet(u"QPushButton {\n"
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
"}")
        self.rd_select_plane_mapper = QRadioButton(self.frame_center)
        self.rd_select_plane_mapper.setObjectName(u"rd_select_plane_mapper")
        self.rd_select_plane_mapper.setGeometry(QRect(130, 10, 211, 21))
        font3 = QFont()
        font3.setPointSize(13)
        font3.setBold(True)
        self.rd_select_plane_mapper.setFont(font3)
        self.rd_select_raster_mapper = QRadioButton(self.frame_center)
        self.rd_select_raster_mapper.setObjectName(u"rd_select_raster_mapper")
        self.rd_select_raster_mapper.setGeometry(QRect(620, 10, 211, 21))
        self.rd_select_raster_mapper.setFont(font3)
        self.frame_plane_mapper = QFrame(self.frame_center)
        self.frame_plane_mapper.setObjectName(u"frame_plane_mapper")
        self.frame_plane_mapper.setGeometry(QRect(20, 50, 451, 211))
        self.frame_plane_mapper.setStyleSheet(u"#frame_plane_mapper{\n"
"		border: 1px solid rgb(170, 170, 255);\n"
"		border-radius:15px;}")
        self.frame_plane_mapper.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_plane_mapper.setFrameShadow(QFrame.Shadow.Raised)
        self.le_plane_height = QLineEdit(self.frame_plane_mapper)
        self.le_plane_height.setObjectName(u"le_plane_height")
        self.le_plane_height.setGeometry(QRect(160, 10, 281, 41))
        font4 = QFont()
        font4.setPointSize(10)
        font4.setBold(True)
        self.le_plane_height.setFont(font4)
        self.le_plane_height.setStyleSheet(u"QLineEdit{background-color: rgb(52, 59, 72);\n"
"}\n"
"QLineEdit:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"")
        self.label_7 = QLabel(self.frame_plane_mapper)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(10, 20, 151, 21))
        font5 = QFont()
        font5.setPointSize(12)
        font5.setBold(True)
        self.label_7.setFont(font5)
        self.pltext_plane_crs = QPlainTextEdit(self.frame_plane_mapper)
        self.pltext_plane_crs.setObjectName(u"pltext_plane_crs")
        self.pltext_plane_crs.setGeometry(QRect(110, 70, 331, 91))
        font6 = QFont()
        font6.setBold(True)
        self.pltext_plane_crs.setFont(font6)
        self.pltext_plane_crs.setStyleSheet(u"")
        self.pltext_plane_crs.setFrameShape(QFrame.Shape.Box)
        self.pltext_plane_crs.setFrameShadow(QFrame.Shadow.Plain)
        self.pltext_plane_crs.setReadOnly(True)
        self.label_10 = QLabel(self.frame_plane_mapper)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(10, 70, 91, 21))
        self.label_10.setFont(font5)
        self.btn_set_std_crs = QPushButton(self.frame_plane_mapper)
        self.btn_set_std_crs.setObjectName(u"btn_set_std_crs")
        self.btn_set_std_crs.setGeometry(QRect(10, 170, 431, 31))
        self.btn_set_std_crs.setFont(font2)
        self.btn_set_std_crs.setStyleSheet(u"QPushButton {\n"
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
"}")
        self.frame_raster_mapper = QFrame(self.frame_center)
        self.frame_raster_mapper.setObjectName(u"frame_raster_mapper")
        self.frame_raster_mapper.setGeometry(QRect(480, 50, 461, 501))
        self.frame_raster_mapper.setStyleSheet(u"#frame_raster_mapper{\n"
"		border: 1px solid rgb(170, 170, 255);\n"
"		border-radius:15px;}")
        self.frame_raster_mapper.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_raster_mapper.setFrameShadow(QFrame.Shadow.Raised)
        self.btn_select_raster = QPushButton(self.frame_raster_mapper)
        self.btn_select_raster.setObjectName(u"btn_select_raster")
        self.btn_select_raster.setGeometry(QRect(20, 460, 431, 31))
        self.btn_select_raster.setFont(font2)
        self.btn_select_raster.setStyleSheet(u"QPushButton {\n"
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
"}")
        self.label = QLabel(self.frame_raster_mapper)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(90, 310, 301, 21))
        self.label.setFont(font3)
        self.label_2 = QLabel(self.frame_raster_mapper)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(90, 350, 351, 21))
        self.label_2.setFont(font3)
        self.led_raster_geo_transform = QPushButton(self.frame_raster_mapper)
        self.led_raster_geo_transform.setObjectName(u"led_raster_geo_transform")
        self.led_raster_geo_transform.setGeometry(QRect(50, 350, 21, 21))
        self.led_raster_geo_transform.setStyleSheet(u"color: white;border-radius: 20;\n"
"        background-color: qlineargradient(spread:pad, x1:0.145, y1:0.16, x2:1, y2:1, stop:0 rgba(255, 25, 7, 255),\n"
"        stop:1 rgba(134, 25, 5, 255));")
        self.led_rasterio_possible = QPushButton(self.frame_raster_mapper)
        self.led_rasterio_possible.setObjectName(u"led_rasterio_possible")
        self.led_rasterio_possible.setGeometry(QRect(50, 310, 21, 21))
        self.led_rasterio_possible.setStyleSheet(u"color: white;border-radius: 20;\n"
"        background-color: qlineargradient(spread:pad, x1:0.145, y1:0.16, x2:1, y2:1, stop:0 rgba(255, 25, 7, 255),\n"
"        stop:1 rgba(134, 25, 5, 255));")
        self.le_raster_pixel_size = QLineEdit(self.frame_raster_mapper)
        self.le_raster_pixel_size.setObjectName(u"le_raster_pixel_size")
        self.le_raster_pixel_size.setGeometry(QRect(120, 90, 331, 31))
        self.le_raster_pixel_size.setReadOnly(True)
        self.le_raster_pixel_size.setClearButtonEnabled(False)
        self.pltext_raster_filepath = QPlainTextEdit(self.frame_raster_mapper)
        self.pltext_raster_filepath.setObjectName(u"pltext_raster_filepath")
        self.pltext_raster_filepath.setGeometry(QRect(120, 10, 331, 71))
        self.pltext_raster_filepath.setStyleSheet(u"")
        self.pltext_raster_filepath.setFrameShape(QFrame.Shape.Box)
        self.pltext_raster_filepath.setFrameShadow(QFrame.Shadow.Plain)
        self.pltext_raster_filepath.setReadOnly(True)
        self.label_4 = QLabel(self.frame_raster_mapper)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(20, 90, 81, 16))
        self.label_4.setFont(font5)
        self.label_8 = QLabel(self.frame_raster_mapper)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(20, 140, 91, 21))
        self.label_8.setFont(font5)
        self.pltext_raster_crs = QPlainTextEdit(self.frame_raster_mapper)
        self.pltext_raster_crs.setObjectName(u"pltext_raster_crs")
        self.pltext_raster_crs.setGeometry(QRect(120, 140, 331, 151))
        self.pltext_raster_crs.setFont(font6)
        self.pltext_raster_crs.setStyleSheet(u"")
        self.pltext_raster_crs.setFrameShape(QFrame.Shape.Box)
        self.pltext_raster_crs.setFrameShadow(QFrame.Shadow.Plain)
        self.pltext_raster_crs.setReadOnly(True)
        self.label_9 = QLabel(self.frame_raster_mapper)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(20, 10, 81, 16))
        self.label_9.setFont(font5)
        self.label_3 = QLabel(self.frame_raster_mapper)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(90, 390, 221, 21))
        self.label_3.setFont(font3)
        self.led_raster_crs = QPushButton(self.frame_raster_mapper)
        self.led_raster_crs.setObjectName(u"led_raster_crs")
        self.led_raster_crs.setGeometry(QRect(50, 390, 21, 21))
        self.led_raster_crs.setStyleSheet(u"color: white;border-radius: 20;\n"
"        background-color: qlineargradient(spread:pad, x1:0.145, y1:0.16, x2:1, y2:1, stop:0 rgba(255, 25, 7, 255),\n"
"        stop:1 rgba(134, 25, 5, 255));")
        self.label_5 = QLabel(self.frame_raster_mapper)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(90, 430, 221, 21))
        self.label_5.setFont(font3)
        self.led_raster_is_vertical = QPushButton(self.frame_raster_mapper)
        self.led_raster_is_vertical.setObjectName(u"led_raster_is_vertical")
        self.led_raster_is_vertical.setGeometry(QRect(50, 430, 21, 21))
        self.led_raster_is_vertical.setStyleSheet(u"color: white;border-radius: 20;\n"
"        background-color: qlineargradient(spread:pad, x1:0.145, y1:0.16, x2:1, y2:1, stop:0 rgba(255, 25, 7, 255),\n"
"        stop:1 rgba(134, 25, 5, 255));")
        self.custom_env_layout = QFrame(self.frame_center)
        self.custom_env_layout.setObjectName(u"custom_env_layout")
        self.custom_env_layout.setGeometry(QRect(20, 270, 451, 141))
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.custom_env_layout.sizePolicy().hasHeightForWidth())
        self.custom_env_layout.setSizePolicy(sizePolicy3)
        self.custom_env_layout.setMinimumSize(QSize(0, 0))
        self.custom_env_layout.setMaximumSize(QSize(16777215, 16777215))
        self.custom_env_layout.setStyleSheet(u"#custom_env_layout{\n"
"border: 1px solid rgb(170, 170, 255);\n"
"border-radius:15px;}\n"
"")
        self.custom_env_layout.setFrameShape(QFrame.Shape.StyledPanel)
        self.custom_env_layout.setFrameShadow(QFrame.Shadow.Raised)
        self.rd_crs_manual = QRadioButton(self.custom_env_layout)
        self.rd_crs_manual.setObjectName(u"rd_crs_manual")
        self.rd_crs_manual.setGeometry(QRect(20, 30, 141, 31))
        font7 = QFont()
        font7.setPointSize(11)
        font7.setBold(True)
        self.rd_crs_manual.setFont(font7)
        self.rd_crs_manual.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.le_manual_crs = QLineEdit(self.custom_env_layout)
        self.le_manual_crs.setObjectName(u"le_manual_crs")
        self.le_manual_crs.setGeometry(QRect(10, 70, 201, 41))
        self.le_manual_crs.setFont(font4)
        self.le_manual_crs.setStyleSheet(u"QLineEdit{background-color: rgb(52, 59, 72);\n"
"}\n"
"QLineEdit:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"")
        self.label_11 = QLabel(self.custom_env_layout)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(220, 20, 211, 101))
        self.label_11.setFont(font5)
        self.label_11.raise_()
        self.rd_crs_manual.raise_()
        self.le_manual_crs.raise_()
        self.rd_recalculate = QRadioButton(self.frame_center)
        self.rd_recalculate.setObjectName(u"rd_recalculate")
        self.rd_recalculate.setGeometry(QRect(80, 460, 311, 21))
        self.rd_recalculate.setFont(font3)
        self.rd_recalculate.setAutoExclusive(False)

        self.verticalLayout_2.addWidget(self.frame_center)


        self.verticalLayout.addWidget(self.frame_main)


        self.retranslateUi(popup_mapper)

        QMetaObject.connectSlotsByName(popup_mapper)
    # setupUi

    def retranslateUi(self, popup_mapper):
        popup_mapper.setWindowTitle(QCoreApplication.translate("popup_mapper", u"MainWindow", None))
        self.lbl_icon.setText("")
#if QT_CONFIG(tooltip)
        self.label_title.setToolTip(QCoreApplication.translate("popup_mapper", u"<html><head/><body><p><span style=\" font-size:8pt; font-weight:400;\">Move window</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_title.setText(QCoreApplication.translate("popup_mapper", u"MAPPER CONFIGURATION", None))
        self.btn_save.setText(QCoreApplication.translate("popup_mapper", u"Save", None))
        self.btn_discard.setText(QCoreApplication.translate("popup_mapper", u"Discard", None))
        self.rd_select_plane_mapper.setText(QCoreApplication.translate("popup_mapper", u"Horizontal Ground", None))
        self.rd_select_raster_mapper.setText(QCoreApplication.translate("popup_mapper", u"Raster File", None))
        self.label_7.setText(QCoreApplication.translate("popup_mapper", u"Ground Height [m]:", None))
        self.label_10.setText(QCoreApplication.translate("popup_mapper", u"CRS System:", None))
        self.btn_set_std_crs.setText(QCoreApplication.translate("popup_mapper", u"Use standrd CRS system( geoid height, aka MSL)", None))
        self.btn_select_raster.setText(QCoreApplication.translate("popup_mapper", u"Select Raster File", None))
        self.label.setText(QCoreApplication.translate("popup_mapper", u"Possible to open with RasterIO", None))
        self.label_2.setText(QCoreApplication.translate("popup_mapper", u"Raster Geo-Transform/World File available", None))
        self.led_raster_geo_transform.setText("")
        self.led_rasterio_possible.setText("")
        self.label_4.setText(QCoreApplication.translate("popup_mapper", u"Pixel Size:", None))
        self.label_8.setText(QCoreApplication.translate("popup_mapper", u"CRS System:", None))
        self.label_9.setText(QCoreApplication.translate("popup_mapper", u"File Path:", None))
        self.label_3.setText(QCoreApplication.translate("popup_mapper", u"CRS System Available", None))
        self.led_raster_crs.setText("")
        self.label_5.setText(QCoreApplication.translate("popup_mapper", u"CRS is Vertical System", None))
        self.led_raster_is_vertical.setText("")
        self.rd_crs_manual.setText(QCoreApplication.translate("popup_mapper", u"Set CRS", None))
        self.label_11.setText(QCoreApplication.translate("popup_mapper", u"EPSG Code:\n"
"Specify the vertical Datum,\n"
"If not a 3d System\n"
"e.g. \"EPSG:4326+3855\"", None))
        self.rd_recalculate.setText(QCoreApplication.translate("popup_mapper", u"Recalculate Objects and Footrpints", None))
    # retranslateUi

