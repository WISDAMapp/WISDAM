# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui_meta.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSlider, QTextEdit, QVBoxLayout, QWidget)

from app.custom_elements.comboInteractive import InteractiveCombo
from app.custom_elements.layoutEnvironment import EnvironmentLayout
from . import files_rc

class Ui_popup_meta(object):
    def setupUi(self, popup_meta):
        if not popup_meta.objectName():
            popup_meta.setObjectName(u"popup_meta")
        popup_meta.resize(1020, 794)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(popup_meta.sizePolicy().hasHeightForWidth())
        popup_meta.setSizePolicy(sizePolicy)
        popup_meta.setMinimumSize(QSize(950, 600))
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
        popup_meta.setPalette(palette)
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(10)
        popup_meta.setFont(font)
        popup_meta.setStyleSheet(u"QWidget {background: transparent; color: rgb(210, 210, 210)}\n"
"QToolTip {\n"
"	color: #ffffff;\n"
"	background-color: rgba(27, 29, 35, 160);\n"
"	border: 1px solid rgb(40, 40, 40);\n"
"	border-radius: 2px;\n"
"}\n"
"\n"
"QLabel {\n"
"	\n"
"	color: rgb(150, 150, 150);\n"
"}\n"
"\n"
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
"    background: rgb(178, 186, 87);\n"
"    min-width: 25px;\n"
"	border-radius: 7px\n"
"}\n"
"QScrollBar::add-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"   "
                        " width: 20px;\n"
"	border-top-right-radius: 7px;\n"
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
"	background: rgb(178, 186, 87);\n"
"    min-height: 25px;\n"
"	border-radius: 7px\n"
" }\n"
" QScrollBar::add-line:vertical {\n"
"     border: none;\n"
"    backgrou"
                        "nd: rgb(55, 63, 77);\n"
"     height: 20px;\n"
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
"    background: 3px soli"
                        "d rgb(52, 59, 72);\n"
"	border: 3px solid rgb(52, 59, 72);\n"
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
"	border-bot"
                        "tom-right-radius: 3px;	\n"
"	background-image: url(:/icons/icons/ico-arrow-bottom.png);\n"
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
"    b"
                        "order-radius: 9px;\n"
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
        self.verticalLayout = QVBoxLayout(popup_meta)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_top = QFrame(popup_meta)
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
        self.horizontalLayout = QHBoxLayout(self.frame_top)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(10, 0, 0, 0)
        self.lbl_icon = QLabel(self.frame_top)
        self.lbl_icon.setObjectName(u"lbl_icon")
        self.lbl_icon.setMinimumSize(QSize(30, 30))
        self.lbl_icon.setMaximumSize(QSize(30, 30))
        self.lbl_icon.setPixmap(QPixmap(u":/icons/icons/WISDAM_Icon_square_small.svg"))

        self.horizontalLayout.addWidget(self.lbl_icon)

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

        self.horizontalLayout.addWidget(self.label_title)

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

        self.horizontalLayout.addWidget(self.btn_close)


        self.verticalLayout.addWidget(self.frame_top)

        self.frame_center = QFrame(popup_meta)
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
        self.btn_save.setGeometry(QRect(240, 700, 201, 41))
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
        self.cropped_image = QLabel(self.frame_center)
        self.cropped_image.setObjectName(u"cropped_image")
        self.cropped_image.setGeometry(QRect(35, 10, 400, 400))
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.cropped_image.sizePolicy().hasHeightForWidth())
        self.cropped_image.setSizePolicy(sizePolicy3)
        self.cropped_image.setMinimumSize(QSize(400, 400))
        self.cropped_image.setMaximumSize(QSize(400, 400))
        self.cropped_image.setFont(font1)
        self.cropped_image.setFrameShadow(QFrame.Shadow.Raised)
        self.cropped_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.btn_delete = QPushButton(self.frame_center)
        self.btn_delete.setObjectName(u"btn_delete")
        self.btn_delete.setGeometry(QRect(40, 700, 181, 41))
        self.btn_delete.setFont(font2)
        self.btn_delete.setStyleSheet(u"QPushButton {\n"
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
        self.frame_border = QFrame(self.frame_center)
        self.frame_border.setObjectName(u"frame_border")
        self.frame_border.setGeometry(QRect(5, 570, 461, 120))
        self.frame_border.setMinimumSize(QSize(461, 120))
        self.frame_border.setMaximumSize(QSize(461, 120))
        self.frame_border.setStyleSheet(u"#frame_border{\n"
"border: 1px solid rgba(170, 170, 255,150);\n"
"border-radius:15px;}\n"
"")
        self.frame_border.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_border.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_border)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.custom_env_layout = EnvironmentLayout(self.frame_border)
        self.custom_env_layout.setObjectName(u"custom_env_layout")
        self.custom_env_layout.setStyleSheet(u"#custom_env_layout{\n"
"border: 0px solid rgb(170, 170, 255);\n"
"border-radius:15px;}\n"
"")

        self.horizontalLayout_2.addWidget(self.custom_env_layout)

        self.label_7 = QLabel(self.frame_center)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(40, 555, 101, 21))
        self.label_7.setStyleSheet(u"border: 1px solid rgba(170, 170, 255,100);\n"
"border-radius:15px;")
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.frame_meta_object = QFrame(self.frame_center)
        self.frame_meta_object.setObjectName(u"frame_meta_object")
        self.frame_meta_object.setGeometry(QRect(470, 305, 545, 441))
        self.frame_meta_object.setStyleSheet(u"#frame_meta_object{\n"
"border: 1px solid rgba(170, 170, 255,150);\n"
"border-radius:15px;}\n"
"")
        self.frame_meta_object.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_meta_object.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_triple_4 = QFrame(self.frame_meta_object)
        self.frame_triple_4.setObjectName(u"frame_triple_4")
        self.frame_triple_4.setGeometry(QRect(275, 105, 265, 91))
        self.frame_triple_4.setFont(font1)
        self.frame_triple_4.setStyleSheet(u"")
        self.frame_triple_4.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_triple_4.setFrameShadow(QFrame.Shadow.Raised)
        self.triple_meta_4 = QSlider(self.frame_triple_4)
        self.triple_meta_4.setObjectName(u"triple_meta_4")
        self.triple_meta_4.setGeometry(QRect(35, 30, 195, 22))
        self.triple_meta_4.setFont(font1)
        self.triple_meta_4.setMaximum(2)
        self.triple_meta_4.setPageStep(1)
        self.triple_meta_4.setOrientation(Qt.Orientation.Horizontal)
        self.le_meta_triple_4_value_2 = QLabel(self.frame_triple_4)
        self.le_meta_triple_4_value_2.setObjectName(u"le_meta_triple_4_value_2")
        self.le_meta_triple_4_value_2.setGeometry(QRect(180, 60, 85, 22))
        font3 = QFont()
        font3.setPointSize(10)
        font3.setBold(True)
        self.le_meta_triple_4_value_2.setFont(font3)
        self.le_meta_triple_4_value_2.setStyleSheet(u"")
        self.le_meta_triple_4_value_2.setText(u"")
        self.le_meta_triple_4_value_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.le_meta_triple_name_4 = QLabel(self.frame_triple_4)
        self.le_meta_triple_name_4.setObjectName(u"le_meta_triple_name_4")
        self.le_meta_triple_name_4.setGeometry(QRect(60, 5, 150, 22))
        self.le_meta_triple_name_4.setFont(font3)
        self.le_meta_triple_name_4.setStyleSheet(u"")
        self.le_meta_triple_name_4.setText(u"")
        self.le_meta_triple_name_4.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.le_meta_triple_4_value_0 = QLabel(self.frame_triple_4)
        self.le_meta_triple_4_value_0.setObjectName(u"le_meta_triple_4_value_0")
        self.le_meta_triple_4_value_0.setGeometry(QRect(0, 60, 85, 22))
        self.le_meta_triple_4_value_0.setFont(font3)
        self.le_meta_triple_4_value_0.setStyleSheet(u"")
        self.le_meta_triple_4_value_0.setText(u"")
        self.le_meta_triple_4_value_0.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.le_meta_triple_4_value_1 = QLabel(self.frame_triple_4)
        self.le_meta_triple_4_value_1.setObjectName(u"le_meta_triple_4_value_1")
        self.le_meta_triple_4_value_1.setGeometry(QRect(90, 60, 85, 22))
        self.le_meta_triple_4_value_1.setFont(font3)
        self.le_meta_triple_4_value_1.setStyleSheet(u"")
        self.le_meta_triple_4_value_1.setText(u"")
        self.le_meta_triple_4_value_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.frame_triple_3 = QFrame(self.frame_meta_object)
        self.frame_triple_3.setObjectName(u"frame_triple_3")
        self.frame_triple_3.setGeometry(QRect(5, 105, 265, 91))
        self.frame_triple_3.setFont(font1)
        self.frame_triple_3.setStyleSheet(u"")
        self.frame_triple_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_triple_3.setFrameShadow(QFrame.Shadow.Raised)
        self.triple_meta_3 = QSlider(self.frame_triple_3)
        self.triple_meta_3.setObjectName(u"triple_meta_3")
        self.triple_meta_3.setGeometry(QRect(35, 30, 195, 22))
        self.triple_meta_3.setFont(font1)
        self.triple_meta_3.setMaximum(2)
        self.triple_meta_3.setPageStep(1)
        self.triple_meta_3.setOrientation(Qt.Orientation.Horizontal)
        self.le_meta_triple_name_3 = QLabel(self.frame_triple_3)
        self.le_meta_triple_name_3.setObjectName(u"le_meta_triple_name_3")
        self.le_meta_triple_name_3.setGeometry(QRect(60, 5, 150, 22))
        self.le_meta_triple_name_3.setFont(font3)
        self.le_meta_triple_name_3.setStyleSheet(u"")
        self.le_meta_triple_name_3.setText(u"")
        self.le_meta_triple_name_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.le_meta_triple_3_value_2 = QLabel(self.frame_triple_3)
        self.le_meta_triple_3_value_2.setObjectName(u"le_meta_triple_3_value_2")
        self.le_meta_triple_3_value_2.setGeometry(QRect(180, 60, 85, 22))
        self.le_meta_triple_3_value_2.setFont(font3)
        self.le_meta_triple_3_value_2.setStyleSheet(u"")
        self.le_meta_triple_3_value_2.setText(u"")
        self.le_meta_triple_3_value_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.le_meta_triple_3_value_0 = QLabel(self.frame_triple_3)
        self.le_meta_triple_3_value_0.setObjectName(u"le_meta_triple_3_value_0")
        self.le_meta_triple_3_value_0.setGeometry(QRect(0, 60, 85, 22))
        self.le_meta_triple_3_value_0.setFont(font3)
        self.le_meta_triple_3_value_0.setStyleSheet(u"")
        self.le_meta_triple_3_value_0.setText(u"")
        self.le_meta_triple_3_value_0.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.le_meta_triple_3_value_1 = QLabel(self.frame_triple_3)
        self.le_meta_triple_3_value_1.setObjectName(u"le_meta_triple_3_value_1")
        self.le_meta_triple_3_value_1.setGeometry(QRect(90, 60, 85, 22))
        self.le_meta_triple_3_value_1.setFont(font3)
        self.le_meta_triple_3_value_1.setStyleSheet(u"")
        self.le_meta_triple_3_value_1.setText(u"")
        self.le_meta_triple_3_value_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.frame_duo_1 = QFrame(self.frame_meta_object)
        self.frame_duo_1.setObjectName(u"frame_duo_1")
        self.frame_duo_1.setGeometry(QRect(5, 205, 175, 81))
        self.frame_duo_1.setFont(font1)
        self.frame_duo_1.setStyleSheet(u"")
        self.frame_duo_1.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_duo_1.setFrameShadow(QFrame.Shadow.Raised)
        self.duo_meta_1 = QSlider(self.frame_duo_1)
        self.duo_meta_1.setObjectName(u"duo_meta_1")
        self.duo_meta_1.setGeometry(QRect(20, 27, 130, 22))
        self.duo_meta_1.setFont(font1)
        self.duo_meta_1.setMaximum(1)
        self.duo_meta_1.setOrientation(Qt.Orientation.Horizontal)
        self.le_meta_duo_1_value_1 = QLabel(self.frame_duo_1)
        self.le_meta_duo_1_value_1.setObjectName(u"le_meta_duo_1_value_1")
        self.le_meta_duo_1_value_1.setGeometry(QRect(90, 60, 85, 22))
        self.le_meta_duo_1_value_1.setFont(font3)
        self.le_meta_duo_1_value_1.setStyleSheet(u"")
        self.le_meta_duo_1_value_1.setText(u"")
        self.le_meta_duo_1_value_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.le_meta_duo_name_1 = QLabel(self.frame_duo_1)
        self.le_meta_duo_name_1.setObjectName(u"le_meta_duo_name_1")
        self.le_meta_duo_name_1.setGeometry(QRect(20, 0, 130, 22))
        self.le_meta_duo_name_1.setFont(font3)
        self.le_meta_duo_name_1.setStyleSheet(u"")
        self.le_meta_duo_name_1.setText(u"")
        self.le_meta_duo_name_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.le_meta_duo_1_value_0 = QLabel(self.frame_duo_1)
        self.le_meta_duo_1_value_0.setObjectName(u"le_meta_duo_1_value_0")
        self.le_meta_duo_1_value_0.setGeometry(QRect(0, 60, 85, 22))
        self.le_meta_duo_1_value_0.setFont(font3)
        self.le_meta_duo_1_value_0.setStyleSheet(u"")
        self.le_meta_duo_1_value_0.setText(u"")
        self.le_meta_duo_1_value_0.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.frame_duo_2 = QFrame(self.frame_meta_object)
        self.frame_duo_2.setObjectName(u"frame_duo_2")
        self.frame_duo_2.setGeometry(QRect(185, 205, 175, 81))
        self.frame_duo_2.setFont(font1)
        self.frame_duo_2.setStyleSheet(u"")
        self.frame_duo_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_duo_2.setFrameShadow(QFrame.Shadow.Raised)
        self.duo_meta_2 = QSlider(self.frame_duo_2)
        self.duo_meta_2.setObjectName(u"duo_meta_2")
        self.duo_meta_2.setGeometry(QRect(20, 27, 131, 22))
        self.duo_meta_2.setFont(font1)
        self.duo_meta_2.setMaximum(1)
        self.duo_meta_2.setOrientation(Qt.Orientation.Horizontal)
        self.le_meta_duo_name_2 = QLabel(self.frame_duo_2)
        self.le_meta_duo_name_2.setObjectName(u"le_meta_duo_name_2")
        self.le_meta_duo_name_2.setGeometry(QRect(20, 0, 130, 22))
        self.le_meta_duo_name_2.setFont(font3)
        self.le_meta_duo_name_2.setStyleSheet(u"")
        self.le_meta_duo_name_2.setText(u"")
        self.le_meta_duo_name_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.le_meta_duo_2_value_0 = QLabel(self.frame_duo_2)
        self.le_meta_duo_2_value_0.setObjectName(u"le_meta_duo_2_value_0")
        self.le_meta_duo_2_value_0.setGeometry(QRect(0, 60, 85, 22))
        self.le_meta_duo_2_value_0.setFont(font3)
        self.le_meta_duo_2_value_0.setStyleSheet(u"")
        self.le_meta_duo_2_value_0.setText(u"")
        self.le_meta_duo_2_value_0.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.le_meta_duo_2_value_1 = QLabel(self.frame_duo_2)
        self.le_meta_duo_2_value_1.setObjectName(u"le_meta_duo_2_value_1")
        self.le_meta_duo_2_value_1.setGeometry(QRect(90, 60, 85, 22))
        self.le_meta_duo_2_value_1.setFont(font3)
        self.le_meta_duo_2_value_1.setStyleSheet(u"")
        self.le_meta_duo_2_value_1.setText(u"")
        self.le_meta_duo_2_value_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.frame_duo_3 = QFrame(self.frame_meta_object)
        self.frame_duo_3.setObjectName(u"frame_duo_3")
        self.frame_duo_3.setGeometry(QRect(365, 205, 175, 81))
        self.frame_duo_3.setFont(font1)
        self.frame_duo_3.setStyleSheet(u"")
        self.frame_duo_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_duo_3.setFrameShadow(QFrame.Shadow.Raised)
        self.duo_meta_3 = QSlider(self.frame_duo_3)
        self.duo_meta_3.setObjectName(u"duo_meta_3")
        self.duo_meta_3.setGeometry(QRect(20, 27, 131, 22))
        self.duo_meta_3.setFont(font1)
        self.duo_meta_3.setMaximum(1)
        self.duo_meta_3.setOrientation(Qt.Orientation.Horizontal)
        self.le_meta_duo_name_3 = QLabel(self.frame_duo_3)
        self.le_meta_duo_name_3.setObjectName(u"le_meta_duo_name_3")
        self.le_meta_duo_name_3.setGeometry(QRect(20, 0, 130, 22))
        self.le_meta_duo_name_3.setFont(font3)
        self.le_meta_duo_name_3.setStyleSheet(u"")
        self.le_meta_duo_name_3.setText(u"")
        self.le_meta_duo_name_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.le_meta_duo_3_value_0 = QLabel(self.frame_duo_3)
        self.le_meta_duo_3_value_0.setObjectName(u"le_meta_duo_3_value_0")
        self.le_meta_duo_3_value_0.setGeometry(QRect(0, 60, 85, 22))
        self.le_meta_duo_3_value_0.setFont(font3)
        self.le_meta_duo_3_value_0.setStyleSheet(u"")
        self.le_meta_duo_3_value_0.setText(u"")
        self.le_meta_duo_3_value_0.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.le_meta_duo_3_value_1 = QLabel(self.frame_duo_3)
        self.le_meta_duo_3_value_1.setObjectName(u"le_meta_duo_3_value_1")
        self.le_meta_duo_3_value_1.setGeometry(QRect(90, 60, 85, 22))
        self.le_meta_duo_3_value_1.setFont(font3)
        self.le_meta_duo_3_value_1.setStyleSheet(u"")
        self.le_meta_duo_3_value_1.setText(u"")
        self.le_meta_duo_3_value_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.frame_triple_2 = QFrame(self.frame_meta_object)
        self.frame_triple_2.setObjectName(u"frame_triple_2")
        self.frame_triple_2.setGeometry(QRect(275, 10, 265, 91))
        self.frame_triple_2.setFont(font1)
        self.frame_triple_2.setStyleSheet(u"")
        self.frame_triple_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_triple_2.setFrameShadow(QFrame.Shadow.Raised)
        self.triple_meta_2 = QSlider(self.frame_triple_2)
        self.triple_meta_2.setObjectName(u"triple_meta_2")
        self.triple_meta_2.setGeometry(QRect(35, 30, 195, 22))
        self.triple_meta_2.setFont(font1)
        self.triple_meta_2.setMaximum(2)
        self.triple_meta_2.setPageStep(1)
        self.triple_meta_2.setOrientation(Qt.Orientation.Horizontal)
        self.le_meta_triple_name_2 = QLabel(self.frame_triple_2)
        self.le_meta_triple_name_2.setObjectName(u"le_meta_triple_name_2")
        self.le_meta_triple_name_2.setGeometry(QRect(60, 5, 150, 22))
        self.le_meta_triple_name_2.setFont(font3)
        self.le_meta_triple_name_2.setStyleSheet(u"")
        self.le_meta_triple_name_2.setText(u"")
        self.le_meta_triple_name_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.le_meta_triple_2_value_2 = QLabel(self.frame_triple_2)
        self.le_meta_triple_2_value_2.setObjectName(u"le_meta_triple_2_value_2")
        self.le_meta_triple_2_value_2.setGeometry(QRect(180, 60, 85, 22))
        self.le_meta_triple_2_value_2.setFont(font3)
        self.le_meta_triple_2_value_2.setStyleSheet(u"")
        self.le_meta_triple_2_value_2.setText(u"")
        self.le_meta_triple_2_value_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.le_meta_triple_2_value_0 = QLabel(self.frame_triple_2)
        self.le_meta_triple_2_value_0.setObjectName(u"le_meta_triple_2_value_0")
        self.le_meta_triple_2_value_0.setGeometry(QRect(0, 60, 85, 22))
        self.le_meta_triple_2_value_0.setFont(font3)
        self.le_meta_triple_2_value_0.setStyleSheet(u"")
        self.le_meta_triple_2_value_0.setText(u"")
        self.le_meta_triple_2_value_0.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.le_meta_triple_2_value_1 = QLabel(self.frame_triple_2)
        self.le_meta_triple_2_value_1.setObjectName(u"le_meta_triple_2_value_1")
        self.le_meta_triple_2_value_1.setGeometry(QRect(90, 60, 85, 22))
        self.le_meta_triple_2_value_1.setFont(font3)
        self.le_meta_triple_2_value_1.setStyleSheet(u"")
        self.le_meta_triple_2_value_1.setText(u"")
        self.le_meta_triple_2_value_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.frame_triple_1 = QFrame(self.frame_meta_object)
        self.frame_triple_1.setObjectName(u"frame_triple_1")
        self.frame_triple_1.setGeometry(QRect(5, 10, 265, 91))
        self.frame_triple_1.setFont(font1)
        self.frame_triple_1.setStyleSheet(u"")
        self.frame_triple_1.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_triple_1.setFrameShadow(QFrame.Shadow.Raised)
        self.triple_meta_1 = QSlider(self.frame_triple_1)
        self.triple_meta_1.setObjectName(u"triple_meta_1")
        self.triple_meta_1.setGeometry(QRect(35, 30, 195, 22))
        self.triple_meta_1.setFont(font1)
        self.triple_meta_1.setMaximum(2)
        self.triple_meta_1.setPageStep(1)
        self.triple_meta_1.setOrientation(Qt.Orientation.Horizontal)
        self.le_meta_triple_1_value_2 = QLabel(self.frame_triple_1)
        self.le_meta_triple_1_value_2.setObjectName(u"le_meta_triple_1_value_2")
        self.le_meta_triple_1_value_2.setGeometry(QRect(180, 60, 85, 22))
        self.le_meta_triple_1_value_2.setFont(font3)
        self.le_meta_triple_1_value_2.setStyleSheet(u"")
        self.le_meta_triple_1_value_2.setText(u"")
        self.le_meta_triple_1_value_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.le_meta_triple_1_value_1 = QLabel(self.frame_triple_1)
        self.le_meta_triple_1_value_1.setObjectName(u"le_meta_triple_1_value_1")
        self.le_meta_triple_1_value_1.setGeometry(QRect(90, 60, 85, 22))
        self.le_meta_triple_1_value_1.setFont(font3)
        self.le_meta_triple_1_value_1.setStyleSheet(u"")
        self.le_meta_triple_1_value_1.setText(u"")
        self.le_meta_triple_1_value_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.le_meta_triple_1_value_0 = QLabel(self.frame_triple_1)
        self.le_meta_triple_1_value_0.setObjectName(u"le_meta_triple_1_value_0")
        self.le_meta_triple_1_value_0.setGeometry(QRect(0, 60, 85, 22))
        self.le_meta_triple_1_value_0.setFont(font3)
        self.le_meta_triple_1_value_0.setStyleSheet(u"")
        self.le_meta_triple_1_value_0.setText(u"")
        self.le_meta_triple_1_value_0.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.le_meta_triple_name_1 = QLabel(self.frame_triple_1)
        self.le_meta_triple_name_1.setObjectName(u"le_meta_triple_name_1")
        self.le_meta_triple_name_1.setGeometry(QRect(60, 5, 150, 22))
        self.le_meta_triple_name_1.setFont(font3)
        self.le_meta_triple_name_1.setStyleSheet(u"")
        self.le_meta_triple_name_1.setText(u"")
        self.le_meta_triple_name_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.frame_cmb_meta_1 = QFrame(self.frame_meta_object)
        self.frame_cmb_meta_1.setObjectName(u"frame_cmb_meta_1")
        self.frame_cmb_meta_1.setGeometry(QRect(20, 300, 151, 71))
        self.frame_cmb_meta_1.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_cmb_meta_1.setFrameShadow(QFrame.Shadow.Raised)
        self.cmb_meta_1 = QComboBox(self.frame_cmb_meta_1)
        self.cmb_meta_1.setObjectName(u"cmb_meta_1")
        self.cmb_meta_1.setGeometry(QRect(0, 30, 151, 31))
        self.cmb_meta_1.setFont(font)
        self.cmb_meta_1.setStyleSheet(u"QComboBox { color: white;background-color: rgb(27, 29, 35);}\n"
"QComboBox QAbstractItemView {\n"
"  color: white;background-color: rgb(27, 29, 35);\n"
"}")
        self.cmb_meta_1.setCurrentText(u"")
        self.le_meta_cmb_name_1 = QLabel(self.frame_cmb_meta_1)
        self.le_meta_cmb_name_1.setObjectName(u"le_meta_cmb_name_1")
        self.le_meta_cmb_name_1.setGeometry(QRect(0, 5, 151, 22))
        self.le_meta_cmb_name_1.setFont(font3)
        self.le_meta_cmb_name_1.setStyleSheet(u"")
        self.le_meta_cmb_name_1.setText(u"")
        self.le_meta_cmb_name_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.frame_cmb_meta_2 = QFrame(self.frame_meta_object)
        self.frame_cmb_meta_2.setObjectName(u"frame_cmb_meta_2")
        self.frame_cmb_meta_2.setGeometry(QRect(200, 300, 151, 71))
        self.frame_cmb_meta_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_cmb_meta_2.setFrameShadow(QFrame.Shadow.Raised)
        self.cmb_meta_2 = QComboBox(self.frame_cmb_meta_2)
        self.cmb_meta_2.setObjectName(u"cmb_meta_2")
        self.cmb_meta_2.setGeometry(QRect(0, 30, 151, 31))
        self.cmb_meta_2.setFont(font)
        self.cmb_meta_2.setStyleSheet(u"QComboBox { color: white;background-color: rgb(27, 29, 35);}\n"
"QComboBox QAbstractItemView {\n"
"  color: white;background-color: rgb(27, 29, 35);\n"
"}")
        self.cmb_meta_2.setCurrentText(u"")
        self.le_meta_cmb_name_2 = QLabel(self.frame_cmb_meta_2)
        self.le_meta_cmb_name_2.setObjectName(u"le_meta_cmb_name_2")
        self.le_meta_cmb_name_2.setGeometry(QRect(0, 5, 151, 22))
        self.le_meta_cmb_name_2.setFont(font3)
        self.le_meta_cmb_name_2.setStyleSheet(u"")
        self.le_meta_cmb_name_2.setText(u"")
        self.le_meta_cmb_name_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.frame_cmb_meta_3 = QFrame(self.frame_meta_object)
        self.frame_cmb_meta_3.setObjectName(u"frame_cmb_meta_3")
        self.frame_cmb_meta_3.setGeometry(QRect(380, 300, 160, 71))
        self.frame_cmb_meta_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_cmb_meta_3.setFrameShadow(QFrame.Shadow.Raised)
        self.cmb_meta_3 = QComboBox(self.frame_cmb_meta_3)
        self.cmb_meta_3.setObjectName(u"cmb_meta_3")
        self.cmb_meta_3.setGeometry(QRect(0, 30, 151, 31))
        self.cmb_meta_3.setFont(font)
        self.cmb_meta_3.setStyleSheet(u"QComboBox { color: white;background-color: rgb(27, 29, 35);}\n"
"QComboBox QAbstractItemView {\n"
"  color: white;background-color: rgb(27, 29, 35);\n"
"}")
        self.cmb_meta_3.setCurrentText(u"")
        self.le_meta_cmb_name_3 = QLabel(self.frame_cmb_meta_3)
        self.le_meta_cmb_name_3.setObjectName(u"le_meta_cmb_name_3")
        self.le_meta_cmb_name_3.setGeometry(QRect(0, 5, 151, 22))
        self.le_meta_cmb_name_3.setFont(font3)
        self.le_meta_cmb_name_3.setStyleSheet(u"")
        self.le_meta_cmb_name_3.setText(u"")
        self.le_meta_cmb_name_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.frame_txt_1 = QFrame(self.frame_meta_object)
        self.frame_txt_1.setObjectName(u"frame_txt_1")
        self.frame_txt_1.setGeometry(QRect(20, 370, 160, 70))
        self.frame_txt_1.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_txt_1.setFrameShadow(QFrame.Shadow.Raised)
        self.le_meta_input_txt_1 = QLineEdit(self.frame_txt_1)
        self.le_meta_input_txt_1.setObjectName(u"le_meta_input_txt_1")
        self.le_meta_input_txt_1.setGeometry(QRect(0, 35, 151, 31))
        self.le_meta_input_txt_1.setStyleSheet(u"color: white;background-color: rgb(27, 29, 35);")
        self.le_meta_input_txt_1.setReadOnly(False)
        self.le_meta_input_txt_name_1 = QLabel(self.frame_txt_1)
        self.le_meta_input_txt_name_1.setObjectName(u"le_meta_input_txt_name_1")
        self.le_meta_input_txt_name_1.setGeometry(QRect(0, 10, 151, 22))
        self.le_meta_input_txt_name_1.setFont(font3)
        self.le_meta_input_txt_name_1.setStyleSheet(u"")
        self.le_meta_input_txt_name_1.setText(u"")
        self.le_meta_input_txt_name_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.frame_txt_2 = QFrame(self.frame_meta_object)
        self.frame_txt_2.setObjectName(u"frame_txt_2")
        self.frame_txt_2.setGeometry(QRect(200, 370, 160, 70))
        self.frame_txt_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_txt_2.setFrameShadow(QFrame.Shadow.Raised)
        self.le_meta_input_txt_2 = QLineEdit(self.frame_txt_2)
        self.le_meta_input_txt_2.setObjectName(u"le_meta_input_txt_2")
        self.le_meta_input_txt_2.setGeometry(QRect(0, 35, 151, 31))
        self.le_meta_input_txt_2.setStyleSheet(u"color: white;background-color: rgb(27, 29, 35);")
        self.le_meta_input_txt_2.setReadOnly(False)
        self.le_meta_input_txt_name_2 = QLabel(self.frame_txt_2)
        self.le_meta_input_txt_name_2.setObjectName(u"le_meta_input_txt_name_2")
        self.le_meta_input_txt_name_2.setGeometry(QRect(0, 10, 151, 22))
        self.le_meta_input_txt_name_2.setFont(font3)
        self.le_meta_input_txt_name_2.setStyleSheet(u"")
        self.le_meta_input_txt_name_2.setText(u"")
        self.le_meta_input_txt_name_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.frame_txt_3 = QFrame(self.frame_meta_object)
        self.frame_txt_3.setObjectName(u"frame_txt_3")
        self.frame_txt_3.setGeometry(QRect(380, 370, 155, 68))
        self.frame_txt_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_txt_3.setFrameShadow(QFrame.Shadow.Raised)
        self.le_meta_input_txt_3 = QLineEdit(self.frame_txt_3)
        self.le_meta_input_txt_3.setObjectName(u"le_meta_input_txt_3")
        self.le_meta_input_txt_3.setGeometry(QRect(0, 35, 151, 31))
        self.le_meta_input_txt_3.setStyleSheet(u"color: white;background-color: rgb(27, 29, 35);")
        self.le_meta_input_txt_3.setReadOnly(False)
        self.le_meta_input_txt_name_3 = QLabel(self.frame_txt_3)
        self.le_meta_input_txt_name_3.setObjectName(u"le_meta_input_txt_name_3")
        self.le_meta_input_txt_name_3.setGeometry(QRect(0, 10, 151, 22))
        self.le_meta_input_txt_name_3.setFont(font3)
        self.le_meta_input_txt_name_3.setStyleSheet(u"")
        self.le_meta_input_txt_name_3.setText(u"")
        self.le_meta_input_txt_name_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.frame_txt_1.raise_()
        self.frame_cmb_meta_1.raise_()
        self.frame_triple_4.raise_()
        self.frame_triple_3.raise_()
        self.frame_duo_1.raise_()
        self.frame_duo_2.raise_()
        self.frame_duo_3.raise_()
        self.frame_triple_2.raise_()
        self.frame_triple_1.raise_()
        self.frame_cmb_meta_2.raise_()
        self.frame_cmb_meta_3.raise_()
        self.frame_txt_2.raise_()
        self.frame_txt_3.raise_()
        self.frame_main_type = QFrame(self.frame_center)
        self.frame_main_type.setObjectName(u"frame_main_type")
        self.frame_main_type.setGeometry(QRect(470, 10, 545, 181))
        self.frame_main_type.setStyleSheet(u"#frame_main_type{\n"
"border: 1px solid rgba(170, 170, 255,150);\n"
"border-radius:15px;}\n"
"")
        self.frame_main_type.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_main_type.setFrameShadow(QFrame.Shadow.Raised)
        self.le_object_main_naming = QLabel(self.frame_main_type)
        self.le_object_main_naming.setObjectName(u"le_object_main_naming")
        self.le_object_main_naming.setGeometry(QRect(10, 10, 201, 31))
        font4 = QFont()
        font4.setFamilies([u"Segoe UI"])
        font4.setPointSize(13)
        font4.setBold(True)
        self.le_object_main_naming.setFont(font4)
        self.cmb_obejcet_types_main = InteractiveCombo(self.frame_main_type)
        self.cmb_obejcet_types_main.setObjectName(u"cmb_obejcet_types_main")
        self.cmb_obejcet_types_main.setGeometry(QRect(10, 40, 261, 31))
        self.cmb_obejcet_types_main.setFont(font)
        self.cmb_obejcet_types_main.setStyleSheet(u"QComboBox{\n"
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
"}")
        self.cmb_obejcet_types_main.setEditable(False)
        self.cmb_obejcet_types_main.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)
        self.cmb_obejcet_types_main.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContentsOnFirstShow)
        self.frame_certainty_main_type = QFrame(self.frame_main_type)
        self.frame_certainty_main_type.setObjectName(u"frame_certainty_main_type")
        self.frame_certainty_main_type.setGeometry(QRect(330, 10, 131, 61))
        self.frame_certainty_main_type.setFont(font1)
        self.frame_certainty_main_type.setStyleSheet(u"")
        self.frame_certainty_main_type.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_certainty_main_type.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_main_type_option = QFrame(self.frame_main_type)
        self.frame_main_type_option.setObjectName(u"frame_main_type_option")
        self.frame_main_type_option.setGeometry(QRect(340, 5, 181, 81))
        self.frame_main_type_option.setFont(font1)
        self.frame_main_type_option.setStyleSheet(u"")
        self.frame_main_type_option.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_main_type_option.setFrameShadow(QFrame.Shadow.Raised)
        self.duo_main_type_option = QSlider(self.frame_main_type_option)
        self.duo_main_type_option.setObjectName(u"duo_main_type_option")
        self.duo_main_type_option.setGeometry(QRect(25, 25, 131, 22))
        self.duo_main_type_option.setFont(font1)
        self.duo_main_type_option.setMaximum(1)
        self.duo_main_type_option.setPageStep(1)
        self.duo_main_type_option.setOrientation(Qt.Orientation.Horizontal)
        self.le_main_type_option_value_0 = QLabel(self.frame_main_type_option)
        self.le_main_type_option_value_0.setObjectName(u"le_main_type_option_value_0")
        self.le_main_type_option_value_0.setGeometry(QRect(-10, 55, 85, 22))
        self.le_main_type_option_value_0.setFont(font3)
        self.le_main_type_option_value_0.setStyleSheet(u"")
        self.le_main_type_option_value_0.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.le_main_type_option_value_1 = QLabel(self.frame_main_type_option)
        self.le_main_type_option_value_1.setObjectName(u"le_main_type_option_value_1")
        self.le_main_type_option_value_1.setGeometry(QRect(100, 55, 85, 22))
        self.le_main_type_option_value_1.setFont(font3)
        self.le_main_type_option_value_1.setStyleSheet(u"")
        self.le_main_type_option_value_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.le_main_type_option_name = QLabel(self.frame_main_type_option)
        self.le_main_type_option_name.setObjectName(u"le_main_type_option_name")
        self.le_main_type_option_name.setGeometry(QRect(15, 0, 150, 22))
        self.le_main_type_option_name.setFont(font3)
        self.le_main_type_option_name.setStyleSheet(u"")
        self.le_main_type_option_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.frame_7 = QFrame(self.frame_main_type)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setGeometry(QRect(80, 100, 131, 61))
        self.frame_7.setFont(font1)
        self.frame_7.setStyleSheet(u"")
        self.frame_7.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.slider_certainty = QSlider(self.frame_7)
        self.slider_certainty.setObjectName(u"slider_certainty")
        self.slider_certainty.setEnabled(True)
        self.slider_certainty.setGeometry(QRect(10, 20, 111, 22))
        self.slider_certainty.setFont(font1)
        self.slider_certainty.setMaximum(1)
        self.slider_certainty.setValue(1)
        self.slider_certainty.setOrientation(Qt.Orientation.Horizontal)
        self.label_19 = QLabel(self.frame_7)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setGeometry(QRect(30, 0, 71, 16))
        font5 = QFont()
        font5.setFamilies([u"Segoe UI"])
        font5.setPointSize(11)
        font5.setBold(True)
        self.label_19.setFont(font5)
        self.label_20 = QLabel(self.frame_7)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setGeometry(QRect(10, 40, 31, 21))
        self.label_20.setFont(font5)
        self.label_21 = QLabel(self.frame_7)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setGeometry(QRect(100, 40, 31, 21))
        self.label_21.setFont(font5)
        self.frame_certainty_manual_override = QFrame(self.frame_main_type)
        self.frame_certainty_manual_override.setObjectName(u"frame_certainty_manual_override")
        self.frame_certainty_manual_override.setGeometry(QRect(290, 95, 251, 81))
        self.frame_certainty_manual_override.setStyleSheet(u"#frame_certainty_manual_override{\n"
"border: 1px solid rgba(170, 170, 255,100);\n"
"border-radius:15px;}\n"
"")
        self.frame_certainty_manual_override.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_certainty_manual_override.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_5 = QFrame(self.frame_certainty_manual_override)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setGeometry(QRect(10, 15, 100, 61))
        self.frame_5.setFont(font1)
        self.frame_5.setStyleSheet(u"")
        self.frame_5.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.slider_first_certain = QSlider(self.frame_5)
        self.slider_first_certain.setObjectName(u"slider_first_certain")
        self.slider_first_certain.setGeometry(QRect(15, 20, 70, 22))
        self.slider_first_certain.setFont(font1)
        self.slider_first_certain.setMaximum(1)
        self.slider_first_certain.setOrientation(Qt.Orientation.Horizontal)
        self.label_10 = QLabel(self.frame_5)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(15, 0, 71, 16))
        self.label_10.setFont(font)
        self.label_11 = QLabel(self.frame_5)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(10, 40, 31, 21))
        self.label_11.setFont(font)
        self.label_12 = QLabel(self.frame_5)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(70, 40, 31, 21))
        self.label_12.setFont(font)
        self.frame_6 = QFrame(self.frame_certainty_manual_override)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setGeometry(QRect(140, 15, 100, 61))
        self.frame_6.setFont(font1)
        self.frame_6.setStyleSheet(u"")
        self.frame_6.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.slider_resight = QSlider(self.frame_6)
        self.slider_resight.setObjectName(u"slider_resight")
        self.slider_resight.setGeometry(QRect(15, 20, 70, 22))
        self.slider_resight.setFont(font1)
        self.slider_resight.setMaximum(1)
        self.slider_resight.setOrientation(Qt.Orientation.Horizontal)
        self.label_13 = QLabel(self.frame_6)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(25, 0, 51, 16))
        self.label_13.setFont(font)
        self.label_14 = QLabel(self.frame_6)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(QRect(10, 40, 31, 21))
        self.label_14.setFont(font)
        self.label_15 = QLabel(self.frame_6)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setGeometry(QRect(70, 40, 31, 21))
        self.label_15.setFont(font)
        self.label_9 = QLabel(self.frame_main_type)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(360, 90, 101, 16))
        self.label_9.setStyleSheet(u"border: 1px solid rgba(170, 170, 255,100);\n"
"border-radius:15px;")
        self.label_9.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.txt_notes = QTextEdit(self.frame_center)
        self.txt_notes.setObjectName(u"txt_notes")
        self.txt_notes.setGeometry(QRect(5, 430, 460, 111))
        self.txt_notes.setStyleSheet(u"QTextEdit {\n"
"	background-color: rgb(52, 59, 72);\n"
"	color: white;\n"
"	border-radius:15px;\n"
"}")
        self.txt_notes.setFrameShape(QFrame.Shape.NoFrame)
        self.txt_notes.setAcceptRichText(False)
        self.frame_subtype = QFrame(self.frame_center)
        self.frame_subtype.setObjectName(u"frame_subtype")
        self.frame_subtype.setGeometry(QRect(470, 200, 545, 91))
        self.frame_subtype.setStyleSheet(u"#frame_subtype{\n"
"border: 1px solid rgba(170, 170, 255,150);\n"
"border-radius:15px;}\n"
"")
        self.frame_subtype.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_subtype.setFrameShadow(QFrame.Shadow.Raised)
        self.cmb_obejcet_types_sub = InteractiveCombo(self.frame_subtype)
        self.cmb_obejcet_types_sub.setObjectName(u"cmb_obejcet_types_sub")
        self.cmb_obejcet_types_sub.setGeometry(QRect(10, 40, 261, 31))
        self.cmb_obejcet_types_sub.setFont(font)
        self.cmb_obejcet_types_sub.setStyleSheet(u"QComboBox{\n"
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
"}")
        self.le_object_sub_naming = QLabel(self.frame_subtype)
        self.le_object_sub_naming.setObjectName(u"le_object_sub_naming")
        self.le_object_sub_naming.setGeometry(QRect(10, 10, 191, 21))
        font6 = QFont()
        font6.setFamilies([u"Segoe UI"])
        font6.setPointSize(12)
        font6.setBold(True)
        self.le_object_sub_naming.setFont(font6)
        self.frame_sub_type_option = QFrame(self.frame_subtype)
        self.frame_sub_type_option.setObjectName(u"frame_sub_type_option")
        self.frame_sub_type_option.setGeometry(QRect(290, 5, 251, 81))
        self.frame_sub_type_option.setFont(font1)
        self.frame_sub_type_option.setStyleSheet(u"")
        self.frame_sub_type_option.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_sub_type_option.setFrameShadow(QFrame.Shadow.Raised)
        self.triple_sub_type_option = QSlider(self.frame_sub_type_option)
        self.triple_sub_type_option.setObjectName(u"triple_sub_type_option")
        self.triple_sub_type_option.setGeometry(QRect(35, 25, 185, 22))
        self.triple_sub_type_option.setFont(font1)
        self.triple_sub_type_option.setMaximum(2)
        self.triple_sub_type_option.setPageStep(1)
        self.triple_sub_type_option.setOrientation(Qt.Orientation.Horizontal)
        self.le_sub_type_option_value_0 = QLabel(self.frame_sub_type_option)
        self.le_sub_type_option_value_0.setObjectName(u"le_sub_type_option_value_0")
        self.le_sub_type_option_value_0.setGeometry(QRect(0, 55, 80, 22))
        self.le_sub_type_option_value_0.setFont(font3)
        self.le_sub_type_option_value_0.setStyleSheet(u"")
        self.le_sub_type_option_value_0.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.le_sub_type_option_value_1 = QLabel(self.frame_sub_type_option)
        self.le_sub_type_option_value_1.setObjectName(u"le_sub_type_option_value_1")
        self.le_sub_type_option_value_1.setGeometry(QRect(85, 55, 80, 22))
        self.le_sub_type_option_value_1.setFont(font3)
        self.le_sub_type_option_value_1.setStyleSheet(u"")
        self.le_sub_type_option_value_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.le_sub_type_option_value_2 = QLabel(self.frame_sub_type_option)
        self.le_sub_type_option_value_2.setObjectName(u"le_sub_type_option_value_2")
        self.le_sub_type_option_value_2.setGeometry(QRect(170, 55, 80, 22))
        self.le_sub_type_option_value_2.setFont(font3)
        self.le_sub_type_option_value_2.setStyleSheet(u"")
        self.le_sub_type_option_value_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.le_sub_type_option_name = QLabel(self.frame_sub_type_option)
        self.le_sub_type_option_name.setObjectName(u"le_sub_type_option_name")
        self.le_sub_type_option_name.setGeometry(QRect(60, 0, 150, 22))
        self.le_sub_type_option_name.setFont(font3)
        self.le_sub_type_option_name.setStyleSheet(u"")
        self.le_sub_type_option_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_8 = QLabel(self.frame_center)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(690, 300, 91, 16))
        self.label_8.setStyleSheet(u"border: 1px solid rgba(170, 170, 255,100);\n"
"border-radius:15px;")
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.frame_meta_object.raise_()
        self.btn_save.raise_()
        self.cropped_image.raise_()
        self.btn_delete.raise_()
        self.frame_border.raise_()
        self.label_7.raise_()
        self.frame_main_type.raise_()
        self.txt_notes.raise_()
        self.frame_subtype.raise_()
        self.label_8.raise_()

        self.verticalLayout.addWidget(self.frame_center)


        self.retranslateUi(popup_meta)

        QMetaObject.connectSlotsByName(popup_meta)
    # setupUi

    def retranslateUi(self, popup_meta):
        popup_meta.setWindowTitle(QCoreApplication.translate("popup_meta", u"MainWindow", None))
        self.lbl_icon.setText("")
