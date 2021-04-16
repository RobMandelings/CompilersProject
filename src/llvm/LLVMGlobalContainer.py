import src.DataType as DataType
import src.llvm.LLVMInterfaces as LLVMInterfaces


class LLVMGlobalContainer(LLVMInterfaces.IToLLVM):
    """
    Contains all global instructions that do not belong in any function
    """

    def update_numbering(self, counter):
        pass

    def __init__(self):
        self.global_declaration_instructions = list()
        self.__printf_type_strings = dict()
        pass

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
        for global_declaration in self.global_declaration_instructions:
            string_to_return += global_declaration + "\n"
        return string_to_return
