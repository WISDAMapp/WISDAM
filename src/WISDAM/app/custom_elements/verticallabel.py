
from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtGui import (QPixmap, QPainter)
from PySide6.QtCore import Qt, Signal, Slot, QSize


class VerticalLabel(QLabel):

    def __init__(self, *args):
        QLabel.__init__(self, *args)

    def paintEvent(self, event):
        #QLabel.paintEvent(self, event)
        painter = QPainter(self)
        painter.translate(0, self.height()-1)
        painter.rotate(-90)
        painter.drawText(int(self.height()/2), int(self.width()), self.text())
        painter.end()

    def minimumSizeHint(self):
        size = QLabel.minimumSizeHint(self)
        return QSize(size.height(), size.width())

    def sizeHint(self):
        size = QLabel.sizeHint(self)
        return QSize(size.height(), size.width())

