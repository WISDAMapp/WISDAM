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


import json
import pandas
import csv
from pathlib import Path

from PySide6.QtCore import QRect, QPoint
from PySide6 import QtCore
from PySide6.QtGui import (QPixmap)


from app.var_classes import (ExternalSighting, external_surety)
from core_interface.image_loader import image_loader

# WISDAM core
from WISDAMcore.mapping.store_geom import store_geom
from WISDAMcore.image.imageWisdam import WISDAMImage
from WISDAMcore.db.dbHandler import DBHandler


def crop_image_external(picture: QPixmap, rectangle: QRect):
    cropped_image = picture.copy(rectangle)
    ba = QtCore.QByteArray()
    buff = QtCore.QBuffer(ba)
    buff.open(QtCore.QIODevice.WriteOnly)
    ok = cropped_image.save(buff, "JPG")
    assert ok
    pixmap_bytes = ba.data()
    return pixmap_bytes


def no_yes_value(string: 'str'):
    if string == 'yes':
        return 1
    return 0


def mumandcalf_oldImageSightings(string: 'str', string2: 'str'):
    if string == 'Single':
        return 'Single'
    if string2 == 'No':
        return 'Mother'
    else:
        return 'Calf'


def water_pos(string: 'str'):
    if string == 'Surface':
        return 0
    elif string == 'Mid-water':
        return 1
    else:
        return 2


class HeaderExcel:
    SurveyName = ''
    File = ''
    X1 = ''
    X2 = ''
    Y1 = ''
    Animal = ''
    MumAndCalf = ''
    Calf = ''
    Certainty = ''
    FirstCertainty = ''
    WaterPosition = ''
    Turbidity = ''
    Glare = ''
    SeaState = ''
    Resight = ''


def check_header(header_strings_list, string_to_find):

    if any(string_to_find in s.lower() for s in header_strings_list):
        found = [s for s in header_strings_list if string_to_find in s.lower()]
        if len(found)>1:
            for x in found:
                if x == string_to_find:
                    found_single=x
        else:
            found_single = found
        return found_single

    return ''