#if QT_CONFIG(tooltip)
        self.label_title.setToolTip(QCoreApplication.translate("popup_meta", u"<html><head/><body><p><span style=\" font-size:8pt; font-weight:400;\">Move window</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_title.setText(QCoreApplication.translate("popup_meta", u"OBJECT INSPECTOR", None))
        self.btn_save.setText(QCoreApplication.translate("popup_meta", u"Save Changes", None))
        self.cropped_image.setText("")
        self.btn_delete.setText(QCoreApplication.translate("popup_meta", u"Delete Object", None))
        self.label_7.setText(QCoreApplication.translate("popup_meta", u"ENVIRONMENT", None))
        self.cmb_meta_1.setPlaceholderText("")
        self.cmb_meta_2.setPlaceholderText("")
        self.cmb_meta_3.setPlaceholderText("")
        self.le_meta_input_txt_1.setPlaceholderText(QCoreApplication.translate("popup_meta", u"enter text/value", None))
        self.le_meta_input_txt_2.setPlaceholderText(QCoreApplication.translate("popup_meta", u"enter text/value", None))
        self.le_meta_input_txt_3.setPlaceholderText(QCoreApplication.translate("popup_meta", u"enter text/value", None))
        self.le_object_main_naming.setText(QCoreApplication.translate("popup_meta", u" -", None))
        self.le_main_type_option_value_0.setText("")
        self.le_main_type_option_value_1.setText("")
        self.le_main_type_option_name.setText("")
        self.label_19.setText(QCoreApplication.translate("popup_meta", u"Certainty", None))
        self.label_20.setText(QCoreApplication.translate("popup_meta", u"no", None))
        self.label_21.setText(QCoreApplication.translate("popup_meta", u"yes", None))
        self.label_10.setText(QCoreApplication.translate("popup_meta", u"First Certain", None))
        self.label_11.setText(QCoreApplication.translate("popup_meta", u"no", None))
        self.label_12.setText(QCoreApplication.translate("popup_meta", u"yes", None))
        self.label_13.setText(QCoreApplication.translate("popup_meta", u"Resight", None))
        self.label_14.setText(QCoreApplication.translate("popup_meta", u"no", None))
        self.label_15.setText(QCoreApplication.translate("popup_meta", u"yes", None))
        self.label_9.setText(QCoreApplication.translate("popup_meta", u"manual override", None))
        self.txt_notes.setHtml(QCoreApplication.translate("popup_meta", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'MS Shell Dlg 2'; font-size:8.25pt;\"><br /></p></body></html>", None))
        self.txt_notes.setPlaceholderText(QCoreApplication.translate("popup_meta", u"Notes/Comments", None))
        self.le_object_sub_naming.setText(QCoreApplication.translate("popup_meta", u" -", None))
        self.le_sub_type_option_value_0.setText("")
        self.le_sub_type_option_value_1.setText("")
        self.le_sub_type_option_value_2.setText("")
        self.le_sub_type_option_name.setText("")
        self.label_8.setText(QCoreApplication.translate("popup_meta", u"META DATA", None))
    # retranslateUi

