import datetime
import os
import sys
import subprocess
import smtplib
import time

from models import BuildFailure
from builders import PackageBuilder
from views import CliView


def gather_pkgbuild_paths(root_pkgs_dir):
    pkgbuild_paths = []

    for root, dirs, files in os.walk(root_pkgs_dir):
        if 'PKGBUILD' in files:
            pkgbuild_paths.append(root)

    # return pkgbuild_paths

    return ['/home/andrew/Dev/aur/firefox-developer', '/home/andrew/Dev/aur/gtk4-git']


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


def email_results(message):
    server = smtplib.SMTP('localhost')
    now = datetime.datetime.now()
    subject = f"Arrakis AUR build results on {now.strftime('%Y-%m-%d %H:%M:%S')}"
    message = f"From: duncan@planet.arrakis\r\nTo: andrew@crerar.io\r\nSubject: {subject} \r\n\r\n{message}"

    email = {
        'from': 'duncan@planet.arrakis',
        'to': ['andrew@crerar.io'],
        'subject': subject,
        'message': message
    }

    server.sendmail(email['from'], email['to'], email['message'])
    server.quit()


def format_output(msgs, build_time):
    output = []
    build_header = ('-' * 30) + ' Build Results ' + ('-' * 30)
    output.append(build_header + '\n')

    paths = msgs.keys()

    for path in paths:
        output.append(msgs[path]['makepkg'] + '\n')

    minutes, seconds = divmod(build_time, 60)
    output.append(f"\nTotal build time: {minutes}m {seconds}s\n")
    output.append(('-' * len(build_header)) + '\n\n')

    # TODO: Make this better

    fail_header = ('-' * 30) + ' Failures ' + ('-' * 30)
    output.append(fail_header + '\n')
    for path in paths:
        if 'makepkg_fail' in msgs[path]:
            fail_msg_header = f"\nxxxxxxxxxxxxxxx [{msgs[path]['makepkg_fail']['path']}] xxxxxxxxxxxxxxx"
            fail_msg_header_len = len(fail_msg_header)
            output.append(fail_msg_header + '\n')

            for line in msgs[path]['makepkg_fail']['errors']:
                output.append(line + '\n')

            output.append(('x' * fail_msg_header_len) + '\n')

    output.append((len(fail_header) * '-') + '\n\n')

    # TODO: Make this better
    namcap_pkgbuild_header = ('-' * 30) + ' Namcap PKGBUILD Results ' + ('-' * 30)
    output.append(namcap_pkgbuild_header + '\n')
    for path in paths:
        if 'namcap_pkgbuild' in msgs[path]:
            for namcap_msg in msgs[path]['namcap_pkgbuild']:
                output.append(namcap_msg + '\n')

    output.append((len(namcap_pkgbuild_header) * '-') + '\n\n')

    # TODO: Make this better
    namcap_pkg_header = ('-' * 30) + ' Namcap Package Results ' + ('-' * 30)
    output.append(namcap_pkg_header + '\n')
    for path in paths:
        if 'namcap_pkg' in msgs[path]:
            namcap_pkg_header = f"\n??????????????? [{msgs[path]['namcap_pkg']['pkgname']}] ????????????\n"
            namcap_pkg_header_len = len(namcap_pkg_header)
            output.append(namcap_pkg_header)

            for namcap_msg in msgs[path]['namcap_pkg']['output']:
                output.append(namcap_msg + '\n')

            output.append(('?' * namcap_pkg_header_len) + '\n')

    output.append(('-' * len(namcap_pkg_header)) + '\n')
    return ''.join(output)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Error: Missing path to directory containing AUR packages.')
        print('Usage: python checkthat.py <dir>')
        quit()

    start_time = time.time()
    abs_paths = gather_pkgbuild_paths(sys.argv[1])  # ABS path to where all the folders for packages are located

    msgs = {}
    builder = PackageBuilder()
    builds = []
    view = CliView()

    for path in abs_paths:
        msgs[path] = {}

        build = builder.build(path)
        build.namcap_pkgbuild_analysis = builder.analyze_pkgbuild(path)

        if type(build) is not BuildFailure:
            # NOTE: We should only try to analyze the package if the build
            # was actually successful
            build.namcap_pkg_analysis = builder.analyze_pkg(path)

        builds.append(build)

    view.generate_output(builds)

    """
    namcap_pkgbuild_check_msgs = namcap_check_pkgbuild(path)
    if namcap_pkgbuild_check_msgs:
        msgs[path]['namcap_pkgbuild'] = []

        for output_line in namcap_pkgbuild_check_msgs:
            msgs[path]['namcap_pkgbuild'].append(f"[{path}]: {output_line}")

    try:
        makepkg_result = makepkg(path)
        msgs[path]['makepkg'] = makepkg_result

        # NOTE: Namcap should only lint the pkg if it was a successful build
        namcap_pkg_check_msgs = namcap_check_pkg(path)
        if namcap_pkg_check_msgs:
            msgs[path]['namcap_pkg'] = {'pkgname': generate_built_package_name(path), 'output': []}
            for output_line in namcap_pkg_check_msgs:
                msgs[path]['namcap_pkg']['output'].append(output_line)

    except BuildError as e:
        msgs[path]['makepkg'] = str(e)
        msgs[path]['makepkg_fail'] = {'path': path, 'errors': e.errors}

end_time = time.time()
email_results(format_output(msgs, (end_time - start_time)))
"""
