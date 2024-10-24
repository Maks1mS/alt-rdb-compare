import argparse
import json

from alt_rdb_comp.lib import compare_branches

parser = argparse.ArgumentParser(
    prog="alt-rdb-comp",
    description="ALTLinux RDB Compare"
)

parser.add_argument("first_branch")
parser.add_argument("second_branch")
parser.add_argument("arch")

args = parser.parse_args()


print(json.dumps(
    compare_branches(
        args.first_branch, 
        args.second_branch, 
        args.arch
    ),
    indent=4
))

