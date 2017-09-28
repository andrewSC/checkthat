import datetime
import os
import sys
import smtplib

from models import BuildFailure
from builders import PackageBuilder
from views import EmailView


def gather_pkgbuild_paths(root_pkgs_dir):
    pkgbuild_paths = []

    for root, dirs, files in os.walk(root_pkgs_dir):
        if 'PKGBUILD' in files:
            pkgbuild_paths.append(root)

    return pkgbuild_paths


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


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Error: Missing path to directory containing AUR packages.')
        print('Usage: python checkthat.py <dir>')
        quit()

    abs_paths = gather_pkgbuild_paths(sys.argv[1])  # ABS path to where all the folders for packages are located

    builder = PackageBuilder()
    view = EmailView()
    builds = []

    for path in abs_paths:
        build = builder.build(path)
        build.namcap_pkgbuild_analysis = builder.analyze_pkgbuild(path)

        if type(build) is not BuildFailure:
            # NOTE: We should only try to analyze the package if the build
            # was actually successful
            build.namcap_pkg_analysis = builder.analyze_pkg(path)

        builds.append(build)

    # TODO: Make cli output or email results output configurable
    email_results(view.generate_output(builds))
