from typing import Set
from cmp_version import cmp_version

from alt_rdb_comp.api import ALTLinuxRDBApi
from alt_rdb_comp.utils import convert_packages_to_dict_and_filter, eprint, build_version_string

api = ALTLinuxRDBApi()

def get_branch_packages(branch, arch_list = None):
    arch = None
    if arch_list:
        arch = arch_list[0]

    response = api.export_branch_binary_packages(
        branch,
        arch,
    )

    return convert_packages_to_dict_and_filter(response['packages'], arch_list)

def log_missing_architectures(
    missing_arches: Set[str],
    missing_in: str,
    exists_in: str
) -> None:
    for arch in missing_arches:
        eprint(
            f"Warning: Architecture '{arch}' is missing in '{missing_in}' "
            f"but exists in '{exists_in}', so it will be skipped."
        )

def compare_branches(first_branch, second_branch, arch_list = None):
    first_repo = get_branch_packages(first_branch, arch_list)
    second_repo = get_branch_packages(second_branch, arch_list)

    arches_first = set(first_repo.keys())
    arches_second = set(second_repo.keys())

    missing_in_first = arches_second - arches_first
    missing_in_second = arches_first - arches_second
    same_arches = arches_first & arches_second
    
    log_missing_architectures(missing_in_first, first_branch, second_branch)
    log_missing_architectures(missing_in_second, second_branch, first_branch)

    comparison_result = {}

    for arch in same_arches:
        first_pkgs_dict, second_packages_dict = first_repo[arch], second_repo[arch]
        packages_in_first = set(first_pkgs_dict.keys())
        packages_in_second = set(second_packages_dict.keys())
        same_packages = packages_in_first & packages_in_second
        
        newer_fist = []
        
        for package_name in same_packages:
            first_package, second_package = first_pkgs_dict[package_name], second_packages_dict[package_name]
            
            version_first = build_version_string(
                first_package
            )
            version_second = build_version_string(
                second_package
            )
            
            if cmp_version(version_first, version_second) > 0:
                newer_fist.append({
                    "name": package_name,
                    "first": {
                        "version": first_package['version'],
                        "epoch": first_package['epoch'],
                    },
                    "second": {
                        "version": second_package['version'],
                        "epoch": second_package['epoch'],
                    },
                })

        comparison_result[arch] = {
            'exists': {
                'first': list(packages_in_first - packages_in_second),
                'second': list(packages_in_second - packages_in_first),
            },
            'newer': {
                'first': newer_fist
            }
        }


    return comparison_result
