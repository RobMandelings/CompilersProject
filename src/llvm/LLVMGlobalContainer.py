import src.DataType as DataType
import src.llvm.LLVMInterfaces as LLVMInterfaces


class LLVMGlobalContainer(LLVMInterfaces.IToLLVM):
    """
    Contains all global instructions that do not belong in any function
    """

    def update_numbering(self, counter):
        pass

    def __init__(self):
        self.global_strings = list()
        self.global_declaration_instructions = list()
        self.global_array_declaration_instructions = list()
        self.__printf_type_strings = dict()
        self.__memcpy_declaration_added = False
        pass

    def add_memcpy_declaration(self):
        if not self.__memcpy_declaration_added:
            self.global_declaration_instructions.append(
                'declare void @llvm.memcpy.p0i8.p0i8.i64(i8* noalias nocapture writeonly,'
                ' i8* noalias nocapture readonly, i64, i1 immarg)')
            self.__memcpy_declaration_added = True

    def add_global_string(self, length, string):
        string_created = f"@.str.{len(self.global_strings)}"
        self.global_strings.append(
            f"{string_created} = "
            f"private unnamed_addr constant [{length} x i8] c\"{string}\", align 1")
        return string_created

    def has_printf_type_string(self):
        return len(self.__printf_type_strings) > 0

    def __add_printf_type_string(self, data_type_to_print: DataType.DataType):

        global_variable = f'@.str.{len(self.global_declaration_instructions)}'

        # E.g. %i for printf('%i', int)
        # Null termination is necessary
        c_type_selection = None
        if data_type_to_print == DataType.NORMAL_CHAR:
            c_type_selection = '%c'
        elif data_type_to_print == DataType.NORMAL_INT:
            c_type_selection = '%i'
        elif data_type_to_print == DataType.NORMAL_FLOAT:
            c_type_selection = '%f'
        else:
            raise NotImplementedError

        global_declaration_instruction = f'{global_variable} = private unnamed_addr constant [3 x i8] c"{c_type_selection}\\00", align 1'
        self.global_declaration_instructions.append(global_declaration_instruction)
        self.__printf_type_strings[data_type_to_print.get_name()] = global_variable

    def get_printf_type_string(self, data_type_to_print: DataType.DataType):
        """
        Returns the global constant that holds the type to print
        For example, they would be defined as follows: @.i = private unnamed_addr constant [3 x i8] c"%i\00", align 1
        This @.i corresponds to '%i' type to print in c ( printf('%i', your_int) )
        """
        if data_type_to_print.is_pointer():
            # TODO implement
            raise NotImplementedError
        else:

            data_type_name = data_type_to_print.get_name()

            printf_type_string = self.__printf_type_strings.get(data_type_name)

            if printf_type_string is None:
                self.__add_printf_type_string(data_type_to_print)
                printf_type_string = self.__printf_type_strings.get(data_type_name)

            assert printf_type_string is not None
            return printf_type_string

    def to_llvm(self):
        string_to_return = ''
        for global_string in self.global_strings:
            string_to_return += global_string + "\n"
        for global_declaration in self.global_declaration_instructions:
            string_to_return += global_declaration + "\n"
        for array_declaration in self.global_array_declaration_instructions:
            string_to_return += array_declaration + "\n"
        return string_to_return
