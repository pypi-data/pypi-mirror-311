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


import os
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


CONFIG = None


def config_path():
    xdg_cfg_home =  Path(os.getenv("XDG_CONFIG_HOME", Path.home() / ".config"))
    return xdg_cfg_home / "datatrack" / "config.toml"

def cache_dir():
    xdg_data_home = Path(os.getenv("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    return xdg_data_home / "datatrack" / "cache"

def config():
    global CONFIG
    if CONFIG is None:
        with open(config_path(), "rb") as f:
            CONFIG = tomllib.load(f)
    return CONFIG
