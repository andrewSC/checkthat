import argparse
import datetime
import os
import smtplib
import toml

from pathlib import Path

from .models import BuildFailure
from .builders import PackageBuilder
from .views import CliView, EmailView


def gather_pkgbuild_paths(root_pkgs_dir):
    pkgbuild_paths = []

    for root, dirs, files in os.walk(root_pkgs_dir):
        if 'PKGBUILD' in files:
            pkgbuild_paths.append(root)

    return pkgbuild_paths


def email_results(frm, to, subject, message):
    server = smtplib.SMTP('localhost')
    now = datetime.datetime.now()
    subject += f" on {now.strftime('%Y-%m-%d %H:%M:%S')}"
    message = f"From: {frm}\r\nTo: {to}\r\nSubject: {subject} \r\n\r\n{message}"

    server.sendmail(frm, [to], message)
    server.quit()


def read_config(conf_path):
    with open(conf_path, 'r') as conf_file:
        return toml.load(conf_file)


def main():
    parser = argparse.ArgumentParser(description='A automated Arch Linux AUR package builder and analyzer written in Python')
    parser.add_argument('path', help='Path to where packages are located')
    args = parser.parse_args()

    config_path = '/'.join([str(Path(__file__).resolve().parents[1]), 'config.toml'])
    config = read_config(config_path)
    abs_paths = gather_pkgbuild_paths(args.path)  # ABS path to where all the folders for packages are located

    builder = PackageBuilder()
    builds = []

    for path in abs_paths:
        build = builder.build(path, config['fetch_latest'])

        if config['analyze_pkgbuild']:
            build.namcap_pkgbuild_analysis = builder.analyze_pkgbuild(path)

        if type(build) is not BuildFailure:
            # NOTE: We should only try to analyze the package if the build
            # was actually successful
            if config['analyze_package']:
                build.namcap_pkg_analysis = builder.analyze_pkg(path)

            if config['cleanup']:
                builder.cleanup(build)  # TODO: Make this better

        builds.append(build)

    if config['output'] == 'email':
        email_results(config['email']['addresses']['from'],
                      config['email']['addresses']['to'],
                      config['email']['subject'],
                      EmailView().generate_output(builds))

    elif config['output'] == 'cli':
        CliView().generate_output(builds)
