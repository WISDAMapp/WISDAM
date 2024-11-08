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
import json
import shapely

from db.dbHandler import DBHandler

from compare.utils import (CompareSighting, compare_list_header)
from app.model_views.compareViews import CompareListModel


def compare_searcher(db_path1: Path,
                     db_path2: Path,
                     user,
                     source1: list,
                     source2: list,
                     non_grouping=False) -> tuple[CompareListModel | None, str]:
    # Be aware that ids are not sorted after searching

    # load DB1
    db1 = DBHandler.from_path(db_path1, user)

    # load DB2
    db2 = DBHandler.from_path(db_path2, user)

    # read all sightings from DB1
    sights1 = db1.obj_load_all()
    sights1_list = []
    for idx, x in enumerate(sights1):
        if x['source'] in source1:
            geometry = shapely.geometry.shape(json.loads(x['geo2d']))

            if non_grouping:
                resight_set = 0
            else:
                resight_set = x['resight_set']

            new_sighting = CompareSighting(id_comp=x['id'], image=x['image'], img_path=x['img_path'],
                                           meta_type=x['meta_type'],
                                           object_type=x['object_type'],
                                           resight_set=resight_set,
                                           geometry=geometry,
                                           data=x['data'],
                                           data_env=x['data_env'])
            sights1_list.append(new_sighting)

    # read all sightings from DB2
    sights2 = db2.obj_load_all()
    sights2_list = []
    for idx, x in enumerate(sights2):
        if x['source'] in source2:
            geometry = shapely.geometry.shape(json.loads(x['geo2d']))

            if non_grouping:
                resight_set = 0
            else:
                resight_set = x['resight_set']

            new_sighting = CompareSighting(id_comp=x['id'], image=x['image'], img_path=x['img_path'],
                                           meta_type=x['meta_type'],
                                           object_type=x['object_type'],
                                           resight_set=resight_set,
                                           geometry=geometry,
                                           data=x['data'],
                                           data_env=x['data_env'])
            sights2_list.append(new_sighting)

    model_list = []

    # Run over sights1 list as long as there are elements
    # Compare sightings for position in same image and for resight sets
    while len(sights1_list) > 0:

        # Start object
        sight_start = sights1_list[0]
        resight_set_db1 = []

        # Start object is in a resight set ?
        if sight_start.resight_set > 0:
            resight_set_db1.append(sight_start.resight_set)

        # Check now if any sightings from db1  are somehow connected either over location or over resight sets
        groups_db1 = []
        for idx, sub_sights1 in enumerate(sights1_list):
            if sub_sights1.img_path == sight_start.img_path:

                # Check if this object is in the range for being a comparison.
                # Objects geometries need to overlap
                # For points we could continue using distance metric

                # if np.linalg.norm(np.array(sub_sights1.geometry) -
                #                  np.array(sight_start.geometry)) < dist_compare_search:
                if sight_start.geometry.intersects(sub_sights1.geometry):
                    # if it is in the range than check if this one is in a resight set
                    if sub_sights1.resight_set > 0:
                        resight_set_db1.append(sub_sights1.resight_set)

                    # If this sub sighting is not already in groups for sighting1 add it
                    if sub_sights1 not in groups_db1:
                        groups_db1.append(sub_sights1)

        # Check all sightings from db1 if they are in one of the groups now processed
        for idx, sub_sights1 in enumerate(sights1_list):
            if sub_sights1.resight_set in resight_set_db1:
                if sub_sights1 not in groups_db1:
                    groups_db1.append(sub_sights1)

        # Clear found sightings from list
        if groups_db1:
            for x_del in groups_db1:
                sights1_list.remove(x_del)

        # Check now if any sightings from db1  are somehow connected either over location or over resight sets to db2
        group_found_db2 = []
        resight_set_db2 = []
        for idx, sub_sights1 in enumerate(groups_db1):
            for idx2, sub_sights2 in enumerate(sights2_list):
                if sub_sights2.img_path == sub_sights1.img_path:
                    # if np.linalg.norm(np.array(sub_sights1.geometry) -
                    #                  np.array(sub_sights2.geometry)) < dist_compare_search:
                    if sub_sights2.geometry.intersects(sub_sights1.geometry):

                        if sub_sights2 not in group_found_db2:
                            group_found_db2.append(sub_sights2)

                        if sub_sights2.resight_set > 0:
                            resight_set_db2.append(sub_sights2.resight_set)

        # Check all sightings from db2 if they are in one of the groups now processed in db2
        for idx2, sub_sights2 in enumerate(sights2_list):
            if sub_sights2.resight_set in resight_set_db2:
                if sub_sights2 not in group_found_db2:
                    group_found_db2.append(sub_sights2)

        if group_found_db2:
            for x_del in group_found_db2:
                sights2_list.remove(x_del)

        flag_group_found = 'yes' if (len(resight_set_db1) > 0) or (len(resight_set_db2) > 0) else 'no'

        # If nothing is found in DB2 make them all single elements if not a resight set
        if len(group_found_db2) < 1 and len(resight_set_db1) < 1:

            resighting_groups1_done = []
            sub_ids = []
            for sub_groups in groups_db1:

                if sub_groups.resight_set > 0:
                    if sub_groups.resight_set not in resighting_groups1_done:
                        sub_ids = [x.id for x in groups_db1
                                   if x.resight_set == sub_groups.resight_set]
                        resighting_groups1_done.append(sub_groups.resight_set)
                else:
                    sub_ids = [sub_groups.id]

                if len(sub_ids) > 1:
                    flag_group_found = 'yes'
                else:
                    flag_group_found = 'no'

                model_list.append([sub_ids[0],  # First id of id list
                                   [x.object_type for x in groups_db1 if x.id in sub_ids],
                                   1,
                                   0,
                                   len(sub_ids),
                                   0,
                                   flag_group_found,
                                   [x.id for x in groups_db1 if x.id in sub_ids],
                                   [],
                                   0,
                                   [],
                                   [1 for x in groups_db1 if x.id in sub_ids],
                                   [],
                                   [x.resight_set for x in groups_db1 if x.id in sub_ids],
                                   [],
                                   [x.image for x in groups_db1 if x.id in sub_ids],
                                   [],
                                   [x.data for x in groups_db1 if x.id in sub_ids],
                                   [],
                                   [x.data_env for x in groups_db1 if x.id in sub_ids],
                                   []])

        else:

            model_list.append([groups_db1[0].id,
                               [x.object_type for x in groups_db1],
                               1,
                               0,
                               len(groups_db1),
                               len(group_found_db2),
                               flag_group_found,
                               [x.id for x in groups_db1],
                               [x.id for x in group_found_db2],
                               0,
                               [x.object_type for x in group_found_db2],
                               [1] * len(groups_db1),
                               [1] * len(group_found_db2),
                               [x.resight_set for x in groups_db1],
                               [x.resight_set for x in group_found_db2],
                               [x.image for x in groups_db1],
                               [x.image for x in group_found_db2],
                               [x.data for x in groups_db1],
                               [x.data for x in group_found_db2],
                               [x.data_env for x in groups_db1],
                               [x.data_env for x in group_found_db2]])

    # Now process all sightings of sights2_list
    while len(sights2_list) > 0:

        sight_start = sights2_list[0]
        resight_set_db2 = []

        if sight_start.resight_set > 0:
            resight_set_db2.append(sight_start.resight_set)

        groups_db2 = []
        for idx, sub_sights2 in enumerate(sights2_list):

            if sub_sights2.img_path == sight_start.img_path:
                # if np.linalg.norm(np.array(sub_sights2.geometry) -
                #                  np.array(sight_start.geometry)) < dist_compare_search:
                if sight_start.geometry.intersects(sub_sights2.geometry):

                    if sub_sights2.resight_set > 0:
                        resight_set_db2.append(sight_start.resight_set)

                    if sub_sights2 not in groups_db2:
                        groups_db2.append(sub_sights2)

        for idx, sub_sights2 in enumerate(sights2_list):
            if sub_sights2.resight_set in resight_set_db2:
                if sub_sights2 not in groups_db2:
                    groups_db2.append(sub_sights2)

        if groups_db2:
            for x_del in groups_db2:
                sights2_list.remove(x_del)

        resighting_groups2_done = []

        for sub_group in groups_db2:

            if sub_group.resight_set not in resighting_groups2_done:
                # if elements of this in a group than combine to one entry
                if sub_group.resight_set > 0:
                    sub_ids = [x.id for x in groups_db2
                               if x.resight_set == sub_group.resight_set]
                    resighting_groups2_done.append(sub_group.resight_set)
                else:
                    sub_ids = [sub_group.id]

                if len(sub_ids) > 1:
                    flag_group_found = 'yes'
                else:
                    flag_group_found = 'no'

                model_list.append([sub_ids[0],
                                   [],
                                   2,
                                   0,
                                   0,
                                   len(sub_ids),
                                   flag_group_found,
                                   [],
                                   [x.id for x in groups_db2 if x.id in sub_ids],
                                   0,
                                   [x.object_type for x in groups_db2 if x.id in sub_ids],
                                   [],
                                   [1 for x in groups_db2 if x.id in sub_ids],
                                   [],
                                   [x.resight_set for x in groups_db2 if x.id in sub_ids],
                                   [],
                                   [x.image for x in groups_db2 if x.id in sub_ids],
                                   [],
                                   [x.data for x in groups_db2 if x.id in sub_ids],
                                   [],
                                   [x.data_env for x in groups_db2 if x.id in sub_ids]
                                   ])

    # Assign Model to QTable View

    model = None
    if model_list:
        model = CompareListModel(model_list, compare_list_header)
        text = 'Results loaded: ' + str(len(model_list)) + ' differences found'
    else:
        text = 'No differences found'

    return model, text


def compare_searcher_single_db_ai_to_ai_review(db: DBHandler):
    sights1 = db.load_ai_detections_compare()

    model_list = []
    model = []
    for idx, x in enumerate(sights1):
        if x['active'] or x['imported']:
            if (x['object_type'] != x['object_type_orig']) or (x['data'] != x['data_orig']):
                model_list.append([x['id'],
                                   [x['object_type']],
                                   'ai',
                                   0,
                                   1,
                                   0,
                                   0,
                                   [x['id']],
                                   [],
                                   0,
                                   [x['object_type_orig']],
                                   [1],
                                   [1],
                                   [0],
                                   [0],
                                   [x['image']],
                                   [x['image']],
                                   [x['data']],
                                   [''],
                                   [''],
                                   ['']])

    if model_list:
        model = CompareListModel(model_list, compare_list_header)
        text = 'Results loaded: ' + str(len(model_list)) + ' differences found'
    else:
        text = 'No differences found'

    return model, text


