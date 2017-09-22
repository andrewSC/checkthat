
class BuildError(Exception):
    def __init__(self, message, errors):
        super(BuildError, self).__init__(message)

        self.errors = errors
