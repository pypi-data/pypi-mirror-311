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


import getpass
import logging
from contextlib import contextmanager
from enum import IntEnum
from datetime import datetime
from . import dbaccess as db
from .dataset import Dataset


class Run:
    class DatasetType(IntEnum):
        INPUT = 0,
        OUTPUT = 1,

    def __init__(self, experiment):
        self._exp = experiment
        self._id = db.create_run(self._exp._id, getpass.getuser())

    @property
    def id(self):
        return self._id

    def get_dataset(self, ds, path=None):
        db.run_register_dataset(self._id, ds.id, Run.DatasetType.INPUT)
        return ds.download(path)

    def create_dataset(self, path, name=None):
        ds_name = name or self._exp.name
        ds = Dataset.create(self._exp.project, ds_name, path)
        db.run_register_dataset(self._id, ds.id, Run.DatasetType.OUTPUT)
        return ds

    def __repr__(self):
        return f"<Run id={self._id}>"


class Experiment:
    def __init__(self, project, name):
        self.project = project
        self.name = name
        self._id = db.get_or_create_experiment(project, name)

    @contextmanager
    def run(self):
        start_time = datetime.now()
        r = Run(self)
        logging.info(f"{r}: started")

        try:
            yield r
        except:
            status = db.RunStatus.ERROR
            logging.error(f"{r}: failed after {datetime.now() - start_time}")
            raise
        else:
            status = db.RunStatus.FINISHED
            logging.info(f"{r}: finished in {datetime.now() - start_time}")
        finally:
            db.finish_run(r.id, status)

    def __repr__(self):
        return f"Experiment(project='{self.project}', name='{self.name}')"
