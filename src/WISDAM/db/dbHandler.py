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


from __future__ import annotations
from typing import TypeAlias
import json
import sqlite3
from pathlib import Path
from sqlite3 import dbapi2

from db.createDb import create
from db.createDb import init

from WISDAM import software_version
from core_interface.wisdamIMAGE import WISDAMImage

from WISDAMcore.image.base_class import ImageType

JSON: TypeAlias = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class DBHandler:
    """ This class contains all DB manipulation and readings for WISDAM
    The base DB system used is SQLITE with the spatialite mod as extension provided under /bin/spatialite***
    This class is designed to be clean and QT free so that it can be used or implemented to other modules
    without dependencies"""

    def __init__(self, path: Path, user: str = ''):
        self.con: dbapi2.Connection = dbapi2.connect(path.as_posix())
        init(self.con)
        self.con.row_factory = dict_factory
        self.path: Path = path
        self.user = user

    @classmethod
    def from_path(cls, db_path: Path, user: str = '') -> None | DBHandler:
        """Create DBHandler from existing path
        :param db_path: Path of database
        :param user: Current user
        :return: True if successfully loaded otherwise False"""
        try:
            db = cls(db_path, user)
            return db
        except sqlite3.Error:
            return None

    def close(self):
        self.con.close()

    @classmethod
    def create(cls, db_path: Path, user, time_created, config: dict) -> None | DBHandler:

        try:
            create(db_path.as_posix())
            db = cls(db_path, user)

            query = r"""Insert into configuration 
                (created_by,date_created, version, configuration)
                Values
                (:user,:time_created, :version, :configuration)"""
            db.con.execute(query, {'user': user, 'time_created': time_created,
                                   'version': software_version, 'configuration': json.dumps(config)})
            db.con.commit()
            return db

        except sqlite3.Error:
            return None

    @property
    def version(self) -> str:
        """Get version of WISDAM database
        :return: WISDAM DB version"""
        query = r"""select version from configuration"""
        data = self.con.execute(query).fetchone()
        return data

    @property
    def created_by(self) -> str:
        """Get the user string who created that DB
        :return: User who created DB"""
        query = r"""select crated_by from configuration"""
        data = self.con.execute(query).fetchone()
        return data

    # ------------------------------------------------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------------------------------------------------
    @property
    def last_image(self) -> int:
        """Get the last image opened
        :return: ID of last image"""
        query = r"""select last_image from configuration
                    WHERE
                id = 1"""
        data = self.con.execute(query).fetchone()
        if data:
            return data['last_image']
        return 0

    @last_image.setter
    def last_image(self, image_id: int):
        """Sets the last image in the database
        :param image_id: Image ID"""
        query = r"""UPDATE configuration
                SET last_image = :image
                    WHERE
                id = 1"""
        self.con.execute(query, {'image': int(image_id)})
        self.con.commit()

    @property
    def color_scheme(self):
        """Get color scheme from database
        :return: Color scheme"""

        query = r"""select color_scheme from configuration"""
        data = self.con.execute(query).fetchone()
        return data['color_scheme']

    @color_scheme.setter
    def color_scheme(self, data: dict):

        color_str = json.dumps(data)
        query = r"""Update configuration
        Set 
        color_scheme = :data"""
        self.con.execute(query, {'data': color_str})
        self.con.commit()

    @property
    def object_types(self):
        """Get object types from database
        :return: Color scheme"""

        query = r"""select object_types from configuration"""
        data = self.con.execute(query).fetchone()
        return data[0]

    def load_config(self):
        query = r"""select * from configuration"""
        data = self.con.execute(query).fetchone()
        return data

    def store_object_types(self, object_types: dict, config_name: str | None = None):
        config = self.load_config()
        config = json.loads(config['configuration'])

        if config_name is None:
            config_name = list(config['meta_config'].keys())[0]

        config['meta_config'][config_name]['object_types'] = object_types

        query = r"""Update configuration
                    Set 
                    configuration = :configuration"""
        self.con.execute(query, {'configuration': json.dumps(config)})
        self.con.commit()

    def add_object_types(self, object_types_to_add, config_name: str | None = None):
        config = self.load_config()
        config = json.loads(config['configuration'])

        if config_name is None:
            config_name = list(config['meta_config'].keys())[0]
        object_types = config['meta_config'][config_name]['object_types']
        for obj_type in object_types_to_add:
            if obj_type not in object_types.keys():
                object_types[obj_type] = []
        query = r"""Update configuration
                    Set 
                    configuration = :configuration"""
        self.con.execute(query, {'configuration': json.dumps(config)})
        self.con.commit()

    @property
    def mapper(self) -> dict | None:

        query = r"""select mapper from configuration"""
        data = self.con.execute(query).fetchone()
        if data:
            return json.loads(data)
        return None

    @mapper.setter
    def mapper(self, mapper_dict: dict | None):

        mapper_store = None
        if mapper_dict:
            mapper_store = json.dumps(mapper_dict)
        query = r"""Update configuration
        Set 
        mapper = :mapper"""
        self.con.execute(query, {'mapper': mapper_store})
        self.con.commit()

    # Not really a config but It's used to be heavy calculation, so we process only if images imported
    # and otherwise load from here
    @property
    def area_gsd(self) -> tuple[float, float]:
        """Get the area and gsd from config for image union
        :return: tuple(area,gsd)"""
        query = r"""select area, gsd from configuration"""
        data = self.con.execute(query).fetchone()
        return data["area"], data["gsd"]

    def set_area_gsd(self, union_area, img_gsd):
        """Sets the last image in the database"""
        query = r"""UPDATE configuration
                SET area = :area,
                    gsd = :gsd
                    WHERE
                id = 1"""
        self.con.execute(query, {'area': union_area, 'gsd': img_gsd})
        self.con.commit()

    # -------------------------------------------------------------------------
    # Image
    # -------------------------------------------------------------------------
    def update_path(self, path1, path2):
        query = r"""UPDATE
                        images
                    SET
                        path = REPLACE(path,:path_to_replace,:path_replace)"""
        self.con.execute(query, {'path_to_replace': path1, 'path_replace': path2})
        self.con.commit()

    def set_image_as_inspected(self, image_id):
        query = r"""UPDATE images
                SET inspected = 1
                    WHERE
                id = :image"""
        self.con.execute(query, {'image': int(image_id)})
        self.con.commit()

    def get_image_id_by_folder(self, folder: Path) -> list[int] | None:

        query = r"""SELECT id, path from images"""
        data = self.con.execute(query, {'path': folder.as_posix()}).fetchall()
        if data:
            return [x['id'] for x in data if Path(x['path']).parent.as_posix() == folder.as_posix()]
        else:
            return None

    def delete_images(self, image_id_list: list):

        self.con.execute(f"""DELETE FROM objects 
                        WHERE
                            image in ({','.join([str(x) for x in image_id_list])})""")
        self.con.commit()

        self.con.execute(f"""DELETE FROM ai_detections 
                        WHERE
                            image in ({','.join([str(x) for x in image_id_list])})""")
        self.con.commit()

        query = f"""Update configuration set last_image = 
                   (select min(id) from images where id not in ({','.join([str(x) for x in image_id_list])}) )"""
        self.con.execute(query)
        self.con.commit()

        self.con.execute(f"""DELETE FROM images
                            WHERE
                            id in ({','.join([str(x) for x in image_id_list])})""")
        self.con.commit()

        query = """Update objects
                    set
                    resight_set=0
                    where id in (
                    SELECT id  FROM objects
                    group by resight_set
                    having count(resight_set)==1)"""

        self.con.execute(query)
        self.con.commit()

    def store_image(self, image: WISDAMImage, user: str | None = None) -> int:

        if user is None:
            user = self.user

        name = image.path.name
        path = image.path.as_posix()
        datetime = image.datetime
        width = image.width
        height = image.height
        importer = image.importer
        flight_ref = image.flight_ref
        transect = image.transect
        group_image = image.group_image
        block = image.block
        meta_image = json.dumps(image.meta_image)
        meta_user = json.dumps(image.meta_user)

        type_image = ImageType.Unknown.value
        math_model = None
        if image.image_model is not None:
            type_image = image.image_model.type.value
            math_model = json.dumps(image.image_model.param_dict)

        position_json = None
        if image.is_geo_referenced:
            position_json = image.position_wgs84_geojson
            position_json['crs'] = {"type": "name", "properties": {"name": "EPSG:4979"}}

        query = r"""Insert into images 
        (type, name ,path , datetime ,width, height, user, importer, meta_user, meta_image,
        transect,block,flight_ref,group_image,
         math_model, position)
        Values
        (:type,:name,:path,:datetime,:width,:height,:user,:importer,:meta_user,:meta_image,
        :transect,:block,:flight_ref,:group_image,
         :math_model, GeomFromGeoJSON(:position))"""

        data = self.con.execute(query, {'type': type_image, 'name': name, 'path': path, 'datetime': datetime,
                                        'width': width, 'height': height, 'user': user, 'importer': importer,
                                        'meta_user': meta_user, 'meta_image': meta_image,
                                        'math_model': math_model,
                                        'group_image': group_image, 'flight_ref': flight_ref,
                                        'transect': transect, 'block': block,
                                        'position': json.dumps(position_json)})
        self.con.commit()

        return data.lastrowid

    def store_image_all_fields_list(self, image: WISDAMImage, user: str | None = None, data_env=None,
                                    gsd: float = 0.0, area: float = 0.0, inspected: int = 0,
                                    center_json: dict | None = None, footprint_json: dict | None = None) -> dict:

        if footprint_json is not None:
            footprint_json['crs'] = {"type": "name", "properties": {"name": "EPSG:4979"}}
        if center_json is not None:
            center_json['crs'] = {"type": "name", "properties": {"name": "EPSG:4979"}}

        if user is None:
            user = self.user

        name = image.path.name
        path = image.path.as_posix()
        datetime = image.datetime
        width = image.width
        height = image.height
        importer = image.importer
        flight_ref = image.flight_ref
        transect = image.transect
        group_image = image.group_image
        block = image.block
        meta_image = json.dumps(image.meta_image)
        meta_user = json.dumps(image.meta_user)

        type_image = ImageType.Unknown.value
        math_model = None
        if image.image_model is not None:
            type_image = image.image_model.type.value
            math_model = json.dumps(image.image_model.param_dict)

        position_json = None
        if image.is_geo_referenced:
            position_json = image.position_wgs84_geojson
            position_json['crs'] = {"type": "name", "properties": {"name": "EPSG:4979"}}

        env_data = None
        if data_env is not None:
            env_data = json.dumps(data_env)

        return {'type': type_image, 'name': name, 'path': path, 'datetime': datetime,
                'width': width, 'height': height, 'user': user, 'importer': importer,
                'meta_user': meta_user, 'meta_image': meta_image,
                'math_model': math_model,
                'group_image': group_image, 'inspected': inspected,
                'flight_ref': flight_ref,
                'transect': transect, 'block': block,
                'position': json.dumps(position_json),
                'data_env': env_data,
                'gsd': gsd, 'area': area,
                'center': json.dumps(center_json),
                'footprint': json.dumps(footprint_json)
                }

    def image_create_multi(self, images_dict: dict[Path | None, dict]):
        # {'image': WISDAMimage, 'gsd': float, 'area': float, 'center_json': json, 'footprint_json': json}

        query_list = []
        for key, value in images_dict.items():
            image: WISDAMImage = value['image']
            gsd: float = value['gsd']
            area: float = value['area']
            center_json: JSON = value['center_json']
            footprint_json: JSON = value['footprint_json']

            name = image.path.name
            path = image.path.as_posix()
            datetime = image.datetime
            width = image.width
            height = image.height
            importer = image.importer

            flight_ref = image.flight_ref
            transect = image.transect
            block = image.block
            group_image = image.group_image

            meta_image = json.dumps(image.meta_image) if image.meta_image is not None else None
            meta_user = json.dumps(image.meta_user) if image.meta_user is not None else None

            type_image = ImageType.Unknown.value
            param_dict = None
            if image.image_model is not None:
                type_image = image.image_model.type.value
                param_dict = json.dumps(image.image_model.param_dict)

            position_json = None
            if image.is_geo_referenced:
                position_json = image.position_wgs84_geojson
                position_json['crs'] = {"type": "name", "properties": {"name": "EPSG:4979"}}

            if footprint_json is not None:
                footprint_json['crs'] = {"type": "name", "properties": {"name": "EPSG:4979"}}

            if center_json is not None:
                center_json['crs'] = {"type": "name", "properties": {"name": "EPSG:4979"}}

            query_list.append({'type': type_image, 'name': name, 'path': path, 'datetime': datetime,
                               'width': width, 'height': height, 'user': self.user, 'importer': importer,
                               'group_image': group_image, 'flight_ref': flight_ref,
                               'transect': transect, 'block': block,
                               'math_model': param_dict, 'meta_user': meta_user, 'meta_image': meta_image,
                               'position': json.dumps(position_json), 'gsd': gsd, 'area': area,
                               'center': json.dumps(center_json),
                               'footprint': json.dumps(footprint_json), 'id': image.id})

        query = r"""Insert into images 
        (type, name ,path , datetime ,width, height, user, importer, meta_user, meta_image,
        transect,block,flight_ref,group_image,
         math_model, position, gsd, area, centerpoint, footprint)
        Values
        (:type,:name,:path,:datetime,:width,:height,:user,:importer,:meta_user,:meta_image,
        :transect,:block,:flight_ref,:group_image,
         :math_model, GeomFromGeoJSON(:position),
         :gsd,:area,GeomFromGeoJSON(:center),GeomFromGeoJSON(:footprint))"""

        self.con.executemany(query, query_list)
        self.con.commit()

    def image_create_multi_all_fields(self, image_dict: dict[Path | None, dict]):

        query_list = []
        for key, value in image_dict.items():
            image: WISDAMImage = value['image']
            gsd: float = value['gsd']
            area: float = value['area']
            center_json: JSON = value['center_json']
            footprint_json: JSON = value['footprint_json']
            data_env: dict = value['data_env']
            inspected: int = value['inspected']
            user: str = value['user']

            if footprint_json is not None:
                footprint_json['crs'] = {"type": "name", "properties": {"name": "EPSG:4979"}}
            if center_json is not None:
                center_json['crs'] = {"type": "name", "properties": {"name": "EPSG:4979"}}

            if user is None:
                user = self.user

            name = image.path.name
            path = image.path.as_posix()
            datetime = image.datetime
            width = image.width
            height = image.height
            importer = image.importer
            flight_ref = image.flight_ref
            transect = image.transect
            group_image = image.group_image
            block = image.block
            meta_image = json.dumps(image.meta_image)
            meta_user = json.dumps(image.meta_user)

            type_image = ImageType.Unknown.value
            math_model = None
            if image.image_model is not None:
                type_image = image.image_model.type.value
                math_model = json.dumps(image.image_model.param_dict)

            position_json = None
            if image.is_geo_referenced:
                position_json = image.position_wgs84_geojson
                position_json['crs'] = {"type": "name", "properties": {"name": "EPSG:4979"}}

            env_data = None
            if data_env is not None:
                env_data = json.dumps(data_env)

            query_list.append({'type': type_image, 'name': name, 'path': path, 'datetime': datetime,
                               'width': width, 'height': height, 'user': user, 'importer': importer,
                               'meta_user': meta_user, 'meta_image': meta_image,
                               'math_model': math_model,
                               'group_image': group_image, 'inspected': inspected,
                               'flight_ref': flight_ref,
                               'transect': transect, 'block': block,
                               'position': json.dumps(position_json),
                               'data_env': env_data,
                               'gsd': gsd, 'area': area,
                               'center': json.dumps(center_json),
                               'footprint': json.dumps(footprint_json)
                               })

        query = r"""Insert into images 
        (type, name ,path , datetime ,width, height, user, importer, meta_user, meta_image,
        transect,block,flight_ref,group_image,inspected,
         math_model, position, data_env, gsd, area, centerpoint, footprint)
        Values
        (:type,:name,:path,:datetime,:width,:height,:user,:importer,:meta_user,:meta_image,
        :transect,:block,:flight_ref,:group_image,:inspected,
         :math_model, GeomFromGeoJSON(:position), :data_env,
         :gsd,:area,GeomFromGeoJSON(:center),GeomFromGeoJSON(:footprint))"""

        self.con.executemany(query, query_list)
        self.con.commit()

    def store_image_all_fields(self, image: WISDAMImage, user: str | None = None, data_env=None,
                               gsd: float = 0.0, area: float = 0.0, inspected: int = 0,
                               center_json: dict | None = None, footprint_json: dict | None = None) -> int:

        if footprint_json is not None:
            footprint_json['crs'] = {"type": "name", "properties": {"name": "EPSG:4979"}}
        if center_json is not None:
            center_json['crs'] = {"type": "name", "properties": {"name": "EPSG:4979"}}

        if user is None:
            user = self.user

        name = image.path.name
        path = image.path.as_posix()
        datetime = image.datetime
        width = image.width
        height = image.height
        importer = image.importer
        flight_ref = image.flight_ref
        transect = image.transect
        group_image = image.group_image
        block = image.block
        meta_image = json.dumps(image.meta_image)
        meta_user = json.dumps(image.meta_user)

        type_image = ImageType.Unknown.value
        math_model = None
        if image.image_model is not None:
            type_image = image.image_model.type.value
            math_model = json.dumps(image.image_model.param_dict)

        position_json = None
        if image.is_geo_referenced:
            position_json = image.position_wgs84_geojson
            position_json['crs'] = {"type": "name", "properties": {"name": "EPSG:4979"}}

        env_data = None
        if data_env is not None:
            env_data = json.dumps(data_env)

        query = r"""Insert into images 
        (type, name ,path , datetime ,width, height, user, importer, meta_user, meta_image,
        transect,block,flight_ref,group_image,inspected,
         math_model, position, data_env, gsd, area, centerpoint, footprint)
        Values
        (:type,:name,:path,:datetime,:width,:height,:user,:importer,:meta_user,:meta_image,
        :transect,:block,:flight_ref,:group_image,:inspected,
         :math_model, GeomFromGeoJSON(:position), :data_env,
         :gsd,:area,GeomFromGeoJSON(:center),GeomFromGeoJSON(:footprint))"""

        data = self.con.execute(query, {'type': type_image, 'name': name, 'path': path, 'datetime': datetime,
                                        'width': width, 'height': height, 'user': user, 'importer': importer,
                                        'meta_user': meta_user, 'meta_image': meta_image,
                                        'math_model': math_model,
                                        'group_image': group_image, 'inspected': inspected,
                                        'flight_ref': flight_ref,
                                        'transect': transect, 'block': block,
                                        'position': json.dumps(position_json),
                                        'data_env': env_data,
                                        'gsd': gsd, 'area': area,
                                        'center': json.dumps(center_json),
                                        'footprint': json.dumps(footprint_json)
                                        })
        self.con.commit()

        return data.lastrowid

    def image_creation_update_multi(self, images_dict: dict[Path | None, dict]):
        # {'image': WISDAMimage, 'gsd': float, 'area': float, 'center_json': json, 'footprint_json': json}

        query_list = []
        for key, value in images_dict.items():
            image: WISDAMImage = value['image']
            gsd: float = value['gsd']
            area: float = value['area']
            center_json: JSON = value['center_json']
            footprint_json: JSON = value['footprint_json']

            name = image.path.name
            path = image.path.as_posix()
            datetime = image.datetime
            width = image.width
            height = image.height
            importer = image.importer

            flight_ref = image.flight_ref
            transect = image.transect
            block = image.block
            group_image = image.group_image

            meta_image = json.dumps(image.meta_image) if image.meta_image is not None else None
            meta_user = json.dumps(image.meta_user) if image.meta_user is not None else None

            type_image = ImageType.Unknown.value
            param_dict = None
            if image.image_model is not None:
                type_image = image.image_model.type.value
                param_dict = json.dumps(image.image_model.param_dict)

            position_json = None
            if image.is_geo_referenced:
                position_json = image.position_wgs84_geojson
                position_json['crs'] = {"type": "name", "properties": {"name": "EPSG:4979"}}

            if footprint_json is not None:
                footprint_json['crs'] = {"type": "name", "properties": {"name": "EPSG:4979"}}

            if center_json is not None:
                center_json['crs'] = {"type": "name", "properties": {"name": "EPSG:4979"}}

            query_list.append({'type': type_image, 'name': name, 'path': path, 'datetime': datetime,
                               'width': width, 'height': height, 'user': self.user, 'importer': importer,
                               'group_image': group_image, 'flight_ref': flight_ref,
                               'transect': transect, 'block': block,
                               'math_model': param_dict, 'meta_user': meta_user, 'meta_image': meta_image,
                               'position': json.dumps(position_json), 'gsd': gsd, 'area': area,
                               'center': json.dumps(center_json),
                               'footprint': json.dumps(footprint_json), 'id': image.id})

        query = r"""Update images
        Set 
        type=:type,
        name=:name,
        path=:path,
        datetime=:datetime ,
        width=:width ,
        height=:height ,
        user=:user ,
        importer=:importer ,
        meta_user=:meta_user ,
        meta_image=:meta_image ,
        group_image=:group_image,
        flight_ref=:flight_ref,
        transect=:transect,
        block=:block,
        math_model=:math_model,
        position=GeomFromGeoJSON(:position),
        gsd = :gsd,
        area =:area,
        centerpoint = GeomFromGeoJSON(:center),
        footprint = GeomFromGeoJSON(:footprint)
        where id=:id"""

        self.con.executemany(query, query_list)
        self.con.commit()

    def image_update(self, image: WISDAMImage):

        name = image.path.name
        path = image.path.as_posix()
        datetime = image.datetime
        width = image.width
        height = image.height
        importer = image.importer

        flight_ref = image.flight_ref
        transect = image.transect
        block = image.block
        group_image = image.group_image

        meta_image = json.dumps(image.meta_image)
        meta_user = json.dumps(image.meta_user)

        type_image = ImageType.Unknown.value
        param_dict = None
        if image.image_model is not None:
            type_image = image.image_model.type.value
            param_dict = json.dumps(image.image_model.param_dict)

        position_json = None
        if image.is_geo_referenced:
            position_json = image.position_wgs84_geojson
            position_json['crs'] = {"type": "name", "properties": {"name": "EPSG:4979"}}

        query = r"""Update images
        Set 
        type=:type,
        name=:name,
        path=:path,
        datetime=:datetime ,
        width=:width ,
        height=:height ,
        user=:user ,
        importer=:importer ,
        meta_user=:meta_user ,
        meta_image=:meta_image ,
        group_image=:group_image,
        flight_ref=:flight_ref,
        transect=:transect,
        block=:block,
        math_model=:math_model,
        position=GeomFromGeoJSON(:position)
        where id=:id"""

        self.con.execute(query, {'type': type_image, 'name': name, 'path': path, 'datetime': datetime,
                                 'width': width, 'height': height, 'user': self.user, 'importer': importer,
                                 'group_image': group_image, 'flight_ref': flight_ref,
                                 'transect': transect, 'block': block,
                                 'math_model': param_dict, 'meta_user': meta_user, 'meta_image': meta_image,
                                 'position': json.dumps(position_json), 'id': image.id})
        self.con.commit()

    def image_update_georef(self, image: WISDAMImage,
                            gsd: float, area: float,
                            footprint_json: dict | None,
                            center_json: dict | None):
        type_image = ImageType.Unknown.value
        math_model = None
        if image.image_model is not None:
            type_image = image.image_model.type.value
            math_model = json.dumps(image.image_model.param_dict)
        position_json = None
        if image.is_geo_referenced:
            position_json = image.position_wgs84_geojson
            position_json['crs'] = {"type": "name", "properties": {"name": "EPSG:4979"}}

        if footprint_json is not None:
            footprint_json['crs'] = {"type": "name", "properties": {"name": "EPSG:4979"}}
        if center_json is not None:
            center_json['crs'] = {"type": "name", "properties": {"name": "EPSG:4979"}}

        query = r"""Update images 
        SET
        gsd = :gsd,
        area =:area,
        type=:type,
        math_model = :math_model,
        position=GeomFromGeoJSON(:position),
        centerpoint = GeomFromGeoJSON(:center),
        footprint = GeomFromGeoJSON(:footprint)
        where id=:id"""

        self.con.execute(query, {'id': image.id, 'gsd': gsd, 'area': area,
                                 'type': type_image,
                                 'math_model': math_model,
                                 'position': json.dumps(position_json),
                                 'center': json.dumps(center_json),
                                 'footprint': json.dumps(footprint_json)})
        self.con.commit()

    def image_update_georef_multi(self, update_list: dict[int, dict]):

        # {"image_id": image.id, "gsd": gsd, "area": area,
        # "center_json": center, "footprint_json": footprint})

        rows = []
        for key, value in update_list.items():

            if value['footprint_json'] is not None:
                value['footprint_json']['crs'] = {"type": "name", "properties": {"name": "EPSG:4979"}}
            if value['center_json'] is not None:
                value['center_json']['crs'] = {"type": "name", "properties": {"name": "EPSG:4979"}}

            rows.append({'id': key, 'gsd': value['gsd'], 'area': value['area'],
                         'center': json.dumps(value['center_json']),
                         'footprint': json.dumps(value['footprint_json'])})

        query = r"""Update images 
        SET
        gsd = :gsd,
        area =:area,
        centerpoint = GeomFromGeoJSON(:center),
        footprint = GeomFromGeoJSON(:footprint)
        where id=:id"""

        self.con.executemany(query, rows)
        self.con.commit()

    def image_store_georef(self, image_id: int, gsd: float, area: float,
                           center_json: dict | None, footprint_json: dict | None):

        if footprint_json is not None:
            footprint_json['crs'] = {"type": "name", "properties": {"name": "EPSG:4979"}}
        if center_json is not None:
            center_json['crs'] = {"type": "name", "properties": {"name": "EPSG:4979"}}

        query = r"""Update images 
        SET
        gsd = :gsd,
        area =:area,
        centerpoint = GeomFromGeoJSON(:center),
        footprint = GeomFromGeoJSON(:footprint)
        where id=:id"""

        self.con.execute(query, {'id': image_id, 'gsd': gsd, 'area': area,
                                 'center': json.dumps(center_json),
                                 'footprint': json.dumps(footprint_json)})
        self.con.commit()

    def load_images_list(self):
        query = r""" select images.*, Count(objects.image) as s_count, 
                asgeojson(images.footprint) as geom,
                asgeojson(images.position) as position_json from images
                left join objects on images.id = objects.image
                group by images.id
                order by images.id"""
        data = self.con.execute(query).fetchall()
        return data

    def load_image_export(self) -> list[dict]:
        query = r"""SELECT *, ASGeoJson(footprint) as geom, ST_X(position) as x, ST_Y(position) as y, ST_Z(position) 
        as z from images """
        data = self.con.execute(query).fetchall()
        return data

    def load_image_center(self, image_id) -> tuple | None:
        query = r"""SELECT ST_X(position) as x, ST_Y(position) as y, ST_X(ST_CENTROID(footprint)) as x_footprint,
         ST_Y(ST_CENTROID(footprint)) as y_footprint from images where id=:id"""
        data = self.con.execute(query, {'id': image_id}).fetchone()
        if data:
            if data['x_footprint']:
                return data['x_footprint'], data['y_footprint']
            elif data['x']:
                return data['x'], data['y']
        else:
            return None

    def load_image(self, image_id) -> dict | None:
        query = r"""SELECT *, ASGeoJson(position) as position_json, ASGeoJson(centerpoint) as center_point_json 
                    from images where id=:id"""
        data = self.con.execute(query, {'id': image_id}).fetchone()
        return data

    def load_image_by_path(self, path: Path) -> dict | None:
        query = r"""SELECT *, ASGeoJson(position) as position_json from images where path=:path"""
        data = self.con.execute(query, {'path': path.as_posix()}).fetchone()
        if data:
            return data
        else:
            return None

    def load_image_id(self, path: Path) -> int | None:
        query = r"""SELECT id from images where path=:path"""
        data = self.con.execute(query, {'path': path.as_posix()}).fetchone()
        if data:
            return data['id']
        else:
            return None

    def load_image_id_path_parts(self, path: str) -> list | None:
        query = r"""SELECT id from images where path LIKE :path"""
        data = self.con.execute(query, {'path': path}).fetchall()
        if data:
            return [x['id'] for x in data]
        else:
            return None

    def get_next_images_group(self):
        query = r"""select max(group_image) as max_id from images"""
        data = self.con.execute(query).fetchone()
        return data['max_id']

    def set_group_images(self, id_list, group_index):
        query = f"""Update images SET group_image=:group_index where id in ({','.join([str(x) for x in id_list])})"""

        self.con.execute(query, {'group_index': group_index})
        self.con.commit()

    def get_cropped_image_ai(self, ai_detection_id: int):
        query = r"""select image_detection from ai_detections
                        WHERE
                    id = :id"""
        data = self.con.execute(query, {'id': ai_detection_id}).fetchone()
        return data

    def get_cropped_image(self, object_id: int):
        query = r"""select cropped_image from objects
                        WHERE
                    id = :id"""
        data = self.con.execute(query, {'id': object_id}).fetchone()
        return data

    def get_col_types(self, column: str):
        query = r"""PRAGMA table_info(:column)"""
        data = self.con.execute(query, {':column)': column}).fetchall()
        return data

    def load_geometry_overlap(self, image_id: int):
        query = r"""SELECT objects.id as id, objects.image as image_id,objects.data as data,
        objects.object_type as object_type, objects.meta_type as meta_type,
        objects.resight_set as resight_set,
        objects.group_area as group_area,
        objects.reviewed as reviewed, objects.source as source,
        asgeojson(objects.geom3d) AS geom,
        X(objects.geom3d) as x, Y(objects.geom3d) as y, Z(objects.geom3d) as z, objects.cropped_image as image, 
        1 as projection
        FROM objects JOIN images
        where images.id=:id and intersects(images.footprint,objects.geom3d)  
        and not objects.image = :id and objects.geom3d not NULL  and images.footprint not NULL"""

        data = self.con.execute(query, {'id': image_id}).fetchall()
        return data

    def store_image_environment_data(self, data: dict, image_id: int):

        env_data = None
        if data:
            env_data = json.dumps(data)

        query = r"""Update images
        Set 
          data_env = :data
        where id=:id"""
        self.con.execute(query, {'data': env_data, 'id': image_id})
        self.con.commit()

    def load_image_environment_data(self, image_id: int) -> dict | None:
        query = r"""Select data_env from images
        where id=:id"""
        data = self.con.execute(query, {'id': image_id}).fetchone()
        if data is not None:
            if data["data_env"]:
                return json.loads(data["data_env"])
        return None

    def update_multiple_image_environment_data(self, data: dict | None, image_id_list: list):

        env_data = None
        if data:
            env_data = json.dumps(data)

        query = f"""Update images
        Set 
          data_env = :data
        where id in ({','.join([str(x) for x in image_id_list])})"""
        self.con.execute(query, {'data': env_data})
        self.con.commit()

    def update_image_meta(self, image_id_list: list[int], flight_ref: str = '', transect: str = '', block: str = '',
                          meta_user: dict | None = None, update_all: bool = False):
        commands = []
        if flight_ref or transect or block or meta_user or update_all:
            if flight_ref or update_all:
                commands.append("'flight_ref'= :flight_ref")
            if transect or update_all:
                commands.append("'transect'= :transect")
            if block or update_all:
                commands.append("'block'= :block")
            if meta_user or update_all:
                commands.append("'meta_user'= :meta_user")

            query = f"""Update images
            Set 
              {','.join(commands)}
              where id in ({','.join([str(x) for x in image_id_list])})"""
            self.con.execute(query, {'meta_user': json.dumps(meta_user), 'flight_ref': flight_ref,
                                     'transect': transect, 'block': block})
            self.con.commit()

    # -------------------------------------------------------------------------
    # Objects
    # -------------------------------------------------------------------------

    def obj_exists(self, obj_id: int):
        query = r"""select id from objects where id=:id"""
        data = self.con.execute(query, {'id': obj_id}).fetchone()
        return data

    def obj_delete(self, object_id: int):
        # GET IMAGE ID for IMAGE NAME in SFM DB
        self.con.execute(r'''DELETE FROM objects WHERE id = :id ''', {'id': object_id})
        self.con.commit()

    def load_geometry(self, image_id: int):
        query = r"""SELECT id, image as image_id,data as data,object_type as object_type,resight_set as resight_set,
         reviewed as reviewed, source as source, group_area as group_area,
         meta_type as meta_type, asgeojson(geom2d) AS geom, X(geom2d) as x, Y(geom2d) AS y, 
         cropped_image as image, 0 as projection  
         FROM objects
         Where image = :id """

        data = self.con.execute(query, {'id': image_id}).fetchall()
        return data

    def obj_load_for_ai_import_no_cropped_image(self, flag_first_certain: bool = False):
        query = r"""select  objects.image, asgeojson(objects.geom2d) as geo2d  from objects"""
        data = self.con.execute(query).fetchall()

        return data

    def obj_load_all(self, flag_first_certain: bool = False):
        query = r"""select images.path as img_path, images.name as image_name, images.id as image_id,
                    images.data_env as image_data_env, images.datetime as datetime, images.transect as transect,
                    images.block as block, images.group_image as group_image, 
                    objects.*, asgeojson(objects.geom3d) as geo,
                    asgeojson(objects.geom2d) as geo2d  from objects
                    join images where images.id = objects.image"""
        data = self.con.execute(query).fetchall()

        if flag_first_certain:
            data_first_certain = []
            for row in data:
                if row['data']:
                    json_data = json.loads(row['data'])
                    if json_data.get("firstcertain", '') == 'yes':
                        data_first_certain.append(row)

            return data_first_certain

        return data

    def load_objects_all_sort_by_group(self, order_value='id'):
        query = f"""select images.path as img_path, images.name as image_name, images.math_model as math_model, 
                    images.data_env as data_env, images.datetime as datetime,images.math_model as math_model, objects.*,
                    asgeojson(objects.geom3d) as geo,
                    asgeojson(objects.geom2d) as geo2d  from objects
                    join images where images.id = objects.image
                    order by objects.{order_value}"""

        data = self.con.execute(query).fetchall()
        return data

    def obj_load_from_image_ids(self, image_id_list: list):

        query = f"""SELECT objects.id,image, data, images.data_env from objects join images 
                    where images.id = objects.image and images.id in ({','.join([str(x) for x in image_id_list])}) """

        data = self.con.execute(query).fetchall()
        return data

    def load_objects_single_object(self, object_id: int):
        query = r"""select images.path as img_path, images.name as name,
                images.datetime as datetime, images.math_model as math_model, objects.*,
                asgeojson(objects.geom3d) as geo, 
                asgeojson(objects.geom2d) as geo2d  from objects
                join images where images.id = objects.image AND objects.id=:id"""
        data = self.con.execute(query, {'id': object_id}).fetchone()
        return data

    def load_objects_single(self, object_id: int):
        query = r"""SELECT objects.*, images.data_env as data_env_image from objects 
                    JOIN
                    images
                    WHERE
                    objects.image = images.id and objects.id=:id"""
        data = self.con.execute(query, {'id': object_id}).fetchone()
        return data

    def set_active(self, active, obj_id):
        query = "Update objects SET active = :active where id=:id"
        self.con.execute(query, {'active': active, 'id': obj_id})
        self.con.commit()

    def set_highlighted(self, highlighted, obj_id):
        query = "Update objects SET highlighted = :highlighted where id=:id"
        self.con.execute(query, {'highlighted': highlighted, 'id': obj_id})
        self.con.commit()

    def get_group_ids_by_object_ids(self, id_list):
        query = f"""Select resight_set from objects 
                    where id in ({','.join([str(x) for x in id_list])})"""

        data = self.con.execute(query).fetchall()
        group_ids = [x['resight_set'] for x in data]
        query = f"""Select id, resight_set, image, object_type, meta_type from objects 
                    where resight_set in ({','.join([str(x) for x in group_ids])})"""
        data = self.con.execute(query).fetchall()

        return data

    def get_next_resight_set(self):
        query = r"""select max(resight_set) as max_id from objects"""
        data = self.con.execute(query).fetchone()
        return data['max_id']

    def set_resight_set(self, id_list, group_index):
        query = f"""Update objects SET resight_set=:group_index 
                    where id in ({','.join([str(x) for x in id_list])})"""

        self.con.execute(query, {'group_index': group_index})
        self.con.commit()

    def set_resight_data(self, item_list):

        item_list = sorted(item_list)
        rows = self.load_objects_ids_sort_image(item_list)
        first_certain_found = False

        # Reset resight and first certainty for first element of group
        if rows[0]['data']:
            data = json.loads(rows[0]['data'])
        else:
            data = {'firstcertain': 'no'}

        data['resight'] = 'no'
        if data.get('certainty') == 'yes':
            first_certain_found = True
            data['firstcertain'] = 'yes'

        self.store_objects_meta_data_only(rows[0]['id'], json.dumps(data))

        for x in rows[1:]:
            if x['data']:
                data = json.loads(x['data'])
            else:
                data = {}
            data['resight'] = 'yes'
            if first_certain_found:
                data['firstcertain'] = 'no'
            else:
                if data.get('certainty') == 'yes':
                    first_certain_found = True
                    data['firstcertain'] = 'yes'
            self.store_objects_meta_data_only(x['id'], json.dumps(data))

    # TODO check json dumps
    def clear_resight_data(self, item_list):
        item_list = sorted(item_list)
        dum = self.load_objects_ids(item_list)
        for x in dum:
            if x['data']:
                data = json.loads(x['data'])
                if "resight" in data.keys():
                    data['resight'] = 'no'
                if "firstcertain" in data.keys():
                    data['firstcertain'] = 'no'

            else:
                data = {}
            self.store_objects_meta_data_only(x['id'], json.dumps(data))

    def create_object(self, image_id: int, geojson: dict, cropped_image, user: str | None = None):

        if user is None:
            user = self.user

        query = r"""Insert into objects 
            (geom2d, image, user, cropped_image)
            Values
            (SETSrid(GeomFromGEOJSON(:geometry),-1),:image,:user, :cropped_image)"""
        data = self.con.execute(query, {'geometry': json.dumps(geojson), 'image': image_id,
                                        'user': user, 'cropped_image': cropped_image})
        self.con.commit()

        return data.lastrowid

    def delete_object_mapping(self, obj_id: int):
        query = "Update objects SET geom3d=Null where id={id}"
        query = query.format(id=obj_id)
        self.con.execute(query)
        self.con.commit()

    def update_object_mapping(self, obj_id: int, geojson: dict, gsd: float, area: float):
        geojson['crs'] = {"type": "name", "properties": {"name": "EPSG:4979"}}
        query = r"""Update objects SET 
                 geom3d = GeomFromGeoJSON(:geometry),
                 gsd = :gsd,
                 area = :area
                 where id=:id"""

        self.con.execute(query, {'geometry': json.dumps(geojson), 'id': obj_id, 'gsd': gsd, 'area': area})
        self.con.commit()

    def update_object_mapping_multi(self, update_dict):
        query = r"""Update objects SET 
                 geom3d = GeomFromGeoJSON(:geom3d),
                 gsd = :gsd,
                 area = :area
                 where id=:id"""

        self.con.executemany(query, update_dict)
        self.con.commit()

    def load_objects_ids(self, id_list: list):

        query = f"""SELECT id,image, data,object_type, resight_set, source, user,
                      cropped_image FROM objects where id in ({','.join([str(x) for x in id_list])}) """

        data = self.con.execute(query).fetchall()
        return data

    def load_objects_ids_sort_image(self, id_list: list):
        query = f"""SELECT id,image, data,object_type, resight_set, source, user,
                  cropped_image FROM objects where id in ({','.join([str(x) for x in id_list])})
                  order by image"""

        data = self.con.execute(query).fetchall()
        return data

    def store_cropped_image(self, cropped_image, object_id):
        query = r"""Update objects
        Set 
        cropped_image = :image
        where id=:id"""
        self.con.execute(query, {'image': cropped_image, 'id': object_id})
        self.con.commit()

    def objects_create_all_multi(self, query_list: list[dict]):
        # {'image': WISDAMimage, 'gsd': float, 'area': float, 'center_json': json, 'footprint_json': json}

        query = r"""Insert into objects
        (geom2d, image, user, cropped_image, object_type, source, meta_type, data, reviewed, resight_set, data_env,
        group_area)
        Values
        (SETSrid(GeomFromGEOJSON(:geom2d),-1), :image, :user, :cropped_image, :object_type, :source, :meta_type, :data,
         :reviewed, :resight_set, :data_env, :group_area)"""

        self.con.executemany(query, query_list)
        self.con.commit()

    def objects_create_from_ai_multi(self, query_list: list[dict]):
        query = r"""Insert into objects
                    (image, user, cropped_image, object_type, source, data, geom2d, area, gsd, geom3d)
                    Values
                    (:image, :user, :cropped_image, :object_type, :source, :data, 
                    SETSrid(GeomFromGEOJSON(:geom2d),-1),:area, :gsd, GeomFromGEOJSON(:geom3d) )"""

        self.con.executemany(query, query_list)
        self.con.commit()

    def store_objects_meta(self, object_id, object_type, meta_type, data, reviewed=1, source=0):

        if source:

            query = r"""Update objects
            Set 
            object_type = :object_type,
            source = :source,
            meta_type = :meta_type,
            data = :data,
            reviewed = :reviewed
            where id=:id"""
        else:
            query = r"""Update objects
            Set 
            object_type = :object_type,
            meta_type = :meta_type,
            data = :data,
            reviewed = :reviewed
            where id=:id"""

        self.con.execute(query, {'object_type': object_type, 'meta_type': meta_type, 'data': data,
                                 'id': object_id, 'reviewed': reviewed, 'source': source})
        self.con.commit()

    def store_objects_meta_data_only(self, object_id, data):

        query = r"""Update objects
                    Set 
                    data = :data
                    where id=:id"""

        self.con.execute(query, {'data': data, 'id': object_id})
        self.con.commit()

    def store_objects_env_data(self, object_id: int, data: dict):

        env_data = None
        if data:
            env_data = json.dumps(data)

        query = r"""Update objects
                    Set 
                    data_env = :data
                    where id=:id"""

        self.con.execute(query, {'data': env_data, 'id': object_id})
        self.con.commit()

    def update_multiple_objects_environment_data(self, data: dict | None, image_id_list: list):

        env_data = None
        if data:
            env_data = json.dumps(data)

        query = f"""Update objects
        Set 
          data_env = :data
        where image in ({','.join([str(x) for x in image_id_list])})"""
        self.con.execute(query, {'data': env_data, 'id': image_id_list})
        self.con.commit()

    def store_ai_detection_objects(self, object_id, user, object_type, data_meta):
        query = r"""Update objects
                    Set 
                    source = 1,
                    user = :user,
                    object_type = :object_type,
                    data = :data_meta
                    where id=:id"""
        self.con.execute(query, {'id': object_id, 'user': user,
                                 'object_type': object_type, 'data_meta': data_meta})
        self.con.commit()

    def group_area_reset(self):
        query = r"""Update objects
                     Set 
                     group_area = 0"""
        self.con.execute(query)
        self.con.commit()

    def group_area(self, id_list):

        query = r"""select max(group_area) as max_id from objects"""
        data = self.con.execute(query).fetchone()
        query = f"""Update objects
                     Set 
                     group_area = :max
                     where  id in ({','.join([str(x) for x in id_list])})"""
        self.con.execute(query, {'max': data['max_id'] + 1})

        self.con.commit()

    # -------------------------------------------------------------------------
    # GIS
    # -------------------------------------------------------------------------
    def load_images_gis(self):
        query = r"""SELECT *, asgeojson(footprint) AS geom, x(centroid(footprint)) as x,
         y(centroid(footprint)) as y from images"""

        data = self.con.execute(query).fetchall()
        return data

    def load_objects_gis(self):
        query = r"""SELECT id,image as image_id, data as data,object_type as object_type,
                    resight_set as resight_set,group_area as group_area,
                    asgeojson(geom3d) AS geom,
                    reviewed as reviewed,
                    source as source,
                    X(geom3d) as x, Y(geom3d) AS y,
                    cropped_image as cropped_image
                     FROM objects """

        data = self.con.execute(query).fetchall()
        return data

    def load_objects_gis_single(self, object_id: int):
        query = r"""SELECT id,image as image_id, meta_type as meta_type,resight_set as resight_set,group_area as 
        group_area, object_type as object_type,reviewed as reviewed, source as source, asgeojson(geom3d) AS geom, 
        X(geom3d) as x, Y(geom3d) AS y, cropped_image as cropped_image FROM objects where id=:id """

        data = self.con.execute(query, {'id': object_id}).fetchone()
        return data

    # -------------------------------------------------------------------------
    # AI
    # -------------------------------------------------------------------------
    def load_ai_detections_ids(self, id_list):

        query = f"""SELECT ai_detections.id as id,image, data,object_type, object_type_orig, user,
                     image_detection as cropped_image
                    FROM ai_detections 
                    JOIN
                     ai_processes
                     where
                     ai_detections.ai_run = ai_processes.id and
                     ai_detections.id in ({','.join([str(x) for x in id_list])})"""

        data = self.con.execute(query).fetchall()
        return data

    def load_ai_detections(self, sort_by_image: bool = False):

        query = r"""SELECT ai_detections.id,ai_detections.imported,ai_detections.image,ai_detections.ai_run,
                    ai_detections.object_type_orig,ai_detections.object_type,
                    ai_detections.data_orig,ai_detections.data,ai_detections.active,ai_detections.probability,
                    ai_detections.outline,ai_processes.id as ai_run, ai_processes.user as ai_user FROM ai_detections 
                    JOIN
                    ai_processes
                    WHERE
                    ai_detections.ai_run = ai_processes.id"""

        if sort_by_image:
            query += r""" order by ai_detections.image"""

        data = self.con.execute(query).fetchall()
        return data

    def ai_load_detections_for_import(self):
        query = r"""SELECT ai_detections.id,ai_detections.imported,ai_detections.image,ai_detections.ai_run,
                    ai_detections.object_type_orig,ai_detections.object_type,
                    ai_detections.data_orig,ai_detections.data,ai_detections.active,ai_detections.probability,
                    ai_detections.outline,ai_processes.id as ai_run, ai_processes.user as ai_user FROM ai_detections 
                    JOIN
                    ai_processes
                    WHERE
                    ai_detections.ai_run = ai_processes.id and 
                    ai_detections.imported = 0 and 
                    ai_detections.active > 0"""

        data = self.con.execute(query).fetchall()
        return data

    def load_ai_detections_compare(self):
        query = r"""select * from ai_detections"""
        data = self.con.execute(query).fetchall()
        return data

    def insert_ai_process(self, ai_name, user, folder='', command='', info='', output=''):
        query = r"""insert into ai_processes
                (ai_name,user,folder, command,info,output)
                Values
                (:ai_name,:user,:folder, :command,:info,:output)
                """
        data = self.con.execute(query, {'ai_name': ai_name, 'user': user, 'folder': folder,
                                        'command': command, 'info': info, 'output': output})
        self.con.commit()
        return data.lastrowid

    def ai_create_detection_multi(self, query_list):

        #{'image_id': image_id,
        # 'ai_run': ai_run,
        # 'object_type_orig': object_type,
        # 'object_type': object_type,
        # 'data': object_data,
        # 'data_orig': object_data,
        # 'probability': probability,
        # 'outline': json.dumps(outline),
        # 'image_detection': image_detection}

        query = r"""Insert into ai_detections 
             (image, ai_run, object_type, object_type_orig, data, data_orig, probability, outline, image_detection)
             Values
             (:image_id, :ai_run,:object_type,:object_type_orig, :data, :data_orig,
             :probability,:outline,:image_detection)"""
        self.con.executemany(query, query_list)
        self.con.commit()

    def ai_load_detections_without_cropped_images(self):
        query = r"""select object_type_orig, outline, image from ai_detections"""

        data = self.con.execute(query).fetchall()
        return data

    def store_ai_detection(self, image_id: int, object_type: str, outline: dict, ai_run: int, object_data='',
                           probability: float = 0.0, image_detection=None) -> int | None:

        query = r"""select * from ai_detections
                    where 
                    object_type_orig = :object_type_orig
                    and outline = :outline
                    and image = :image_id
                    """
        data = self.con.execute(query, {'image_id': image_id,
                                        'object_type_orig': object_type,
                                        'object_type': object_type,
                                        'outline': json.dumps(outline)}).fetchone()
        if not data:
            query = r"""Insert into ai_detections 
                 (image, ai_run, object_type, object_type_orig, data, data_orig, probability, outline, image_detection)
                 Values
                 (:image_id, :ai_run,:object_type,:object_type_orig, :data, :data_orig,
                 :probability,:outline,:image_detection)"""
            data = self.con.execute(query, {'image_id': image_id,
                                            'ai_run': ai_run,
                                            'object_type_orig': object_type,
                                            'object_type': object_type,
                                            'data': object_data,
                                            'data_orig': object_data,
                                            'probability': probability,
                                            'outline': json.dumps(outline),
                                            'image_detection': image_detection})
            self.con.commit()
            return data.lastrowid
        return None

    def set_active_ai(self, active, obj_id):
        query = "Update ai_detections SET active = :active where id=:id"
        self.con.execute(query, {'active': active, 'id': obj_id})
        self.con.commit()

    def set_imported_ai(self, id_list: list):
        query = f"""Update ai_detections SET imported = 1 where
                    id in ({','.join([str(x) for x in id_list])})"""
        self.con.execute(query)
        self.con.commit()

    def change_ai_data(self, obj_id, object_type):
        query = "Update ai_detections SET object_type = :object_type where id=:id"
        self.con.execute(query, {'id': obj_id, 'object_type': object_type})
        self.con.commit()
