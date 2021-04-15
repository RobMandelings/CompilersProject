import abc

import src.enum_utils as enum_utils


class DataTypeToken(enum_utils.NamedEnum):
    """
    Ordered from lowest precedence to highest precedence
    """
    # Indicates the richness of the datatype, from low to high
    VOID = ('void', 'void')
    BOOL = ('bool', 'i1')
    CHAR = ('char', 'i8')
    INT = ('int', 'i32')
    FLOAT = ('float', 'float')
    DOUBLE = ('double', 'double')

    def __init__(self, token_name: str, llvm_name: str):
        super().__init__(token_name)
        self.llvm_name = llvm_name

    def is_integral_type(self):
        return self == DataTypeToken.BOOL or self == DataTypeToken.CHAR or self == DataTypeToken.INT

    def is_floating_point_type(self):
        return self == DataTypeToken.FLOAT or self == DataTypeToken.DOUBLE

    def get_name(self):
        return self.token_name

    def get_llvm_name(self):
        return self.llvm_name

    @staticmethod
    def from_str(name: str):
        if name == 'bool':
            return DataTypeToken.BOOL
        if name == 'char':
            return DataTypeToken.CHAR
        if name == 'int':
            return DataTypeToken.INT
        if name == 'float':
            return DataTypeToken.FLOAT
        if name == 'double':
            return DataTypeToken.DOUBLE
        else:
            return None

    @staticmethod
    def is_richer_than(datatype1, datatype2):

        assert isinstance(datatype1, DataTypeToken) and isinstance(datatype2, DataTypeToken)
        """
        Checks whether the first data_type given is richer than the second (richness can be checked above in the _order_ variable)
        """
        return datatype1.value > datatype2.value

    @staticmethod
    def get_richest_data_type(data_type1, data_type2):
        """
        Checks which data type is the richest and returns an index based on the result

        returns:
        0 if datatype1 is the richest data type
        1 if datatype2 is the richest data type
        -1 if they are equally rich
        """

        if DataTypeToken.is_richer_than(data_type1, data_type2):
            return 0
        elif DataTypeToken.is_richer_than(data_type2, data_type1):
            return 1
        else:
            return -1

    @staticmethod
    def get_resulting_data_type(data_type1, data_type2):
        """
        Returns the richest of the two data_types given to be the resulting data type (of an operation)
        """
        if DataTypeToken.is_richer_than(data_type1, data_type2):
            return data_type1
        else:
            return data_type2


class DataType(abc.ABC):
    """
    Uses the DataTypeToken enum under the hood, but also takes into account the pointer levels
    """

    def __init__(self, data_type_token: DataTypeToken, pointer_level: int):
        """
        These are private variables and should not be adjusted once the instance is created
        """
        self.__data_type_token = data_type_token
        self.__pointer_level = pointer_level
        assert self.__pointer_level >= 0, "The pointer level should be at least 0."

    @staticmethod
    def is_richer_than(data_type1, data_type2):
        assert isinstance(data_type1, DataType) and isinstance(data_type2, DataType)
        if data_type1.get_pointer_level() == data_type2.get_pointer_level():
            return DataTypeToken.is_richer_than(data_type1.get_token(), data_type2.get_token())
        else:
            raise ValueError(
                f'Cannot compare richness due to different pointer levels: '
                f'{data_type1.get_pointer_level()} and {data_type2.get_pointer_level()}')

    def equals(self, data_type):
        assert isinstance(data_type, DataType)
        return self.get_token() == data_type.get_token() and self.get_pointer_level() == data_type.get_pointer_level()

    def get_token(self):
        """
        Returns the underlying data type such as char, int or bool regardless of pointer level
        """
        return self.__data_type_token

    def get_name(self):
        """
        Returns the name of the data type, taking in account the pointer level as well (e.g. bool**)
        """
        return self.__data_type_token.get_name() + ('*' * self.__pointer_level)

    def get_pointer_level(self):
        assert self.__pointer_level >= 0, "Pointer level must be at least 0"
        return self.__pointer_level

    def is_pointer(self):
        return self.get_pointer_level() > 0

    def get_llvm_name(self):
        return self.get_token().get_llvm_name() + ('*' * self.get_pointer_level())


class BoolDataType(DataType):

    def __init__(self, pointer_level: int):
        super().__init__(DataTypeToken.BOOL, pointer_level)


class CharDataType(DataType):

    def __init__(self, pointer_level: int):
        super().__init__(DataTypeToken.CHAR, pointer_level)


class IntDataType(DataType):

    def __init__(self, pointer_level: int):
        super().__init__(DataTypeToken.INT, pointer_level)


class FloatDataType(DataType):

    def __init__(self, pointer_level: int):
        super().__init__(DataTypeToken.FLOAT, pointer_level)


class DoubleDataType(DataType):

    def __init__(self, pointer_level: int):
        super().__init__(DataTypeToken.DOUBLE, pointer_level)


class VoidDataType(DataType):

    def __init__(self, pointer_level: int):
        assert pointer_level > 0, "Void datatype must at least be of pointer level 1"
        super().__init__(DataTypeToken.VOID, pointer_level)
