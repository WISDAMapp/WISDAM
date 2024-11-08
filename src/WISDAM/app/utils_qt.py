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


import PIL
from PIL import Image
from io import BytesIO

from PySide6 import QtCore, QtGui
from pathlib import Path
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import QBuffer, Qt, QRect, QPoint, QPointF, QIODevice
from PySide6.QtWidgets import QLabel, QPushButton

from app.var_classes import (source_switch, review_switch, NavRect)


def change_led_color(item: QLabel | QPushButton, on: bool = False):

    if on:
        style_sheet = """color: white;border-radius: 20;
        background-color: qlineargradient(spread:pad, x1:0.145, y1:0.16, x2:1, y2:1, stop:0 rgba(25, 255, 5, 255),
        stop:1 rgba(25, 134, 5, 255));"""
    else:
        style_sheet = """color: white;border-radius: 20;
        background-color: qlineargradient(spread:pad, x1:0.145, y1:0.16, x2:1, y2:1, stop:0 rgba(255, 25, 7, 255),
        stop:1 rgba(134, 25, 5, 255));"""

    item.setStyleSheet(style_sheet)


def list_of_points_to_list(pt_list: list[QPoint] | list[QPointF]):
    p_list = []
    for p in pt_list:
        p_list.append([p.x(), p.y()])

    return p_list

def crop_image_qimage(q_image: QImage, rectangle: QRect):
    cropped_image = q_image.copy(rectangle)
    ba = QtCore.QByteArray()
    buff = QtCore.QBuffer(ba)
    buff.open(QIODevice.WriteOnly)
    ok = cropped_image.save(buff, "JPG")
    assert ok
    pixmap_bytes = ba.data()
    return pixmap_bytes

def crop_image(picture: QImage, rectangle: QRect):
    cropped_image = picture.copy(rectangle)
    ba = QtCore.QByteArray()
    buff = QtCore.QBuffer(ba)
    buff.open(QIODevice.WriteOnly)
    ok = cropped_image.save(buff, "JPG")
    assert ok
    pixmap_bytes = ba.data()
    return pixmap_bytes


def image_to_bytes_qt(path_image: Path):
    img = QtGui.QPixmap(path_image.as_posix())
    ba = QtCore.QByteArray()
    buff = QtCore.QBuffer(ba)
    buff.open(QIODevice.WriteOnly)
    ok = img.save(buff, "JPG")
    assert ok
    pixmap_bytes = ba.data()
    return pixmap_bytes


def image_to_bytes(path_image: Path):
    if not path_image.is_file():
        return None

    try:
        img = Image.open(path_image.as_posix())
    except PIL.UnidentifiedImageError:
        return None
    except OSError:
        return None

    stream_io = BytesIO()

    try:
        img.save(stream_io, format="JPEG")
        return stream_io.getvalue()
    except OSError:
        return None
    except ValueError:
        return None


def image_thumb_grid_navigation_size(image_shape: tuple[int, int] = (100, 100)):
    if image_shape[1] >= image_shape[0]:
        height = NavRect.height
        width = image_shape[0] / image_shape[1] * NavRect.width * 1.0
    else:
        width = NavRect.width
        height = image_shape[1] / image_shape[0] * NavRect.height * 1.0
    return width, height


def create_tooltip_cropped_image(cropped_image, image_id, object_type, resight_set, source, reviewed) -> str:
    pixmap = QPixmap()
    pixmap.loadFromData(cropped_image, 'JPG')

    # if pixmap.width() >300 or pixmap.height() > 300:
    pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio)
    buffer = QBuffer()
    buffer.open(QIODevice.WriteOnly)
    pixmap.save(buffer, "PNG", quality=100)
    image = bytes(buffer.data().toBase64()).decode()
    html = '<html><head/><body"><p>'
    html += '<!-- -->'
    html += '<h2>' + str(object_type) + '</h2>'
    html += '<!-- -->'
    html += '<p>Image: ' + str(image_id) + '</p>'
    html += '<!-- -->'
    html += '<p>Source: ' + source_switch(source) + '</p>'
    html += '<!-- -->'
    if reviewed == 0:
        color = r'style="color:red"'
    else:
        color = ''
    html += '<p ' + color + '>Reviewed: ' + review_switch(reviewed) + '</p>'
    html += '<!-- -->'
    html += '<p>Resight Set: ' + str(resight_set) + '</p>'
    html += '<!-- -->'
    html += '<br><img src="data:image/png;base64,{}">'.format(image)
    html += '</p></body></html>'
    # image = bytes(cropped_image.toBase64()).decode()
    # ba = QByteArray(cropped_image)
    # html = '<img src="data:image/jpg;base64,{}">'.format(ba.toBase64())
    # html = '<img src="data:image/jpg;base64,{}">'.format(bytes(ba.toBase64()).decode())
    return html


def create_tooltip_objects(image_id, object_type, resight_set, source, reviewed) -> str:
    html = '<html><head/><body><p>'
    html += '<!-- -->'
    html += '<h2>' + str(object_type) + '</h2>'
    html += '<!-- -->'
    html += '<p>Image: ' + str(image_id) + '</p>'
    html += '<!-- -->'
    html += '<p>Source: ' + source_switch(source) + '</p>'
    html += '<!-- -->'
    if reviewed == 0:
        color = r'style="color:red"'
    else:
        color = ''
    html += '<p ' + color + '>Reviewed: ' + review_switch(reviewed) + '</p>'
    html += '<!-- -->'
    html += '<p>Resight Set: ' + str(resight_set) + '</p>'
    html += '<!-- -->'
    html += '</p></body></html>'

    return html


def change_tooltip_html(html_txt: str, object_type: str = None, resight_set: int = None, reviewed: int = None) -> str:
    text = html_txt.split('<!-- -->')
    if object_type is not None:
        text[1] = '<h3>' + str(object_type) + '</h3>'
    if resight_set is not None:
        text[5] = '<p>Resight Set: ' + str(resight_set) + '</p>'
    if reviewed is not None:
        if reviewed == 0:
            color = r'style="color:red"'
        else:
            color = ''
        text[4] = '<p ' + color + '>Reviewed: ' + review_switch(reviewed) + '</p>'
    text = '<!-- -->'.join(text)
    return text


# Toggle Frame visibility
def toggle_visible_frame(button, frame):
    if button.text() == '◄\n◄':
        button.setText('►\n►')
    else:
        button.setText('◄\n◄')
    frame.setHidden(not frame.isHidden())
