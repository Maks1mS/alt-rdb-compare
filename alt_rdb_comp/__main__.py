import argparse
import json
import os

from alt_rdb_comp.lib import compare_branches
from alt_rdb_comp.utils import eprint

prog_name = os.getenv("PROG_NAME", os.path.basename(__file__))

parser = argparse.ArgumentParser(prog=prog_name, description="ALTLinux RDB Compare")

parser.add_argument("first_branch", help="First branch to compare")

parser.add_argument("second_branch", help="Second branch to compare")

parser.add_argument("--arch", nargs="+", help="Filter results by architecture")

args = parser.parse_args()

try:
    print(
        json.dumps(
            compare_branches(args.first_branch, args.second_branch, args.arch), indent=4
        )
    )
except Exception as e:
    eprint(f"Exception: {e}")
