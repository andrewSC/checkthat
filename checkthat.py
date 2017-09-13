import os
import sys


packages_dir = sys.argv[1]  # ABS path to where all the folders for packages are located


def read_ignorelist():
    with open('ignorelist') as file:
        return file.read().splitlines()


def gather_package_paths():
    dirs_to_ignore = read_ignorelist()  # Read in dirs to ignore/not consider as packages

    for f in os.listdir(packages_dir):
        actual_abs_path = os.path.abspath('/'.join([packages_dir, f]))

        if os.path.isdir(actual_abs_path) and actual_abs_path not in dirs_to_ignore:
                yield actual_abs_path


for package_path in gather_package_paths():
    print(f"{package_path}: {os.listdir(package_path)}")


