import datetime
import os
import sys
import subprocess
import smtplib
import time

from exceptions import BuildError


def gather_pkgbuild_paths(root_pkgs_dir):
    pkgbuild_paths = []

    for root, dirs, files in os.walk(root_pkgs_dir):
        if 'PKGBUILD' in files:
            pkgbuild_paths.append(root)

    return pkgbuild_paths


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


def makepkg(pkgbuild_path):
    cmd = [
        'makepkg',
        '-cCmf'
    ]
    original_dir = os.getcwd()
    os.chdir(pkgbuild_path)
    subproc_result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    decoded_stdout = subproc_result.stdout.decode('UTF-8')

    os.chdir(original_dir)
    
    if subproc_result.returncode != 0:
        # NOTE: If there's any output from the linter, strip newlines from the output
        # then return a list where each item is a single line of output from namcap
        raise BuildError(f"Failed building [{pkgbuild_path}]", decoded_stdout.rstrip('\n').rsplit('\n'))

    pkgnames = generate_built_package_name(pkgbuild_path)
    return f"Successfully built [{pkgnames}]"


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


# def format_output(namcap_pkgbuild_msgs, namcap_pkg_msgs, makepkg_mgs, makepkg_fail_msgs, total_time):
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
    for path in abs_paths:
        msgs[path] = {}

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
