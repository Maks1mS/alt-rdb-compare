import sys

def build_version_string(package):
    return f"{package['epoch']}:{package['version']}"

def convert_packages_to_dict_and_filter(packages, arch_filter = None):
    is_filter_need = arch_filter is not None

    repo = dict()    

    for package in packages:
        package_arch = package['arch']

        if is_filter_need and package_arch not in arch_filter:
            continue

        if package_arch not in repo:
            repo[package_arch] = {}

        repo[package_arch][package['name']] = package

    return repo

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
