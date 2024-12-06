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
from pathlib import Path

from datatrack import dbaccess as db
from datatrack.s3path import S3Path
from datatrack.config import config


class Dataset:
    def __init__(self, id):
        self._id = id

    @property
    def id(self):
        return self._id

    @staticmethod
    def _make_path(project, dataset_id):
        return str(Path(project) / "datasets" / dataset_id)

    @staticmethod
    def _make_s3path(project, dataset_id):
        return S3Path(config()["s3"]["bucket"], config()["s3"]["prefix"]) / Dataset._make_path(project, dataset_id)

    def download(self, dst=None):
        if not dst:
            dst = config()["cache"]
        dst = Path(dst)
        project = db.get_dataset(self._id)["project"]
        loc = self._make_s3path(project, self._id)
        dst = dst / self._make_path(project, self._id)
        if dst.exists():
            logging.warning(f"{self} is already downloaded to {dst}")
        else:
            loc.download(dst)
        return dst

    @staticmethod
    def create(project, name, src):
        did = db.create_dataset(project, name, getpass.getuser())
        dst = Dataset._make_s3path(project, did)
        if isinstance(src, str) and src.startswith("s3://"):
            dst.copy_from(S3Path.from_uri(src))
        else:
            dst.upload(src)
        db.add_dataset_objects(did, dst.rglob("*"))
        return Dataset(did)

    def __repr__(self):
        return f"Dataset(id='{self._id}')"
