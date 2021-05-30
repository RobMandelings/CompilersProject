
class DataSegment:

    def __init__(self):
        self.lines = list()
        self.printf_strings = dict()

    def add_printf_string(self, key, value: list):
        self.printf_strings[key] = value
