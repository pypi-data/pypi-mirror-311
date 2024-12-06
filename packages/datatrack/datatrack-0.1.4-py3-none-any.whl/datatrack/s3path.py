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


import boto3
from pathlib import Path, PurePath
from urllib.parse import urlparse


class S3Path:
    s3 = boto3.session.Session().client("s3")

    def __init__(self, bucket, key="", meta=None):
        self.bucket = bucket
        self.key = key.removeprefix("/")
        self.meta = meta

    @staticmethod
    def from_uri(uri):
        uri = urlparse(uri)
        bucket = uri.netloc
        key = uri.path.removeprefix("/")
        return S3Path(bucket, key)

    def as_uri(self):
        return f"s3://{self.bucket}/{self.key}"

    def __truediv__(self, path):
        return S3Path(self.bucket, str(PurePath(self.key) / path))

    def rglob(self, pattern):
        objects = self.s3.list_objects_v2(Bucket=self.bucket, Prefix=self.key)
        return [S3Path(self.bucket, obj["Key"], obj) for obj in objects["Contents"]]

    def download(self, dst):
        """
        Downloads all objects to the specified directory.

        :param dst: A directory to save downloaded files, defaults to ".".
        """
        dst = Path(dst)
        for obj in self.rglob("*"):
            if obj.key == self.key: # self.key references a single file
                path = dst / PurePath(obj.key).name
            else:
                path = dst / obj.key.removeprefix(self.key).removeprefix("/")
            path.parent.mkdir(parents=True, exist_ok=True)
            self.s3.download_file(Bucket=self.bucket,
                                  Key=obj.key,
                                  Filename=path)

    def upload(self, src):
        src = Path(src)
        if src.is_dir():
            for f in src.rglob("*"):
                if f.is_file():
                    key = Path(self.key) / f.relative_to(src)
                    self.s3.upload_file(f, self.bucket, str(key))
        else:
            key = Path(self.key) / src.name
            self.s3.upload_file(str(src), self.bucket, str(key))

    def copy_from(self, src):
        for obj in src.rglob("*"):
            if obj.key == src.key: # copy a single file
                path = PurePath(src.key).name
            else:
                path = PurePath(obj.key).relative_to(src.key)
            cp = {"Bucket": obj.bucket, "Key": obj.key}
            self.s3.copy(cp, self.bucket, str(PurePath(self.key) / path))

    def __repr__(self):
        return f"S3Path('{self.bucket}', '{self.key}')"
