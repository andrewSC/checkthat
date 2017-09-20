import os
import sys
import subprocess
import smtplib


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

    pkgnames = generate_built_package_name(pkgbuild_path)
    return f"Build succeeded for [{pkgnames}]"


def generate_built_package_name(pkgbuild_path):
    cmd = [
        'makepkg',
        '--packagelist'
    ]
    original_dir = os.getcwd()
    os.chdir(pkgbuild_path)

    subproc_result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    decoded_stdout = subproc_result.stdout.decode('UTF-8')
    pkgnames = decoded_stdout.rstrip('\n').rsplit('\n')

    # TODO: Make this better
    for root, dirs, filenames in os.walk('.'):
        for filename in filenames:
            for pkgname in pkgnames:
                if pkgname in filename:
                    return filename

    os.chdir(original_dir)


def namcap_check_pkg(pkg_path):
    cmd = [
        'python',
        '/usr/lib/python3.6/site-packages/namcap.py',
        '-i',
        '/'.join([pkg_path, generate_built_package_name(pkg_path)])
    ]
    subproc_result = subprocess.run(cmd, stdout=subprocess.PIPE)
    decoded_stdout = subproc_result.stdout.decode('UTF-8')

    if decoded_stdout:
        # NOTE: If there's any output from the linter, strip newlines from the output
        # then return a list where each item is a single line of output from namcap
        return decoded_stdout.rstrip('\n').rsplit('\n')


def email_results():
    server = smtplib.SMTP('localhost')
    message = "From: duncan@planet.arrakis\r\nTo: andrew@crerar.io\r\nSubject: Simple test\r\n\r\n"

    email = {
        'from': 'duncan@planet.arrakis',
        'to': ['andrew@crerar.io'],
        'subject': 'email test',
        'message': message + 'just a simple test!! hi! :3'
    }

    server.sendmail(email['from'], email['to'], email['message'])
    server.quit()


if __name__ == '__main__':
    email_results()
    quit()

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
    print('---------- Namcap pkg results ----------')
    for path in abs_paths:
        namcap_pkg_result = namcap_check_pkg(path)
        print(namcap_pkg_result)
    print('----------------------------------------')
