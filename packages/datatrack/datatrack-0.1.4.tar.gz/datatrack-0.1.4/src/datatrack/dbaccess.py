# datatrack: tracks your data transformations.
# Copyright (C) 2024  Roman Kindruk

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import random
import psycopg
from enum import IntEnum

from .config import config as cfg


class RunStatus(IntEnum):
    STARTED = 1,
    FINISHED = 2,
    ERROR = -1,

CONN = None

def conn():
    global CONN
    if CONN is None:
        CONN = psycopg.connect(cfg()["database"]["postgresql"]["conninfo"], autocommit=True)
    return CONN


def generate_id():
    return ''.join(random.choices("0123456789abcdef", k=32))


def normalize_project_name(project):
    return project.strip("/")


def get_or_create_project(project):
    project = normalize_project_name(project)
    with conn().cursor() as cur:
        cur.execute("INSERT INTO project(name) VALUES (%s) ON CONFLICT DO NOTHING",
                    (project,))
        return cur.execute("SELECT id FROM project WHERE name = %s", (project,)).fetchone()[0]


def get_or_create_experiment(project, name):
    eid = generate_id()
    prj_id = get_or_create_project(project)
    with conn().cursor() as cur:
        sql = """\
        INSERT INTO experiment(id, prj_id, name)
        VALUES (%s, %s, %s)
        ON CONFLICT (prj_id, name) DO NOTHING
        """
        cur.execute(sql, (eid, prj_id, name))
        return cur.execute("SELECT id FROM experiment WHERE name = %s AND prj_id = %s",
                           (name, prj_id)).fetchone()[0]


def create_run(experiment_id, user):
    run_id = generate_id()
    conn().execute("insert into run(id, exp_id, uid, status, started) values(%s, %s, %s, %s, now())",
                 (run_id, experiment_id, user, RunStatus.STARTED))
    return run_id

def finish_run(run_id, status):
    conn().execute("update run set status=%s, finished=now() where id=%s",
                 (status, run_id))

def run_register_dataset(run_id, ds_id, type_):
    conn().execute("insert into run_dataset(run_id, ds_id, type) values(%s, %s, %s)",
                 (run_id, ds_id, type_))


def create_dataset(project, name, user, parent=None):
    prj_id = get_or_create_project(project)
    ds_id = generate_id()
    conn().execute("insert into dataset(id, parent, prj_id, name, uid) values(%s, %s, %s, %s, %s)",
                 (ds_id, parent, prj_id, name, user))
    return ds_id


def add_dataset_objects(dataset_id, objects):
    with conn().cursor() as cur:
        cur.executemany("INSERT INTO file(ds_id, path, size, etag, modified) values(%s, %s, %s, %s, %s)",
                        [(dataset_id, obj.as_uri(), obj.meta["Size"], obj.meta["ETag"], obj.meta["LastModified"])
                         for obj in objects])


def get_dataset(dataset_id):
    with conn().cursor(row_factory=psycopg.rows.dict_row) as cur:
        return cur.execute("SELECT p.name as project FROM project p INNER JOIN dataset d ON p.id=d.prj_id WHERE d.id = %s", (dataset_id,)).fetchone()


def list_dataset(dataset_id):
    sql = """\
    SELECT f.path
    FROM file f
    INNER JOIN dataset_version v ON f.dsver_id = v.id
    WHERE v.ds_id=%s
    """
    return conn().execute(sql, (dataset_id,)).fetchall()
