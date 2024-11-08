# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui_main.ui'
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
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QButtonGroup, QComboBox,
    QDial, QFrame, QGraphicsView, QGridLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QListView, QMainWindow, QPlainTextEdit,
    QProgressBar, QPushButton, QRadioButton, QScrollBar,
    QSizePolicy, QSlider, QSpacerItem, QSplitter,
    QStackedWidget, QTabWidget, QTableView, QToolButton,
    QVBoxLayout, QWidget)

from app.custom_elements.gaugeProgress import GAUGEProgress
from app.custom_elements.layoutEnvironment import EnvironmentLayout
from app.custom_elements.pieChart import CustomChartView
from app.custom_elements.spinningWaiter import QtWaitingSpinner
from app.graphic.gisView import GISView
from app.graphic.imageView import ImageView
from app.model_views.aiView import AIView
from app.model_views.compareViews import CompareListView
from app.model_views.galleryView import GalleryView
from app.model_views.imageListView import ImageTreeView
from . import files_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1070, 900)
        MainWindow.setMinimumSize(QSize(1070, 900))
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
        brush11 = QBrush(QColor(51, 153, 255, 255))
        brush11.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Highlight, brush11)
        palette.setBrush(QPalette.Disabled, QPalette.Link, brush8)
        palette.setBrush(QPalette.Disabled, QPalette.LinkVisited, brush9)
        palette.setBrush(QPalette.Disabled, QPalette.AlternateBase, brush10)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush10)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipText, brush6)
        MainWindow.setPalette(palette)
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(10)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet(u"QMainWindow {background: transparent; }\n"
"QToolTip {\n"
"	color: white;\n"
"	background-color: rgb(85, 85, 85);\n"
"	border: 1px solid rgb(40, 40, 40);\n"
"	border-radius: 2px;\n"
"}\n"
"\n"
"\n"
"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"background: transparent;\n"
"color: rgb(210, 210, 210);\n"
"\n"
"QToolTip {\n"
"	color: white;\n"
"	background-color: rgb(85, 85, 85);\n"
"	border: 1px solid rgb(40, 40, 40);\n"
"	border-radius: 2px;\n"
"}\n"
"")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_main = QFrame(self.centralwidget)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setStyleSheet(u"QLineEdit {\n"
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
"	border-top-left-ra"
                        "dius: 7px;\n"
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
"    background: rgb(55, 63, 77);\n"
"     hei"
                        "ght: 20px;\n"
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
"QRadioButton::indicator:hover {"
                        "\n"
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
"	padding: 10px;\n"
"	selection-b"
                        "ackground-color: rgb(39, 44, 54);\n"
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
"    background-color:rgb(178, 186, 87);\n"
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
"    height: 18px;\n"
""
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
"")
        self.frame_main.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_main.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_main)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_top = QFrame(self.frame_main)
        self.frame_top.setObjectName(u"frame_top")
        self.frame_top.setMinimumSize(QSize(0, 40))
        self.frame_top.setMaximumSize(QSize(16777215, 40))
        self.frame_top.setStyleSheet(u"background-color:rgb(85, 85, 85)")
        self.frame_top.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_top.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_top)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame_toggle = QFrame(self.frame_top)
        self.frame_toggle.setObjectName(u"frame_toggle")
        self.frame_toggle.setMaximumSize(QSize(60, 16777215))
        self.frame_toggle.setStyleSheet(u"")
        self.frame_toggle.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_toggle.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_toggle)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.btn_toggle_menu = QPushButton(self.frame_toggle)
        self.btn_toggle_menu.setObjectName(u"btn_toggle_menu")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_toggle_menu.sizePolicy().hasHeightForWidth())
        self.btn_toggle_menu.setSizePolicy(sizePolicy)
        self.btn_toggle_menu.setStyleSheet(u"QPushButton {\n"
"	background-position: center;\n"
"	background-repeat: no-reperat;\n"
"	border: none;\n"
"background-color: rgb(27, 29, 35);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: gb(85, 85, 85);\n"
"}")
        icon = QIcon()
        icon.addFile(u":/icons/icons/menu-main.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_toggle_menu.setIcon(icon)

        self.verticalLayout_3.addWidget(self.btn_toggle_menu)


        self.horizontalLayout_3.addWidget(self.frame_toggle)

        self.frame_top_middle = QFrame(self.frame_top)
        self.frame_top_middle.setObjectName(u"frame_top_middle")
        self.frame_top_middle.setMaximumSize(QSize(16777215, 50))
        self.frame_top_middle.setStyleSheet(u"")
        self.frame_top_middle.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_top_middle.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_top_middle)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frame_icon_top_bar = QFrame(self.frame_top_middle)
        self.frame_icon_top_bar.setObjectName(u"frame_icon_top_bar")
        self.frame_icon_top_bar.setMinimumSize(QSize(40, 40))
        self.frame_icon_top_bar.setMaximumSize(QSize(40, 40))
        self.frame_icon_top_bar.setStyleSheet(u"background: transparent;\n"
"background-position: center;\n"
"background-repeat: no-repeat;\n"
"")
        self.frame_icon_top_bar.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_icon_top_bar.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_4.addWidget(self.frame_icon_top_bar)

        self.toolButton_main = QToolButton(self.frame_top_middle)
        self.toolButton_main.setObjectName(u"toolButton_main")
        self.toolButton_main.setMinimumSize(QSize(60, 40))
        self.toolButton_main.setMaximumSize(QSize(20, 16777215))
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(True)
        self.toolButton_main.setFont(font1)
        self.toolButton_main.setStyleSheet(u"background: transparent;\n"
"")
        self.toolButton_main.setText(u"MENU")
        self.toolButton_main.setIconSize(QSize(40, 40))
        self.toolButton_main.setCheckable(False)
        self.toolButton_main.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.toolButton_main.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.toolButton_main.setAutoRaise(False)
        self.toolButton_main.setArrowType(Qt.ArrowType.NoArrow)

        self.horizontalLayout_4.addWidget(self.toolButton_main)

        self.toolButton_help = QToolButton(self.frame_top_middle)
        self.toolButton_help.setObjectName(u"toolButton_help")
        self.toolButton_help.setMinimumSize(QSize(20, 40))
        self.toolButton_help.setMaximumSize(QSize(20, 16777215))
        self.toolButton_help.setFont(font1)
        self.toolButton_help.setStyleSheet(u"background: transparent;\n"
"")
        self.toolButton_help.setText(u"?")
        self.toolButton_help.setIconSize(QSize(40, 40))
        self.toolButton_help.setCheckable(False)
        self.toolButton_help.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.toolButton_help.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.toolButton_help.setAutoRaise(False)
        self.toolButton_help.setArrowType(Qt.ArrowType.NoArrow)

        self.horizontalLayout_4.addWidget(self.toolButton_help)

        self.horizontalSpacer_3 = QSpacerItem(20, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.lbl_database_name = QLabel(self.frame_top_middle)
        self.lbl_database_name.setObjectName(u"lbl_database_name")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lbl_database_name.sizePolicy().hasHeightForWidth())
        self.lbl_database_name.setSizePolicy(sizePolicy1)
        self.lbl_database_name.setMinimumSize(QSize(40, 20))
        self.lbl_database_name.setMaximumSize(QSize(16777215, 30))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(True)
        self.lbl_database_name.setFont(font2)
        self.lbl_database_name.setStyleSheet(u"")
        self.lbl_database_name.setFrameShape(QFrame.Shape.NoFrame)
        self.lbl_database_name.setFrameShadow(QFrame.Shadow.Plain)
        self.lbl_database_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_database_name.setMargin(5)
        self.lbl_database_name.setIndent(10)

        self.horizontalLayout_4.addWidget(self.lbl_database_name)

        self.horizontalSpacer_4 = QSpacerItem(100, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)

        self.label_title_bar_top = QLabel(self.frame_top_middle)
        self.label_title_bar_top.setObjectName(u"label_title_bar_top")
        sizePolicy1.setHeightForWidth(self.label_title_bar_top.sizePolicy().hasHeightForWidth())
        self.label_title_bar_top.setSizePolicy(sizePolicy1)
        self.label_title_bar_top.setMaximumSize(QSize(200, 25))
        font3 = QFont()
        font3.setFamilies([u"Segoe UI"])
        font3.setPointSize(19)
        font3.setBold(True)
        self.label_title_bar_top.setFont(font3)
        self.label_title_bar_top.setStyleSheet(u"")
        self.label_title_bar_top.setPixmap(QPixmap(u":/icons/icons/WISDAM_Aligned Logo_White.svg"))
        self.label_title_bar_top.setScaledContents(True)
        self.label_title_bar_top.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.label_title_bar_top)

        self.horizontalSpacer_5 = QSpacerItem(10, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_5)


        self.horizontalLayout_3.addWidget(self.frame_top_middle)

        self.frame_btns_right = QFrame(self.frame_top)
        self.frame_btns_right.setObjectName(u"frame_btns_right")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.frame_btns_right.sizePolicy().hasHeightForWidth())
        self.frame_btns_right.setSizePolicy(sizePolicy2)
        self.frame_btns_right.setMaximumSize(QSize(120, 16777215))
        self.frame_btns_right.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_btns_right.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_btns_right)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.btn_minimize = QPushButton(self.frame_btns_right)
        self.btn_minimize.setObjectName(u"btn_minimize")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.btn_minimize.sizePolicy().hasHeightForWidth())
        self.btn_minimize.setSizePolicy(sizePolicy3)
        self.btn_minimize.setMinimumSize(QSize(40, 0))
        self.btn_minimize.setMaximumSize(QSize(40, 16777215))
        self.btn_minimize.setStyleSheet(u"QPushButton {	\n"
"	border: none;\n"
"	background-color: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(85, 170, 255);\n"
"}\n"
"")
        self.btn_minimize.setText(u"")
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/ico-window-minimize.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_minimize.setIcon(icon1)

        self.horizontalLayout_5.addWidget(self.btn_minimize)

        self.btn_maximize_restore = QPushButton(self.frame_btns_right)
        self.btn_maximize_restore.setObjectName(u"btn_maximize_restore")
        sizePolicy3.setHeightForWidth(self.btn_maximize_restore.sizePolicy().hasHeightForWidth())
        self.btn_maximize_restore.setSizePolicy(sizePolicy3)
        self.btn_maximize_restore.setMinimumSize(QSize(40, 0))
        self.btn_maximize_restore.setMaximumSize(QSize(40, 16777215))
        self.btn_maximize_restore.setStyleSheet(u"QPushButton {	\n"
"	border: none;\n"
"	background-color: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(85, 170, 255);\n"
"}\n"
"")
        self.btn_maximize_restore.setText(u"")
        icon2 = QIcon()
        icon2.addFile(u":/icons/icons/ico-window-maximize.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_maximize_restore.setIcon(icon2)

        self.horizontalLayout_5.addWidget(self.btn_maximize_restore)

        self.btn_close = QPushButton(self.frame_btns_right)
        self.btn_close.setObjectName(u"btn_close")
        sizePolicy3.setHeightForWidth(self.btn_close.sizePolicy().hasHeightForWidth())
        self.btn_close.setSizePolicy(sizePolicy3)
        self.btn_close.setMinimumSize(QSize(40, 0))
        self.btn_close.setMaximumSize(QSize(40, 16777215))
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
        icon3 = QIcon()
        icon3.addFile(u":/icons/icons/ico-x.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_close.setIcon(icon3)

        self.horizontalLayout_5.addWidget(self.btn_close)


        self.horizontalLayout_3.addWidget(self.frame_btns_right)


        self.verticalLayout.addWidget(self.frame_top)

        self.frame_center = QFrame(self.frame_main)
        self.frame_center.setObjectName(u"frame_center")
        sizePolicy.setHeightForWidth(self.frame_center.sizePolicy().hasHeightForWidth())
        self.frame_center.setSizePolicy(sizePolicy)
        self.frame_center.setStyleSheet(u"")
        self.frame_center.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_center.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_center)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_left_menu = QFrame(self.frame_center)
        self.frame_left_menu.setObjectName(u"frame_left_menu")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.frame_left_menu.sizePolicy().hasHeightForWidth())
        self.frame_left_menu.setSizePolicy(sizePolicy4)
        self.frame_left_menu.setMinimumSize(QSize(60, 0))
        self.frame_left_menu.setMaximumSize(QSize(60, 16777215))
        self.frame_left_menu.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.frame_left_menu.setStyleSheet(u"background-color: rgb(27, 29, 35);")
        self.frame_left_menu.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_left_menu.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_left_menu)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.frame_menus = QFrame(self.frame_left_menu)
        self.frame_menus.setObjectName(u"frame_menus")
        sizePolicy1.setHeightForWidth(self.frame_menus.sizePolicy().hasHeightForWidth())
        self.frame_menus.setSizePolicy(sizePolicy1)
        self.frame_menus.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_menus.setFrameShadow(QFrame.Shadow.Raised)
        self.layout_menus = QVBoxLayout(self.frame_menus)
        self.layout_menus.setSpacing(0)
        self.layout_menus.setObjectName(u"layout_menus")
        self.layout_menus.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_5.addWidget(self.frame_menus)

        self.verticalSpacer_6 = QSpacerItem(20, 617, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_6)

        self.frame_extra_menus = QFrame(self.frame_left_menu)
        self.frame_extra_menus.setObjectName(u"frame_extra_menus")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.frame_extra_menus.sizePolicy().hasHeightForWidth())
        self.frame_extra_menus.setSizePolicy(sizePolicy5)
        self.frame_extra_menus.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_extra_menus.setFrameShadow(QFrame.Shadow.Raised)
        self.layout_menu_bottom = QVBoxLayout(self.frame_extra_menus)
        self.layout_menu_bottom.setSpacing(0)
        self.layout_menu_bottom.setObjectName(u"layout_menu_bottom")
        self.layout_menu_bottom.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_5.addWidget(self.frame_extra_menus)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_7)

        self.frame_35 = QFrame(self.frame_left_menu)
        self.frame_35.setObjectName(u"frame_35")
        sizePolicy5.setHeightForWidth(self.frame_35.sizePolicy().hasHeightForWidth())
        self.frame_35.setSizePolicy(sizePolicy5)
        self.frame_35.setMinimumSize(QSize(0, 100))
        self.frame_35.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_35.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_35)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.waiting_spinner_main = QtWaitingSpinner(self.frame_35)
        self.waiting_spinner_main.setObjectName(u"waiting_spinner_main")
        self.waiting_spinner_main.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_7.addWidget(self.waiting_spinner_main)


        self.verticalLayout_5.addWidget(self.frame_35)


        self.horizontalLayout_2.addWidget(self.frame_left_menu)

        self.frame_content_right = QFrame(self.frame_center)
        self.frame_content_right.setObjectName(u"frame_content_right")
        self.frame_content_right.setStyleSheet(u"background-color: rgb(44, 49, 60);")
        self.frame_content_right.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_content_right.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_content_right)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.page_stack = QStackedWidget(self.frame_content_right)
        self.page_stack.setObjectName(u"page_stack")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.page_stack.sizePolicy().hasHeightForWidth())
        self.page_stack.setSizePolicy(sizePolicy6)
        self.page_stack.setMinimumSize(QSize(100, 0))
        self.page_stack.setMaximumSize(QSize(16777215, 16777215))
        font4 = QFont()
        font4.setPointSize(11)
        self.page_stack.setFont(font4)
        self.page_stack.setStyleSheet(u"")
        self.page_home = QWidget()
        self.page_home.setObjectName(u"page_home")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.page_home.sizePolicy().hasHeightForWidth())
        self.page_home.setSizePolicy(sizePolicy7)
        self.gauge_images_inspected = GAUGEProgress(self.page_home)
        self.gauge_images_inspected.setObjectName(u"gauge_images_inspected")
        self.gauge_images_inspected.setGeometry(QRect(770, 440, 180, 180))
        self.gauge_images_inspected.setStyleSheet(u"background-color:rgb(255, 85, 0)")
        self.label_30 = QLabel(self.page_home)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setGeometry(QRect(30, 430, 151, 51))
        font5 = QFont()
        font5.setPointSize(30)
        font5.setBold(True)
        self.label_30.setFont(font5)
        self.label_30.setStyleSheet(u"color: #61d6e8;")
        self.label_30.setText(u"Images")
        self.label_30.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.gauge_ai_reviewed = GAUGEProgress(self.page_home)
        self.gauge_ai_reviewed.setObjectName(u"gauge_ai_reviewed")
        self.gauge_ai_reviewed.setGeometry(QRect(770, 630, 180, 180))
        self.gauge_ai_reviewed.setStyleSheet(u"background-color:rgb(255, 85, 0)")
        self.label_32 = QLabel(self.page_home)
        self.label_32.setObjectName(u"label_32")
        self.label_32.setGeometry(QRect(50, 290, 121, 41))
        font6 = QFont()
        font6.setPointSize(19)
        font6.setBold(True)
        self.label_32.setFont(font6)
        self.label_32.setStyleSheet(u"color: #88c736")
        self.label_32.setText(u"External")
        self.label_32.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.label_6 = QLabel(self.page_home)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(100, 570, 111, 31))
        font7 = QFont()
        font7.setPointSize(19)
        font7.setBold(False)
        self.label_6.setFont(font7)
        self.label_6.setStyleSheet(u"color: lightblue;")
        self.prj_label_object_external_nr = QLabel(self.page_home)
        self.prj_label_object_external_nr.setObjectName(u"prj_label_object_external_nr")
        self.prj_label_object_external_nr.setGeometry(QRect(180, 280, 151, 51))
        self.prj_label_object_external_nr.setFont(font5)
        self.prj_label_object_external_nr.setStyleSheet(u"color: #88c736")
        self.prj_label_object_external_nr.setText(u"0")
        self.prj_label_object_external_nr.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.label_33 = QLabel(self.page_home)
        self.label_33.setObjectName(u"label_33")
        self.label_33.setGeometry(QRect(30, 160, 141, 60))
        self.label_33.setFont(font5)
        self.label_33.setStyleSheet(u"color: #88c736")
        self.label_33.setText(u"Objects")
        self.label_33.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.gauge_images_georef = GAUGEProgress(self.page_home)
        self.gauge_images_georef.setObjectName(u"gauge_images_georef")
        self.gauge_images_georef.setGeometry(QRect(570, 440, 180, 180))
        font8 = QFont()
        font8.setPointSize(9)
        self.gauge_images_georef.setFont(font8)
        self.gauge_images_georef.setStyleSheet(u"background-color:rgb(255, 85, 0)")
        self.led_image_path = QLabel(self.page_home)
        self.led_image_path.setObjectName(u"led_image_path")
        self.led_image_path.setGeometry(QRect(60, 570, 31, 31))
        self.led_image_path.setStyleSheet(u"color: white;border-radius: 20;\n"
"background-color: qlineargradient(spread:pad, x1:0.145, y1:0.16, x2:1, y2:1, stop:0 rgba(20, 252, 7, 255), stop:1 rgba(25, 134, 5, 255));")
        self.led_image_path.setFrameShape(QFrame.Shape.StyledPanel)
        self.led_image_path.setFrameShadow(QFrame.Shadow.Raised)
        self.led_image_path.setLineWidth(1)
        self.prj_label_object_manual_nr = QLabel(self.page_home)
        self.prj_label_object_manual_nr.setObjectName(u"prj_label_object_manual_nr")
        self.prj_label_object_manual_nr.setGeometry(QRect(180, 220, 151, 51))
        self.prj_label_object_manual_nr.setFont(font5)
        self.prj_label_object_manual_nr.setStyleSheet(u"color: #88c736")
        self.prj_label_object_manual_nr.setText(u"0")
        self.prj_label_object_manual_nr.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.label_31 = QLabel(self.page_home)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setGeometry(QRect(30, 680, 271, 41))
        self.label_31.setFont(font5)
        self.label_31.setStyleSheet(u"color: #35c69b;")
        self.label_31.setText(u"AI  Detections")
        self.label_31.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.prj_label_object_ai_detection_nr = QLabel(self.page_home)
        self.prj_label_object_ai_detection_nr.setObjectName(u"prj_label_object_ai_detection_nr")
        self.prj_label_object_ai_detection_nr.setGeometry(QRect(60, 740, 221, 71))
        font9 = QFont()
        font9.setPointSize(40)
        font9.setBold(True)
        self.prj_label_object_ai_detection_nr.setFont(font9)
        self.prj_label_object_ai_detection_nr.setStyleSheet(u"color: #35c69b;")
        self.prj_label_object_ai_detection_nr.setText(u"0")
        self.prj_label_object_ai_detection_nr.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.led_elevation_service = QLabel(self.page_home)
        self.led_elevation_service.setObjectName(u"led_elevation_service")
        self.led_elevation_service.setGeometry(QRect(50, 30, 25, 25))
        self.led_elevation_service.setStyleSheet(u"color: white;border-radius: 20;\n"
"background-color: qlineargradient(spread:pad, x1:0.145, y1:0.16, x2:1, y2:1, stop:0 rgba(20, 252, 7, 255), stop:1 rgba(25, 134, 5, 255));")
        self.led_elevation_service.setFrameShape(QFrame.Shape.StyledPanel)
        self.led_elevation_service.setFrameShadow(QFrame.Shadow.Raised)
        self.led_elevation_service.setLineWidth(1)
        self.label_2 = QLabel(self.page_home)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(80, 27, 211, 31))
        font10 = QFont()
        font10.setPointSize(16)
        font10.setBold(True)
        self.label_2.setFont(font10)
        self.label_2.setText(u"Elevation Source")
        self.prj_label_image_number = QLabel(self.page_home)
        self.prj_label_image_number.setObjectName(u"prj_label_image_number")
        self.prj_label_image_number.setGeometry(QRect(60, 470, 211, 101))
        self.prj_label_image_number.setFont(font9)
        self.prj_label_image_number.setStyleSheet(u"color: #61d6e8;")
        self.prj_label_image_number.setText(u"0")
        self.prj_label_image_number.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.chart_view_obj_type = CustomChartView(self.page_home)
        self.chart_view_obj_type.setObjectName(u"chart_view_obj_type")
        self.chart_view_obj_type.setGeometry(QRect(330, 0, 671, 431))
        self.label_47 = QLabel(self.page_home)
        self.label_47.setObjectName(u"label_47")
        self.label_47.setGeometry(QRect(270, 440, 101, 51))
        font11 = QFont()
        font11.setPointSize(19)
        self.label_47.setFont(font11)
        self.label_47.setStyleSheet(u"color: #61d6e8;")
        self.label_47.setText(u"Folders")
        self.label_47.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.label_48 = QLabel(self.page_home)
        self.label_48.setObjectName(u"label_48")
        self.label_48.setGeometry(QRect(270, 500, 101, 51))
        font12 = QFont()
        font12.setPointSize(18)
        self.label_48.setFont(font12)
        self.label_48.setStyleSheet(u"color: #61d6e8;")
        self.label_48.setText(u"Types")
        self.label_48.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.label_49 = QLabel(self.page_home)
        self.label_49.setObjectName(u"label_49")
        self.label_49.setGeometry(QRect(270, 560, 121, 51))
        self.label_49.setFont(font12)
        self.label_49.setStyleSheet(u"color: #61d6e8;")
        self.label_49.setText(u"Mean GSD")
        self.label_49.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.label_41 = QLabel(self.page_home)
        self.label_41.setObjectName(u"label_41")
        self.label_41.setGeometry(QRect(50, 230, 121, 41))
        self.label_41.setFont(font6)
        self.label_41.setStyleSheet(u"color: #88c736")
        self.label_41.setText(u"Manual")
        self.label_41.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.label_50 = QLabel(self.page_home)
        self.label_50.setObjectName(u"label_50")
        self.label_50.setGeometry(QRect(50, 350, 121, 41))
        self.label_50.setFont(font6)
        self.label_50.setStyleSheet(u"color: #88c736")
        self.label_50.setText(u"AI import")
        self.label_50.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.prj_label_object_ai_import_nr = QLabel(self.page_home)
        self.prj_label_object_ai_import_nr.setObjectName(u"prj_label_object_ai_import_nr")
        self.prj_label_object_ai_import_nr.setGeometry(QRect(180, 340, 151, 51))
        self.prj_label_object_ai_import_nr.setFont(font5)
        self.prj_label_object_ai_import_nr.setStyleSheet(u"color: #88c736")
        self.prj_label_object_ai_import_nr.setText(u"0")
        self.prj_label_object_ai_import_nr.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.prj_label_image_types = QLabel(self.page_home)
        self.prj_label_image_types.setObjectName(u"prj_label_image_types")
        self.prj_label_image_types.setGeometry(QRect(410, 500, 111, 51))
        font13 = QFont()
        font13.setPointSize(25)
        font13.setBold(True)
        self.prj_label_image_types.setFont(font13)
        self.prj_label_image_types.setStyleSheet(u"color: #61d6e8;")
        self.prj_label_image_types.setText(u"0")
        self.prj_label_image_types.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.prj_label_image_gsd = QLabel(self.page_home)
        self.prj_label_image_gsd.setObjectName(u"prj_label_image_gsd")
        self.prj_label_image_gsd.setGeometry(QRect(410, 560, 111, 51))
        self.prj_label_image_gsd.setFont(font13)
        self.prj_label_image_gsd.setStyleSheet(u"color: #61d6e8;")
        self.prj_label_image_gsd.setText(u"0")
        self.prj_label_image_gsd.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.prj_label_image_folder = QLabel(self.page_home)
        self.prj_label_image_folder.setObjectName(u"prj_label_image_folder")
        self.prj_label_image_folder.setGeometry(QRect(410, 440, 111, 51))
        self.prj_label_image_folder.setFont(font13)
        self.prj_label_image_folder.setStyleSheet(u"color: #61d6e8;")
        self.prj_label_image_folder.setText(u"0")
        self.prj_label_image_folder.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.label_51 = QLabel(self.page_home)
        self.label_51.setObjectName(u"label_51")
        self.label_51.setGeometry(QRect(290, 740, 121, 51))
        self.label_51.setFont(font11)
        self.label_51.setStyleSheet(u"color: #35c69b;")
        self.label_51.setText(u"Runs")
        self.label_51.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.prj_label_object_ai_processes = QLabel(self.page_home)
        self.prj_label_object_ai_processes.setObjectName(u"prj_label_object_ai_processes")
        self.prj_label_object_ai_processes.setGeometry(QRect(420, 740, 91, 51))
        self.prj_label_object_ai_processes.setFont(font13)
        self.prj_label_object_ai_processes.setStyleSheet(u"color: #35c69b;")
        self.prj_label_object_ai_processes.setText(u"0")
        self.prj_label_object_ai_processes.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.gauge_ai_imported = GAUGEProgress(self.page_home)
        self.gauge_ai_imported.setObjectName(u"gauge_ai_imported")
        self.gauge_ai_imported.setGeometry(QRect(570, 630, 180, 180))
        self.gauge_ai_imported.setStyleSheet(u"background-color:rgb(255, 85, 0)")
        self.label_53 = QLabel(self.page_home)
        self.label_53.setObjectName(u"label_53")
        self.label_53.setGeometry(QRect(270, 620, 151, 51))
        self.label_53.setFont(font12)
        self.label_53.setStyleSheet(u"color: #61d6e8;")
        self.label_53.setText(u"Union AREA")
        self.label_53.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.prj_label_image_union_area = QLabel(self.page_home)
        self.prj_label_image_union_area.setObjectName(u"prj_label_image_union_area")
        self.prj_label_image_union_area.setGeometry(QRect(410, 620, 151, 51))
        self.prj_label_image_union_area.setFont(font13)
        self.prj_label_image_union_area.setStyleSheet(u"color: #61d6e8;")
        self.prj_label_image_union_area.setText(u"0")
        self.prj_label_image_union_area.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.page_stack.addWidget(self.page_home)
        self.prj_label_image_number.raise_()
        self.gauge_images_inspected.raise_()
        self.gauge_ai_reviewed.raise_()
        self.label_32.raise_()
        self.label_6.raise_()
        self.prj_label_object_external_nr.raise_()
        self.label_33.raise_()
        self.gauge_images_georef.raise_()
        self.led_image_path.raise_()
        self.prj_label_object_manual_nr.raise_()
        self.label_31.raise_()
        self.prj_label_object_ai_detection_nr.raise_()
        self.led_elevation_service.raise_()
        self.label_2.raise_()
        self.chart_view_obj_type.raise_()
        self.label_47.raise_()
        self.label_48.raise_()
        self.label_49.raise_()
        self.label_30.raise_()
        self.label_41.raise_()
        self.label_50.raise_()
        self.prj_label_object_ai_import_nr.raise_()
        self.prj_label_image_types.raise_()
        self.prj_label_image_gsd.raise_()
        self.prj_label_image_folder.raise_()
        self.label_51.raise_()
        self.prj_label_object_ai_processes.raise_()
        self.gauge_ai_imported.raise_()
        self.label_53.raise_()
        self.prj_label_image_union_area.raise_()
        self.page_import = QWidget()
        self.page_import.setObjectName(u"page_import")
        self.tab_imports = QTabWidget(self.page_import)
        self.tab_imports.setObjectName(u"tab_imports")
        self.tab_imports.setGeometry(QRect(5, 10, 991, 771))
        self.tab_imports.setFont(font2)
        self.tab_imports.setStyleSheet(u"QTabWidget::pane {\n"
"  border: 0px solid lightgray;\n"
"  top:-1px; \n"
"} \n"
"\n"
"QTabBar::tab {\n"
"background-color: rgb(40, 44, 52);\n"
"  border: 0px solid lightgray; \n"
"  padding: 15px;\n"
"} \n"
"\n"
"QTabBar::tab:selected { \n"
"  background: rgb(92,99, 112); \n"
"  margin-bottom: -1px; \n"
"}")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.tab.setStyleSheet(u"background-color: rgb(40, 44, 52);")
        self.import_image_block = QLineEdit(self.tab)
        self.import_image_block.setObjectName(u"import_image_block")
        self.import_image_block.setGeometry(QRect(500, 90, 191, 31))
        self.import_image_block.setFont(font8)
        self.import_image_block.setStyleSheet(u"background-color: rgb(92,99, 112)")
        self.import_image_block.setText(u"")
        self.import_image_block.setPlaceholderText(u"Survey Block")
        self.imp_rd_recursive = QRadioButton(self.tab)
        self.imp_rd_recursive.setObjectName(u"imp_rd_recursive")
        self.imp_rd_recursive.setGeometry(QRect(270, 490, 151, 20))
        font14 = QFont()
        font14.setPointSize(11)
        font14.setBold(True)
        self.imp_rd_recursive.setFont(font14)
        self.imp_rd_recursive.setText(u"Recursive Import")
        self.imp_rd_recursive.setAutoExclusive(False)
        self.import_image_meta_operator = QLineEdit(self.tab)
        self.import_image_meta_operator.setObjectName(u"import_image_meta_operator")
        self.import_image_meta_operator.setGeometry(QRect(500, 206, 191, 31))
        self.import_image_meta_operator.setFont(font8)
        self.import_image_meta_operator.setStyleSheet(u"background-color: rgb(92,99, 112)")
        self.import_image_meta_operator.setText(u"")
        self.import_image_meta_operator.setPlaceholderText(u"Operator")
        self.imp_btn_image_folder = QPushButton(self.tab)
        self.imp_btn_image_folder.setObjectName(u"imp_btn_image_folder")
        self.imp_btn_image_folder.setEnabled(True)
        self.imp_btn_image_folder.setGeometry(QRect(40, 520, 621, 31))
        self.imp_btn_image_folder.setFont(font2)
        self.imp_btn_image_folder.setStyleSheet(u"QPushButton {\n"
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
        self.imp_btn_image_folder.setText(u"START - Import Image Folder")
        self.imp_stack_type = QStackedWidget(self.tab)
        self.imp_stack_type.setObjectName(u"imp_stack_type")
        self.imp_stack_type.setGeometry(QRect(50, 100, 401, 221))
        self.imp_stack_height = QWidget()
        self.imp_stack_height.setObjectName(u"imp_stack_height")
        self.frame_adj_rel_height = QFrame(self.imp_stack_height)
        self.frame_adj_rel_height.setObjectName(u"frame_adj_rel_height")
        self.frame_adj_rel_height.setEnabled(True)
        self.frame_adj_rel_height.setGeometry(QRect(20, 40, 361, 71))
        self.frame_adj_rel_height.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_adj_rel_height.setFrameShadow(QFrame.Shadow.Raised)
        self.input_adj_rel_height = QLineEdit(self.frame_adj_rel_height)
        self.input_adj_rel_height.setObjectName(u"input_adj_rel_height")
        self.input_adj_rel_height.setGeometry(QRect(260, 20, 81, 31))
        self.input_adj_rel_height.setFont(font8)
        self.input_adj_rel_height.setStyleSheet(u"background-color: rgb(92,99, 112)")
        self.label_37 = QLabel(self.frame_adj_rel_height)
        self.label_37.setObjectName(u"label_37")
        self.label_37.setGeometry(QRect(20, 30, 231, 16))
        self.imp_stack_type.addWidget(self.imp_stack_height)
        self.imp_stack_logFile = QWidget()
        self.imp_stack_logFile.setObjectName(u"imp_stack_logFile")
        self.imp_rd_logfile_image_folders = QRadioButton(self.imp_stack_logFile)
        self.imp_rd_logfile_image_folders.setObjectName(u"imp_rd_logfile_image_folders")
        self.imp_rd_logfile_image_folders.setGeometry(QRect(70, 20, 281, 20))
        self.imp_rd_logfile_image_folders.setFont(font14)
        self.imp_rd_logfile_image_folders.setText(u"Search for Logfiles in Image Folders")
        self.imp_rd_logfile_image_folders.setAutoExclusive(False)
        self.frame_logfile_buttons = QFrame(self.imp_stack_logFile)
        self.frame_logfile_buttons.setObjectName(u"frame_logfile_buttons")
        self.frame_logfile_buttons.setGeometry(QRect(10, 50, 381, 191))
        self.frame_logfile_buttons.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_logfile_buttons.setFrameShadow(QFrame.Shadow.Raised)
        self.imp_btn_logfile_folder = QPushButton(self.frame_logfile_buttons)
        self.imp_btn_logfile_folder.setObjectName(u"imp_btn_logfile_folder")
        self.imp_btn_logfile_folder.setEnabled(True)
        self.imp_btn_logfile_folder.setGeometry(QRect(10, 120, 361, 61))
        self.imp_btn_logfile_folder.setFont(font2)
        self.imp_btn_logfile_folder.setStyleSheet(u"QPushButton {\n"
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
        self.imp_btn_logfile = QPushButton(self.frame_logfile_buttons)
        self.imp_btn_logfile.setObjectName(u"imp_btn_logfile")
        self.imp_btn_logfile.setEnabled(True)
        self.imp_btn_logfile.setGeometry(QRect(10, 10, 361, 61))
        self.imp_btn_logfile.setFont(font2)
        self.imp_btn_logfile.setStyleSheet(u"QPushButton {\n"
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
        self.imp_rd_recursive_logfiles_folder = QRadioButton(self.frame_logfile_buttons)
        self.imp_rd_recursive_logfiles_folder.setObjectName(u"imp_rd_recursive_logfiles_folder")
        self.imp_rd_recursive_logfiles_folder.setGeometry(QRect(70, 90, 241, 20))
        self.imp_rd_recursive_logfiles_folder.setFont(font14)
        self.imp_rd_recursive_logfiles_folder.setText(u"Recursive search for logfiles")
        self.imp_rd_recursive_logfiles_folder.setAutoExclusive(False)
        self.imp_stack_type.addWidget(self.imp_stack_logFile)
        self.imp_stack_georef = QWidget()
        self.imp_stack_georef.setObjectName(u"imp_stack_georef")
        self.label_38 = QLabel(self.imp_stack_georef)
        self.label_38.setObjectName(u"label_38")
        self.label_38.setGeometry(QRect(0, 80, 211, 20))
        self.label_38.setFont(font2)
        self.label_36 = QLabel(self.imp_stack_georef)
        self.label_36.setObjectName(u"label_36")
        self.label_36.setGeometry(QRect(220, 20, 101, 20))
        self.label_36.setFont(font2)
        self.imp_georef_latitude = QLineEdit(self.imp_stack_georef)
        self.imp_georef_latitude.setObjectName(u"imp_georef_latitude")
        self.imp_georef_latitude.setGeometry(QRect(0, 40, 151, 31))
        font15 = QFont()
        font15.setPointSize(10)
        self.imp_georef_latitude.setFont(font15)
        self.imp_georef_latitude.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.label_40 = QLabel(self.imp_stack_georef)
        self.label_40.setObjectName(u"label_40")
        self.label_40.setGeometry(QRect(220, 160, 121, 20))
        self.label_40.setFont(font2)
        self.imp_georef_sensor_width = QLineEdit(self.imp_stack_georef)
        self.imp_georef_sensor_width.setObjectName(u"imp_georef_sensor_width")
        self.imp_georef_sensor_width.setGeometry(QRect(0, 180, 151, 31))
        self.imp_georef_sensor_width.setFont(font15)
        self.imp_georef_sensor_width.setStyleSheet(u"background-color:rgb(193, 64, 0)")
        self.imp_georef_height = QLineEdit(self.imp_stack_georef)
        self.imp_georef_height.setObjectName(u"imp_georef_height")
        self.imp_georef_height.setGeometry(QRect(0, 100, 151, 31))
        self.imp_georef_height.setFont(font15)
        self.imp_georef_height.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.label_39 = QLabel(self.imp_stack_georef)
        self.label_39.setObjectName(u"label_39")
        self.label_39.setGeometry(QRect(0, 20, 81, 20))
        self.label_39.setFont(font2)
        self.imp_georef_focal_mm = QLineEdit(self.imp_stack_georef)
        self.imp_georef_focal_mm.setObjectName(u"imp_georef_focal_mm")
        self.imp_georef_focal_mm.setGeometry(QRect(220, 180, 151, 31))
        self.imp_georef_focal_mm.setFont(font15)
        self.imp_georef_focal_mm.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.imp_georef_longitude = QLineEdit(self.imp_stack_georef)
        self.imp_georef_longitude.setObjectName(u"imp_georef_longitude")
        self.imp_georef_longitude.setGeometry(QRect(220, 40, 151, 31))
        self.imp_georef_longitude.setFont(font15)
        self.imp_georef_longitude.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.imp_georef_heading = QLineEdit(self.imp_stack_georef)
        self.imp_georef_heading.setObjectName(u"imp_georef_heading")
        self.imp_georef_heading.setGeometry(QRect(220, 120, 151, 31))
        self.imp_georef_heading.setFont(font15)
        self.imp_georef_heading.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.label_42 = QLabel(self.imp_stack_georef)
        self.label_42.setObjectName(u"label_42")
        self.label_42.setGeometry(QRect(220, 90, 171, 31))
        self.label_42.setFont(font2)
        self.label_43 = QLabel(self.imp_stack_georef)
        self.label_43.setObjectName(u"label_43")
        self.label_43.setGeometry(QRect(0, 160, 161, 21))
        self.label_43.setFont(font2)
        self.label_44 = QLabel(self.imp_stack_georef)
        self.label_44.setObjectName(u"label_44")
        self.label_44.setGeometry(QRect(120, 0, 81, 20))
        self.label_44.setFont(font2)
        self.imp_georef_status = QLabel(self.imp_stack_georef)
        self.imp_georef_status.setObjectName(u"imp_georef_status")
        self.imp_georef_status.setGeometry(QRect(0, 220, 591, 21))
        self.imp_georef_status.setFont(font2)
        self.imp_georef_status.setStyleSheet(u"color: rgb(255, 85, 0)")
        self.imp_stack_type.addWidget(self.imp_stack_georef)
        self.imp_stack_empty = QWidget()
        self.imp_stack_empty.setObjectName(u"imp_stack_empty")
        self.imp_stack_type.addWidget(self.imp_stack_empty)
        self.import_image_meta_comment = QPlainTextEdit(self.tab)
        self.import_image_meta_comment.setObjectName(u"import_image_meta_comment")
        self.import_image_meta_comment.setGeometry(QRect(500, 330, 191, 71))
        self.import_image_meta_comment.setFont(font8)
        self.import_image_meta_comment.setStyleSheet(u"background-color: rgb(92,99, 112)")
        self.import_image_meta_comment.setFrameShape(QFrame.Shape.NoFrame)
        self.import_image_meta_comment.setFrameShadow(QFrame.Shadow.Plain)
        self.import_image_meta_comment.setPlaceholderText(u"Comments")
        self.label_8 = QLabel(self.tab)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(500, 182, 181, 21))
        self.label_8.setFont(font14)
        self.label_8.setText(u"Image Metadata:")
        self.imp_cmb_input_type = QComboBox(self.tab)
        self.imp_cmb_input_type.setObjectName(u"imp_cmb_input_type")
        self.imp_cmb_input_type.setEnabled(True)
        self.imp_cmb_input_type.setGeometry(QRect(70, 40, 361, 61))
        font16 = QFont()
        font16.setFamilies([u"Segoe UI"])
        font16.setPointSize(10)
        font16.setBold(True)
        self.imp_cmb_input_type.setFont(font16)
        self.imp_cmb_input_type.setStyleSheet(u"QComboBox{\n"
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
        self.imp_cmb_input_type.setIconSize(QSize(16, 16))
        self.imp_cmb_input_type.setDuplicatesEnabled(False)
        self.label_9 = QLabel(self.tab)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(70, 10, 201, 21))
        self.label_9.setFont(font14)
        self.label_9.setText(u"Data Loader")
        self.import_image_reference = QLineEdit(self.tab)
        self.import_image_reference.setObjectName(u"import_image_reference")
        self.import_image_reference.setGeometry(QRect(500, 50, 191, 31))
        self.import_image_reference.setFont(font8)
        self.import_image_reference.setStyleSheet(u"background-color: rgb(92,99, 112)")
        self.import_image_reference.setText(u"")
        self.import_image_reference.setPlaceholderText(u"Flight ID / Reference")
        self.import_image_meta_camera = QLineEdit(self.tab)
        self.import_image_meta_camera.setObjectName(u"import_image_meta_camera")
        self.import_image_meta_camera.setGeometry(QRect(500, 246, 191, 31))
        self.import_image_meta_camera.setFont(font8)
        self.import_image_meta_camera.setStyleSheet(u"background-color: rgb(92,99, 112)")
        self.import_image_meta_camera.setText(u"")
        self.import_image_meta_camera.setPlaceholderText(u"Camera ID / Reference")
        self.import_image_transect = QLineEdit(self.tab)
        self.import_image_transect.setObjectName(u"import_image_transect")
        self.import_image_transect.setGeometry(QRect(500, 130, 191, 31))
        self.import_image_transect.setFont(font8)
        self.import_image_transect.setStyleSheet(u"background-color: rgb(92,99, 112)")
        self.import_image_transect.setText(u"")
        self.import_image_transect.setPlaceholderText(u"Transect")
        self.import_image_conditions = QLineEdit(self.tab)
        self.import_image_conditions.setObjectName(u"import_image_conditions")
        self.import_image_conditions.setGeometry(QRect(500, 288, 191, 31))
        self.import_image_conditions.setFont(font8)
        self.import_image_conditions.setStyleSheet(u"background-color: rgb(92,99, 112)")
        self.import_image_conditions.setText(u"")
        self.import_image_conditions.setPlaceholderText(u"Conditions")
        self.label_18 = QLabel(self.tab)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setGeometry(QRect(500, 28, 181, 21))
        self.label_18.setFont(font14)
        self.label_18.setText(u"Survey Data:")
        self.stack_image_test = QStackedWidget(self.tab)
        self.stack_image_test.setObjectName(u"stack_image_test")
        self.stack_image_test.setGeometry(QRect(40, 570, 621, 141))
        self.stack_image_test.setStyleSheet(u"#stack_image_test{\n"
"border: 1px solid rgb(170, 170, 255);\n"
"border-radius:10px;\n"
"padding-left: 6px;\n"
"padding-right: 6px;\n"
"padding-top: 6px;}\n"
"")
        self.stack_image_test.setFrameShape(QFrame.Shape.Box)
        self.stack_image_test.setFrameShadow(QFrame.Shadow.Plain)
        self.stack_image_test.setLineWidth(5)
        self.stack_image_test.setMidLineWidth(0)
        self.page_exif_test = QWidget()
        self.page_exif_test.setObjectName(u"page_exif_test")
        self.btn_test_image_exif = QPushButton(self.page_exif_test)
        self.btn_test_image_exif.setObjectName(u"btn_test_image_exif")
        self.btn_test_image_exif.setEnabled(True)
        self.btn_test_image_exif.setGeometry(QRect(10, 10, 111, 101))
        self.btn_test_image_exif.setFont(font2)
        self.btn_test_image_exif.setStyleSheet(u"QPushButton {\n"
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
        self.btn_test_image_exif.setText(u"Test Image for\n"
"Metadata")
        self.led_focal_length = QPushButton(self.page_exif_test)
        self.led_focal_length.setObjectName(u"led_focal_length")
        self.led_focal_length.setGeometry(QRect(140, 12, 18, 18))
        self.led_focal_length.setStyleSheet(u"color: white;border-radius: 20;\n"
"        background-color: qlineargradient(spread:pad, x1:0.145, y1:0.16, x2:1, y2:1, stop:0 rgba(255, 25, 7, 255),\n"
"        stop:1 rgba(134, 25, 5, 255));")
        self.led_gnss_data = QPushButton(self.page_exif_test)
        self.led_gnss_data.setObjectName(u"led_gnss_data")
        self.led_gnss_data.setGeometry(QRect(140, 50, 18, 18))
        self.led_gnss_data.setStyleSheet(u"color: white;border-radius: 20;\n"
"        background-color: qlineargradient(spread:pad, x1:0.145, y1:0.16, x2:1, y2:1, stop:0 rgba(255, 25, 7, 255),\n"
"        stop:1 rgba(134, 25, 5, 255));")
        self.led_image_pose = QPushButton(self.page_exif_test)
        self.led_image_pose.setObjectName(u"led_image_pose")
        self.led_image_pose.setGeometry(QRect(140, 90, 18, 18))
        self.led_image_pose.setStyleSheet(u"color: white;border-radius: 20;\n"
"        background-color: qlineargradient(spread:pad, x1:0.145, y1:0.16, x2:1, y2:1, stop:0 rgba(255, 25, 7, 255),\n"
"        stop:1 rgba(134, 25, 5, 255));")
        self.led_crs_vertical = QPushButton(self.page_exif_test)
        self.led_crs_vertical.setObjectName(u"led_crs_vertical")
        self.led_crs_vertical.setGeometry(QRect(310, 90, 18, 18))
        self.led_crs_vertical.setStyleSheet(u"color: white;border-radius: 20;\n"
"        background-color: qlineargradient(spread:pad, x1:0.145, y1:0.16, x2:1, y2:1, stop:0 rgba(255, 25, 7, 255),\n"
"        stop:1 rgba(134, 25, 5, 255));")
        self.led_crs_data = QPushButton(self.page_exif_test)
        self.led_crs_data.setObjectName(u"led_crs_data")
        self.led_crs_data.setGeometry(QRect(310, 50, 18, 18))
        self.led_crs_data.setStyleSheet(u"color: white;border-radius: 20;\n"
"        background-color: qlineargradient(spread:pad, x1:0.145, y1:0.16, x2:1, y2:1, stop:0 rgba(255, 25, 7, 255),\n"
"        stop:1 rgba(134, 25, 5, 255));")
        self.label_20 = QLabel(self.page_exif_test)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setGeometry(QRect(170, 5, 291, 31))
        font17 = QFont()
        font17.setPointSize(13)
        font17.setBold(True)
        self.label_20.setFont(font17)
        self.label_20.setText(u"Focal Length in Pixel Possible")
        self.label_56 = QLabel(self.page_exif_test)
        self.label_56.setObjectName(u"label_56")
        self.label_56.setGeometry(QRect(340, 50, 251, 21))
        self.label_56.setFont(font17)
        self.label_56.setText(u"CRS Specified")
        self.label_55 = QLabel(self.page_exif_test)
        self.label_55.setObjectName(u"label_55")
        self.label_55.setGeometry(QRect(170, 85, 141, 31))
        self.label_55.setFont(font17)
        self.label_55.setText(u"Image Pose")
        self.label_58 = QLabel(self.page_exif_test)
        self.label_58.setObjectName(u"label_58")
        self.label_58.setGeometry(QRect(340, 90, 261, 21))
        self.label_58.setFont(font17)
        self.label_58.setText(u"Vertical Datum Specified")
        self.label_54 = QLabel(self.page_exif_test)
        self.label_54.setObjectName(u"label_54")
        self.label_54.setGeometry(QRect(170, 50, 131, 21))
        self.label_54.setFont(font17)
        self.label_54.setText(u"GNSS Data")
        self.stack_image_test.addWidget(self.page_exif_test)
        self.page_ortho_test = QWidget()
        self.page_ortho_test.setObjectName(u"page_ortho_test")
        self.label_57 = QLabel(self.page_ortho_test)
        self.label_57.setObjectName(u"label_57")
        self.label_57.setGeometry(QRect(170, 50, 411, 21))
        self.label_57.setFont(font17)
        self.led_ortho_coordinates = QPushButton(self.page_ortho_test)
        self.led_ortho_coordinates.setObjectName(u"led_ortho_coordinates")
        self.led_ortho_coordinates.setGeometry(QRect(140, 50, 18, 18))
        self.led_ortho_coordinates.setStyleSheet(u"color: white;border-radius: 20;\n"
"        background-color: qlineargradient(spread:pad, x1:0.145, y1:0.16, x2:1, y2:1, stop:0 rgba(255, 25, 7, 255),\n"
"        stop:1 rgba(134, 25, 5, 255));")
        self.btn_test_image_ortho = QPushButton(self.page_ortho_test)
        self.btn_test_image_ortho.setObjectName(u"btn_test_image_ortho")
        self.btn_test_image_ortho.setEnabled(True)
        self.btn_test_image_ortho.setGeometry(QRect(10, 10, 111, 101))
        self.btn_test_image_ortho.setFont(font2)
        self.btn_test_image_ortho.setStyleSheet(u"QPushButton {\n"
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
        self.btn_test_image_ortho.setText(u"Test\n"
"Ortho imagery \n"
"for META data")
        self.label_59 = QLabel(self.page_ortho_test)
        self.label_59.setObjectName(u"label_59")
        self.label_59.setGeometry(QRect(170, 10, 301, 21))
        self.label_59.setFont(font17)
        self.led_rasterio_possible = QPushButton(self.page_ortho_test)
        self.led_rasterio_possible.setObjectName(u"led_rasterio_possible")
        self.led_rasterio_possible.setGeometry(QRect(140, 10, 18, 18))
        self.led_rasterio_possible.setStyleSheet(u"color: white;border-radius: 20;\n"
"        background-color: qlineargradient(spread:pad, x1:0.145, y1:0.16, x2:1, y2:1, stop:0 rgba(255, 25, 7, 255),\n"
"        stop:1 rgba(134, 25, 5, 255));")
        self.led_ortho_crs = QPushButton(self.page_ortho_test)
        self.led_ortho_crs.setObjectName(u"led_ortho_crs")
        self.led_ortho_crs.setGeometry(QRect(140, 90, 18, 18))
        self.led_ortho_crs.setStyleSheet(u"color: white;border-radius: 20;\n"
"        background-color: qlineargradient(spread:pad, x1:0.145, y1:0.16, x2:1, y2:1, stop:0 rgba(255, 25, 7, 255),\n"
"        stop:1 rgba(134, 25, 5, 255));")
        self.label_60 = QLabel(self.page_ortho_test)
        self.label_60.setObjectName(u"label_60")
        self.label_60.setGeometry(QRect(170, 90, 221, 21))
        self.label_60.setFont(font17)
        self.stack_image_test.addWidget(self.page_ortho_test)
        self.frame_imp_epsg = QFrame(self.tab)
        self.frame_imp_epsg.setObjectName(u"frame_imp_epsg")
        self.frame_imp_epsg.setGeometry(QRect(70, 350, 361, 131))
        self.frame_imp_epsg.setStyleSheet(u"background-color: rgb(52, 59, 72);border-radius: 5px;")
        self.frame_imp_epsg.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_imp_epsg.setFrameShadow(QFrame.Shadow.Raised)
        self.label_26 = QLabel(self.frame_imp_epsg)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setGeometry(QRect(10, 4, 341, 71))
        self.label_26.setFont(font1)
        self.label_26.setText(u"<html><head/><body><p><span style=\" font-size:8pt;\">!OPTIONAL! - Override CRS (e.g. for JPG orhto where no &quot;.prj&quot;-File is present, or for CSV importer)</span></p><p><span style=\" font-size:10pt;\">CRS like e.g &quot;EPSG:4326+3855&quot; or &quot;EPSG:28533&quot;: </span></p></body></html>")
        self.label_26.setWordWrap(True)
        self.imp_epsg_input = QLineEdit(self.frame_imp_epsg)
        self.imp_epsg_input.setObjectName(u"imp_epsg_input")
        self.imp_epsg_input.setGeometry(QRect(10, 80, 341, 41))
        self.imp_epsg_input.setFont(font1)
        self.imp_epsg_input.setText(u"")
        self.tab_imports.addTab(self.tab, "")
        self.tab_imports.setTabText(self.tab_imports.indexOf(self.tab), u"Import Images")
        self.progressBar_importer = QProgressBar(self.page_import)
        self.progressBar_importer.setObjectName(u"progressBar_importer")
        self.progressBar_importer.setGeometry(QRect(5, 790, 991, 23))
        self.progressBar_importer.setFont(font2)
        self.progressBar_importer.setStyleSheet(u"QProgressBar{\n"
"    border: 2px solid grey;\n"
"    border-radius: 5px;\n"
"    text-align: center;\n"
"	color: darkgreen;\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"   background-color: lightgreen;\n"
"    margin: 1px;\n"
"}")
        self.progressBar_importer.setValue(0)
        self.progressBar_importer.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.progressBar_importer.setTextVisible(True)
        self.progressBar_importer.setInvertedAppearance(False)
        self.progressBar_importer.setTextDirection(QProgressBar.Direction.TopToBottom)
        self.page_stack.addWidget(self.page_import)
        self.page_gis = QWidget()
        self.page_gis.setObjectName(u"page_gis")
        self.horizontalLayout_13 = QHBoxLayout(self.page_gis)
        self.horizontalLayout_13.setSpacing(0)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.btn_gis_toggle_list = QPushButton(self.page_gis)
        self.btn_gis_toggle_list.setObjectName(u"btn_gis_toggle_list")
        sizePolicy8 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.btn_gis_toggle_list.sizePolicy().hasHeightForWidth())
        self.btn_gis_toggle_list.setSizePolicy(sizePolicy8)
        self.btn_gis_toggle_list.setMinimumSize(QSize(0, 0))
        font18 = QFont()
        font18.setFamilies([u"MS Gothic"])
        font18.setPointSize(9)
        self.btn_gis_toggle_list.setFont(font18)
        self.btn_gis_toggle_list.setStyleSheet(u"QPushButton {\n"
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

        self.horizontalLayout_13.addWidget(self.btn_gis_toggle_list)

        self.splitter_gis = QSplitter(self.page_gis)
        self.splitter_gis.setObjectName(u"splitter_gis")
        self.splitter_gis.setOrientation(Qt.Orientation.Horizontal)
        self.splitter_gis.setChildrenCollapsible(False)
        self.frame_gis_object_list = QFrame(self.splitter_gis)
        self.frame_gis_object_list.setObjectName(u"frame_gis_object_list")
        self.frame_gis_object_list.setEnabled(True)
        sizePolicy4.setHeightForWidth(self.frame_gis_object_list.sizePolicy().hasHeightForWidth())
        self.frame_gis_object_list.setSizePolicy(sizePolicy4)
        self.frame_gis_object_list.setMinimumSize(QSize(300, 0))
        self.frame_gis_object_list.setMaximumSize(QSize(16777215, 16777215))
        self.frame_gis_object_list.setStyleSheet(u"background-color: rgb(40, 44, 52);")
        self.frame_gis_object_list.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_gis_object_list.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_14 = QVBoxLayout(self.frame_gis_object_list)
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.gis_image_panel = ImageTreeView(self.frame_gis_object_list)
        self.gis_image_panel.setObjectName(u"gis_image_panel")
        sizePolicy9 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(2)
        sizePolicy9.setHeightForWidth(self.gis_image_panel.sizePolicy().hasHeightForWidth())
        self.gis_image_panel.setSizePolicy(sizePolicy9)
        self.gis_image_panel.setStyleSheet(u"QHeaderView::section { background-color:rgb(98, 103, 111) }\n"
"\n"
"QTreeView{alternate-background-color: #222222; background: transparent;}\n"
"\n"
"QTreeView::branch:has-children:!has-siblings:closed,\n"
"QTreeView::branch:closed:has-children:has-siblings {\n"
"        border-image: none;\n"
"        image: url(:/icons/icons/ico-size-grip.png);\n"
"}\n"
"\n"
"QTreeView::branch:open:has-children:!has-siblings,\n"
"QTreeView::branch:open:has-children:has-siblings  {\n"
"        border-image: none;\n"
"        image:url(:/icons/icons/circle.svg);\n"
"}\n"
"QToolTip {\n"
"	color: white;\n"
"	background-color: black;\n"
"	border: 1px solid rgb(40, 40, 40);\n"
"	border-radius: 2px;\n"
"};")
        self.gis_image_panel.setFrameShape(QFrame.Shape.StyledPanel)
        self.gis_image_panel.setFrameShadow(QFrame.Shadow.Plain)
        self.gis_image_panel.setLineWidth(1)
        self.gis_image_panel.setMidLineWidth(0)
        self.gis_image_panel.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.gis_image_panel.setProperty(u"showDropIndicator", True)
        self.gis_image_panel.setAlternatingRowColors(False)
        self.gis_image_panel.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.gis_image_panel.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.gis_image_panel.setRootIsDecorated(True)
        self.gis_image_panel.setSortingEnabled(True)
        self.gis_image_panel.header().setCascadingSectionResizes(True)
        self.gis_image_panel.header().setStretchLastSection(False)

        self.verticalLayout_14.addWidget(self.gis_image_panel)

        self.frame_36 = QFrame(self.frame_gis_object_list)
        self.frame_36.setObjectName(u"frame_36")
        self.frame_36.setMinimumSize(QSize(0, 70))
        self.frame_36.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_36.setFrameShadow(QFrame.Shadow.Raised)
        self.label_25 = QLabel(self.frame_36)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setGeometry(QRect(1, 10, 61, 51))
        self.label_25.setFont(font1)
        self.label_25.setText(u"Spatial\n"
"Cluster")
        self.gis_btn_calc_group_area = QPushButton(self.frame_36)
        self.gis_btn_calc_group_area.setObjectName(u"gis_btn_calc_group_area")
        self.gis_btn_calc_group_area.setGeometry(QRect(160, 10, 131, 30))
        self.gis_btn_calc_group_area.setMinimumSize(QSize(0, 30))
        self.gis_btn_calc_group_area.setStyleSheet(u"QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(180, 59, 72);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(200, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}")
        self.gis_btn_calc_group_area.setText(u"Calculate")
        self.gis_slider_area_distance = QSlider(self.frame_36)
        self.gis_slider_area_distance.setObjectName(u"gis_slider_area_distance")
        self.gis_slider_area_distance.setGeometry(QRect(160, 45, 131, 21))
        self.gis_slider_area_distance.setStyleSheet(u"background-color: transparent;")
        self.gis_slider_area_distance.setMinimum(2)
        self.gis_slider_area_distance.setMaximum(100)
        self.gis_slider_area_distance.setSingleStep(2)
        self.gis_slider_area_distance.setPageStep(100)
        self.gis_slider_area_distance.setValue(20)
        self.gis_slider_area_distance.setTracking(False)
        self.gis_slider_area_distance.setOrientation(Qt.Orientation.Horizontal)
        self.gis_slider_area_distance.setInvertedAppearance(False)
        self.gis_slider_area_distance.setInvertedControls(False)
        self.gis_slider_area_distance.setTickPosition(QSlider.TickPosition.NoTicks)
        self.gis_slider_area_distance.setTickInterval(50)
        self.frame = QFrame(self.frame_36)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(60, 10, 91, 51))
        self.frame.setFrameShape(QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_14 = QHBoxLayout(self.frame)
        self.horizontalLayout_14.setSpacing(0)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.gis_group_waiting_spinner = QtWaitingSpinner(self.frame)
        self.gis_group_waiting_spinner.setObjectName(u"gis_group_waiting_spinner")
        self.gis_group_waiting_spinner.setMinimumSize(QSize(50, 50))
        self.gis_group_waiting_spinner.setBaseSize(QSize(0, 0))

        self.horizontalLayout_14.addWidget(self.gis_group_waiting_spinner)


        self.verticalLayout_14.addWidget(self.frame_36)

        self.gis_group_area_panel = QTableView(self.frame_gis_object_list)
        self.gis_group_area_panel.setObjectName(u"gis_group_area_panel")
        self.gis_group_area_panel.setMinimumSize(QSize(0, 300))
        self.gis_group_area_panel.setMaximumSize(QSize(16777215, 500))
        self.gis_group_area_panel.setStyleSheet(u"QHeaderView::section { background-color:rgb(98, 103, 111) }\n"
"")
        self.gis_group_area_panel.setFrameShape(QFrame.Shape.StyledPanel)
        self.gis_group_area_panel.setFrameShadow(QFrame.Shadow.Sunken)
        self.gis_group_area_panel.setLineWidth(1)
        self.gis_group_area_panel.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)
        self.gis_group_area_panel.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.gis_group_area_panel.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.gis_group_area_panel.setShowGrid(False)
        self.gis_group_area_panel.horizontalHeader().setStretchLastSection(True)
        self.gis_group_area_panel.verticalHeader().setVisible(False)

        self.verticalLayout_14.addWidget(self.gis_group_area_panel)

        self.splitter_gis.addWidget(self.frame_gis_object_list)
        self.gis_view = GISView(self.splitter_gis)
        self.gis_view.setObjectName(u"gis_view")
        sizePolicy2.setHeightForWidth(self.gis_view.sizePolicy().hasHeightForWidth())
        self.gis_view.setSizePolicy(sizePolicy2)
        self.gis_view.setMinimumSize(QSize(500, 0))
        self.gis_view.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.gis_view.setFrameShape(QFrame.Shape.NoFrame)
        self.gis_view.setLineWidth(1)
        self.splitter_gis.addWidget(self.gis_view)

        self.horizontalLayout_13.addWidget(self.splitter_gis)

        self.frame_gis_properties = QFrame(self.page_gis)
        self.frame_gis_properties.setObjectName(u"frame_gis_properties")
        sizePolicy7.setHeightForWidth(self.frame_gis_properties.sizePolicy().hasHeightForWidth())
        self.frame_gis_properties.setSizePolicy(sizePolicy7)
        self.frame_gis_properties.setMinimumSize(QSize(170, 0))
        self.frame_gis_properties.setStyleSheet(u"background-color: rgb(40, 44, 52);")
        self.frame_gis_properties.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_gis_properties.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_13 = QFrame(self.frame_gis_properties)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setGeometry(QRect(10, 140, 151, 181))
        self.frame_13.setStyleSheet(u"background-color: rgb(127, 84, 0); border-radius:10px;")
        self.frame_13.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_13.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_22 = QVBoxLayout(self.frame_13)
        self.verticalLayout_22.setSpacing(4)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.verticalLayout_22.setContentsMargins(10, 7, 0, 0)
        self.gis_hide_objects = QRadioButton(self.frame_13)
        self.gis_hide_objects.setObjectName(u"gis_hide_objects")
        font19 = QFont()
        font19.setFamilies([u"Segoe UI"])
        font19.setPointSize(11)
        font19.setBold(True)
        self.gis_hide_objects.setFont(font19)
        self.gis_hide_objects.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.gis_hide_objects.setText(u"Hide Objects")
        self.gis_hide_objects.setAutoExclusive(False)

        self.verticalLayout_22.addWidget(self.gis_hide_objects)

        self.line_2 = QFrame(self.frame_13)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setStyleSheet(u"")
        self.line_2.setFrameShadow(QFrame.Shadow.Plain)
        self.line_2.setLineWidth(2)
        self.line_2.setMidLineWidth(0)
        self.line_2.setFrameShape(QFrame.Shape.HLine)

        self.verticalLayout_22.addWidget(self.line_2)

        self.line = QFrame(self.frame_13)
        self.line.setObjectName(u"line")
        self.line.setStyleSheet(u"")
        self.line.setFrameShadow(QFrame.Shadow.Plain)
        self.line.setLineWidth(2)
        self.line.setMidLineWidth(0)
        self.line.setFrameShape(QFrame.Shape.HLine)

        self.verticalLayout_22.addWidget(self.line)

        self.gis_hide_image_centers = QRadioButton(self.frame_13)
        self.gis_hide_image_centers.setObjectName(u"gis_hide_image_centers")
        self.gis_hide_image_centers.setFont(font19)
        self.gis_hide_image_centers.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.gis_hide_image_centers.setText(u"Hide Images")
        self.gis_hide_image_centers.setAutoExclusive(False)

        self.verticalLayout_22.addWidget(self.gis_hide_image_centers)

        self.gis_show_image_center_footprints = QRadioButton(self.frame_13)
        self.gis_show_image_center_footprints.setObjectName(u"gis_show_image_center_footprints")
        self.gis_show_image_center_footprints.setFont(font19)
        self.gis_show_image_center_footprints.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.gis_show_image_center_footprints.setText(u"Show Footprint \n"
"on Hover")
        self.gis_show_image_center_footprints.setChecked(True)
        self.gis_show_image_center_footprints.setAutoExclusive(False)

        self.verticalLayout_22.addWidget(self.gis_show_image_center_footprints)

        self.gis_hide_images = QRadioButton(self.frame_13)
        self.gis_hide_images.setObjectName(u"gis_hide_images")
        self.gis_hide_images.setFont(font19)
        self.gis_hide_images.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.gis_hide_images.setText(u"Hide Footprints")
        self.gis_hide_images.setChecked(True)
        self.gis_hide_images.setAutoExclusive(False)

        self.verticalLayout_22.addWidget(self.gis_hide_images)

        self.frame_28 = QFrame(self.frame_gis_properties)
        self.frame_28.setObjectName(u"frame_28")
        self.frame_28.setGeometry(QRect(10, 580, 151, 221))
        self.frame_28.setStyleSheet(u"background-color: #184d50;border-radius:10px;")
        self.frame_28.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_28.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_21 = QVBoxLayout(self.frame_28)
        self.verticalLayout_21.setSpacing(4)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.verticalLayout_21.setContentsMargins(10, 0, 0, 0)
        self.label_23 = QLabel(self.frame_28)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setMaximumSize(QSize(16777215, 20))
        self.label_23.setFont(font14)
        self.label_23.setText(u"Colour Images")

        self.verticalLayout_21.addWidget(self.label_23)

        self.gis_color_image_folder = QRadioButton(self.frame_28)
        self.buttonGroup_gis_color_images = QButtonGroup(MainWindow)
        self.buttonGroup_gis_color_images.setObjectName(u"buttonGroup_gis_color_images")
        self.buttonGroup_gis_color_images.addButton(self.gis_color_image_folder)
        self.gis_color_image_folder.setObjectName(u"gis_color_image_folder")
        self.gis_color_image_folder.setFont(font19)
        self.gis_color_image_folder.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.gis_color_image_folder.setText(u"Image Folder")
        self.gis_color_image_folder.setChecked(True)
        self.gis_color_image_folder.setAutoExclusive(False)

        self.verticalLayout_21.addWidget(self.gis_color_image_folder)

        self.gis_color_image_group = QRadioButton(self.frame_28)
        self.buttonGroup_gis_color_images.addButton(self.gis_color_image_group)
        self.gis_color_image_group.setObjectName(u"gis_color_image_group")
        self.gis_color_image_group.setFont(font19)
        self.gis_color_image_group.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.gis_color_image_group.setText(u"Image Group")
        self.gis_color_image_group.setChecked(False)
        self.gis_color_image_group.setAutoExclusive(False)

        self.verticalLayout_21.addWidget(self.gis_color_image_group)

        self.gis_color_image_refid = QRadioButton(self.frame_28)
        self.buttonGroup_gis_color_images.addButton(self.gis_color_image_refid)
        self.gis_color_image_refid.setObjectName(u"gis_color_image_refid")
        self.gis_color_image_refid.setFont(font19)
        self.gis_color_image_refid.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.gis_color_image_refid.setText(u"Flight ID / Ref")
        self.gis_color_image_refid.setChecked(False)
        self.gis_color_image_refid.setAutoExclusive(False)

        self.verticalLayout_21.addWidget(self.gis_color_image_refid)

        self.gis_color_image_transect = QRadioButton(self.frame_28)
        self.buttonGroup_gis_color_images.addButton(self.gis_color_image_transect)
        self.gis_color_image_transect.setObjectName(u"gis_color_image_transect")
        self.gis_color_image_transect.setFont(font19)
        self.gis_color_image_transect.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.gis_color_image_transect.setText(u"Transect")
        self.gis_color_image_transect.setChecked(False)
        self.gis_color_image_transect.setAutoExclusive(False)

        self.verticalLayout_21.addWidget(self.gis_color_image_transect)

        self.gis_color_image_block = QRadioButton(self.frame_28)
        self.buttonGroup_gis_color_images.addButton(self.gis_color_image_block)
        self.gis_color_image_block.setObjectName(u"gis_color_image_block")
        self.gis_color_image_block.setFont(font19)
        self.gis_color_image_block.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.gis_color_image_block.setText(u"Block")
        self.gis_color_image_block.setChecked(False)
        self.gis_color_image_block.setAutoExclusive(False)

        self.verticalLayout_21.addWidget(self.gis_color_image_block)

        self.gis_color_image_inspected = QRadioButton(self.frame_28)
        self.buttonGroup_gis_color_images.addButton(self.gis_color_image_inspected)
        self.gis_color_image_inspected.setObjectName(u"gis_color_image_inspected")
        self.gis_color_image_inspected.setFont(font19)
        self.gis_color_image_inspected.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.gis_color_image_inspected.setText(u"Inspected")
        self.gis_color_image_inspected.setChecked(False)
        self.gis_color_image_inspected.setAutoExclusive(False)

        self.verticalLayout_21.addWidget(self.gis_color_image_inspected)

        self.frame_20 = QFrame(self.frame_gis_properties)
        self.frame_20.setObjectName(u"frame_20")
        self.frame_20.setGeometry(QRect(10, 340, 151, 221))
        self.frame_20.setStyleSheet(u"background-color: rgb(0, 66, 100);border-radius:10px;")
        self.frame_20.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_20.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_20 = QVBoxLayout(self.frame_20)
        self.verticalLayout_20.setSpacing(4)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.verticalLayout_20.setContentsMargins(10, 0, 0, 0)
        self.label_15 = QLabel(self.frame_20)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMaximumSize(QSize(16777215, 20))
        self.label_15.setFont(font14)
        self.label_15.setText(u"Colour Sightings")

        self.verticalLayout_20.addWidget(self.label_15)

        self.gis_color_objects_resight_set = QRadioButton(self.frame_20)
        self.buttonGroup_gis_color_objects = QButtonGroup(MainWindow)
        self.buttonGroup_gis_color_objects.setObjectName(u"buttonGroup_gis_color_objects")
        self.buttonGroup_gis_color_objects.addButton(self.gis_color_objects_resight_set)
        self.gis_color_objects_resight_set.setObjectName(u"gis_color_objects_resight_set")
        self.gis_color_objects_resight_set.setFont(font19)
        self.gis_color_objects_resight_set.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.gis_color_objects_resight_set.setText(u"Resight Set")
        self.gis_color_objects_resight_set.setChecked(False)
        self.gis_color_objects_resight_set.setAutoExclusive(False)

        self.verticalLayout_20.addWidget(self.gis_color_objects_resight_set)

        self.gis_color_objects_group_area = QRadioButton(self.frame_20)
        self.buttonGroup_gis_color_objects.addButton(self.gis_color_objects_group_area)
        self.gis_color_objects_group_area.setObjectName(u"gis_color_objects_group_area")
        self.gis_color_objects_group_area.setFont(font19)
        self.gis_color_objects_group_area.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.gis_color_objects_group_area.setText(u"Spatial Cluster")
        self.gis_color_objects_group_area.setChecked(False)
        self.gis_color_objects_group_area.setAutoExclusive(False)

        self.verticalLayout_20.addWidget(self.gis_color_objects_group_area)

        self.gis_color_objects_reviewed = QRadioButton(self.frame_20)
        self.buttonGroup_gis_color_objects.addButton(self.gis_color_objects_reviewed)
        self.gis_color_objects_reviewed.setObjectName(u"gis_color_objects_reviewed")
        self.gis_color_objects_reviewed.setFont(font19)
        self.gis_color_objects_reviewed.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.gis_color_objects_reviewed.setText(u"Reviewed")
        self.gis_color_objects_reviewed.setChecked(False)
        self.gis_color_objects_reviewed.setAutoExclusive(False)

        self.verticalLayout_20.addWidget(self.gis_color_objects_reviewed)

        self.gis_color_objects_type = QRadioButton(self.frame_20)
        self.buttonGroup_gis_color_objects.addButton(self.gis_color_objects_type)
        self.gis_color_objects_type.setObjectName(u"gis_color_objects_type")
        self.gis_color_objects_type.setFont(font19)
        self.gis_color_objects_type.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.gis_color_objects_type.setText(u"Object Type")
        self.gis_color_objects_type.setChecked(False)
        self.gis_color_objects_type.setAutoExclusive(False)

        self.verticalLayout_20.addWidget(self.gis_color_objects_type)

        self.gis_color_objects_source = QRadioButton(self.frame_20)
        self.buttonGroup_gis_color_objects.addButton(self.gis_color_objects_source)
        self.gis_color_objects_source.setObjectName(u"gis_color_objects_source")
        self.gis_color_objects_source.setFont(font19)
        self.gis_color_objects_source.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.gis_color_objects_source.setText(u"Source\n"
"(man,AI,ext)")
        self.gis_color_objects_source.setChecked(False)
        self.gis_color_objects_source.setAutoExclusive(False)

        self.verticalLayout_20.addWidget(self.gis_color_objects_source)

        self.gis_color_objects_image = QRadioButton(self.frame_20)
        self.buttonGroup_gis_color_objects.addButton(self.gis_color_objects_image)
        self.gis_color_objects_image.setObjectName(u"gis_color_objects_image")
        self.gis_color_objects_image.setFont(font19)
        self.gis_color_objects_image.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.gis_color_objects_image.setText(u"Image")
        self.gis_color_objects_image.setChecked(True)
        self.gis_color_objects_image.setAutoExclusive(False)

        self.verticalLayout_20.addWidget(self.gis_color_objects_image)

        self.verticalLayout_20.setStretch(1, 1)
        self.verticalLayout_20.setStretch(3, 1)
        self.verticalLayout_20.setStretch(4, 1)
        self.verticalLayout_20.setStretch(5, 1)
        self.verticalLayout_20.setStretch(6, 1)
        self.groupBox_2 = QGroupBox(self.frame_gis_properties)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(10, 20, 151, 85))
        self.groupBox_2.setMinimumSize(QSize(151, 85))
        self.groupBox_2.setMaximumSize(QSize(151, 131))
        self.groupBox_2.setFont(font1)
        self.gridLayout_2 = QGridLayout(self.groupBox_2)
        self.gridLayout_2.setSpacing(2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(2, 0, 2, 2)
        self.btn_selection_rectangle = QPushButton(self.groupBox_2)
        self.btn_selection_rectangle.setObjectName(u"btn_selection_rectangle")
        sizePolicy1.setHeightForWidth(self.btn_selection_rectangle.sizePolicy().hasHeightForWidth())
        self.btn_selection_rectangle.setSizePolicy(sizePolicy1)
        self.btn_selection_rectangle.setMinimumSize(QSize(45, 45))
        self.btn_selection_rectangle.setMaximumSize(QSize(40, 40))
        self.btn_selection_rectangle.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.btn_selection_rectangle.setStyleSheet(u"QPushButton {\n"
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
        self.btn_selection_rectangle.setText(u"")
        icon4 = QIcon()
        icon4.addFile(u":/icons/icons/rectangle.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_selection_rectangle.setIcon(icon4)
        self.btn_selection_rectangle.setIconSize(QSize(45, 45))

        self.gridLayout_2.addWidget(self.btn_selection_rectangle, 0, 0, 1, 1)

        self.btn_selection_lasso = QPushButton(self.groupBox_2)
        self.btn_selection_lasso.setObjectName(u"btn_selection_lasso")
        sizePolicy1.setHeightForWidth(self.btn_selection_lasso.sizePolicy().hasHeightForWidth())
        self.btn_selection_lasso.setSizePolicy(sizePolicy1)
        self.btn_selection_lasso.setMinimumSize(QSize(45, 45))
        self.btn_selection_lasso.setMaximumSize(QSize(40, 40))
        self.btn_selection_lasso.setStyleSheet(u"QPushButton {\n"
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
        self.btn_selection_lasso.setText(u"")
        icon5 = QIcon()
        icon5.addFile(u":/icons/icons/lasso.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_selection_lasso.setIcon(icon5)
        self.btn_selection_lasso.setIconSize(QSize(45, 45))

        self.gridLayout_2.addWidget(self.btn_selection_lasso, 0, 1, 1, 1)


        self.horizontalLayout_13.addWidget(self.frame_gis_properties)

        self.btn_gis_toggle_props = QPushButton(self.page_gis)
        self.btn_gis_toggle_props.setObjectName(u"btn_gis_toggle_props")
        sizePolicy8.setHeightForWidth(self.btn_gis_toggle_props.sizePolicy().hasHeightForWidth())
        self.btn_gis_toggle_props.setSizePolicy(sizePolicy8)
        font20 = QFont()
        font20.setFamilies([u"MS Gothic"])
        font20.setPointSize(9)
        font20.setBold(True)
        self.btn_gis_toggle_props.setFont(font20)
        self.btn_gis_toggle_props.setStyleSheet(u"QPushButton {\n"
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

        self.horizontalLayout_13.addWidget(self.btn_gis_toggle_props)

        self.page_stack.addWidget(self.page_gis)
        self.page_digitizer = QWidget()
        self.page_digitizer.setObjectName(u"page_digitizer")
        self.horizontalLayout_8 = QHBoxLayout(self.page_digitizer)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.btn_picking_toggle_list = QPushButton(self.page_digitizer)
        self.btn_picking_toggle_list.setObjectName(u"btn_picking_toggle_list")
        sizePolicy8.setHeightForWidth(self.btn_picking_toggle_list.sizePolicy().hasHeightForWidth())
        self.btn_picking_toggle_list.setSizePolicy(sizePolicy8)
        self.btn_picking_toggle_list.setMinimumSize(QSize(0, 0))
        self.btn_picking_toggle_list.setFont(font20)
        self.btn_picking_toggle_list.setStyleSheet(u"QPushButton {\n"
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

        self.horizontalLayout_8.addWidget(self.btn_picking_toggle_list)

        self.picking_splitter = QSplitter(self.page_digitizer)
        self.picking_splitter.setObjectName(u"picking_splitter")
        sizePolicy4.setHeightForWidth(self.picking_splitter.sizePolicy().hasHeightForWidth())
        self.picking_splitter.setSizePolicy(sizePolicy4)
        self.picking_splitter.setBaseSize(QSize(0, 0))
        self.picking_splitter.setOrientation(Qt.Orientation.Horizontal)
        self.picking_splitter.setOpaqueResize(True)
        self.picking_splitter.setChildrenCollapsible(False)
        self.frame_picking_image_list = QFrame(self.picking_splitter)
        self.frame_picking_image_list.setObjectName(u"frame_picking_image_list")
        self.frame_picking_image_list.setEnabled(True)
        sizePolicy2.setHeightForWidth(self.frame_picking_image_list.sizePolicy().hasHeightForWidth())
        self.frame_picking_image_list.setSizePolicy(sizePolicy2)
        self.frame_picking_image_list.setMinimumSize(QSize(250, 0))
        self.frame_picking_image_list.setMaximumSize(QSize(16777215, 16777215))
        self.frame_picking_image_list.setStyleSheet(u"background-color:rgb(40, 44, 52);")
        self.frame_picking_image_list.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_picking_image_list.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.frame_picking_image_list)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.digitizer_image_panel = ImageTreeView(self.frame_picking_image_list)
        self.digitizer_image_panel.setObjectName(u"digitizer_image_panel")
        sizePolicy9.setHeightForWidth(self.digitizer_image_panel.sizePolicy().hasHeightForWidth())
        self.digitizer_image_panel.setSizePolicy(sizePolicy9)
        self.digitizer_image_panel.setMinimumSize(QSize(0, 0))
        self.digitizer_image_panel.setStyleSheet(u"QHeaderView::section { background-color:rgb(98, 103, 111) }\n"
"\n"
"QTreeView{alternate-background-color: #222222; background: transparent;}\n"
"\n"
"QTreeView::branch:has-children:!has-siblings:closed,\n"
"QTreeView::branch:closed:has-children:has-siblings {\n"
"        border-image: none;\n"
"        image: url(:/icons/icons/ico-size-grip.png);\n"
"}\n"
"\n"
"QTreeView::branch:open:has-children:!has-siblings,\n"
"QTreeView::branch:open:has-children:has-siblings  {\n"
"        border-image: none;\n"
"        image:url(:/icons/icons/circle.svg);\n"
"}\n"
"\n"
"QToolTip {\n"
"	color: white;\n"
"	background-color: black;\n"
"	border: 1px solid rgb(40, 40, 40);\n"
"	border-radius: 2px;\n"
"};")
        self.digitizer_image_panel.setFrameShape(QFrame.Shape.StyledPanel)
        self.digitizer_image_panel.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.digitizer_image_panel.setProperty(u"showDropIndicator", False)
        self.digitizer_image_panel.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.digitizer_image_panel.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.digitizer_image_panel.header().setStretchLastSection(False)

        self.verticalLayout_9.addWidget(self.digitizer_image_panel)

        self.picking_splitter.addWidget(self.frame_picking_image_list)
        self.frame_15 = QFrame(self.picking_splitter)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_15.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_15)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.custom_env_layout = QFrame(self.frame_15)
        self.custom_env_layout.setObjectName(u"custom_env_layout")
        sizePolicy2.setHeightForWidth(self.custom_env_layout.sizePolicy().hasHeightForWidth())
        self.custom_env_layout.setSizePolicy(sizePolicy2)
        self.custom_env_layout.setMinimumSize(QSize(500, 120))
        self.custom_env_layout.setMaximumSize(QSize(500, 120))
        self.custom_env_layout.setStyleSheet(u"#custom_env_layout{\n"
"border: 1px solid rgb(170, 170, 255);\n"
"border-radius:15px;}\n"
"")
        self.custom_env_layout.setFrameShape(QFrame.Shape.StyledPanel)
        self.custom_env_layout.setFrameShadow(QFrame.Shadow.Raised)
        self.environment_image = EnvironmentLayout(self.custom_env_layout)
        self.environment_image.setObjectName(u"environment_image")
        self.environment_image.setGeometry(QRect(10, 10, 401, 101))
        self.environment_image.setMaximumSize(QSize(16777215, 120))
        self.environment_image.setStyleSheet(u"")
        self.label_3 = QLabel(self.custom_env_layout)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(430, 50, 55, 32))
        self.label_3.setText(u"Propagate\n"
"always")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.btn_propagate_always = QRadioButton(self.custom_env_layout)
        self.btn_propagate_always.setObjectName(u"btn_propagate_always")
        self.btn_propagate_always.setGeometry(QRect(446, 25, 27, 21))
        self.btn_propagate_always.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.horizontalLayout_10.addWidget(self.custom_env_layout)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_2)


        self.verticalLayout_6.addLayout(self.horizontalLayout_10)

        self.qgraphic_digitizer = ImageView(self.frame_15)
        self.qgraphic_digitizer.setObjectName(u"qgraphic_digitizer")
        sizePolicy6.setHeightForWidth(self.qgraphic_digitizer.sizePolicy().hasHeightForWidth())
        self.qgraphic_digitizer.setSizePolicy(sizePolicy6)
        self.qgraphic_digitizer.setMinimumSize(QSize(400, 0))
        self.qgraphic_digitizer.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.qgraphic_digitizer.setFrameShape(QFrame.Shape.NoFrame)
        self.qgraphic_digitizer.setFrameShadow(QFrame.Shadow.Plain)
        self.qgraphic_digitizer.setLineWidth(0)
        self.qgraphic_digitizer.setDragMode(QGraphicsView.DragMode.NoDrag)

        self.verticalLayout_6.addWidget(self.qgraphic_digitizer)

        self.picking_splitter.addWidget(self.frame_15)

        self.horizontalLayout_8.addWidget(self.picking_splitter)

        self.frame_picking_properties = QFrame(self.page_digitizer)
        self.frame_picking_properties.setObjectName(u"frame_picking_properties")
        sizePolicy7.setHeightForWidth(self.frame_picking_properties.sizePolicy().hasHeightForWidth())
        self.frame_picking_properties.setSizePolicy(sizePolicy7)
        self.frame_picking_properties.setMinimumSize(QSize(170, 0))
        self.frame_picking_properties.setStyleSheet(u"background-color: rgb(40, 44, 52);")
        self.frame_picking_properties.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_picking_properties.setFrameShadow(QFrame.Shadow.Raised)
        self.groupBox = QGroupBox(self.frame_picking_properties)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 10, 151, 131))
        self.groupBox.setMinimumSize(QSize(151, 131))
        self.groupBox.setMaximumSize(QSize(151, 131))
        self.groupBox.setFont(font1)
        self.groupBox.setTitle(u"Geometries")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(2, 0, 2, 2)
        self.btn_create_point = QPushButton(self.groupBox)
        self.buttonGroup_digitizing_geometric_operation = QButtonGroup(MainWindow)
        self.buttonGroup_digitizing_geometric_operation.setObjectName(u"buttonGroup_digitizing_geometric_operation")
        self.buttonGroup_digitizing_geometric_operation.addButton(self.btn_create_point)
        self.btn_create_point.setObjectName(u"btn_create_point")
        sizePolicy1.setHeightForWidth(self.btn_create_point.sizePolicy().hasHeightForWidth())
        self.btn_create_point.setSizePolicy(sizePolicy1)
        self.btn_create_point.setMinimumSize(QSize(45, 45))
        self.btn_create_point.setMaximumSize(QSize(40, 40))
        self.btn_create_point.setStyleSheet(u"QPushButton {\n"
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
        self.btn_create_point.setText(u"")
        icon6 = QIcon()
        icon6.addFile(u":/icons/icons/point.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_create_point.setIcon(icon6)
        self.btn_create_point.setIconSize(QSize(45, 45))

        self.gridLayout.addWidget(self.btn_create_point, 0, 0, 1, 1)

        self.btn_create_line = QPushButton(self.groupBox)
        self.buttonGroup_digitizing_geometric_operation.addButton(self.btn_create_line)
        self.btn_create_line.setObjectName(u"btn_create_line")
        sizePolicy1.setHeightForWidth(self.btn_create_line.sizePolicy().hasHeightForWidth())
        self.btn_create_line.setSizePolicy(sizePolicy1)
        self.btn_create_line.setMinimumSize(QSize(45, 45))
        self.btn_create_line.setMaximumSize(QSize(40, 40))
        self.btn_create_line.setStyleSheet(u"QPushButton {\n"
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
        self.btn_create_line.setText(u"")
        icon7 = QIcon()
        icon7.addFile(u":/icons/icons/linestring.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_create_line.setIcon(icon7)
        self.btn_create_line.setIconSize(QSize(45, 45))

        self.gridLayout.addWidget(self.btn_create_line, 0, 1, 1, 1)

        self.btn_create_rectangle = QPushButton(self.groupBox)
        self.buttonGroup_digitizing_geometric_operation.addButton(self.btn_create_rectangle)
        self.btn_create_rectangle.setObjectName(u"btn_create_rectangle")
        sizePolicy1.setHeightForWidth(self.btn_create_rectangle.sizePolicy().hasHeightForWidth())
        self.btn_create_rectangle.setSizePolicy(sizePolicy1)
        self.btn_create_rectangle.setMinimumSize(QSize(45, 45))
        self.btn_create_rectangle.setMaximumSize(QSize(40, 40))
        self.btn_create_rectangle.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.btn_create_rectangle.setStyleSheet(u"QPushButton {\n"
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
        self.btn_create_rectangle.setText(u"")
        self.btn_create_rectangle.setIcon(icon4)
        self.btn_create_rectangle.setIconSize(QSize(45, 45))

        self.gridLayout.addWidget(self.btn_create_rectangle, 1, 0, 1, 1)

        self.btn_create_polygon = QPushButton(self.groupBox)
        self.buttonGroup_digitizing_geometric_operation.addButton(self.btn_create_polygon)
        self.btn_create_polygon.setObjectName(u"btn_create_polygon")
        sizePolicy1.setHeightForWidth(self.btn_create_polygon.sizePolicy().hasHeightForWidth())
        self.btn_create_polygon.setSizePolicy(sizePolicy1)
        self.btn_create_polygon.setMinimumSize(QSize(45, 45))
        self.btn_create_polygon.setMaximumSize(QSize(40, 40))
        self.btn_create_polygon.setStyleSheet(u"QPushButton {\n"
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
        self.btn_create_polygon.setText(u"")
        icon8 = QIcon()
        icon8.addFile(u":/icons/icons/polygon.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_create_polygon.setIcon(icon8)
        self.btn_create_polygon.setIconSize(QSize(45, 45))

        self.gridLayout.addWidget(self.btn_create_polygon, 1, 1, 1, 1)

        self.frame_42 = QFrame(self.frame_picking_properties)
        self.frame_42.setObjectName(u"frame_42")
        self.frame_42.setGeometry(QRect(10, 250, 151, 211))
        self.frame_42.setStyleSheet(u"background-color: rgb(0, 66, 100);border-radius:10px;")
        self.frame_42.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_42.setFrameShadow(QFrame.Shadow.Raised)
        self.digitizing_color_reprojection = QRadioButton(self.frame_42)
        self.buttonGroup_digitizing_color_object = QButtonGroup(MainWindow)
        self.buttonGroup_digitizing_color_object.setObjectName(u"buttonGroup_digitizing_color_object")
        self.buttonGroup_digitizing_color_object.addButton(self.digitizing_color_reprojection)
        self.digitizing_color_reprojection.setObjectName(u"digitizing_color_reprojection")
        self.digitizing_color_reprojection.setGeometry(QRect(10, 40, 135, 21))
        self.digitizing_color_reprojection.setFont(font19)
        self.digitizing_color_reprojection.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.digitizing_color_reprojection.setText(u"Projections")
        self.digitizing_color_reprojection.setChecked(True)
        self.digitizing_color_reprojection.setAutoExclusive(False)
        self.digitizing_color_object_type = QRadioButton(self.frame_42)
        self.buttonGroup_digitizing_color_object.addButton(self.digitizing_color_object_type)
        self.digitizing_color_object_type.setObjectName(u"digitizing_color_object_type")
        self.digitizing_color_object_type.setGeometry(QRect(10, 131, 135, 21))
        self.digitizing_color_object_type.setFont(font19)
        self.digitizing_color_object_type.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.digitizing_color_object_type.setText(u"Object Type")
        self.digitizing_color_object_type.setChecked(False)
        self.digitizing_color_object_type.setAutoExclusive(False)
        self.digitizing_color_resight_set = QRadioButton(self.frame_42)
        self.buttonGroup_digitizing_color_object.addButton(self.digitizing_color_resight_set)
        self.digitizing_color_resight_set.setObjectName(u"digitizing_color_resight_set")
        self.digitizing_color_resight_set.setGeometry(QRect(10, 102, 135, 21))
        self.digitizing_color_resight_set.setFont(font19)
        self.digitizing_color_resight_set.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.digitizing_color_resight_set.setText(u"Resight Set")
        self.digitizing_color_resight_set.setChecked(False)
        self.digitizing_color_resight_set.setAutoExclusive(True)
        self.digitizing_color_source = QRadioButton(self.frame_42)
        self.buttonGroup_digitizing_color_object.addButton(self.digitizing_color_source)
        self.digitizing_color_source.setObjectName(u"digitizing_color_source")
        self.digitizing_color_source.setGeometry(QRect(10, 160, 135, 40))
        self.digitizing_color_source.setFont(font19)
        self.digitizing_color_source.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.digitizing_color_source.setText(u"Source\n"
"(man, AI, ext)")
        self.digitizing_color_source.setChecked(False)
        self.digitizing_color_source.setAutoExclusive(False)
        self.digitizing_color_image = QRadioButton(self.frame_42)
        self.buttonGroup_digitizing_color_object.addButton(self.digitizing_color_image)
        self.digitizing_color_image.setObjectName(u"digitizing_color_image")
        self.digitizing_color_image.setGeometry(QRect(10, 73, 135, 21))
        self.digitizing_color_image.setFont(font19)
        self.digitizing_color_image.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.digitizing_color_image.setText(u"Image")
        self.digitizing_color_image.setChecked(False)
        self.digitizing_color_image.setAutoExclusive(False)
        self.label_16 = QLabel(self.frame_42)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setGeometry(QRect(10, 6, 121, 20))
        self.label_16.setFont(font14)
        self.label_16.setText(u"Colour Objects")
        self.frame_43 = QFrame(self.frame_picking_properties)
        self.frame_43.setObjectName(u"frame_43")
        self.frame_43.setGeometry(QRect(10, 150, 151, 91))
        self.frame_43.setStyleSheet(u"background-color: rgb(127, 84, 0);border-radius:10px;")
        self.frame_43.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_43.setFrameShadow(QFrame.Shadow.Raised)
        self.picking_hide = QRadioButton(self.frame_43)
        self.picking_hide.setObjectName(u"picking_hide")
        self.picking_hide.setGeometry(QRect(10, 30, 135, 21))
        self.picking_hide.setFont(font19)
        self.picking_hide.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.picking_hide.setText(u"Current Image")
        self.picking_hide.setAutoExclusive(False)
        self.picking_hide_projections = QRadioButton(self.frame_43)
        self.picking_hide_projections.setObjectName(u"picking_hide_projections")
        self.picking_hide_projections.setGeometry(QRect(10, 60, 135, 21))
        self.picking_hide_projections.setFont(font19)
        self.picking_hide_projections.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.picking_hide_projections.setText(u"Projections")
        self.picking_hide_projections.setAutoExclusive(False)
        self.label_24 = QLabel(self.frame_43)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setGeometry(QRect(10, 6, 121, 20))
        self.label_24.setFont(font14)
        self.stack_navigation = QStackedWidget(self.frame_picking_properties)
        self.stack_navigation.setObjectName(u"stack_navigation")
        self.stack_navigation.setGeometry(QRect(10, 470, 151, 341))
        self.stack_navigation.setStyleSheet(u"background-color: rgb(92, 99, 112);")
        self.stack_navigation.setFrameShape(QFrame.Shape.NoFrame)
        self.stack_navigation.setFrameShadow(QFrame.Shadow.Plain)
        self.nav_page_grid = QWidget()
        self.nav_page_grid.setObjectName(u"nav_page_grid")
        self.nav_page_grid.setStyleSheet(u"")
        self.btn_navigation_chg_to_free = QPushButton(self.nav_page_grid)
        self.btn_navigation_chg_to_free.setObjectName(u"btn_navigation_chg_to_free")
        self.btn_navigation_chg_to_free.setGeometry(QRect(6, 5, 141, 31))
        self.btn_navigation_chg_to_free.setMinimumSize(QSize(0, 0))
        self.btn_navigation_chg_to_free.setMaximumSize(QSize(16777215, 16777215))
        self.btn_navigation_chg_to_free.setFont(font14)
        self.btn_navigation_chg_to_free.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_navigation_chg_to_free.setStyleSheet(u"QPushButton {\n"
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
        self.btn_navigation_chg_to_free.setText(u"Free Navigation")
        self.btn_navigation_chg_to_free.setIconSize(QSize(45, 45))
        self.frame_6 = QFrame(self.nav_page_grid)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setGeometry(QRect(85, 40, 61, 61))
        self.frame_6.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.label_7 = QLabel(self.frame_6)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(17, 24, 30, 16))
        font21 = QFont()
        font21.setPointSize(6)
        font21.setBold(True)
        self.label_7.setFont(font21)
        self.label_7.setStyleSheet(u"background: transparent;\n"
"color:rgb(52, 59, 72);")
        self.label_7.setText(u"Zoom")
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dial_image_scale = QDial(self.frame_6)
        self.dial_image_scale.setObjectName(u"dial_image_scale")
        self.dial_image_scale.setGeometry(QRect(0, 0, 61, 61))
        self.dial_image_scale.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.dial_image_scale.setAutoFillBackground(False)
        self.dial_image_scale.setStyleSheet(u"QDial {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"   \n"
"}\n"
"QDial:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"QDial:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}")
        self.dial_image_scale.setMinimum(1)
        self.dial_image_scale.setMaximum(10)
        self.dial_image_scale.setValue(3)
        self.dial_image_scale.setTracking(False)
        self.dial_image_scale.setOrientation(Qt.Orientation.Horizontal)
        self.dial_image_scale.setInvertedAppearance(False)
        self.dial_image_scale.setInvertedControls(False)
        self.dial_image_scale.setWrapping(False)
        self.dial_image_scale.setNotchTarget(3.700000000000000)
        self.dial_image_scale.setNotchesVisible(False)
        self.dial_image_scale.raise_()
        self.label_7.raise_()
        self.label_walk_modus = QLabel(self.nav_page_grid)
        self.label_walk_modus.setObjectName(u"label_walk_modus")
        self.label_walk_modus.setGeometry(QRect(20, 220, 121, 20))
        font22 = QFont()
        font22.setPointSize(9)
        font22.setBold(True)
        self.label_walk_modus.setFont(font22)
        self.label_walk_modus.setStyleSheet(u"color: rgb(106, 0, 0)")
        self.label_walk_modus.setText(u"WALK MODUS ON")
        self.label_walk_modus.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.btn_navigation_r = QPushButton(self.nav_page_grid)
        self.btn_navigation_r.setObjectName(u"btn_navigation_r")
        self.btn_navigation_r.setGeometry(QRect(90, 130, 31, 28))
        font23 = QFont()
        font23.setBold(True)
        self.btn_navigation_r.setFont(font23)
        self.btn_navigation_r.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_navigation_r.setStyleSheet(u"QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(72, 79, 92);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}")
        self.btn_navigation_r.setText(u"\u25ba")
        self.btn_navigation_d = QPushButton(self.nav_page_grid)
        self.btn_navigation_d.setObjectName(u"btn_navigation_d")
        self.btn_navigation_d.setGeometry(QRect(60, 130, 31, 28))
        self.btn_navigation_d.setFont(font23)
        self.btn_navigation_d.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_navigation_d.setStyleSheet(u"QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(72, 79, 92);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}")
        self.btn_navigation_d.setText(u"\u25bc")
        self.btn_walkmodus_alway_on = QRadioButton(self.nav_page_grid)
        self.btn_walkmodus_alway_on.setObjectName(u"btn_walkmodus_alway_on")
        self.btn_walkmodus_alway_on.setGeometry(QRect(20, 160, 121, 21))
        self.btn_walkmodus_alway_on.setFont(font2)
        self.btn_walkmodus_alway_on.setText(u"Always Start")
        self.btn_walkmodus_alway_on.setAutoExclusive(False)
        self.btn_navigation_l = QPushButton(self.nav_page_grid)
        self.btn_navigation_l.setObjectName(u"btn_navigation_l")
        self.btn_navigation_l.setGeometry(QRect(30, 130, 31, 28))
        self.btn_navigation_l.setFont(font23)
        self.btn_navigation_l.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_navigation_l.setStyleSheet(u"QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(72, 79, 92);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}")
        self.btn_navigation_l.setText(u"\u25c4")
        self.rect_nav_overview = QFrame(self.nav_page_grid)
        self.rect_nav_overview.setObjectName(u"rect_nav_overview")
        self.rect_nav_overview.setGeometry(QRect(30, 240, 100, 90))
        self.rect_nav_overview.setAutoFillBackground(False)
        self.rect_nav_overview.setStyleSheet(u"QFrame {\n"
"	border: 0px solid rgb(52, 59, 72);\n"
"	background-color: rgb(72, 100, 92);\n"
"}")
        self.rect_nav_overview.setFrameShape(QFrame.Shape.StyledPanel)
        self.rect_nav_overview.setFrameShadow(QFrame.Shadow.Raised)
        self.rect_nav_grid = QFrame(self.rect_nav_overview)
        self.rect_nav_grid.setObjectName(u"rect_nav_grid")
        self.rect_nav_grid.setGeometry(QRect(0, 0, 21, 21))
        self.rect_nav_grid.setStyleSheet(u"QFrame {\n"
"	background-color: rgb(150, 0, 0);\n"
"	border: 0px solid rgb(52, 59, 72);\n"
"}")
        self.rect_nav_grid.setFrameShape(QFrame.Shape.NoFrame)
        self.rect_nav_grid.setFrameShadow(QFrame.Shadow.Sunken)
        self.rect_nav_grid.setLineWidth(0)
        self.btn_navigation_topleft = QPushButton(self.nav_page_grid)
        self.btn_navigation_topleft.setObjectName(u"btn_navigation_topleft")
        self.btn_navigation_topleft.setGeometry(QRect(20, 50, 41, 41))
        self.btn_navigation_topleft.setFont(font22)
        self.btn_navigation_topleft.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_navigation_topleft.setStyleSheet(u"QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(72, 79, 92);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}")
        self.btn_navigation_topleft.setText(u"TOP\n"
"LEFT")
        self.btn_navigation_u = QPushButton(self.nav_page_grid)
        self.btn_navigation_u.setObjectName(u"btn_navigation_u")
        self.btn_navigation_u.setGeometry(QRect(60, 100, 31, 28))
        self.btn_navigation_u.setFont(font23)
        self.btn_navigation_u.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_navigation_u.setStyleSheet(u"QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(72, 79, 92);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}")
        self.btn_navigation_u.setText(u"\u25b2")
        self.btn_navigation_startwalk = QPushButton(self.nav_page_grid)
        self.btn_navigation_startwalk.setObjectName(u"btn_navigation_startwalk")
        self.btn_navigation_startwalk.setGeometry(QRect(30, 190, 101, 31))
        self.btn_navigation_startwalk.setFont(font22)
        self.btn_navigation_startwalk.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_navigation_startwalk.setStyleSheet(u"QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(72, 100, 92);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(72, 120, 92);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}")
        self.btn_navigation_startwalk.setText(u"START WALK")
        self.stack_navigation.addWidget(self.nav_page_grid)
        self.nav_page_free = QWidget()
        self.nav_page_free.setObjectName(u"nav_page_free")
        self.nav_page_free.setStyleSheet(u"")
        self.btn_navigation_chg_to_grid = QPushButton(self.nav_page_free)
        self.btn_navigation_chg_to_grid.setObjectName(u"btn_navigation_chg_to_grid")
        self.btn_navigation_chg_to_grid.setGeometry(QRect(6, 5, 141, 31))
        self.btn_navigation_chg_to_grid.setMinimumSize(QSize(0, 0))
        self.btn_navigation_chg_to_grid.setMaximumSize(QSize(16777215, 16777215))
        self.btn_navigation_chg_to_grid.setFont(font14)
        self.btn_navigation_chg_to_grid.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_navigation_chg_to_grid.setStyleSheet(u"QPushButton {\n"
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
        self.btn_navigation_chg_to_grid.setText(u"Grid Navigation")
        self.btn_navigation_chg_to_grid.setIconSize(QSize(45, 45))
        self.btn_fit_view = QPushButton(self.nav_page_free)
        self.btn_fit_view.setObjectName(u"btn_fit_view")
        self.btn_fit_view.setGeometry(QRect(50, 50, 47, 47))
        self.btn_fit_view.setMinimumSize(QSize(0, 0))
        self.btn_fit_view.setMaximumSize(QSize(16777215, 16777215))
        self.btn_fit_view.setFont(font2)
        self.btn_fit_view.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_fit_view.setStyleSheet(u"QPushButton {\n"
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
        self.btn_fit_view.setText(u"")
        icon9 = QIcon()
        icon9.addFile(u":/icons/icons/fit_view.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_fit_view.setIcon(icon9)
        self.btn_fit_view.setIconSize(QSize(45, 45))
        self.stack_navigation.addWidget(self.nav_page_free)
        self.stack_navigation.raise_()
        self.frame_42.raise_()
        self.groupBox.raise_()
        self.frame_43.raise_()

        self.horizontalLayout_8.addWidget(self.frame_picking_properties)

        self.btn_picking_toggle_props = QPushButton(self.page_digitizer)
        self.btn_picking_toggle_props.setObjectName(u"btn_picking_toggle_props")
        sizePolicy8.setHeightForWidth(self.btn_picking_toggle_props.sizePolicy().hasHeightForWidth())
        self.btn_picking_toggle_props.setSizePolicy(sizePolicy8)
        self.btn_picking_toggle_props.setFont(font20)
        self.btn_picking_toggle_props.setStyleSheet(u"QPushButton {\n"
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

        self.horizontalLayout_8.addWidget(self.btn_picking_toggle_props)

        self.page_stack.addWidget(self.page_digitizer)
        self.page_gallery = QWidget()
        self.page_gallery.setObjectName(u"page_gallery")
        self.horizontalLayout_12 = QHBoxLayout(self.page_gallery)
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.gallery_listview = GalleryView(self.page_gallery)
        self.gallery_listview.setObjectName(u"gallery_listview")
        self.gallery_listview.setFrameShape(QFrame.Shape.NoFrame)
        self.gallery_listview.setFrameShadow(QFrame.Shadow.Sunken)
        self.gallery_listview.setDragEnabled(False)
        self.gallery_listview.setDragDropMode(QAbstractItemView.DragDropMode.DropOnly)
        self.gallery_listview.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.gallery_listview.setMovement(QListView.Movement.Static)
        self.gallery_listview.setFlow(QListView.Flow.LeftToRight)
        self.gallery_listview.setUniformItemSizes(False)
        self.gallery_listview.setSelectionRectVisible(False)

        self.horizontalLayout_12.addWidget(self.gallery_listview)

        self.frame_gallery_properties = QFrame(self.page_gallery)
        self.frame_gallery_properties.setObjectName(u"frame_gallery_properties")
        sizePolicy7.setHeightForWidth(self.frame_gallery_properties.sizePolicy().hasHeightForWidth())
        self.frame_gallery_properties.setSizePolicy(sizePolicy7)
        self.frame_gallery_properties.setMinimumSize(QSize(170, 0))
        font24 = QFont()
        font24.setPointSize(7)
        self.frame_gallery_properties.setFont(font24)
        self.frame_gallery_properties.setStyleSheet(u"background-color: rgb(40, 44, 52);")
        self.frame_gallery_properties.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_gallery_properties.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_18 = QFrame(self.frame_gallery_properties)
        self.frame_18.setObjectName(u"frame_18")
        self.frame_18.setGeometry(QRect(10, 10, 151, 41))
        self.frame_18.setStyleSheet(u"background-color: rgb(92, 99, 112);border-radius:10px;")
        self.frame_18.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_18.setFrameShadow(QFrame.Shadow.Raised)
        self.gallery_fast_activate = QRadioButton(self.frame_18)
        self.gallery_fast_activate.setObjectName(u"gallery_fast_activate")
        self.gallery_fast_activate.setGeometry(QRect(10, 0, 141, 41))
        self.gallery_fast_activate.setFont(font16)
        self.gallery_fast_activate.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.gallery_fast_activate.setStyleSheet(u"")
        self.gallery_fast_activate.setText(u"Fast Activate\n"
"Deactivate")
        self.gallery_fast_activate.setAutoExclusive(False)
        self.frame_33 = QFrame(self.frame_gallery_properties)
        self.frame_33.setObjectName(u"frame_33")
        self.frame_33.setGeometry(QRect(10, 550, 151, 151))
        self.frame_33.setStyleSheet(u"background-color: rgb(92, 99, 112);border-radius:10px;")
        self.frame_33.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_33.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_13 = QVBoxLayout(self.frame_33)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(10, -1, -1, -1)
        self.label_34 = QLabel(self.frame_33)
        self.label_34.setObjectName(u"label_34")
        font25 = QFont()
        font25.setPointSize(15)
        font25.setBold(True)
        self.label_34.setFont(font25)
        self.label_34.setText(u"Order")

        self.verticalLayout_13.addWidget(self.label_34)

        self.gallery_btn_order_id = QRadioButton(self.frame_33)
        self.buttonGroup_gallery_order = QButtonGroup(MainWindow)
        self.buttonGroup_gallery_order.setObjectName(u"buttonGroup_gallery_order")
        self.buttonGroup_gallery_order.addButton(self.gallery_btn_order_id)
        self.gallery_btn_order_id.setObjectName(u"gallery_btn_order_id")
        self.gallery_btn_order_id.setEnabled(True)
        self.gallery_btn_order_id.setFont(font19)
        self.gallery_btn_order_id.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.gallery_btn_order_id.setText(u"ID")
        self.gallery_btn_order_id.setCheckable(True)
        self.gallery_btn_order_id.setChecked(False)
        self.gallery_btn_order_id.setAutoExclusive(False)

        self.verticalLayout_13.addWidget(self.gallery_btn_order_id)

        self.gallery_btn_order_object_type = QRadioButton(self.frame_33)
        self.buttonGroup_gallery_order.addButton(self.gallery_btn_order_object_type)
        self.gallery_btn_order_object_type.setObjectName(u"gallery_btn_order_object_type")
        self.gallery_btn_order_object_type.setEnabled(True)
        self.gallery_btn_order_object_type.setFont(font19)
        self.gallery_btn_order_object_type.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.gallery_btn_order_object_type.setText(u"Object Type")
        self.gallery_btn_order_object_type.setCheckable(True)
        self.gallery_btn_order_object_type.setChecked(False)
        self.gallery_btn_order_object_type.setAutoExclusive(False)

        self.verticalLayout_13.addWidget(self.gallery_btn_order_object_type)

        self.gallery_btn_order_area = QRadioButton(self.frame_33)
        self.buttonGroup_gallery_order.addButton(self.gallery_btn_order_area)
        self.gallery_btn_order_area.setObjectName(u"gallery_btn_order_area")
        self.gallery_btn_order_area.setEnabled(True)
        self.gallery_btn_order_area.setFont(font19)
        self.gallery_btn_order_area.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.gallery_btn_order_area.setText(u"Spatial Cluster")
        self.gallery_btn_order_area.setCheckable(True)
        self.gallery_btn_order_area.setChecked(False)
        self.gallery_btn_order_area.setAutoExclusive(False)

        self.verticalLayout_13.addWidget(self.gallery_btn_order_area)

        self.gallery_btn_order_resight = QRadioButton(self.frame_33)
        self.buttonGroup_gallery_order.addButton(self.gallery_btn_order_resight)
        self.gallery_btn_order_resight.setObjectName(u"gallery_btn_order_resight")
        self.gallery_btn_order_resight.setEnabled(True)
        self.gallery_btn_order_resight.setFont(font19)
        self.gallery_btn_order_resight.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.gallery_btn_order_resight.setText(u"Resight Set")
        self.gallery_btn_order_resight.setCheckable(True)
        self.gallery_btn_order_resight.setChecked(False)
        self.gallery_btn_order_resight.setAutoExclusive(False)

        self.verticalLayout_13.addWidget(self.gallery_btn_order_resight)

        self.frame_38 = QFrame(self.frame_gallery_properties)
        self.frame_38.setObjectName(u"frame_38")
        self.frame_38.setGeometry(QRect(10, 60, 151, 481))
        self.frame_38.setStyleSheet(u"QFrame{background-color: rgb(92, 99, 112);border-radius:10px;}")
        self.frame_38.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_38.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_19 = QFrame(self.frame_38)
        self.frame_19.setObjectName(u"frame_19")
        self.frame_19.setGeometry(QRect(10, 410, 131, 66))
        self.frame_19.setStyleSheet(u"background-color: rgb(127, 84, 0);border-radius:10px;")
        self.frame_19.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_19.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.frame_19)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(10, 0, 0, 0)
        self.gallery_filter_activated = QRadioButton(self.frame_19)
        self.gallery_filter_activated.setObjectName(u"gallery_filter_activated")
        font26 = QFont()
        font26.setFamilies([u"MS Shell Dlg 2"])
        font26.setPointSize(11)
        font26.setBold(True)
        self.gallery_filter_activated.setFont(font26)
        self.gallery_filter_activated.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.gallery_filter_activated.setText(u"Activated")
        self.gallery_filter_activated.setAutoExclusive(False)

        self.verticalLayout_12.addWidget(self.gallery_filter_activated)

        self.gallery_filter_deactivated = QRadioButton(self.frame_19)
        self.gallery_filter_deactivated.setObjectName(u"gallery_filter_deactivated")
        self.gallery_filter_deactivated.setFont(font26)
        self.gallery_filter_deactivated.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.gallery_filter_deactivated.setText(u"Deactivated")
        self.gallery_filter_deactivated.setAutoExclusive(False)

        self.verticalLayout_12.addWidget(self.gallery_filter_deactivated)

        self.btn_gallery_filter_reset = QPushButton(self.frame_38)
        self.btn_gallery_filter_reset.setObjectName(u"btn_gallery_filter_reset")
        self.btn_gallery_filter_reset.setGeometry(QRect(100, 5, 41, 21))
        self.btn_gallery_filter_reset.setFont(font16)
        self.btn_gallery_filter_reset.setStyleSheet(u"QPushButton {\n"
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
        self.btn_gallery_filter_reset.setText(u"Reset")
        self.label_5 = QLabel(self.frame_38)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(10, 0, 71, 32))
        font27 = QFont()
        font27.setFamilies([u"Segoe UI"])
        font27.setPointSize(15)
        font27.setBold(True)
        font27.setUnderline(False)
        self.label_5.setFont(font27)
        self.label_5.setText(u"FILTERS")
        self.gallery_filter_group_area = QLineEdit(self.frame_38)
        self.gallery_filter_group_area.setObjectName(u"gallery_filter_group_area")
        self.gallery_filter_group_area.setGeometry(QRect(10, 120, 131, 20))
        self.gallery_filter_group_area.setFont(font15)
        self.gallery_filter_group_area.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.frame_10 = QFrame(self.frame_38)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setGeometry(QRect(10, 290, 131, 41))
        self.frame_10.setStyleSheet(u"background-color:rgb(103, 40, 23);border-radius:10px;")
        self.frame_10.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_23 = QVBoxLayout(self.frame_10)
        self.verticalLayout_23.setSpacing(0)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.verticalLayout_23.setContentsMargins(10, 0, 0, 0)
        self.gallery_filter_reviewed = QRadioButton(self.frame_10)
        self.gallery_filter_reviewed.setObjectName(u"gallery_filter_reviewed")
        self.gallery_filter_reviewed.setEnabled(True)
        self.gallery_filter_reviewed.setFont(font26)
        self.gallery_filter_reviewed.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.gallery_filter_reviewed.setText(u"Not\n"
"Reviewed")
        self.gallery_filter_reviewed.setChecked(False)
        self.gallery_filter_reviewed.setAutoExclusive(False)

        self.verticalLayout_23.addWidget(self.gallery_filter_reviewed)

        self.frame_17 = QFrame(self.frame_38)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setGeometry(QRect(10, 338, 131, 66))
        self.frame_17.setStyleSheet(u"background-color: rgb(0, 66, 100);border-radius:10px;")
        self.frame_17.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_17.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.frame_17)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(10, 0, 0, 0)
        self.gallery_filter_perspective_image = QRadioButton(self.frame_17)
        self.gallery_filter_perspective_image.setObjectName(u"gallery_filter_perspective_image")
        self.gallery_filter_perspective_image.setFont(font26)
        self.gallery_filter_perspective_image.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.gallery_filter_perspective_image.setText(u"Perspective")
        self.gallery_filter_perspective_image.setAutoExclusive(False)

        self.verticalLayout_8.addWidget(self.gallery_filter_perspective_image)

        self.gallery_filter_ortho_image = QRadioButton(self.frame_17)
        self.gallery_filter_ortho_image.setObjectName(u"gallery_filter_ortho_image")
        self.gallery_filter_ortho_image.setFont(font26)
        self.gallery_filter_ortho_image.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.gallery_filter_ortho_image.setText(u"Ortho")
        self.gallery_filter_ortho_image.setAutoExclusive(False)

        self.verticalLayout_8.addWidget(self.gallery_filter_ortho_image)

        self.gallery_filter_object = QLineEdit(self.frame_38)
        self.gallery_filter_object.setObjectName(u"gallery_filter_object")
        self.gallery_filter_object.setGeometry(QRect(10, 80, 131, 20))
        self.gallery_filter_object.setFont(font15)
        self.gallery_filter_object.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.label_13 = QLabel(self.frame_38)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(10, 140, 111, 20))
        self.label_13.setFont(font14)
        self.label_13.setText(u"Resight Set")
        self.gallery_filter_resight_set = QLineEdit(self.frame_38)
        self.gallery_filter_resight_set.setObjectName(u"gallery_filter_resight_set")
        self.gallery_filter_resight_set.setGeometry(QRect(10, 160, 131, 20))
        self.gallery_filter_resight_set.setFont(font15)
        self.gallery_filter_resight_set.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.frame_16 = QFrame(self.frame_38)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setGeometry(QRect(10, 190, 131, 93))
        self.frame_16.setStyleSheet(u"background-color: rgb(0, 100, 70);border-radius:10px;")
        self.frame_16.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_16.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.frame_16)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(10, 0, 0, 0)
        self.gallery_filter_manual = QRadioButton(self.frame_16)
        self.gallery_filter_manual.setObjectName(u"gallery_filter_manual")
        self.gallery_filter_manual.setEnabled(True)
        self.gallery_filter_manual.setFont(font26)
        self.gallery_filter_manual.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.gallery_filter_manual.setText(u"Manual")
        self.gallery_filter_manual.setCheckable(True)
        self.gallery_filter_manual.setChecked(False)
        self.gallery_filter_manual.setAutoExclusive(False)

        self.verticalLayout_7.addWidget(self.gallery_filter_manual)

        self.gallery_filter_ai = QRadioButton(self.frame_16)
        self.gallery_filter_ai.setObjectName(u"gallery_filter_ai")
        self.gallery_filter_ai.setFont(font26)
        self.gallery_filter_ai.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.gallery_filter_ai.setText(u"AI")
        self.gallery_filter_ai.setChecked(False)
        self.gallery_filter_ai.setAutoExclusive(False)

        self.verticalLayout_7.addWidget(self.gallery_filter_ai)

        self.gallery_filter_external = QRadioButton(self.frame_16)
        self.gallery_filter_external.setObjectName(u"gallery_filter_external")
        self.gallery_filter_external.setEnabled(True)
        self.gallery_filter_external.setFont(font26)
        self.gallery_filter_external.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.gallery_filter_external.setText(u"External")
        self.gallery_filter_external.setChecked(False)
        self.gallery_filter_external.setAutoExclusive(False)

        self.verticalLayout_7.addWidget(self.gallery_filter_external)

        self.gallery_filter_starred = QRadioButton(self.frame_38)
        self.gallery_filter_starred.setObjectName(u"gallery_filter_starred")
        self.gallery_filter_starred.setGeometry(QRect(20, 30, 111, 31))
        self.gallery_filter_starred.setFont(font19)
        self.gallery_filter_starred.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.gallery_filter_starred.setStyleSheet(u"background-color: rgb(92, 99, 112);")
        self.gallery_filter_starred.setText(u"Images")
        icon10 = QIcon()
        icon10.addFile(u":/icons/icons/starred.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.gallery_filter_starred.setIcon(icon10)
        self.gallery_filter_starred.setChecked(False)
        self.gallery_filter_starred.setAutoExclusive(False)
        self.label_11 = QLabel(self.frame_38)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(10, 60, 91, 20))
        self.label_11.setFont(font14)
        self.label_11.setText(u"Object Type")
        self.label_12 = QLabel(self.frame_38)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(10, 100, 111, 20))
        self.label_12.setFont(font14)
        self.label_12.setText(u"Spatial Cluster")
        self.frame_39 = QFrame(self.frame_gallery_properties)
        self.frame_39.setObjectName(u"frame_39")
        self.frame_39.setGeometry(QRect(10, 710, 151, 61))
        self.frame_39.setStyleSheet(u"background-color: rgb(92, 99, 112);border-radius:10px;")
        self.frame_39.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_39.setFrameShadow(QFrame.Shadow.Raised)
        self.gallery_slider_thumb_size = QSlider(self.frame_39)
        self.gallery_slider_thumb_size.setObjectName(u"gallery_slider_thumb_size")
        self.gallery_slider_thumb_size.setGeometry(QRect(6, 20, 140, 41))
        self.gallery_slider_thumb_size.setMinimum(150)
        self.gallery_slider_thumb_size.setMaximum(600)
        self.gallery_slider_thumb_size.setSingleStep(25)
        self.gallery_slider_thumb_size.setPageStep(100)
        self.gallery_slider_thumb_size.setValue(250)
        self.gallery_slider_thumb_size.setOrientation(Qt.Orientation.Horizontal)
        self.gallery_slider_thumb_size.setTickPosition(QSlider.TickPosition.NoTicks)
        self.gallery_slider_thumb_size.setTickInterval(50)
        self.label_28 = QLabel(self.frame_39)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setGeometry(QRect(10, 6, 111, 20))
        self.label_28.setFont(font27)
        self.label_28.setText(u"Size")
        self.frame_38.raise_()
        self.frame_33.raise_()
        self.frame_18.raise_()
        self.frame_39.raise_()

        self.horizontalLayout_12.addWidget(self.frame_gallery_properties)

        self.btn_gallery_toggle_props = QPushButton(self.page_gallery)
        self.btn_gallery_toggle_props.setObjectName(u"btn_gallery_toggle_props")
        sizePolicy8.setHeightForWidth(self.btn_gallery_toggle_props.sizePolicy().hasHeightForWidth())
        self.btn_gallery_toggle_props.setSizePolicy(sizePolicy8)
        self.btn_gallery_toggle_props.setFont(font20)
        self.btn_gallery_toggle_props.setStyleSheet(u"QPushButton {\n"
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

        self.horizontalLayout_12.addWidget(self.btn_gallery_toggle_props)

        self.page_stack.addWidget(self.page_gallery)
        self.page_export = QWidget()
        self.page_export.setObjectName(u"page_export")
        self.btn_exp_obj_kml = QPushButton(self.page_export)
        self.btn_exp_obj_kml.setObjectName(u"btn_exp_obj_kml")
        self.btn_exp_obj_kml.setEnabled(True)
        self.btn_exp_obj_kml.setGeometry(QRect(30, 380, 200, 81))
        self.btn_exp_obj_kml.setFont(font16)
#if QT_CONFIG(tooltip)
        self.btn_exp_obj_kml.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.btn_exp_obj_kml.setStyleSheet(u"QPushButton {\n"
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
        self.btn_exp_obj_kml.setText(u"Export Sightings\n"
"KML")
        self.btn_exp_footprint_kml = QPushButton(self.page_export)
        self.btn_exp_footprint_kml.setObjectName(u"btn_exp_footprint_kml")
        self.btn_exp_footprint_kml.setEnabled(True)
        self.btn_exp_footprint_kml.setGeometry(QRect(30, 640, 200, 81))
        self.btn_exp_footprint_kml.setFont(font16)
        self.btn_exp_footprint_kml.setStyleSheet(u"QPushButton {\n"
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
        self.btn_exp_footprint_kml.setText(u"EXPORT Footrpints\n"
"KML\n"
"(test mode)")
        self.btn_exp_obj_csv = QPushButton(self.page_export)
        self.btn_exp_obj_csv.setObjectName(u"btn_exp_obj_csv")
        self.btn_exp_obj_csv.setEnabled(True)
        self.btn_exp_obj_csv.setGeometry(QRect(250, 380, 200, 81))
        self.btn_exp_obj_csv.setFont(font16)
        self.btn_exp_obj_csv.setStyleSheet(u"QPushButton {\n"
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
        self.btn_exp_obj_csv.setText(u"Export Objects\n"
"CSV FILE")
        self.btn_exp_footprint_csv = QPushButton(self.page_export)
        self.btn_exp_footprint_csv.setObjectName(u"btn_exp_footprint_csv")
        self.btn_exp_footprint_csv.setEnabled(True)
        self.btn_exp_footprint_csv.setGeometry(QRect(250, 640, 200, 81))
        self.btn_exp_footprint_csv.setFont(font16)
        self.btn_exp_footprint_csv.setStyleSheet(u"QPushButton {\n"
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
        self.btn_exp_footprint_csv.setText(u"Export Footprints\n"
"CSV FILE")
        self.label_35 = QLabel(self.page_export)
        self.label_35.setObjectName(u"label_35")
        self.label_35.setGeometry(QRect(20, 580, 211, 31))
        self.label_35.setFont(font10)
        self.label_35.setText(u"Image information")
        self.label_45 = QLabel(self.page_export)
        self.label_45.setObjectName(u"label_45")
        self.label_45.setGeometry(QRect(20, 300, 231, 41))
        self.label_45.setFont(font10)
        self.label_45.setText(u"Objects  information")
        self.label_46 = QLabel(self.page_export)
        self.label_46.setObjectName(u"label_46")
        self.label_46.setGeometry(QRect(60, 150, 431, 31))
        self.label_46.setFont(font10)
        self.label_46.setText(u"Export Objects Information for AI Training")
        self.epxort_project_information = QPushButton(self.page_export)
        self.epxort_project_information.setObjectName(u"epxort_project_information")
        self.epxort_project_information.setEnabled(True)
        self.epxort_project_information.setGeometry(QRect(70, 30, 200, 81))
        self.epxort_project_information.setFont(font16)
        self.epxort_project_information.setStyleSheet(u"QPushButton {\n"
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
        self.epxort_project_information.setText(u"EXPORT Project Information\n"
"TEXT FILE")
        self.rd_export_first_certain = QRadioButton(self.page_export)
        self.rd_export_first_certain.setObjectName(u"rd_export_first_certain")
        self.rd_export_first_certain.setEnabled(True)
        self.rd_export_first_certain.setGeometry(QRect(260, 300, 151, 51))
        font28 = QFont()
        font28.setFamilies([u"MS Shell Dlg 2"])
        font28.setPointSize(10)
        font28.setBold(True)
        self.rd_export_first_certain.setFont(font28)
        self.rd_export_first_certain.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.rd_export_first_certain.setStyleSheet(u"QRadioButton:checked{  padding-left: 5px; background-color: rgb(3,172,70); border-radius: 10px;}\n"
"\n"
"QRadioButton:unchecked{ padding-left: 5px; background-color: rgb(72, 79, 92); border-radius: 10px;}")
        self.rd_export_first_certain.setText(u"First Certain only")
        self.rd_export_first_certain.setIconSize(QSize(20, 20))
        self.rd_export_first_certain.setCheckable(True)
        self.rd_export_first_certain.setChecked(False)
        self.rd_export_first_certain.setAutoExclusive(False)
        self.db_check_export_ai_full_images = QRadioButton(self.page_export)
        self.db_check_export_ai_full_images.setObjectName(u"db_check_export_ai_full_images")
        self.db_check_export_ai_full_images.setGeometry(QRect(70, 190, 171, 31))
        self.db_check_export_ai_full_images.setFont(font2)
        self.db_check_export_ai_full_images.setStyleSheet(u"QRadioButton:checked{  padding-left: 5px; background-color: rgb(3,172,70); border-radius: 10px;}\n"
"\n"
"QRadioButton:unchecked{ padding-left: 5px; background-color: rgb(72, 79, 92); border-radius: 10px;}")
        self.db_check_export_ai_full_images.setText(u"Include Full Images")
        self.db_check_export_ai_full_images.setAutoExclusive(False)
        self.db_check_export_ai_detections = QRadioButton(self.page_export)
        self.db_check_export_ai_detections.setObjectName(u"db_check_export_ai_detections")
        self.db_check_export_ai_detections.setGeometry(QRect(70, 230, 171, 31))
        self.db_check_export_ai_detections.setFont(font2)
        self.db_check_export_ai_detections.setStyleSheet(u"QRadioButton:checked{  padding-left: 5px; background-color: rgb(3,172,70); border-radius: 10px;}\n"
"\n"
"QRadioButton:unchecked{ padding-left: 5px; background-color: rgb(72, 79, 92); border-radius: 10px;}")
        self.db_check_export_ai_detections.setText(u"Exclude AI Detections")
        self.db_check_export_ai_detections.setAutoExclusive(False)
        self.db_export_trainingsdata = QPushButton(self.page_export)
        self.db_export_trainingsdata.setObjectName(u"db_export_trainingsdata")
        self.db_export_trainingsdata.setGeometry(QRect(270, 190, 191, 71))
        sizePolicy6.setHeightForWidth(self.db_export_trainingsdata.sizePolicy().hasHeightForWidth())
        self.db_export_trainingsdata.setSizePolicy(sizePolicy6)
        self.db_export_trainingsdata.setFont(font16)
        self.db_export_trainingsdata.setStyleSheet(u"QPushButton {\n"
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
        self.db_export_trainingsdata.setText(u"Export Training Data")
        self.frame_geojson = QFrame(self.page_export)
        self.frame_geojson.setObjectName(u"frame_geojson")
        self.frame_geojson.setGeometry(QRect(470, 360, 251, 441))
        sizePolicy2.setHeightForWidth(self.frame_geojson.sizePolicy().hasHeightForWidth())
        self.frame_geojson.setSizePolicy(sizePolicy2)
        self.frame_geojson.setMinimumSize(QSize(0, 0))
        self.frame_geojson.setMaximumSize(QSize(16777215, 16777215))
        self.frame_geojson.setStyleSheet(u"#frame_geojson{\n"
"border: 1px solid #35c69b;\n"
"border-radius:15px;}\n"
"")
        self.frame_geojson.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_geojson.setFrameShadow(QFrame.Shadow.Raised)
        self.btn_exp_footprint_json = QPushButton(self.frame_geojson)
        self.btn_exp_footprint_json.setObjectName(u"btn_exp_footprint_json")
        self.btn_exp_footprint_json.setEnabled(True)
        self.btn_exp_footprint_json.setGeometry(QRect(25, 280, 200, 81))
        self.btn_exp_footprint_json.setFont(font16)
        self.btn_exp_footprint_json.setStyleSheet(u"QPushButton {\n"
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
        self.btn_exp_footprint_json.setText(u"Export Footprints\n"
"GEO JSON")
        self.btn_exp_obj_point_json = QPushButton(self.frame_geojson)
        self.btn_exp_obj_point_json.setObjectName(u"btn_exp_obj_point_json")
        self.btn_exp_obj_point_json.setEnabled(True)
        self.btn_exp_obj_point_json.setGeometry(QRect(25, 110, 200, 81))
        self.btn_exp_obj_point_json.setFont(font16)
        self.btn_exp_obj_point_json.setStyleSheet(u"QPushButton {\n"
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
        self.btn_exp_obj_point_json.setText(u"Export Objects - Center Points\n"
"GEO JSON")
        self.btn_exp_obj_json = QPushButton(self.frame_geojson)
        self.btn_exp_obj_json.setObjectName(u"btn_exp_obj_json")
        self.btn_exp_obj_json.setEnabled(True)
        self.btn_exp_obj_json.setGeometry(QRect(25, 20, 200, 81))
        self.btn_exp_obj_json.setFont(font16)
        self.btn_exp_obj_json.setStyleSheet(u"QPushButton {\n"
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
        self.btn_exp_obj_json.setText(u"Export Objects\n"
"GEO JSON")
        self.label_27 = QLabel(self.frame_geojson)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setGeometry(QRect(30, 390, 201, 31))
        self.label_27.setStyleSheet(u"color: rgb(85, 170, 127)")
        self.label_27.setText(u"Recommended using GEO JSON\n"
"to load into GIS packages")
        self.frame_shape = QFrame(self.page_export)
        self.frame_shape.setObjectName(u"frame_shape")
        self.frame_shape.setGeometry(QRect(740, 360, 251, 441))
        sizePolicy2.setHeightForWidth(self.frame_shape.sizePolicy().hasHeightForWidth())
        self.frame_shape.setSizePolicy(sizePolicy2)
        self.frame_shape.setMinimumSize(QSize(0, 0))
        self.frame_shape.setMaximumSize(QSize(16777215, 16777215))
        self.frame_shape.setStyleSheet(u"#frame_shape{\n"
"border: 1px solid rgb(170, 92, 85);\n"
"border-radius:15px;}\n"
"")
        self.frame_shape.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_shape.setFrameShadow(QFrame.Shadow.Raised)
        self.label_61 = QLabel(self.frame_shape)
        self.label_61.setObjectName(u"label_61")
        self.label_61.setGeometry(QRect(20, 370, 221, 61))
        self.label_61.setStyleSheet(u"color: rgb(170, 92, 85)")
        self.btn_exp_footprint_shp = QPushButton(self.frame_shape)
        self.btn_exp_footprint_shp.setObjectName(u"btn_exp_footprint_shp")
        self.btn_exp_footprint_shp.setGeometry(QRect(25, 280, 200, 81))
        self.btn_exp_footprint_shp.setFont(font16)
        self.btn_exp_footprint_shp.setStyleSheet(u"QPushButton {\n"
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
        self.btn_exp_footprint_shp.setText(u"Export Footprints\n"
"ESRI SHAPE")
        self.btn_exp_obj_shp = QPushButton(self.frame_shape)
        self.btn_exp_obj_shp.setObjectName(u"btn_exp_obj_shp")
        self.btn_exp_obj_shp.setEnabled(True)
        self.btn_exp_obj_shp.setGeometry(QRect(25, 20, 200, 81))
        self.btn_exp_obj_shp.setFont(font16)
        self.btn_exp_obj_shp.setAutoFillBackground(False)
        self.btn_exp_obj_shp.setStyleSheet(u"QPushButton {\n"
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
        self.btn_exp_obj_shp.setText(u"Export Objects\n"
"ESRI SHAPE")
        self.btn_exp_obj_poin_shp = QPushButton(self.frame_shape)
        self.btn_exp_obj_poin_shp.setObjectName(u"btn_exp_obj_poin_shp")
        self.btn_exp_obj_poin_shp.setEnabled(True)
        self.btn_exp_obj_poin_shp.setGeometry(QRect(25, 110, 200, 81))
        self.btn_exp_obj_poin_shp.setFont(font16)
        self.btn_exp_obj_poin_shp.setStyleSheet(u"QPushButton {\n"
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
        self.btn_exp_obj_poin_shp.setText(u"Export Objects - Center Points\n"
"ESRI SHAPE")
        self.btn_exp_obj_point_kml = QPushButton(self.page_export)
        self.btn_exp_obj_point_kml.setObjectName(u"btn_exp_obj_point_kml")
        self.btn_exp_obj_point_kml.setEnabled(True)
        self.btn_exp_obj_point_kml.setGeometry(QRect(30, 470, 200, 81))
        self.btn_exp_obj_point_kml.setFont(font16)
#if QT_CONFIG(tooltip)
        self.btn_exp_obj_point_kml.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.btn_exp_obj_point_kml.setStyleSheet(u"QPushButton {\n"
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
        self.btn_exp_obj_point_kml.setText(u"Export Objects - Center Points\n"
"KML")
        self.page_stack.addWidget(self.page_export)
        self.page_ai = QWidget()
        self.page_ai.setObjectName(u"page_ai")
        self.horizontalLayout_21 = QHBoxLayout(self.page_ai)
        self.horizontalLayout_21.setSpacing(0)
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.horizontalLayout_21.setContentsMargins(0, 0, 0, 0)
        self.frame_24 = QFrame(self.page_ai)
        self.frame_24.setObjectName(u"frame_24")
        sizePolicy7.setHeightForWidth(self.frame_24.sizePolicy().hasHeightForWidth())
        self.frame_24.setSizePolicy(sizePolicy7)
        self.frame_24.setMinimumSize(QSize(300, 0))
        self.frame_24.setMaximumSize(QSize(350, 16777215))
        self.frame_24.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_24.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_16 = QVBoxLayout(self.frame_24)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.label = QLabel(self.frame_24)
        self.label.setObjectName(u"label")
        self.label.setFont(font14)
        self.label.setText(u"Choose AI Workflow:")

        self.verticalLayout_16.addWidget(self.label)

        self.ai_cmb_input_type = QComboBox(self.frame_24)
        self.ai_cmb_input_type.setObjectName(u"ai_cmb_input_type")
        self.ai_cmb_input_type.setFont(font23)
        self.ai_cmb_input_type.setCurrentText(u"")

        self.verticalLayout_16.addWidget(self.ai_cmb_input_type)

        self.verticalSpacer_5 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_16.addItem(self.verticalSpacer_5)

        self.btn_load_ai_res_filesystem = QPushButton(self.frame_24)
        self.btn_load_ai_res_filesystem.setObjectName(u"btn_load_ai_res_filesystem")
        self.btn_load_ai_res_filesystem.setEnabled(True)
        self.btn_load_ai_res_filesystem.setMinimumSize(QSize(100, 40))
        self.btn_load_ai_res_filesystem.setFont(font16)
        self.btn_load_ai_res_filesystem.setStyleSheet(u"QPushButton {\n"
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

        self.verticalLayout_16.addWidget(self.btn_load_ai_res_filesystem)

        self.verticalSpacer_4 = QSpacerItem(20, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_16.addItem(self.verticalSpacer_4)

        self.ai_frame_start = QFrame(self.frame_24)
        self.ai_frame_start.setObjectName(u"ai_frame_start")
        self.ai_frame_start.setFrameShape(QFrame.Shape.StyledPanel)
        self.ai_frame_start.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_15 = QVBoxLayout(self.ai_frame_start)
        self.verticalLayout_15.setSpacing(13)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.rd_ai_all_follders = QRadioButton(self.ai_frame_start)
        self.rd_ai_all_follders.setObjectName(u"rd_ai_all_follders")
        self.rd_ai_all_follders.setFont(font2)
        self.rd_ai_all_follders.setText(u"Run all folders")
        self.rd_ai_all_follders.setAutoExclusive(False)

        self.verticalLayout_15.addWidget(self.rd_ai_all_follders)

        self.ai_folder_chooser = QComboBox(self.ai_frame_start)
        self.ai_folder_chooser.setObjectName(u"ai_folder_chooser")
        self.ai_folder_chooser.setCurrentText(u"")

        self.verticalLayout_15.addWidget(self.ai_folder_chooser)

        self.ai_radio_different_image_folder = QRadioButton(self.ai_frame_start)
        self.ai_radio_different_image_folder.setObjectName(u"ai_radio_different_image_folder")
        self.ai_radio_different_image_folder.setEnabled(False)
        self.ai_radio_different_image_folder.setFont(font2)
        self.ai_radio_different_image_folder.setText(u"Use different image folder for raw\n"
" images (e.g. JPG for NEF).")
        self.ai_radio_different_image_folder.setAutoExclusive(False)

        self.verticalLayout_15.addWidget(self.ai_radio_different_image_folder)

        self.btn_start_ai = QPushButton(self.ai_frame_start)
        self.btn_start_ai.setObjectName(u"btn_start_ai")
        self.btn_start_ai.setEnabled(True)
        self.btn_start_ai.setMinimumSize(QSize(100, 40))
        self.btn_start_ai.setFont(font16)
        self.btn_start_ai.setStyleSheet(u"QPushButton {\n"
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
        self.btn_start_ai.setText(u"START AI")

        self.verticalLayout_15.addWidget(self.btn_start_ai)


        self.verticalLayout_16.addWidget(self.ai_frame_start)

        self.ai_waiting_spinner = QtWaitingSpinner(self.frame_24)
        self.ai_waiting_spinner.setObjectName(u"ai_waiting_spinner")
        self.ai_waiting_spinner.setMinimumSize(QSize(0, 100))
        self.ai_waiting_spinner.setBaseSize(QSize(0, 50))

        self.verticalLayout_16.addWidget(self.ai_waiting_spinner)

        self.verticalSpacer = QSpacerItem(20, 60, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_16.addItem(self.verticalSpacer)

        self.btn_import_ai = QPushButton(self.frame_24)
        self.btn_import_ai.setObjectName(u"btn_import_ai")
        self.btn_import_ai.setEnabled(True)
        self.btn_import_ai.setMinimumSize(QSize(100, 0))
        self.btn_import_ai.setFont(font16)
        self.btn_import_ai.setStyleSheet(u"QPushButton {\n"
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
        self.btn_import_ai.setText(u"IMPORT Activated Detections to Objects")

        self.verticalLayout_16.addWidget(self.btn_import_ai)

        self.progressBar_ai = QProgressBar(self.frame_24)
        self.progressBar_ai.setObjectName(u"progressBar_ai")
        sizePolicy4.setHeightForWidth(self.progressBar_ai.sizePolicy().hasHeightForWidth())
        self.progressBar_ai.setSizePolicy(sizePolicy4)
        self.progressBar_ai.setMinimumSize(QSize(0, 0))
        self.progressBar_ai.setStyleSheet(u"QProgressBar{\n"
"    border: 2px solid grey;\n"
"    border-radius: 5px;\n"
"    text-align: center;\n"
"	color: darkgreen;\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"   background-color: lightgreen;\n"
"    margin: 1px;\n"
"}")
        self.progressBar_ai.setValue(0)
        self.progressBar_ai.setTextVisible(True)

        self.verticalLayout_16.addWidget(self.progressBar_ai)


        self.horizontalLayout_21.addWidget(self.frame_24)

        self.ai_listview = AIView(self.page_ai)
        self.ai_listview.setObjectName(u"ai_listview")
        self.ai_listview.setFrameShape(QFrame.Shape.StyledPanel)
        self.ai_listview.setFrameShadow(QFrame.Shadow.Sunken)
        self.ai_listview.setDragEnabled(False)
        self.ai_listview.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.ai_listview.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.ai_listview.setUniformItemSizes(False)
        self.ai_listview.setSelectionRectVisible(False)

        self.horizontalLayout_21.addWidget(self.ai_listview)

        self.frame_ai_properties = QFrame(self.page_ai)
        self.frame_ai_properties.setObjectName(u"frame_ai_properties")
        self.frame_ai_properties.setMinimumSize(QSize(150, 0))
        self.frame_ai_properties.setStyleSheet(u"background-color: rgb(40, 44, 52);")
        self.frame_ai_properties.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_ai_properties.setFrameShadow(QFrame.Shadow.Raised)
        self.rd_toggle_labels = QRadioButton(self.frame_ai_properties)
        self.rd_toggle_labels.setObjectName(u"rd_toggle_labels")
        self.rd_toggle_labels.setGeometry(QRect(40, 30, 81, 51))
        self.rd_toggle_labels.setFont(font14)
        self.rd_toggle_labels.setText(u"Toggle\n"
"Labels")
        self.frame_ai_icon_size = QFrame(self.frame_ai_properties)
        self.frame_ai_icon_size.setObjectName(u"frame_ai_icon_size")
        self.frame_ai_icon_size.setGeometry(QRect(10, 600, 131, 61))
        self.frame_ai_icon_size.setStyleSheet(u"background-color: rgb(92, 99, 112);border-radius:10px;")
        self.frame_ai_icon_size.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_ai_icon_size.setFrameShadow(QFrame.Shadow.Raised)
        self.ai_slider_thumb_size = QSlider(self.frame_ai_icon_size)
        self.ai_slider_thumb_size.setObjectName(u"ai_slider_thumb_size")
        self.ai_slider_thumb_size.setGeometry(QRect(6, 20, 121, 41))
        self.ai_slider_thumb_size.setMinimum(150)
        self.ai_slider_thumb_size.setMaximum(600)
        self.ai_slider_thumb_size.setSingleStep(25)
        self.ai_slider_thumb_size.setPageStep(100)
        self.ai_slider_thumb_size.setValue(250)
        self.ai_slider_thumb_size.setOrientation(Qt.Orientation.Horizontal)
        self.ai_slider_thumb_size.setTickPosition(QSlider.TickPosition.NoTicks)
        self.ai_slider_thumb_size.setTickInterval(50)
        self.label_29 = QLabel(self.frame_ai_icon_size)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setGeometry(QRect(10, 6, 111, 20))
        self.label_29.setFont(font27)
        self.label_29.setText(u"Size")
        self.btn_ai_filter_reset = QPushButton(self.frame_ai_properties)
        self.btn_ai_filter_reset.setObjectName(u"btn_ai_filter_reset")
        self.btn_ai_filter_reset.setGeometry(QRect(90, 148, 51, 21))
        self.btn_ai_filter_reset.setFont(font15)
        self.btn_ai_filter_reset.setStyleSheet(u"QPushButton {\n"
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
        self.btn_ai_filter_reset.setText(u"Reset")
        self.frame_2 = QFrame(self.frame_ai_properties)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setGeometry(QRect(10, 290, 131, 111))
        self.frame_2.setStyleSheet(u"QFrame{background-color: rgb(92, 99, 112);border-radius:10px;}")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.label_19 = QLabel(self.frame_2)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setGeometry(QRect(10, 60, 121, 20))
        self.label_19.setFont(font1)
        self.label_19.setText(u"AI Run Number")
        self.label_21 = QLabel(self.frame_2)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setGeometry(QRect(10, 10, 101, 20))
        self.label_21.setFont(font1)
        self.label_21.setText(u"Object Type")
        self.ai_filter_object = QLineEdit(self.frame_2)
        self.ai_filter_object.setObjectName(u"ai_filter_object")
        self.ai_filter_object.setGeometry(QRect(10, 30, 111, 20))
        self.ai_filter_object.setFont(font15)
        self.ai_filter_object.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.ai_filter_object.setFrame(False)
        self.ai_filter_ai_run = QLineEdit(self.frame_2)
        self.ai_filter_ai_run.setObjectName(u"ai_filter_ai_run")
        self.ai_filter_ai_run.setGeometry(QRect(10, 80, 111, 20))
        self.ai_filter_ai_run.setFont(font15)
        self.ai_filter_ai_run.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.ai_filter_ai_run.setFrame(False)
        self.label_17 = QLabel(self.frame_ai_properties)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setGeometry(QRect(10, 140, 81, 32))
        self.label_17.setFont(font27)
        self.label_17.setText(u"FILTERS")
        self.frame_26 = QFrame(self.frame_ai_properties)
        self.frame_26.setObjectName(u"frame_26")
        self.frame_26.setGeometry(QRect(10, 200, 131, 81))
        self.frame_26.setStyleSheet(u"background-color:rgb(103, 40, 23);border-radius:10px;")
        self.frame_26.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_26.setFrameShadow(QFrame.Shadow.Raised)
        self.ai_filter_activated = QRadioButton(self.frame_26)
        self.ai_filter_activated.setObjectName(u"ai_filter_activated")
        self.ai_filter_activated.setGeometry(QRect(10, 10, 111, 31))
        font29 = QFont()
        font29.setFamilies([u"Segoe UI"])
        font29.setPointSize(12)
        font29.setBold(True)
        self.ai_filter_activated.setFont(font29)
        self.ai_filter_activated.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.ai_filter_activated.setText(u"Activated")
        self.ai_filter_activated.setAutoExclusive(False)
        self.ai_filter_deactivated = QRadioButton(self.frame_26)
        self.ai_filter_deactivated.setObjectName(u"ai_filter_deactivated")
        self.ai_filter_deactivated.setGeometry(QRect(10, 45, 111, 31))
        self.ai_filter_deactivated.setFont(font19)
        self.ai_filter_deactivated.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.ai_filter_deactivated.setText(u"Deactivated")
        self.ai_filter_deactivated.setAutoExclusive(False)
        self.frame_27 = QFrame(self.frame_ai_properties)
        self.frame_27.setObjectName(u"frame_27")
        self.frame_27.setGeometry(QRect(10, 410, 131, 181))
        self.frame_27.setStyleSheet(u"background-color: #184d50;border-radius:10px;")
        self.frame_27.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_27.setFrameShadow(QFrame.Shadow.Raised)
        self.ai_prob_slider_value = QLabel(self.frame_27)
        self.ai_prob_slider_value.setObjectName(u"ai_prob_slider_value")
        self.ai_prob_slider_value.setGeometry(QRect(10, 70, 51, 41))
        self.ai_prob_slider_value.setFont(font17)
        self.ai_prob_slider_value.setText(u"0%")
        self.label_22 = QLabel(self.frame_27)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setGeometry(QRect(10, 10, 91, 20))
        self.label_22.setFont(font1)
        self.label_22.setText(u"Probability")
        self.ai_filter_probability_slider = QScrollBar(self.frame_27)
        self.ai_filter_probability_slider.setObjectName(u"ai_filter_probability_slider")
        self.ai_filter_probability_slider.setGeometry(QRect(100, 10, 16, 160))
        self.ai_filter_probability_slider.setAutoFillBackground(False)
        self.ai_filter_probability_slider.setValue(0)
        self.ai_filter_probability_slider.setTracking(True)
        self.ai_filter_probability_slider.setOrientation(Qt.Orientation.Vertical)
        self.ai_filter_probability_slider.setInvertedAppearance(True)
        self.ai_filter_prob_lower = QRadioButton(self.frame_27)
        self.ai_filter_prob_lower.setObjectName(u"ai_filter_prob_lower")
        self.ai_filter_prob_lower.setGeometry(QRect(10, 140, 81, 31))
        self.ai_filter_prob_lower.setFont(font19)
        self.ai_filter_prob_lower.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.ai_filter_prob_lower.setText(u"Lower")
        self.ai_filter_prob_lower.setAutoExclusive(False)

        self.horizontalLayout_21.addWidget(self.frame_ai_properties)

        self.btn_ai_toggle_props = QPushButton(self.page_ai)
        self.btn_ai_toggle_props.setObjectName(u"btn_ai_toggle_props")
        sizePolicy8.setHeightForWidth(self.btn_ai_toggle_props.sizePolicy().hasHeightForWidth())
        self.btn_ai_toggle_props.setSizePolicy(sizePolicy8)
        self.btn_ai_toggle_props.setFont(font20)
        self.btn_ai_toggle_props.setStyleSheet(u"QPushButton {\n"
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

        self.horizontalLayout_21.addWidget(self.btn_ai_toggle_props)

        self.page_stack.addWidget(self.page_ai)
        self.page_compare = QWidget()
        self.page_compare.setObjectName(u"page_compare")
        self.horizontalLayout_11 = QHBoxLayout(self.page_compare)
        self.horizontalLayout_11.setSpacing(0)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.frame_31 = QFrame(self.page_compare)
        self.frame_31.setObjectName(u"frame_31")
        self.frame_31.setMinimumSize(QSize(250, 0))
        self.frame_31.setMaximumSize(QSize(200, 16777215))
        self.frame_31.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_31.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_19 = QVBoxLayout(self.frame_31)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.btn_cmp_load = QPushButton(self.frame_31)
        self.btn_cmp_load.setObjectName(u"btn_cmp_load")
        self.btn_cmp_load.setEnabled(True)
        self.btn_cmp_load.setMinimumSize(QSize(100, 40))
        self.btn_cmp_load.setFont(font16)
        self.btn_cmp_load.setStyleSheet(u"QPushButton {\n"
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
        self.btn_cmp_load.setText(u"Load Comparison")

        self.verticalLayout_19.addWidget(self.btn_cmp_load)

        self.verticalSpacer_9 = QSpacerItem(20, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_19.addItem(self.verticalSpacer_9)

        self.compare_modus_combobox = QComboBox(self.frame_31)
        self.compare_modus_combobox.addItem("")
        self.compare_modus_combobox.addItem("")
        self.compare_modus_combobox.addItem("")
        self.compare_modus_combobox.addItem("")
        self.compare_modus_combobox.setObjectName(u"compare_modus_combobox")
        self.compare_modus_combobox.setAutoFillBackground(False)
        self.compare_modus_combobox.setCurrentText(u"1) Single DB: SELF to AI")
        self.compare_modus_combobox.setFrame(False)

        self.verticalLayout_19.addWidget(self.compare_modus_combobox)

        self.compare_individual_check = QRadioButton(self.frame_31)
        self.compare_individual_check.setObjectName(u"compare_individual_check")
        self.compare_individual_check.setFont(font23)
        self.compare_individual_check.setText(u"Compare Individuals Only")

        self.verticalLayout_19.addWidget(self.compare_individual_check)

        self.btn_cmp_start = QPushButton(self.frame_31)
        self.btn_cmp_start.setObjectName(u"btn_cmp_start")
        self.btn_cmp_start.setEnabled(True)
        self.btn_cmp_start.setMinimumSize(QSize(100, 40))
        self.btn_cmp_start.setFont(font16)
        self.btn_cmp_start.setStyleSheet(u"QPushButton {\n"
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
        self.btn_cmp_start.setText(u"Compare")

        self.verticalLayout_19.addWidget(self.btn_cmp_start)

        self.compare_label_info = QLabel(self.frame_31)
        self.compare_label_info.setObjectName(u"compare_label_info")

        self.verticalLayout_19.addWidget(self.compare_label_info)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_19.addItem(self.verticalSpacer_2)

        self.btn_cmp_reject = QPushButton(self.frame_31)
        self.btn_cmp_reject.setObjectName(u"btn_cmp_reject")
        self.btn_cmp_reject.setMinimumSize(QSize(120, 40))
        self.btn_cmp_reject.setFont(font2)
        self.btn_cmp_reject.setStyleSheet(u"QPushButton {\n"
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
        self.btn_cmp_reject.setText(u"No FIT")

        self.verticalLayout_19.addWidget(self.btn_cmp_reject)

        self.btn_cmp_accept = QPushButton(self.frame_31)
        self.btn_cmp_accept.setObjectName(u"btn_cmp_accept")
        self.btn_cmp_accept.setMinimumSize(QSize(120, 40))
        self.btn_cmp_accept.setFont(font2)
        self.btn_cmp_accept.setStyleSheet(u"QPushButton {\n"
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
        self.btn_cmp_accept.setText(u"OK")

        self.verticalLayout_19.addWidget(self.btn_cmp_accept)

        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_19.addItem(self.verticalSpacer_8)

        self.btn_cmp_split = QPushButton(self.frame_31)
        self.btn_cmp_split.setObjectName(u"btn_cmp_split")
        self.btn_cmp_split.setMinimumSize(QSize(120, 40))
        self.btn_cmp_split.setFont(font2)
        self.btn_cmp_split.setStyleSheet(u"QPushButton {\n"
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
        self.btn_cmp_split.setText(u"Split")

        self.verticalLayout_19.addWidget(self.btn_cmp_split)

        self.btn_cmp_merge = QPushButton(self.frame_31)
        self.btn_cmp_merge.setObjectName(u"btn_cmp_merge")
        self.btn_cmp_merge.setMinimumSize(QSize(120, 40))
        self.btn_cmp_merge.setFont(font2)
        self.btn_cmp_merge.setStyleSheet(u"QPushButton {\n"
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
        self.btn_cmp_merge.setText(u"Merge")

        self.verticalLayout_19.addWidget(self.btn_cmp_merge)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_19.addItem(self.verticalSpacer_3)

        self.btn_cmp_save = QPushButton(self.frame_31)
        self.btn_cmp_save.setObjectName(u"btn_cmp_save")
        self.btn_cmp_save.setMinimumSize(QSize(120, 40))
        self.btn_cmp_save.setFont(font2)
        self.btn_cmp_save.setStyleSheet(u"QPushButton {\n"
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
        self.btn_cmp_save.setText(u"Save Comparison")

        self.verticalLayout_19.addWidget(self.btn_cmp_save)

        self.btn_cmp_export = QPushButton(self.frame_31)
        self.btn_cmp_export.setObjectName(u"btn_cmp_export")
        self.btn_cmp_export.setMinimumSize(QSize(120, 40))
        self.btn_cmp_export.setFont(font2)
        self.btn_cmp_export.setStyleSheet(u"QPushButton {\n"
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
        self.btn_cmp_export.setText(u"Export to CSV")

        self.verticalLayout_19.addWidget(self.btn_cmp_export)


        self.horizontalLayout_11.addWidget(self.frame_31)

        self.splitter_2 = QSplitter(self.page_compare)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Orientation.Horizontal)
        self.splitter_2.setOpaqueResize(True)
        self.splitter_2.setChildrenCollapsible(False)
        self.frame_34 = QFrame(self.splitter_2)
        self.frame_34.setObjectName(u"frame_34")
        self.frame_34.setMaximumSize(QSize(800, 16777215))
        self.frame_34.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_34.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_25 = QHBoxLayout(self.frame_34)
        self.horizontalLayout_25.setSpacing(0)
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.horizontalLayout_25.setContentsMargins(0, 0, 0, 0)
        self.compare_tableView = QTableView(self.frame_34)
        self.compare_tableView.setObjectName(u"compare_tableView")
        self.compare_tableView.setMaximumSize(QSize(16777215, 16777215))
        self.compare_tableView.setStyleSheet(u"QHeaderView::section { background-color:rgb(98, 103, 111) }")
        self.compare_tableView.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.compare_tableView.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.compare_tableView.setShowGrid(False)
        self.compare_tableView.verticalHeader().setVisible(False)

        self.horizontalLayout_25.addWidget(self.compare_tableView)

        self.splitter_2.addWidget(self.frame_34)
        self.frame_32 = QFrame(self.splitter_2)
        self.frame_32.setObjectName(u"frame_32")
        self.frame_32.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_32.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.frame_32)
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 0, 5, 0)
        self.compare_thumbs1 = CompareListView(self.frame_32)
        self.compare_thumbs1.setObjectName(u"compare_thumbs1")
        self.compare_thumbs1.setFrameShape(QFrame.Shape.NoFrame)
        self.compare_thumbs1.setFrameShadow(QFrame.Shadow.Sunken)
        self.compare_thumbs1.setDragEnabled(False)
        self.compare_thumbs1.setDragDropMode(QAbstractItemView.DragDropMode.DropOnly)
        self.compare_thumbs1.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.compare_thumbs1.setMovement(QListView.Movement.Static)
        self.compare_thumbs1.setFlow(QListView.Flow.LeftToRight)
        self.compare_thumbs1.setUniformItemSizes(False)
        self.compare_thumbs1.setSelectionRectVisible(False)

        self.verticalLayout_10.addWidget(self.compare_thumbs1)

        self.compare_slider_size = QSlider(self.frame_32)
        self.compare_slider_size.setObjectName(u"compare_slider_size")
        self.compare_slider_size.setMinimumSize(QSize(0, 20))
        self.compare_slider_size.setMinimum(150)
        self.compare_slider_size.setMaximum(600)
        self.compare_slider_size.setSingleStep(25)
        self.compare_slider_size.setPageStep(100)
        self.compare_slider_size.setValue(250)
        self.compare_slider_size.setOrientation(Qt.Orientation.Horizontal)
        self.compare_slider_size.setTickPosition(QSlider.TickPosition.NoTicks)
        self.compare_slider_size.setTickInterval(50)

        self.verticalLayout_10.addWidget(self.compare_slider_size)

        self.compare_thumbs2 = CompareListView(self.frame_32)
        self.compare_thumbs2.setObjectName(u"compare_thumbs2")
        self.compare_thumbs2.setFrameShape(QFrame.Shape.NoFrame)
        self.compare_thumbs2.setEditTriggers(QAbstractItemView.EditTrigger.EditKeyPressed)
        self.compare_thumbs2.setFlow(QListView.Flow.LeftToRight)
        self.compare_thumbs2.setSpacing(8)

        self.verticalLayout_10.addWidget(self.compare_thumbs2)

        self.splitter_2.addWidget(self.frame_32)

        self.horizontalLayout_11.addWidget(self.splitter_2)

        self.page_stack.addWidget(self.page_compare)
        self.page_help = QWidget()
        self.page_help.setObjectName(u"page_help")
        self.horizontalLayout_9 = QHBoxLayout(self.page_help)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.frame_3 = QFrame(self.page_help)
        self.frame_3.setObjectName(u"frame_3")
        sizePolicy4.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy4)
        self.frame_3.setMinimumSize(QSize(220, 0))
        self.frame_3.setMaximumSize(QSize(400, 16777215))
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_4 = QLabel(self.frame_3)
        self.label_4.setObjectName(u"label_4")
        sizePolicy2.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy2)
        font30 = QFont()
        font30.setFamilies([u"Segoe UI"])
        font30.setBold(False)
        self.label_4.setFont(font30)
        self.label_4.setText(u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700; color:#88c736;\">WISDAM</span></p><p align=\"justify\"><span style=\" font-size:11pt;\">WISDAM (</span><span style=\" font-size:11pt; color:#88c736;\">Wildlife Imagery Survey \u2013 Detection and Mapping</span><span style=\" font-size:11pt;\">) is a software package used for the digitisation of objects within images and to enrich objects with meta-data. </span></p><p align=\"justify\"><span style=\" font-size:11pt;\">The software uses the power of georeferenced images to map objects and to use the mapped location to perform actions, such as grouping or statistics. </span></p><p align=\"justify\"><span style=\" font-size:11pt;\">WISDAM handle images from different sources (such as piloted aircraft and drones) and allow you to import them with their georeference information. Alternatively you can import orthophotos.</span></p><p align=\"justify\"><span style=\" font-size:11pt;\">With this georeference information, image footprints and geometri"
                        "es of objects can be mapped to real world coordinates. For mapping in WISDAM either a raster model (e.g. DTM, DSM) or a simple plain (e.g. sea level) can be used.</span></p><p align=\"justify\"><span style=\" font-size:11pt;\">WISDAM also allows you to run an AI background process on images, to extract objects that my not have been detected through manual review process. WISDAM helps to visualise and enrich these objects with meta-data.</span></p><p align=\"justify\"><span style=\" font-size:11pt;\">WISDAM has been designed to optimise the workflow of environmental observation and is focused on the fast and easy handling of images and digitisation of objects. </span><br/></p></body></html>")
        self.label_4.setTextFormat(Qt.TextFormat.RichText)
        self.label_4.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label_4)

        self.btn_wisdam_homepage = QPushButton(self.frame_3)
        self.btn_wisdam_homepage.setObjectName(u"btn_wisdam_homepage")
        self.btn_wisdam_homepage.setMinimumSize(QSize(0, 70))
        self.btn_wisdam_homepage.setStyleSheet(u"QPushButton {\n"
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
        self.btn_wisdam_homepage.setText(u"")
        icon11 = QIcon()
        icon11.addFile(u":/icons/icons/WISDAM_Hero Logo_White.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_wisdam_homepage.setIcon(icon11)
        self.btn_wisdam_homepage.setIconSize(QSize(81, 48))
        self.btn_wisdam_homepage.setAutoDefault(False)
        self.btn_wisdam_homepage.setFlat(False)

        self.verticalLayout_2.addWidget(self.btn_wisdam_homepage)


        self.horizontalLayout_9.addWidget(self.frame_3)

        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setSpacing(5)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.btn_open_manual = QPushButton(self.page_help)
        self.btn_open_manual.setObjectName(u"btn_open_manual")
        self.btn_open_manual.setFont(font15)
        self.btn_open_manual.setStyleSheet(u"QPushButton {\n"
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
        self.btn_open_manual.setText(u"Open Manual")

        self.verticalLayout_11.addWidget(self.btn_open_manual)

        self.pdf_viewer = QPdfView(self.page_help)
        self.pdf_viewer.setObjectName(u"pdf_viewer")
        self.pdf_viewer.setEnabled(True)
        sizePolicy6.setHeightForWidth(self.pdf_viewer.sizePolicy().hasHeightForWidth())
        self.pdf_viewer.setSizePolicy(sizePolicy6)

        self.verticalLayout_11.addWidget(self.pdf_viewer)


        self.horizontalLayout_9.addLayout(self.verticalLayout_11)

        self.page_stack.addWidget(self.page_help)

        self.verticalLayout_4.addWidget(self.page_stack)


        self.horizontalLayout_2.addWidget(self.frame_content_right)


        self.verticalLayout.addWidget(self.frame_center)

        self.frame_low = QFrame(self.frame_main)
        self.frame_low.setObjectName(u"frame_low")
        sizePolicy4.setHeightForWidth(self.frame_low.sizePolicy().hasHeightForWidth())
        self.frame_low.setSizePolicy(sizePolicy4)
        self.frame_low.setMinimumSize(QSize(0, 40))
        self.frame_low.setMaximumSize(QSize(16777215, 40))
        self.frame_low.setStyleSheet(u"background-color: rgb(27, 29, 35);")
        self.frame_low.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_low.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_low)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.btn_info_popup = QPushButton(self.frame_low)
        self.btn_info_popup.setObjectName(u"btn_info_popup")
        self.btn_info_popup.setMinimumSize(QSize(50, 40))
        self.btn_info_popup.setMaximumSize(QSize(50, 40))
        icon12 = QIcon()
        icon12.addFile(u":/icons/icons/info-40.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_info_popup.setIcon(icon12)
        self.btn_info_popup.setIconSize(QSize(35, 35))
        self.btn_info_popup.setFlat(True)

        self.horizontalLayout_6.addWidget(self.btn_info_popup)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer)

        self.label_version = QLabel(self.frame_low)
        self.label_version.setObjectName(u"label_version")
        self.label_version.setMaximumSize(QSize(100, 16777215))
        font31 = QFont()
        font31.setFamilies([u"Segoe UI"])
        self.label_version.setFont(font31)
        self.label_version.setStyleSheet(u"color: rgb(98, 103, 111);")
        self.label_version.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_6.addWidget(self.label_version)

        self.frame_size_grip = QFrame(self.frame_low)
        self.frame_size_grip.setObjectName(u"frame_size_grip")
        self.frame_size_grip.setMinimumSize(QSize(20, 20))
        self.frame_size_grip.setMaximumSize(QSize(20, 20))
        self.frame_size_grip.setStyleSheet(u"QSizeGrip {\n"
"	background-image: url(:/icons/icons/ico-size-grip.png);\n"
"	background-position: center;\n"
"	background-repeat: no-reperat;\n"
"}")
        self.frame_size_grip.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_size_grip.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_6.addWidget(self.frame_size_grip)


        self.verticalLayout.addWidget(self.frame_low)


        self.horizontalLayout.addWidget(self.frame_main)

        MainWindow.setCentralWidget(self.centralwidget)
        QWidget.setTabOrder(self.btn_toggle_menu, self.btn_exp_obj_kml)
        QWidget.setTabOrder(self.btn_exp_obj_kml, self.btn_exp_footprint_kml)
        QWidget.setTabOrder(self.btn_exp_footprint_kml, self.btn_exp_footprint_shp)
        QWidget.setTabOrder(self.btn_exp_footprint_shp, self.btn_exp_obj_shp)
        QWidget.setTabOrder(self.btn_exp_obj_shp, self.btn_exp_obj_csv)
        QWidget.setTabOrder(self.btn_exp_obj_csv, self.btn_exp_footprint_csv)
        QWidget.setTabOrder(self.btn_exp_footprint_csv, self.btn_exp_footprint_json)
        QWidget.setTabOrder(self.btn_exp_footprint_json, self.btn_exp_obj_json)
        QWidget.setTabOrder(self.btn_exp_obj_json, self.btn_exp_obj_poin_shp)

        self.retranslateUi(MainWindow)

        self.page_stack.setCurrentIndex(0)
        self.tab_imports.setCurrentIndex(0)
        self.imp_stack_type.setCurrentIndex(1)
        self.stack_image_test.setCurrentIndex(0)
        self.stack_navigation.setCurrentIndex(1)
        self.btn_wisdam_homepage.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
#if QT_CONFIG(tooltip)
        self.btn_toggle_menu.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Fold/Unfold menue names</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.btn_toggle_menu.setText("")
#if QT_CONFIG(tooltip)
        self.lbl_database_name.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lbl_database_name.setText("")
#if QT_CONFIG(tooltip)
        self.label_title_bar_top.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.label_title_bar_top.setText("")
#if QT_CONFIG(tooltip)
        self.btn_minimize.setToolTip(QCoreApplication.translate("MainWindow", u"Minimize", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.btn_maximize_restore.setToolTip(QCoreApplication.translate("MainWindow", u"Maximize", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.btn_close.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Close</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Paths", None))
        self.led_image_path.setText("")
        self.led_elevation_service.setText("")
        self.input_adj_rel_height.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_37.setText(QCoreApplication.translate("MainWindow", u"Adjust relative altitude for all images to [m]:", None))
        self.imp_btn_logfile_folder.setText(QCoreApplication.translate("MainWindow", u"Select Log File Folder", None))
        self.imp_btn_logfile.setText(QCoreApplication.translate("MainWindow", u"Select Single Log File", None))
        self.label_38.setText(QCoreApplication.translate("MainWindow", u"Height (reference  is geoid) [m]", None))
        self.label_36.setText(QCoreApplication.translate("MainWindow", u"Longitude [\u00b0]", None))
        self.imp_georef_latitude.setText("")
        self.label_40.setText(QCoreApplication.translate("MainWindow", u"Focal length [mm]", None))
        self.imp_georef_sensor_width.setText("")
        self.label_39.setText(QCoreApplication.translate("MainWindow", u"Latitude [\u00b0]", None))
        self.imp_georef_focal_mm.setText("")
        self.imp_georef_heading.setText("")
        self.label_42.setText(QCoreApplication.translate("MainWindow", u"Heading [\u00b0]\n"
"(e.g. North 0\u00b0; East +90\u00b0)", None))
        self.label_43.setText(QCoreApplication.translate("MainWindow", u"Sensor width [mm]", None))
        self.label_44.setText(QCoreApplication.translate("MainWindow", u"! OPTIONAL !", None))
        self.imp_georef_status.setText("")
        self.import_image_meta_comment.setPlainText("")
#if QT_CONFIG(tooltip)
        self.imp_cmb_input_type.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Change Input Data Type</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.led_focal_length.setText("")
        self.led_gnss_data.setText("")
        self.led_image_pose.setText("")
        self.led_crs_vertical.setText("")
        self.led_crs_data.setText("")
        self.label_57.setText(QCoreApplication.translate("MainWindow", u"Raster Geo-Transform or World File available", None))
        self.led_ortho_coordinates.setText("")
        self.label_59.setText(QCoreApplication.translate("MainWindow", u"Possible to open with RasterIO", None))
        self.led_rasterio_possible.setText("")
        self.led_ortho_crs.setText("")
        self.label_60.setText(QCoreApplication.translate("MainWindow", u"CRS System available", None))
#if QT_CONFIG(tooltip)
        self.btn_gis_toggle_list.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Fold/Unfold image list</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.btn_gis_toggle_list.setText(QCoreApplication.translate("MainWindow", u"\u25c4\n"
"\u25c4", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Selection", None))
#if QT_CONFIG(tooltip)
        self.btn_selection_rectangle.setToolTip(QCoreApplication.translate("MainWindow", u"Rectangle Selection", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.btn_selection_lasso.setToolTip(QCoreApplication.translate("MainWindow", u"Lasso Selection", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.btn_gis_toggle_props.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Fold/Unfold operations list</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.btn_gis_toggle_props.setText(QCoreApplication.translate("MainWindow", u"\u25ba\n"
"\u25ba", None))
#if QT_CONFIG(tooltip)
        self.btn_picking_toggle_list.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Fold/Unfold image list</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.btn_picking_toggle_list.setText(QCoreApplication.translate("MainWindow", u"\u25c4\n"
"\u25c4", None))
        self.btn_propagate_always.setText("")
#if QT_CONFIG(tooltip)
        self.btn_create_point.setToolTip(QCoreApplication.translate("MainWindow", u"Point", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.btn_create_line.setToolTip(QCoreApplication.translate("MainWindow", u"LineString", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.btn_create_rectangle.setToolTip(QCoreApplication.translate("MainWindow", u"Rectangle", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.btn_create_polygon.setToolTip(QCoreApplication.translate("MainWindow", u"Polygon", None))
#endif // QT_CONFIG(tooltip)
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"Hide Objects", None))
#if QT_CONFIG(tooltip)
        self.dial_image_scale.setToolTip(QCoreApplication.translate("MainWindow", u"Scaling of image", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.btn_navigation_startwalk.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Navigate in Snake Lines through the image. <br/>Keys: Right and left to move the window along the path (snake line)<br/></p><p>Load another image: Enter - next image . Backspace - last image</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.btn_picking_toggle_props.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Fold/Unfold operations list</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.btn_picking_toggle_props.setText(QCoreApplication.translate("MainWindow", u"\u25ba\n"
"\u25ba", None))
#if QT_CONFIG(tooltip)
        self.frame_19.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.gallery_filter_object.setText("")
        self.gallery_filter_resight_set.setText("")
#if QT_CONFIG(tooltip)
        self.btn_gallery_toggle_props.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Fold/Unfold grid operations</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.btn_gallery_toggle_props.setText(QCoreApplication.translate("MainWindow", u"\u25ba\n"
"\u25ba", None))
#if QT_CONFIG(tooltip)
        self.db_export_trainingsdata.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Change Paths of images if location changed</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_61.setText(QCoreApplication.translate("MainWindow", u"Shape File is not recomended\n"
"It can produce unexpected outputs\n"
"(for example, field length truncated to\n"
"10 characters only.)", None))
        self.btn_load_ai_res_filesystem.setText(QCoreApplication.translate("MainWindow", u"Load AI Results From Filesystem", None))
        self.ai_filter_object.setText("")
#if QT_CONFIG(tooltip)
        self.frame_26.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.btn_ai_toggle_props.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Fold/Unfold grid operations</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.btn_ai_toggle_props.setText(QCoreApplication.translate("MainWindow", u"\u25ba\n"
"\u25ba", None))
        self.compare_modus_combobox.setItemText(0, QCoreApplication.translate("MainWindow", u"1) Single DB: SELF to AI", None))
        self.compare_modus_combobox.setItemText(1, QCoreApplication.translate("MainWindow", u"2) Single DB: AI to AI REVIEW", None))
        self.compare_modus_combobox.setItemText(2, QCoreApplication.translate("MainWindow", u"3) Dual DB: MANUAL to MANUAL", None))
        self.compare_modus_combobox.setItemText(3, QCoreApplication.translate("MainWindow", u"4) Dual DB: ALL to ALL", None))

        self.compare_label_info.setText("")
#if QT_CONFIG(tooltip)
        self.label_4.setToolTip(QCoreApplication.translate("MainWindow", u"Double Click to expand", None))
#endif // QT_CONFIG(tooltip)
        self.btn_info_popup.setText("")
        self.label_version.setText(QCoreApplication.translate("MainWindow", u"v1.2", None))
#if QT_CONFIG(tooltip)
        self.frame_size_grip.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Change window size</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi

