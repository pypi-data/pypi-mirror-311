#!/usr/bin/env python

"""
Tests a basic ETL scenario

Usage:
  test_e2e.py [--project=PROJECT] [--name=NAME] --id=DATASET_ID

Options:
  -p, --project=PROJECT     a name of the project [default: test]
  -n, --name=NAME           a name of the project [default: e2e]
      --id=DATASET_ID       an input dataset
  -h, --help                display this help and exit
"""


import logging
import sys
import tempfile
from pathlib import Path
from docopt import docopt
from datatrack import Dataset, Experiment


logging.basicConfig(
    stream=sys.stderr,
    level=logging.getLevelName(logging.INFO),
    format="%(asctime)s %(levelname)s %(filename)s:%(lineno)d -- %(message)s",
)


def process_data(path, dst):
    for f in Path(path).rglob('*'):
        outname = Path(dst) / f.relative_to(path)
        logging.info(f"Creating {outname}")
        if f.is_dir():
            outname.mkdir()
        else:
            with open(outname, "w") as out:
                print(f.stat().st_size, file=out)


if __name__ == "__main__":
    args = docopt(__doc__)
    with Experiment(args["--project"], args["--name"]).run() as run:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = run.get_dataset(Dataset(args["--id"]))
            process_data(path, tmpdir)
            ds = run.create_dataset(tmpdir)
            print(ds)
