#!/usr/bin/env python

"""
Tests dataset creation

Usage:
  test_dataset_create.py --project=PROJECT --name=NAME SOURCE

Arguments:
  SOURCE     a location of the files, can be a local path or S3 URI

Options:
  -p, --project=PROJECT     a name of the project
  -n, --name=NAME           a name of the project
  -h, --help                display this help and exit
"""


from docopt import docopt
from datatrack import Dataset


if __name__ == "__main__":
    args = docopt(__doc__)
    ds = Dataset.create(args["--project"], args["--name"], args["SOURCE"])
    print(ds)
