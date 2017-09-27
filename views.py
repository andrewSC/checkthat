
class Formatter:
    def __init__(self):
        self.char_padding_len = 30


class OutputFormatter(Formatter):

    def get_build_header(self):
        return "{0} Build Results {0}".format('-' * self.char_padding_len)


class EmailFormatter(OutputFormatter):
    def __init__(self):
        super(EmailFormatter, self).__init__()


class ConsoleFormatter(OutputFormatter):
    pass
