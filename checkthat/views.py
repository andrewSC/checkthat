from .models import BuildFailure


# TODO: Make this class and its methods better in general.
class View:
    def __init__(self):
        self.char_padding_len = 30

    def get_build_header(self):
        return "{0} Build Results {0}".format('-' * self.char_padding_len)

    def get_build_footer(self):
        return "-" * len(self.get_build_header())

    def get_failure_header(self):
        return "{0} Failures {0}".format('-' * self.char_padding_len)

    def get_failure_footer(self):
        return "-" * len(self.get_failure_header())

    def get_namcap_pkg_header(self):
        return "{0} Namcap Pkg Analysis {0}".format('-' * self.char_padding_len)

    def get_namcap_pkg_footer(self):
        return "-" * len(self.get_namcap_pkg_header())

    def get_namcap_pkgbuild_header(self):
        return "{0} Namcap PKGBUILD Analysis {0}".format('-' * self.char_padding_len)

    def get_namcap_pkgbuild_footer(self):
        return "-" * len(self.get_namcap_pkgbuild_header())


# TODO: Refactor EmailView and CliView to remove duplicate code!!
# TODO: Make this better ASAP
class CliView(View):
    def __init__(self):
        super(CliView, self).__init__()

    def generate_output(self, builds):
        total_build_time = 0
        has_failures = False

        print(self.get_build_header())

        for build in builds:
            print(build.status_msg)
            total_build_time += build.total_build_time

            if type(build) is BuildFailure:
                has_failures = True

        mins, secs = divmod(total_build_time, 60)
        print(f"Total build time: {mins}m {secs}s")
        print(self.get_build_footer())

        if has_failures:
            print(self.get_failure_header())
            for build in builds:
                if type(build) is BuildFailure:
                    header = f"xxxxxxxxxxxxxxx {build.status_msg} xxxxxxxxxxxxxxx"
                    footer = "x" * len(header)

                    print(header)
                    for error in build.error_msgs:
                        print(error)

                    print(footer)

            print(self.get_failure_footer())

        print(self.get_namcap_pkgbuild_header())
        for build in builds:
            msgs = build.namcap_pkgbuild_analysis.msgs

            # NOTE: We need to check the list to make sure it has actual
            # content and not just the empty string
            if any([item for item in msgs if item != '']):
                for msg in msgs:
                    print(msg)
        print(self.get_namcap_pkgbuild_footer())

        print(self.get_namcap_pkg_header())
        for build in builds:
            if type(build) is not BuildFailure:
                for msg in build.namcap_pkg_analysis.msgs:
                    print(msg)
        print(self.get_namcap_pkg_footer())


# TODO: Refactor EmailView and CliView to remove duplicate code!!
# TODO: Make this better ASAP
class EmailView(View):
    def __init__(self):
        super(EmailView, self).__init__()

    def generate_output(self, builds):
        total_build_time = 0
        has_failures = False
        output = []

        output.append(self.get_build_header() + '\n')

        for build in builds:
            output.append(build.status_msg + '\n')
            total_build_time += build.total_build_time

            if type(build) is BuildFailure:
                has_failures = True

        mins, secs = divmod(total_build_time, 60)
        output.append(f"\nTotal build time: {mins}m {secs}s\n")
        output.append(self.get_build_footer() + '\n\n')

        if has_failures:
            output.append(self.get_failure_header() + '\n')
            for build in builds:
                if type(build) is BuildFailure:
                    header = f"xxxxxxxxxxxxxxx {build.status_msg} xxxxxxxxxxxxxxx"
                    footer = "x" * len(header)

                    output.append('\n' + header + '\n')
                    for error in build.error_msgs:
                        output.append(error + '\n')

                    output.append(footer + '\n')

            output.append(self.get_failure_footer() + '\n\n')

        output.append(self.get_namcap_pkgbuild_header() + '\n')
        for build in builds:
            msgs = build.namcap_pkgbuild_analysis.msgs

            # NOTE: We need to check the list to make sure it has actual
            # content and not just the empty string
            if any([item for item in msgs if item != '']):
                for msg in msgs:
                    output.append(msg + '\n')

        output.append(self.get_namcap_pkgbuild_footer() + '\n\n')

        output.append(self.get_namcap_pkg_header() + '\n')
        for build in builds:
            if type(build) is not BuildFailure:
                for msg in build.namcap_pkg_analysis.msgs:
                    output.append(msg + '\n')

        output.append(self.get_namcap_pkg_footer() + '\n')

        return ''.join(output)
