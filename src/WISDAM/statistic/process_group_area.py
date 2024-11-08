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
import numpy
import logging
import shapely.geometry as gm
from pyproj import Transformer
from pathlib import Path
from multiprocessing import Process, Queue

from db.dbHandler import DBHandler

logger = logging.getLogger(__name__)


def inside_dist(p01, p02, max_distance):
    if numpy.all(numpy.linalg.norm(p01 - p02, axis=1) > max_distance):
        return False

    return True


def group_area_multiprocess_start(db_path: Path, distance: float = 20.0):
    q = Queue()
    proc = Process(target=spatial_cluster_processing,
                   args=(db_path, distance, q))

    proc.daemon = True
    proc.start()
    proc.join()
    result = q.get()

    if result:
        logger.info('Spatial Cluster processed. Found %i clusters' % result, extra={"finished": True})
        return True

    logger.warning('No Objects with geo-reference available for spatial cluster calculation')
    return False


def spatial_cluster_processing(db_path: Path, distance: float = 20.0, queue=None):
    """Group areas by distance. If distance to one member of the group is within the distance it will be in the same
        group
    :param db_path: Path to database to run group area calculation
    :param distance: Distance of which objects within are grouped
    :param queue: Multiproces queue providing as result number of groups"""

    db = DBHandler.from_path(db_path)

    data = db.obj_load_all()

    if data:

        # Transform ellipsoid to geocentric for calculation with cartesian coordinates
        transformer = Transformer.from_crs(4979, 4978, always_xy=True)
        object_list = []

        for idx, row in enumerate(data):
            if row['geo']:
                geom = gm.shape(json.loads(row['geo']))
                pos_prj = transformer.transform(geom.centroid.x, geom.centroid.y, 0)
                object_list.append([row['id'], [pos_prj[0], pos_prj[1], pos_prj[2]]])

        all_groups = []
        # iterate as long as still objects are not assigned to any area group
        while len(object_list) > 0:

            groups_outer = []
            current_cluster = [object_list[0][1], object_list[0][1]]
            len_cluster = 0
            # we will iterate as long as we can not add any new object to the current cluster
            while len(current_cluster) != len_cluster:
                groups = []
                len_cluster = len(current_cluster)
                # print(len_cluster)
                cluster_numpy = numpy.array(current_cluster)
                for idx, x in enumerate(object_list):
                    x_numpy = numpy.array(x[1])

                    # check if current object is within distance to any object of the current cluster
                    is_inside = inside_dist(x_numpy, cluster_numpy, distance)

                    if is_inside:
                        groups.append(x)
                        groups_outer.append(x)

                for x in groups:
                    current_cluster = current_cluster + [x[1]]
                    object_list.remove(x)

            # This is just so that the main program will have more response time
            # Not sure if needed actually
            all_groups.append(groups_outer)

        # Reset group areas
        db.group_area_reset()

        # Assign for all groups new group area ids

        for grp in all_groups:
            ids = [x[0] for x in grp]
            db.group_area(ids)

        db.close()

        if queue is not None:
            queue.put(len(all_groups))
            return

    if queue is not None:
        queue.put('')
