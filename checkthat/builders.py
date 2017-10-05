import subprocess
import os
import time
import sys

from models import BuildSuccess, BuildFailure, NamcapPkgAnalysis, NamcapPkgBuildAnalysis, PkgbuildFetchFailure


# TODO: Refactor subprocess run logic into generic method
class PackageBuilder:
    def build(self, pkgbuild_path, fetch_latest_pkgbuild=False):
        if fetch_latest_pkgbuild:
            self.__fetch_latest_pkgbuild(pkgbuild_path)

        cmd = [
            'makepkg',
            '-cCmf'
        ]
        orig_dir = os.getcwd()
        os.chdir(pkgbuild_path)
        start_time = time.time()

        proc_result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        end_time = time.time()
        total_time = end_time - start_time
        cmd_output = proc_result.stdout.decode('UTF-8')

        os.chdir(orig_dir)

        if proc_result.returncode != 0:
            # NOTE: If there's any output from the linter, strip newlines from the output
            # then return a list where each item is a single line of output from namcap
            return BuildFailure(error_msgs=cmd_output.rstrip('\n').rsplit('\n'),
                                status_msg=f"Failed building [{pkgbuild_path}]",
                                total_build_time=total_time)

        pkg_name = self.__generate_built_package_name(pkgbuild_path)

        return BuildSuccess(status_msg=f"Successfully built [{pkg_name}]",
                            total_build_time=total_time,
                            pkg_name=pkg_name,
                            pkg_path=pkgbuild_path)  # TODO: Make this better

    def cleanup(self, success_build):
        cmd = [
            'rm',
            '/'.join([success_build.pkg_path, success_build.pkg_name])
        ]

        orig_dir = os.getcwd()
        os.chdir(success_build.pkg_path)

        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        # TODO: Log outputs of git subprocesses to output

        os.chdir(orig_dir)

    def analyze_pkg(self, pkg_path):
        cmd = [
            sys.executable,
            '/usr/lib/python3.6/site-packages/namcap.py',  # TODO: Remove hardcoded path
            '-i',
            '/'.join([pkg_path, self.__generate_built_package_name(pkg_path)])
        ]
        proc_result = subprocess.run(cmd, stdout=subprocess.PIPE)
        cmd_output = proc_result.stdout.decode('UTF-8')

        # NOTE: If there's any output from the linter, strip newlines from the output
        # then return a list where each item is a single line of output from namcap
        return NamcapPkgAnalysis(cmd_output.rstrip('\n').rsplit('\n'))

    def analyze_pkgbuild(self, pkgbuild_path):
        cmd = [
            sys.executable,
            '/usr/lib/python3.6/site-packages/namcap.py',  # TODO: Remove hardcoded path
            '-i',
            '/'.join([pkgbuild_path, 'PKGBUILD'])
        ]
        proc_result = subprocess.run(cmd, stdout=subprocess.PIPE)
        cmd_output = proc_result.stdout.decode('UTF-8')

        # NOTE: If there's any output from the linter, strip newlines from the output
        # then return a list where each item is a single line of output from namcap
        return NamcapPkgBuildAnalysis(cmd_output.rstrip('\n').rsplit('\n'))

    def __fetch_latest_pkgbuild(self, pkgbuild_path):
        cmd_fetch = ['git', 'fetch', '-all']
        cmd_reset = ['git', 'reset', '--hard', 'origin/master']
        orig_dir = os.getcwd()
        os.chdir(pkgbuild_path)

        subprocess.run(cmd_fetch, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        subprocess.run(cmd_reset, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # TODO: Log outputs of git subprocesses to output

        os.chdir(orig_dir)

    def __generate_built_package_name(self, pkgbuild_path):
        name = None
        cmd = [
            'makepkg',
            '--packagelist'
        ]
        orig_dir = os.getcwd()
        os.chdir(pkgbuild_path)

        proc_result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        cmd_output = proc_result.stdout.decode('UTF-8')
        pkgnames = cmd_output.rstrip('\n').rsplit('\n')

        # TODO: Make this better
        for root, dirs, filenames in os.walk('.'):
            for filename in filenames:
                for pkgname in pkgnames:
                    if pkgname in filename:
                        name = filename

        os.chdir(orig_dir)
        return name
