import os
from pathlib import Path
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

default = {
    "config": Path.home() / ".config",
    "cache": Path.home() / ".local" / "share",
}

cfg_dir_path = Path(os.getenv("XDG_CONFIG_HOME", default["config"])) / __package__
with open(cfg_dir_path / "config.toml", "rb") as f:
    config = tomllib.load(f)

if "cache" not in config:
    data_dir =  Path(os.getenv("XDG_DATA_HOME", default["cache"])) / __package__
    config["cache"] = data_dir / "cache"
