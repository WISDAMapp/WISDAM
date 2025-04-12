# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui_about.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QFrame,
    QHBoxLayout, QHeaderView, QLabel, QPushButton,
    QSizePolicy, QTreeView, QVBoxLayout, QWidget)
from . import files_rc

class Ui_popup_about(object):
    def setupUi(self, popup_about):
        if not popup_about.objectName():
            popup_about.setObjectName(u"popup_about")
        popup_about.resize(850, 761)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(popup_about.sizePolicy().hasHeightForWidth())
        popup_about.setSizePolicy(sizePolicy)
        popup_about.setMinimumSize(QSize(850, 600))
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
        popup_about.setPalette(palette)
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(10)
        popup_about.setFont(font)
        popup_about.setStyleSheet(u"QWidget {background: transparent; color: rgb(210, 210, 210)}\n"
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
"	background: rgb(178, 186, 87);\n"
"    min-width: 25px;\n"
"	border-radius: 7px\n"
"}\n"
"QScrollBar::add-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    wi"
                        "dth: 20px;\n"
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
"    background:"
                        " rgb(55, 63, 77);\n"
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
"")
        self.verticalLayout = QVBoxLayout(popup_about)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_top = QFrame(popup_about)
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

        self.frame_center = QFrame(popup_about)
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
        self.label_8 = QLabel(self.frame_center)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(360, 420, 91, 16))
        self.label_8.setStyleSheet(u"border: 1px solid rgba(170, 170, 255,100);\n"
"border-radius:15px;")
        self.label_8.setText(u"License Table")
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_title_bar_top = QLabel(self.frame_center)
        self.label_title_bar_top.setObjectName(u"label_title_bar_top")
        self.label_title_bar_top.setGeometry(QRect(40, 80, 201, 101))
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_title_bar_top.sizePolicy().hasHeightForWidth())
        self.label_title_bar_top.setSizePolicy(sizePolicy3)
        self.label_title_bar_top.setMaximumSize(QSize(300, 300))
        font3 = QFont()
        font3.setFamilies([u"Segoe UI"])
        font3.setPointSize(19)
        font3.setBold(True)
        self.label_title_bar_top.setFont(font3)
        self.label_title_bar_top.setStyleSheet(u"")
        self.label_title_bar_top.setText(u"")
        self.label_title_bar_top.setPixmap(QPixmap(u":/icons/icons/WISDAM_Hero Logo_White.svg"))
        self.label_title_bar_top.setScaledContents(True)
        self.label_title_bar_top.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.label_title_bar_top.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        self.label = QLabel(self.frame_center)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 387, 991, 31))
        self.label.setText(u"WISDAM thankfully relies on packages provided as open source. The  table below try to list packages and used libraries with their license informatoin.\n"
"If you find any missing information please file an issue. License info can also be found in the folder license. Double click to expand license information.")
        self.label_2 = QLabel(self.frame_center)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(290, 10, 541, 161))
        self.label_2.setText(u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:700; color:#b49629;\">WISDAM</span><span style=\" font-size:11pt;\"> </span><span style=\" font-size:11pt; font-weight:700;\">(</span><span style=\" font-size:11pt; font-weight:700; color:#b49629;\">Wildlife Imagery Survey \u2013 Detection and Mapping</span><span style=\" font-size:11pt; font-weight:700;\">)</span><span style=\" font-size:11"
                        "pt;\"> is a software package for digitalization of objects within images and to enrich objects with meta data.<br />Information about the WISDAM Project can be found at </span><span style=\" font-size:11pt; font-weight:700;\">www.wisdamapp.org </span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">The Repository can be found at </span><span style=\" font-size:11pt; font-weight:700;\">github.com/wisdamapp</span><span style=\" font-size:11pt;\">.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:700; color:#da4900;\">It's the main contact point f"
                        "or discussion, bug reporting and info how to get involved.</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.label_2.setWordWrap(True)
        self.label_2.setOpenExternalLinks(True)
        self.label_2.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse)
        self.lbl_copyright = QLabel(self.frame_center)
        self.lbl_copyright.setObjectName(u"lbl_copyright")
        self.lbl_copyright.setGeometry(QRect(290, 190, 531, 81))
        font4 = QFont()
        font4.setPointSize(12)
        font4.setBold(True)
        self.lbl_copyright.setFont(font4)
        self.lbl_copyright.setFrameShape(QFrame.Shape.NoFrame)
        self.lbl_copyright.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.treeView_license = QTreeView(self.frame_center)
        self.treeView_license.setObjectName(u"treeView_license")
        self.treeView_license.setGeometry(QRect(10, 430, 831, 281))
        self.treeView_license.setStyleSheet(u"QTreeView{alternate-background-color: rgb(38, 40, 56); background: transparent;}\n"
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
"")
        self.treeView_license.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.treeView_license.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
        self.treeView_license.setAutoScroll(False)
        self.treeView_license.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.treeView_license.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.treeView_license.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.treeView_license.setHeaderHidden(True)
        self.treeView_license.header().setMinimumSectionSize(220)
        self.treeView_license.header().setDefaultSectionSize(220)
        self.treeView_license.header().setStretchLastSection(True)
        self.label_3 = QLabel(self.frame_center)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(20, 340, 731, 41))
        font5 = QFont()
        font5.setPointSize(10)
        font5.setBold(True)
        self.label_3.setFont(font5)
        self.label_3.setStyleSheet(u"")
        self.label_3.setText(u"<html><head/><body><p>WISDAM is using <span style=\" color:#2cde85;\">Qt's QT6 engine with Pyside6/shiboken6</span> under the GPLv3 and <span style=\" color:#016cb1;\">LibRAW</span> under the LGPLv.2.1<br/>Instructions to obtain the source coude can be found under github.com/wisdamapp</p></body></html>")
        self.label_3.setTextFormat(Qt.TextFormat.RichText)
        self.label_title_bar_top.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.lbl_copyright.raise_()
        self.treeView_license.raise_()
        self.label_8.raise_()
        self.label_3.raise_()

        self.verticalLayout.addWidget(self.frame_center)


        self.retranslateUi(popup_about)

        QMetaObject.connectSlotsByName(popup_about)
    # setupUi

    def retranslateUi(self, popup_about):
        popup_about.setWindowTitle(QCoreApplication.translate("popup_about", u"MainWindow", None))
        self.lbl_icon.setText("")
#if QT_CONFIG(tooltip)
        self.label_title.setToolTip(QCoreApplication.translate("popup_about", u"<html><head/><body><p><span style=\" font-size:8pt; font-weight:400;\">Move window</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_title.setText(QCoreApplication.translate("popup_about", u"About WISDAM", None))
#if QT_CONFIG(tooltip)
        self.label_title_bar_top.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lbl_copyright.setText("")
#if QT_CONFIG(tooltip)
        self.treeView_license.setToolTip(QCoreApplication.translate("popup_about", u"Double click to expand", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi

