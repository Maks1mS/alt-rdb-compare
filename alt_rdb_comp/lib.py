from typing import List, Optional, Set
from cmp_version import cmp_version

from alt_rdb_comp.api import ALTLinuxRDBApi
from alt_rdb_comp.utils import (
    convert_packages_to_dict_and_filter,
    eprint,
    build_version_string,
)

api = ALTLinuxRDBApi()


def get_branch_packages(branch: str, arch_list: Optional[List[str]] = None):
    """
    Get branch packages from API
    """

    arch = None
    if arch_list and len(arch_list) == 1:
        arch = arch_list[0]

    response = api.export_branch_binary_packages(
        branch,
        arch,
    )

    return convert_packages_to_dict_and_filter(response["packages"], arch_list)


def log_missing_architectures_one_branch(
    missing_arches: Set[str], missing_in: str, exists_in: str
) -> None:
    for arch in missing_arches:
        eprint(
            f"Warning: Architecture '{arch}' is missing in '{missing_in}' "
            f"but exists in '{exists_in}', so it will be skipped."
        )


def log_missing_architectures_both(missing_arches: Set[str]) -> None:
    for arch in missing_arches:
        eprint(
            f"Warning: Architecture '{arch}' is missing at 2 branches, so it will be skipped."
        )


def compare_branches(
    first_branch: str, second_branch: str, arch_list: Optional[List[str]] = None
):
    """
    Compare packages in branches

    :arch_list: compare only selected archs. If not specified, compare all available ones.
    """

    first_packages = get_branch_packages(first_branch, arch_list)
    second_packages = get_branch_packages(second_branch, arch_list)

    arches_first = set(first_packages.keys())
    arches_second = set(second_packages.keys())

    same_arches = arches_first & arches_second
    missing_both = set(arch_list) - (arches_first | arches_second)

    missing_in_first = arches_second - arches_first
    missing_in_second = arches_first - arches_second

    log_missing_architectures_both(missing_both)
    log_missing_architectures_one_branch(missing_in_first, first_branch, second_branch)
    log_missing_architectures_one_branch(missing_in_second, second_branch, first_branch)

    same_arches = arches_first & arches_second

    comparison_result = {}

    for arch in same_arches:
        first_arch_packages = first_packages.get(arch, {})
        second_arch_packages = second_packages.get(arch, {})

        first_pkg_names = set(first_arch_packages.keys())
        second_pkg_names = set(second_arch_packages.keys())

        missing_in_second_pkgs = first_pkg_names - second_pkg_names
        missing_in_first_pkgs = second_pkg_names - first_pkg_names
        same_packages = first_pkg_names & second_pkg_names

        newer_fist = []

        for package_name in same_packages:
            first_pkg, second_pkg = (
                first_arch_packages[package_name],
                second_arch_packages[package_name],
            )

            version_first = build_version_string(first_pkg)
            version_second = build_version_string(second_pkg)

            if cmp_version(version_first, version_second) > 0:
                newer_fist.append(
                    {
                        "name": package_name,
                        "first": {
                            "version": first_pkg["version"],
                            "epoch": first_pkg["epoch"],
                        },
                        "second": {
                            "version": second_pkg["version"],
                            "epoch": second_pkg["epoch"],
                        },
                    }
                )

        comparison_result[arch] = {
            "missing": {
                "first": list(missing_in_first_pkgs),
                "second": list(missing_in_second_pkgs),
            },
            "newer": {"first": newer_fist},
        }

    return comparison_result
