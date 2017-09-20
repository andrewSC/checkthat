import os
import sys
import subprocess


def gather_pkgbuild_paths(root_pkgs_dir):
    pkgbuild_paths = []

    for root, dirs, files in os.walk(root_pkgs_dir):
        if 'PKGBUILD' in files:
            pkgbuild_paths.append(root)

    # return pkgbuild_paths
    return ['/home/andrew/Dev/aur/firefox-developer']


def namcap_check_pkgbuild(pkgbuild_path):
    cmd = [
        'python',
        '/usr/lib/python3.6/site-packages/namcap.py',
        '-i',
        '/'.join([pkgbuild_path, 'PKGBUILD'])
    ]
    subproc_result = subprocess.run(cmd, stdout=subprocess.PIPE)
    decoded_stdout = subproc_result.stdout.decode('UTF-8')

    if decoded_stdout:
        # NOTE: If there's any output from the linter, strip newlines from the output
        # then return a list where each item is a single line of output from namcap
        return decoded_stdout.rstrip('\n').rsplit('\n')

    return


def makepkg(pkgbuild_path):
    cmd = [
        'makepkg',
        '-cCmf'
    ]
    original_dir = os.getcwd()
    os.chdir(pkgbuild_path)
    subproc_result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    decoded_stdout = subproc_result.stdout.decode('UTF-8')

    if subproc_result.returncode != 0:
        # NOTE: If there's any output from the linter, strip newlines from the output
        # then return a list where each item is a single line of output from namcap
        return decoded_stdout.rstrip('\n').rsplit('\n')

    os.chdir(original_dir)

    return f"Build succeeded for [{pkgbuild_path}]"


def namcap_check_pkg(pkg_path):
    pkg_path
    pass


def email_results():
    pass


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Error: Missing path to directory containing AUR packages.')
        print('Usage: python checkthat.py <dir>')
        quit()

    abs_paths = gather_pkgbuild_paths(sys.argv[1])  # ABS path to where all the folders for packages are located

    print('------------ Namcap results ------------')
    for path in abs_paths:
        namcap_check_result = namcap_check_pkgbuild(path)
        if namcap_check_result:
            for output in namcap_check_result:
                print(f"[{path}]: {output}")
    print('----------------------------------------')
    print('----------- Makepkg results ------------')
    for path in abs_paths:
        makepkg_result = makepkg(path)
        print(makepkg_result)
    print('----------------------------------------')
