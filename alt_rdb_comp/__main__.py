import argparse
from alt_rdb_comp.api import ALTLinuxRDBApi

parser = argparse.ArgumentParser(
    prog="alt-rdb-comp",
    description="ALTLinux RDB Compare"
)

parser.add_argument("first_branch")
parser.add_argument("second_branch")
parser.add_argument("arch")

args = parser.parse_args()

api = ALTLinuxRDBApi()

