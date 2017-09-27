
class Build:
    def __init__(self, status_msg='', total_build_time=0, namcap_pkg_analysis=None, namcap_pkgbuild_analysis=None):
        self.status_msg = status_msg
        self.total_build_time = total_build_time
        self.namcap_pkg_analysis = namcap_pkg_analysis
        self.namcap_pkgbuild_analysis = namcap_pkgbuild_analysis


class BuildSuccess(Build):
    def __init__(self, *args, **kwargs):
        super(BuildSuccess, self).__init__(*args, **kwargs)


class BuildFailure(Build):
    def __init__(self, error_msgs=[], *args, **kwargs):
        self.error_msgs = error_msgs
        super(BuildFailure, self).__init__(*args, **kwargs)


class Namcap:
    def __init__(self, msgs=[]):
        self.msgs = msgs


class NamcapPkgAnalysis(Namcap):
    def __init__(self, *args, **kwargs):
        super(NamcapPkgAnalysis, self).__init__(*args, **kwargs)


class NamcapPkgBuildAnalysis(Namcap):
    def __init__(self, *args, **kwargs):
        super(NamcapPkgBuildAnalysis, self).__init__(*args, **kwargs)
