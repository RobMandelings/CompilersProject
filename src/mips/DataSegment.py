class DataSegment:

    def __init__(self):
        """
        string_lines: lines in the data segment which have an ascii or asciiz 'data type'
        floating_point_lines: lines in the data segment which have a .float as data type
        """
        self.ascii_data = list()
        self.floating_point_data = list()
        self.printf_strings = dict()

    def add_printf_string(self, key, value: list):
        """
        Adds a ascii word to the data, and returns the identifier of the added data
        """
        identifier = f"ascii_word_{len(self.ascii_data)}"
        self.printf_strings[key] = value
        return identifier

    def add_floating_point_number(self, value: float):
        """
        Adds a floating point number to the data, and returns the identifier of the added data
        """
        identifier = f"floating_point{len(self.floating_point_data)}"
        self.floating_point_data.append(f'{identifier}: .float {value}')
        return identifier
