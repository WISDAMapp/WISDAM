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


from pathlib import Path
from multiprocessing import Process, Queue
import rawpy
import logging

import numpy
from PIL import ImageQt
from PIL import Image
from PIL import UnidentifiedImageError
import rasterio
from rasterio.plot import reshape_as_raster, reshape_as_image


from PySide6.QtGui import QPixmap, QImage, QImageReader

Image.MAX_IMAGE_PIXELS = None

logger = logging.getLogger(__name__)

QImageReader.setAllocationLimit(0)

image_formats_direct_load = []
for x in QImageReader.supportedImageFormats():
    image_formats_direct_load.append('.' + x.data().decode())


def image_loader_standard(filename: Path | str) -> QImage | None:
    q_image = None

    if Path(filename).suffix.lower() in image_formats_direct_load:
        q_image = QImage(Path(filename).as_posix())
        if not q_image.isNull():
            return q_image

    try:
        # imread is just to try if raw file can be read without reading full image
        res = loader_raw(Path(filename).as_posix())

        if res:
            buf, w, h, bytes_per_line = res
            q_image = QImage(buf, w, h, bytes_per_line, QImage.Format_RGB888)

    except (rawpy.LibRawError, rawpy.NotSupportedError):
        try:
            img_pil = Image.open(Path(filename).as_posix())
            img_pil = img_pil.convert("RGBA")
            q_image = img_pil.toqimage()

        except UnidentifiedImageError:
            pass

    return q_image


def image_loader_rasterio_standard(filename: Path | str) -> QImage | None:

    try:
        with rasterio.open(filename) as xx:
            ii = xx.read()
        ii = numpy.ma.transpose(ii, [1, 2, 0])[:, :, :3]

        if (ii.dtype != 'uint8' or ii.max() < 2) and ii.max() != 0:
            data_8bit = (ii - numpy.min(ii)) / (numpy.max(ii) - numpy.min(ii)) * 255
        else:
            data_8bit = ii
        if data_8bit.shape[2] > 2:
            pi = Image.fromarray(data_8bit.astype('uint8'), 'RGB')
        else:
            pi = Image.fromarray(data_8bit[:, :, 0].astype('uint8'), 'L')

        #ii4 = xx.read([1,2,3],out_dtype='uint8')
        #ii5 = reshape_as_image(ii4)
        #pi = Image.fromarray(ii5, 'RGB')
        q_image = pi.toqimage()

    except:

        #logger.error("Image Loading failed")
        return None

    return q_image



def image_loader_rasterio(filename: Path | str) -> QPixmap | None:

    try:
        with rasterio.open(filename) as xx:
            ii = xx.read()
        ii = numpy.ma.transpose(ii, [1, 2, 0])[:, :, :3]

        if (ii.dtype != 'uint8' or ii.max() < 2) and ii.max() != 0:
            data_8bit = (ii - numpy.min(ii)) / (numpy.max(ii) - numpy.min(ii)) * 255
        else:
            data_8bit = ii
        if data_8bit.shape[2] > 2:
            pi = Image.fromarray(data_8bit.astype('uint8'), 'RGB')
        else:
            pi = Image.fromarray(data_8bit[:, :, 0].astype('uint8'), 'L')

        #ii4 = xx.read([1,2,3],out_dtype='uint8')
        #ii5 = reshape_as_image(ii4)
        #pi = Image.fromarray(ii5, 'RGB')
        q_pix = pi.toqpixmap()
    except:
        logger.error("Image Loading failed")
        return None

    return q_pix


def image_loader(filename: Path | str) -> QPixmap | None:
    q_pix = None

    if Path(filename).suffix.lower() in image_formats_direct_load:
        q_pix = QPixmap(filename)
        if not q_pix.isNull():
            return q_pix

    try:
        # imread is just to try if raw file can be read without reading full image
        rawpy.imread(filename.as_posix())
        q = Queue()
        proc = Process(target=loader_raw_multiproc, args=(filename.as_posix(), q))
        proc.start()
        q_image = q.get()
        proc.join()
        if q_image:
            buf, w, h, bytes_per_line = q_image
            q_pix = QPixmap.fromImage(QImage(buf, w, h, bytes_per_line, QImage.Format_RGB888))

    except (rawpy.LibRawError, rawpy.NotSupportedError):
        try:
            img_pil = Image.open(filename)
            img_pil = img_pil.convert("RGBA")
            q_pix = img_pil.toqpixmap()

        except UnidentifiedImageError:
            pass

    return q_pix


def image_loader_slower(filename: Path | str) -> QPixmap | None:
    if filename.suffix.lower() in image_formats_direct_load:
        q_pix = QPixmap(filename)
        if not q_pix.isNull():
            return q_pix

    q = Queue()
    proc = Process(target=image_loader_call, args=(filename, q))
    proc.start()
    q_image = q.get()
    proc.join()
    q_pix = None
    if q_image is not None:
        if isinstance(q_image, Image.Image):
            q_pix = QPixmap.fromImage(ImageQt.ImageQt(q_image))
        elif isinstance(q_image, tuple):
            buf, w, h, bytes_per_line = q_image
            q_pix = QPixmap.fromImage(QImage(buf, w, h, bytes_per_line, QImage.Format_RGB888))

    return q_pix


def image_loader_call(filename: Path, queue: Queue):
    try:
        rawpy.imread(filename.as_posix())
        raw_image = loader_raw(filename.as_posix())
        if raw_image is not None:
            # buf, w, h, bytes_per_line = raw_image
            # q_image = QImage(buf, w, h, bytes_per_line, QImage.Format_RGB888)
            queue.put(raw_image)
    except (rawpy.LibRawError, rawpy.NotSupportedError):
        try:
            img_pil = Image.open(filename)
            img_pil = img_pil.convert("RGBA")
            # queue.put(img_pil)
            # q_image = QImage(ImageQt.ImageQt(img_pil))
            queue.put(img_pil)

        except UnidentifiedImageError:
            pass


def loader_raw(path: str):
    try:
        with rawpy.imread(path) as raw:
            src = raw.postprocess(user_flip=0)
            h, w, ch = src.shape
            bytes_per_line = ch * w
            buf = src.data.tobytes()  # or bytes(src.data)
            return buf, w, h, bytes_per_line
    except rawpy.LibRawError:
        return None


def loader_raw_multiproc(path: str, queue: Queue):
    try:
        with rawpy.imread(path) as raw:
            src = raw.postprocess(user_flip=0)
            h, w, ch = src.shape
            bytes_per_line = ch * w
            buf = src.data.tobytes()  # or bytes(src.data)
            queue.put([buf, w, h, bytes_per_line])
    except rawpy.LibRawError:
        queue.put([])
