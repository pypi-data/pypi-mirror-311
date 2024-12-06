#!/usr/bin/env python

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


"""
Usage: dt configure

Options:
  -h, --help      display this help and exit
      --version   output version information and exit
"""

from docopt import docopt
from pathlib import Path
from importlib.metadata import version

from .config import config, config_path, cache_dir


def main():
    args = docopt(__doc__, version=version("datatrack"))

    try:
        cfg = config()
    except FileNotFoundError:
        cfg = {}

    cfg_s3 = cfg.get("s3", {})
    cfg_bucket = cfg_s3.get("bucket") or ""
    cfg_prefix = cfg_s3.get("prefix") or ""

    cfg_db = cfg.get("database", {})
    cfg_psql = cfg_db.get("postgresql", {})
    cfg_conn = cfg_psql.get("conninfo", "")

    cfg_cache = cfg.get("cache", cache_dir())

    bucket = input(f"S3 bucket name [{cfg_bucket}]: ")
    prefix = input(f"S3 prefix [{cfg_prefix}]: ")
    conninfo = input(f"DB connection string [{cfg_conn}]: ")
    cachedir = input(f"File cache directory [{cfg_cache}]: ")

    toml = f"""cache = "{cachedir or cfg_cache}"

[s3]
bucket = "{bucket or cfg_bucket}"
prefix = "{prefix or cfg_prefix}"

[database.postgresql]
conninfo = "{conninfo or cfg_conn}"
"""
    cfg_path = config_path()
    cfg_path.parent.mkdir(parents=True, exist_ok=True)
    with open(cfg_path, "w") as f:
        f.write(toml)


if __name__ == "__main__":
    main()
