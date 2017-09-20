import os
import sys
import subprocess


packages_dir = sys.argv[1]  # ABS path to where all the folders for packages are located


def gather_pkgbuild_paths(root_pkgs_dir):
    pkgbuild_paths = []

    for root, dirs, files in os.walk(root_pkgs_dir):
        if 'PKGBUILD' in files:
            pkgbuild_paths.append(root)

    return pkgbuild_paths


def namcap_check_pkgbuild(pkgbuild_path):
    abs_pkgbuild_path = '/'.join([pkgbuild_path, 'PKGBUILD'])
    subproc_result = subprocess.run(['python', '/usr/lib/python3.6/site-packages/namcap.py', '-i', abs_pkgbuild_path], stdout=subprocess.PIPE)
    return subproc_result.stdout.decode('UTF-8')


def makepkg(pkgbuild_path):
    pkgbuild_path
    pass


def namcap_check_pkg(pkg_path):
    pkg_path
    pass


def email_results():
    pass


if __name__ == '__main__':
    paths = gather_pkgbuild_paths(packages_dir)
    for path in paths:
        print(namcap_check_pkgbuild(path))
