# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui_info.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QPushButton,
    QSizePolicy, QTextEdit, QVBoxLayout, QWidget)
from . import files_rc

class Ui_info(object):
    def setupUi(self, info):
        if not info.objectName():
            info.setObjectName(u"info")
        info.resize(600, 200)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(info.sizePolicy().hasHeightForWidth())
        info.setSizePolicy(sizePolicy)
        info.setMinimumSize(QSize(450, 200))
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
        info.setPalette(palette)
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(10)
        info.setFont(font)
        info.setStyleSheet(u"background: transparent;\n"
"\n"
"")
        self.verticalLayout = QVBoxLayout(info)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(info)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(450, 200))
        self.frame.setStyleSheet(u"QScrollBar::handle:horizontal {\n"
"	background: rgb(178, 186, 87);\n"
"    min-width: 25px;\n"
"}\n"
"\n"
"QScrollBar::add-page:horizontal\n"
"{\n"
"      background: rgb(47,49,65);\n"
"}\n"
"\n"
"QScrollBar::sub-page:horizontal\n"
"{\n"
"      background: rgb(47,49,65);\n"
"}\n"
"\n"
" QScrollBar::handle:vertical {	\n"
"	background: rgb(178, 186, 87);\n"
"    min-height: 25px;\n"
" }\n"
"\n"
"QScrollBar::sub-page:vertical {\n"
"    background:  rgb(47,49,65);\n"
"}\n"
"\n"
"QScrollBar::add-page:vertical {\n"
"    background:  rgb(47,49,65);\n"
"}")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_info = QFrame(self.frame)
        self.frame_info.setObjectName(u"frame_info")
        self.frame_info.setStyleSheet(u"background-color: rgba(34, 113, 150, 190);")
        self.frame_info.setFrameShape(QFrame.StyledPanel)
        self.frame_info.setFrameShadow(QFrame.Raised)
        self.btn_save = QPushButton(self.frame_info)
        self.btn_save.setObjectName(u"btn_save")
        self.btn_save.setEnabled(True)
        self.btn_save.setGeometry(QRect(540, 0, 40, 31))
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.btn_save.sizePolicy().hasHeightForWidth())
        self.btn_save.setSizePolicy(sizePolicy1)
        self.btn_save.setMinimumSize(QSize(40, 0))
        self.btn_save.setMaximumSize(QSize(40, 16777215))
        self.btn_save.setStyleSheet(u"QPushButton {	\n"
"	border: none;\n"
"	background-color: transparent;\n"
" QToolTip {\n"
"	color: white;\n"
"	background-color: black;\n"
"	border: 1px solid rgb(40, 40, 40);\n"
"	border-radius: 2px;\n"
"};\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(120, 100, 41);\n"
" QToolTip {\n"
"	color: white;\n"
"	background-color: black;\n"
"	border: 1px solid rgb(40, 40, 40);\n"
"	border-radius: 2px;\n"
"};\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(180, 150, 41);\n"
" QToolTip {\n"
"	color: white;\n"
"	background-color: black;\n"
"	border: 1px solid rgb(40, 40, 40);\n"
"	border-radius: 2px;\n"
"};\n"
"}\n"
" QToolTip {\n"
"	color: white;\n"
"	background-color: black;\n"
"	border: 1px solid rgb(40, 40, 40);\n"
"	border-radius: 2px;\n"
"}\n"
"")
        icon = QIcon()
        icon.addFile(u":/icons/icons/menu-save.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_save.setIcon(icon)
        self.info_screen = QTextEdit(self.frame_info)
        self.info_screen.setObjectName(u"info_screen")
        self.info_screen.setGeometry(QRect(10, 30, 580, 160))
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.info_screen.sizePolicy().hasHeightForWidth())
        self.info_screen.setSizePolicy(sizePolicy2)
        self.info_screen.setMinimumSize(QSize(0, 0))
        self.info_screen.setBaseSize(QSize(0, 0))
        self.info_screen.setStyleSheet(u"QTextEdit {\n"
"	background-color: rgb(47,49,65);\n"
"	border-radius: 5px;\n"
"	padding: 10px;\n"
"}\n"
"QPTextEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QPTextEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}")
        self.info_screen.setUndoRedoEnabled(False)
        self.info_screen.setReadOnly(True)
        self.info_screen.setMarkdown(u"")
        self.info_screen.setHtml(u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>")

        self.horizontalLayout.addWidget(self.frame_info)


        self.verticalLayout.addWidget(self.frame)


        self.retranslateUi(info)

        QMetaObject.connectSlotsByName(info)
    # setupUi

    def retranslateUi(self, info):
        info.setWindowTitle(QCoreApplication.translate("info", u"MainWindow", None))
#if QT_CONFIG(tooltip)
        self.btn_save.setToolTip(QCoreApplication.translate("info", u"Save logs", None))
#endif // QT_CONFIG(tooltip)
        self.btn_save.setText("")
    # retranslateUi

