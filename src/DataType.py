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
    def is_richer_than(data_type1, data_type2):
        assert isinstance(data_type1, DataTypeToken) and isinstance(data_type2, DataTypeToken)
        return data_type1.value > data_type2.value


class DataType:
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
        assert isinstance(self.__data_type_token, DataTypeToken)

    def __str__(self):
        return self.get_name()

    @staticmethod
    def get_resulting_data_type(data_type1, data_type2):
        """
        Returns the resulting data type, given the fact that they aren't pointers. This compiler doesn't
        support implicit conversion of types yet.
        """
        assert isinstance(data_type1, DataType) and isinstance(data_type2, DataType)
        assert data_type1.get_pointer_level() == data_type2.get_pointer_level() == 0
        if DataTypeToken.is_richer_than(data_type1.get_token(), data_type2.get_token()):
            return data_type1
        else:
            return data_type2

    def __eq__(self, other):
        return self.get_token() == other.get_token() and self.get_pointer_level() == other.get_pointer_level()

    def equals(self, other):
        assert isinstance(other, DataType)
        return self.__eq__(other)

    def get_token(self):
        """
        Returns the underlying data type such as char, int or bool regardless of pointer level
        """
        assert isinstance(self.__data_type_token, DataTypeToken)
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
        pointer_level = self.get_pointer_level()
        return self.get_token().get_llvm_name() + ('*' * self.get_pointer_level())


def get_llvm_for_data_type(data_type_token: DataTypeToken, pointer_level):
    """
    A helper function to easily get the llvm name of artbitrary DataTypes with given pointer level.
    Use this function if you don't have an instance of the specific DataType to get the llvm name for.
    (look at alloca instruction)
    """
    return DataTypeToken.get_llvm_name(data_type_token) + ('*' * pointer_level)


# Final

NORMAL_BOOL = DataType(DataTypeToken.BOOL, 0)
NORMAL_CHAR = DataType(DataTypeToken.CHAR, 0)
NORMAL_INT = DataType(DataTypeToken.INT, 0)
NORMAL_FLOAT = DataType(DataTypeToken.FLOAT, 0)
NORMAL_DOUBLE = DataType(DataTypeToken.DOUBLE, 0)
