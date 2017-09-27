
class Build:
    def __init__(self, status_msg='', total_build_time=0, namcap=None):
        self.status_msg = status_msg
        self.total_build_time = total_build_time
        self.namcap = namcap


class BuildSuccess(Build):
    def __init__(self, **kwargs):
        super(BuildSuccess, self).__init__(**kwargs)


class BuildFailure(Build):
    def __init__(self, error_msgs=[], **kwargs):
        self.error_msgs = error_msgs
        super(BuildFailure, super).__init__(**kwargs)


class Namcap:
    def __init__(self, msgs=[]):
        self.msgs = msgs


class NamcapPkgAnalysis:
    def __init__(self, **kwargs):
        super(NamcapPkgAnalysis, self).__init__(**kwargs)


class NamcapPkgBuildAnalysis:
    def __init__(self, **kwargs):
        super(NamcapPkgBuildAnalysis, self).__init__(**kwargs)
