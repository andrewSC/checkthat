
class Build:
    def __init__(self, status_msg='', total_build_time=0, namcap=None):
        self.status_msg = status_msg
        self.total_build_time = total_build_time
        self.namcap = namcap


class BuildSuccess(Build):
    def __init__(self, *args, **kwargs):
        super(BuildSuccess, self).__init__(*args, **kwargs)


class BuildFailure(Build):
    def __init__(self, error_msgs=[], *args, **kwargs):
        self.error_msgs = error_msgs
        super(BuildFailure, super).__init__(*args, **kwargs)


class Namcap:
    def __init__(self, msgs=[]):
        self.msgs = msgs


class NamcapPkgAnalysis:
    def __init__(self, *args, **kwargs):
        super(NamcapPkgAnalysis, self).__init__(*args, **kwargs)


class NamcapPkgBuildAnalysis:
    def __init__(self, *args, **kwargs):
        super(NamcapPkgBuildAnalysis, self).__init__(*args, **kwargs)
