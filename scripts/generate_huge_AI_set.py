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
import random
import sys
from datetime import datetime


def generate_generic_ai_random_dataset(path_base_images: str, path_output: str, width: int, height: int):
    """With this function you can generate random huge AI dataset for testing AI page
    First argument is path to images where ".jpg" images are present, second path to output folder
    Third and Fourth argument are image-width and -height which should be used."""

    path_base_images = Path(path_base_images)
    path_output = Path(path_output)
    fid = open(path_output / ("output_" + datetime.now().strftime("%Y%m%d_%H%M%S") + '.txt'), 'w')
    fid.write("image_path,type,probability,xmin,ymin,xmax,ymax\n")

    object_types = ["dugong", "dolpgin", "bird", "turtle", "fox", "cat", "dog", "human", "shark", "elephant"]

    images = list(path_base_images.glob('*.jpg'))

    for x in range(150000):
        image_nr = random.randint(1, len(images)-1)
        probability = random.random()

        object_type = object_types[random.randint(0, len(object_types) - 1)]

        x_min = random.randint(20, width-300)
        y_min = random.randint(20, height-300)

        x_max = x_min + random.randint(20, 300)
        y_max = y_min + random.randint(20, 300)
        fid.write("%s,%s,%1.2f,%i,%i,%i,%i\n" % (images[image_nr].as_posix(), object_type, probability,
                                                 x_min, y_min, x_max, y_max))


if __name__ == "__main__":
    path_to_images = sys.argv[1]
    path_to_output = sys.argv[2]
    width_input = int(sys.argv[3])
    height_input = int(sys.argv[4])
    generate_generic_ai_random_dataset(path_to_images, path_to_output, width_input, height_input)