def process_external_data(path_data: Path, path_img_folder: Path, db_path: Path, user: 'str', height, type, delimiter,
                          swap_xy=False,
                          progress_callback=None):

    external_sightings_list = []

    db = DBHandler.from_path(db_path, user)

    success_csv = 0
    fail_csv = 0

    if type=='Orthos_NT':
        # Read Excel File and check content
        try:
            data_excel = pandas.read_excel(path_data)
        except:
            progress_callback.emit((1, 1))
            db.close()
            return 'Can not parse data. Maybe wrong format'

        data_excel_columns = data_excel.keys()

        # Check header for strings
        header_strings = list(data_excel_columns)
        header_excel_pos = HeaderExcel()

        position_all = []
        for index, row in data_excel.iterrows():
            # print(row[header_excel_pos.Resight], row[header_excel_pos.X1])
            try:
                sight = ExternalSighting()
                name = row[1].split('.')[0]
                shift_x = int(name.split('_')[-2].split('-')[1])
                shift_y = int(name.split('_')[-1].split('-')[1])

                rec = [int(row[2])+shift_x, int(row[3])+shift_y, int(row[4])+shift_x, int(row[5])+shift_y]
                # rec = [int(float(x)) for x in row[2:6]]
                if swap_xy:
                    rec = [rec[1], rec[0], rec[3], rec[2]]
                if rec[2] < rec[0]:
                    dum = rec[0] + 0.0
                    rec[0] = rec[2]
                    rec[2] = dum
                if rec[3] < rec[1]:
                    dum = rec[1] + 0.0
                    rec[1] = rec[3]
                    rec[3] = dum
                sight.geometry = [rec[0:2], rec[2:]]
                sight.name = row[0]
                sight.img = Path('_'.join(row[1].split('_')[:-2]) + '.tif')

                sight.geom_type = 'Rectangle'
                row = row.fillna(' ')
                sight.object_type = row[6]
                data_string = {
                    'Species': row[17],
                    'Resight': row[15].lower(),
                    'Certainty': row[9].lower(),
                    'FirstCertain': row[10].lower(),
                    'WaterPosition': row[11],
                    'MumCalf': mumandcalf_oldImageSightings(row[7], row[8]),
                    'SpeciesSurety': external_surety(row[16]),
                    'Notes': row[18],

                }
                data_string = json.dumps(data_string)

                sight.env_data = json.dumps({'Glare': str(row[13]),
                                             'Turbidity': str(row[12]),
                                             'SeaState': str(row[14])})

                sight.meta_data = data_string
                success_csv += 1
                external_sightings_list.append(sight)
            except:
                fail_csv += 1
                continue
    if type == 'Normal':

        with open(path_data, 'r') as csvfile:
            # creating a csv reader object
            csvreader = csv.reader(csvfile, delimiter=delimiter)
            # extracting each data row one by one
            for row in csvreader:
                if len(row) == 16:
                    try:
                        sight = ExternalSighting()
                        rec = [int(float(x)) for x in row[2:6]]
                        if swap_xy:
                            rec = [rec[1],rec[0],rec[3],rec[2]]
                        if rec[2] < rec[0]:
                            dum = rec[0] + 0.0
                            rec[0] = rec[2]
                            rec[2] = dum
                        if rec[3] < rec[1]:
                            dum = rec[1] + 0.0
                            rec[1] = rec[3]
                            rec[3] = dum
                        sight.geometry = [rec[0:2], rec[2:]]
                        sight.name = row[0]
                        sight.img = Path(row[1])

                        sight.geom_type = 'Rectangle'
                        sight.object_type = row[6]
                        data_string = json.dumps({
                            'Species': row[6],
                            'Resight': row[15].lower(),
                            'Certainty': row[9].lower(),
                            'FirstCertain': row[10].lower(),
                            'WaterPosition': row[11],
                            'MumCalf': mumandcalf_oldImageSightings(row[7],row[8]),
                            'SpeciesSurety': 0,
                            'Notes': ''
                        })

                        sight.meta_data = data_string
                        sight.env_data = json.dumps({'Glare': str(row[13]),
                                                     'Turbidity': str(row[12]),
                                                     'SeaState': str(row[14])})
                        success_csv += 1
                        external_sightings_list.append(sight)
                    except:
                        fail_csv += 1
                        continue
                else:
                    fail_csv += 1

    print('Found ' + str(success_csv) + ' valid data rows in file')
    print('Import can take some while..calculating cropped Images')


        # load external data

    if external_sightings_list:
        success = []
        fail = []
        image = WISDAMImage()
        duplicates = 0
        image_old_path = ''
        for idx, sighting in enumerate(external_sightings_list):

            image = db.load_image_by_path(path_img_folder / sighting.img)
            if image is not None:

                try:
                    points_image = [[sighting.geometry[0][0], sighting.geometry[0][1]],
                                    [sighting.geometry[1][0], sighting.geometry[0][1]],
                                    [sighting.geometry[1][0], sighting.geometry[1][1]],
                                    [sighting.geometry[0][0], sighting.geometry[1][1]],
                                    [sighting.geometry[0][0], sighting.geometry[0][1]]]
                    geo = 'POLYGON((' + ', '.join([' '.join([str(int(x)) for x in t]) for t in points_image]) + '))'
                    query = r"""select * from sightings
                    join images
                    where 
                    data = :data
                    and astext(geom2d) = :geo 
                    and images.path = :img
                    """

                    data = db.con.execute(query, {
                        'data': sighting.meta_data,
                        'geo': geo, 'img': (path_img_folder / sighting.img).as_posix()}).fetchone()
                    if not data:
                        rect = QRect(sighting.geometry[0][0], sighting.geometry[0][1],
                                     sighting.geometry[1][0] - sighting.geometry[0][0],
                                     sighting.geometry[1][1] - sighting.geometry[0][1])

                        sight_id = store_geom(db, image, height, sighting.geom_type, [QPoint(x, y) for x, y in points_image])
                        db.store_objects_meta(sight_id, sighting.object_type, sighting.meta_data, source=2)

                        if image.path != image_old_path:
                            img = image_loader(image.path)
                            image_old_path = image.path

                        cropped_image = crop_image_external(img, rect)
                        db.store_cropped_image(cropped_image, sight_id)
                        success.append(sighting.img)
                    else:
                        duplicates += 1
                except:
                    fail.append(sighting.img)
                    continue
            else:
                fail.append(sighting.img)

            progress_callback.emit((len(external_sightings_list) - 1, idx))

        db.close()
        return 'Nr of success= ' + str(len(success)) + '; Failed imports:' + str(len(fail)) + '; Duplicates: ' +\
               str(duplicates)

    else:
        progress_callback.emit((1, 1))
        db.close()
        return 'Can not parse data'
