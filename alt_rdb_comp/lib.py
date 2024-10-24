from alt_rdb_comp.api import ALTLinuxRDBApi

from cmp_version import cmp_version

api = ALTLinuxRDBApi()

def convert_packages_to_dict(packages):
    repo = dict()
    for package in packages:
        repo[package['name']] = package
    return repo

def build_version_string(package):
    return f"{package['epoch']}:{package['version']}"

def compare_branches(first_branch, second_branch, arch):
    first_res = api.export_branch_binary_packages(
        first_branch,
        arch,
    )

    first_repo = convert_packages_to_dict(first_res['packages'])
    del first_res

    second_res = api.export_branch_binary_packages(
        second_branch,
        arch,
    )

    second_repo = convert_packages_to_dict(second_res['packages'])
    del second_res

    packages_in_first = set(first_repo.keys())
    packages_in_second = set(second_repo.keys())

    same_packages = packages_in_first & packages_in_second

    newer_fist = []

    for package_name in same_packages:
        first, second = first_repo[package_name], second_repo[package_name]

        a, b = (
            build_version_string(
                first
            ),
            build_version_string(
                second
            )
        )

        if cmp_version(a, b) > 0:
            newer_fist.append({
                "name": package_name,
                "first": {
                    "version": first['version'],
                    "epoch": first['epoch'],
                },
                "second": {
                    "version": second['version'],
                    "epoch": second['epoch'],
                },
            })


        
    return {
        'exists': {
            'first': list(packages_in_first - packages_in_second),
            'second': list(packages_in_second - packages_in_first),
        },
        'newer': {
            'first': newer_fist
        }
    }