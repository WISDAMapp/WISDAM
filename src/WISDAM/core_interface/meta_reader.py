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


from datetime import datetime, timedelta


def meta_image_time(meta_data: dict) -> datetime | None:
    time_strings = [
        ("EXIF:DateTimeOriginal", "EXIF:SubSecTimeOriginal", "EXIF:OffsetTimeOriginal"),
        ("EXIF:DateTimeDigitized", "EXIF:SubSecTimeDigitized", "EXIF:OffsetTimeDigitized"),
        ("Image:DateTime", "Image:SubSecTime", "Image:OffsetTime"),
    ]
    for datetime_tag, sub_sec_tag, offset_tag in time_strings:
        if datetime_tag in meta_data:
            date_time = meta_data[datetime_tag]
            if sub_sec_tag in meta_data:

                # Not sure if this actually can happen in EXIF but just catch if to be sure
                # Sub-second present in EXIF but zero. Needed as seen below
                if meta_data[sub_sec_tag] != 0:
                    sub_sec_time = str(meta_data[sub_sec_tag])
                else:
                    sub_sec_time = "001"

            else:
                # This is to make sure sub-second is present for geopandas conversion
                # to shape where timedata frame has to be converted and all images need to have the same format
                # As a non-existing sub-second would save for example in 10:01:44 and others in 20:10:44.15,
                # which geopandas can not parse if the format is %H:%M:%S.%f mixed with %H:%M:%S
                # Time format save to sqlite does not preserve zero sub-seconds.
                sub_sec_time = "001"
            try:
                s = "{0:s}.{1:s}".format(date_time, sub_sec_time)
                d = datetime.strptime(s, "%Y:%m:%d %H:%M:%S.%f")
            except ValueError:
                continue

            # Check if timezone offset is present
            if offset_tag in meta_data:
                offset_time = meta_data[offset_tag]
                try:
                    d += timedelta(hours=-int(offset_time[0:3]), minutes=int(offset_time[4:6]))
                except (TypeError, ValueError):
                    pass

            return d

    return None
