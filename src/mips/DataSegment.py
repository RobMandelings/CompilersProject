class DataSegment:

    def __init__(self):
        """
        string_lines: lines in the data segment which have an ascii or asciiz 'data type'
        floating_point_lines: lines in the data segment which have a .float as data type
        """
        self.ascii_data = list()
        self.floating_point_data = list()
        self.printf_strings = dict()

    def get_printf_string(self, key):
        return self.printf_strings[key]

    def add_printf_string(self, key, value: list):
        self.printf_strings[key] = value

    def add_ascii_data(self, string_element: str, last_element: bool = False):
        identifier = f'ascii_word{len(self.ascii_data)}'
        if last_element:
            self.ascii_data.append(f'{identifier}: .asciiz {string_element}')
        else:
            self.ascii_data.append(f'{identifier}: .ascii {string_element}')
        return identifier

    def add_floating_point_number(self, value: float):
        """
        Adds a floating point number to the data, and returns the identifier of the added data
        """
        identifier = f"floating_point{len(self.floating_point_data)}"
        self.floating_point_data.append(f'{identifier}: .float {value}')
        return identifier

    def to_mips(self):
        mips_code = ".data\n\n"

        for current_line in self.ascii_data:
            mips_code += f"  {current_line}\n"

        for current_line in self.floating_point_data:
            mips_code += f"  {current_line}\n"

        mips_code += "\n"

        return mips_code
