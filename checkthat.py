import os
import sys


packages_dir = sys.argv[1]  # ABS path to where all the folders for packages are located


def gather_pkgbuild_paths(root_pkgs_dir):
    pkgbuild_paths = []

    for root, dirs, files in os.walk(root_pkgs_dir):
        if 'PKGBUILD' in files:
            pkgbuild_paths.append(os.path.join(root, 'PKGBUILD'))

    print(pkgbuild_paths)


gather_pkgbuild_paths(packages_dir)
