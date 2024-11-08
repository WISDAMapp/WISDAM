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


import os
from pathlib import Path
from sqlite3 import dbapi2


def uri4sqlite(fn: str) -> str:
    uri = Path(fn).resolve().as_uri()
    if len(uri) > 7 and uri[7] != '/':
        # a network path. Insert 2 more slashes after the scheme.
        uri = '{}//{}'.format(uri[:7], uri[7:])
    return uri


def init(db):
    db.row_factory = dbapi2.Row
    db.execute("PRAGMA foreign_keys = ON")
    supports_foreign_keys = db.execute("PRAGMA foreign_keys").fetchone()[0]
    assert supports_foreign_keys

    n_cpus = os.cpu_count()
    if n_cpus:
        db.execute("PRAGMA threads = {}".format(n_cpus))

    db.enable_load_extension(True)
    # mod_spatialite.dll must be on PATH
    db.execute("SELECT load_extension('mod_spatialite','sqlite3_modspatialite_init')")

    meta, = db.execute("SELECT CheckSpatialMetaData()").fetchone()

    if meta == 0:  # geometry_columns and spatial_ref_sys tables do not exist
        db.execute('SELECT InitSpatialMetadata(1)')
        assert db.execute("SELECT CheckSpatialMetaData()").fetchone()[0], \
            'Spatial metadata could not be inserted. Probably the SQLite db-connection was opened as read-only'
    elif meta == 1:
        # https://www.gaia-gis.it/fossil/libspatialite/wiki?name=switching-to-4.0
        raise Exception('Spatialite metadata tables follow a legacy layout. update, e.g. using spatialite_convert')
    elif meta == 2:  # both tables exist, and their layout is the one used by FDO/OGR
        db.execute('SELECT AutoFDOStart()')
    elif meta == 3:  # both tables exist, and their layout is the one currently used by SpatiaLite
        # (4.0.0 or any subsequent version)
        pass
    elif meta == 4:
        db.execute('SELECT AutoGPKGStart()')
    else:
        raise Exception('CheckSpatialMetaData() returned an unknown value: {}'.format(meta))


def create(db_fn: str):
    with dbapi2.connect(db_fn) as db:
        init(db)

        db.executescript('''
            CREATE TABLE images ( 
                id INTEGER NOT NULL PRIMARY KEY,
                user TEXT,
                flight_ref TEXT,
                transect TEXT,
                block TEXT,
                group_image INTEGER Default 0,
                width REAL,
                height REAL,
                math_model TEXT,
                type INTEGER default 0, 
                importer TEXT,
                data_env TEXT,
                inspected INTEGER default 0,
                name TEXT,
                path TEXT NOT NULL UNIQUE, 
                datetime TIMESTAMP,
                meta_image TEXT,           
                area REAL default 0.0,
                gsd REAL default 0.0,
                meta_user TEXT,
                tags TEXT     
            ); 

            CREATE TABLE configuration (
                id INTEGER NOT NULL PRIMARY KEY,
                created_by TEXT NOT NULL UNIQUE,
                version TEXT NOT NULL,
                date_created TEXT,
                mapper TEXT,
                area REAL default 0.0,
                gsd REAL  default 0.0,
                configuration TEXT,
                last_image REFERENCES images(id),
                color_scheme TEXT
            );

            CREATE TABLE objects (
                id INTEGER NOT NULL PRIMARY KEY,
                image REFERENCES images(id),
                user TEXT,
                source INTEGER default 0,
                reviewed INTEGER default 0,
                area REAL default 0.0,
                gsd REAL default 0.0,
                resight_set INTEGER default 0,
                group_area INTEGER default 0,
                meta_type TEXT,
                object_type TEXT,
                data TEXT,
                data_env TEXT,
                active INTEGER default 1,
                highlighted INTEGER default 0,
                tags TEXT,
                cropped_image BLOB
            ); 
            
            CREATE TABLE ai_processes (
                id INTEGER NOT NULL PRIMARY KEY,
                ai_name TEXT,
                user TEXT,
                folder TEXT,
                command TEXT,
                info TEXT,
                output TEXT
            ); 
            
            CREATE TABLE ai_detections (
                id INTEGER NOT NULL PRIMARY KEY,
                imported INTEGER default 0,
                image REFERENCES images(id),
                ai_run REFERENCES ai_processes(id),
                object_type_orig TEXT,
                object_type TEXT,
                data_orig TEXT,
                data TEXT,
                active INTEGER default 0,
                probability REAL,
                outline TEXT,
                image_detection BLOB
            ); 
                    
            ''')

        db.execute("""
            SELECT AddGeometryColumn(
                'images', -- table
                'position',   -- column
                4979,           -- srid
                'POINTZ',  -- geom_type. 
                'XYZ',        -- dimension
                0             -- Can be empty
            )""")

        db.execute("""
            SELECT AddGeometryColumn(
                'images', -- table
                'footprint',   -- column
                4979,           -- srid
                'POLYGONZ',  -- geom_type. 
                'XYZ',        -- dimension
                0             -- Can be empty            
            )""")

        db.execute("""
            SELECT AddGeometryColumn(
                'images', -- table
                'centerpoint',   -- column
                4979,           -- srid: undefined/local cartesian cooSys
                'POINTZ',     -- geom_type. 
                'XYZ',        -- dimension
                0            -- Can be empty        
            )""")

        db.execute("""
            SELECT AddGeometryColumn(
                'objects', -- table
                'geom2d',   -- column
                -1,           -- srid: undefined/local cartesian cooSys
                'GEOMETRY',     -- geom_type. 
                'XY',        -- dimension
                0            -- Can be empty        
            )""")

        db.execute("""
            SELECT AddGeometryColumn(
                'objects', -- table
                'geom3d',   -- column
                4979,           -- srid: undefined/local cartesian cooSys
                'GEOMETRY',     -- geom_type. 
                'XYZ',        -- dimension
                0            -- Can be empty        
            )""")

        db.executescript('''
            CREATE INDEX idx_image_objects ON objects(image);
        ''')


def insert_example_date(db_fn):

    with dbapi2.connect(uri4sqlite(db_fn) + '?mode=rw', uri=True) as db:

        # ... insert data

        db.execute("ANALYZE")
        # update indices


if __name__ == '__main__':
    dbFn = 'test_debug.sqlite'
    create(dbFn)
