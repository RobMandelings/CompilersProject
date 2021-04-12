from enum import Enum


class NamedEnum(Enum):
    def __new__(cls, *args, **kwargs):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, token_name: str):
        assert isinstance(token_name, str)
        self.token_name = token_name

    def __str__(self):
        return self.token_name


class DataTypeToken(NamedEnum):
    """
    Ordered from lowest precedence to highest precedence
    """
    # Indicates the richness of the datatype, from low to high
    BOOL = ('bool', False)
    CHAR = ('char', False)
    INT = ('int', False)
    FLOAT = ('float', False)
    DOUBLE = ('double', False)
    BOOL_POINTER = ('bool*', True)
    CHAR_POINTER = ('char*', True)
    INT_POINTER = ('int*', True)
    FLOAT_POINTER = ('float*', True)
    DOUBLE_POINTER = ('double*', True)

    def __init__(self, token_name: str, pointer_type: bool):
        super().__init__(token_name)
        self.pointer_type = pointer_type

    def is_pointer_type(self):
        return self.pointer_type

    def is_integral_type(self):
        if self.is_pointer_type():
            print("WARN: what to do with pointer types?")
            raise NotImplementedError
        else:
            return self == DataTypeToken.BOOL or self == DataTypeToken.CHAR or self == DataTypeToken.INT

    def is_floating_point_type(self):
        print("WARN: no integral type automatically results in floating point type currently. Could be wrong")
        if self.is_pointer_type():
            return False
        else:
            return not self.is_integral_type()

    @staticmethod
    def from_str(name: str):
        if name.startswith('bool'):
            if name == 'bool*':
                return DataTypeToken.BOOL_POINTER
            else:
                return DataTypeToken.BOOL
        elif name.startswith('char'):
            if name == 'char*':
                return DataTypeToken.CHAR_POINTER
            else:
                return DataTypeToken.CHAR
        elif name.startswith('int'):
            if name == 'int*':
                return DataTypeToken.INT_POINTER
            else:
                return DataTypeToken.INT
        elif name.startswith('float'):
            if name == 'float*':
                return DataTypeToken.FLOAT_POINTER
            else:
                return DataTypeToken.FLOAT
        elif name.startswith('double'):
            if name == 'double*':
                return DataTypeToken.DOUBLE_POINTER
            else:
                return DataTypeToken.DOUBLE
        else:
            return None

    # Improve the methods below, maybe don't use them anymore as it would be part of the class

    def get_pointer_version(self):
        """
        Retrieves the pointer version of the given datatype (pointer = true)
        E.g. int -> int*
        Used in: computeExpression, ASTVariable. Take a look there
        """

        assert not self.is_pointer_type()

        if self == DataTypeToken.BOOL:
            return DataTypeToken.BOOL_POINTER
        elif self == DataTypeToken.CHAR:
            return DataTypeToken.CHAR_POINTER
        elif self == DataTypeToken.INT:
            return DataTypeToken.INT_POINTER
        elif self == DataTypeToken.FLOAT:
            return DataTypeToken.FLOAT_POINTER
        elif self == DataTypeToken.DOUBLE:
            return DataTypeToken.DOUBLE_POINTER
        else:
            raise NotImplementedError

    def get_normal_version(self):
        """
        Retrieves the normal version of the given datatype (pointer == false)
        E.g. int* -> int
        Used in: computeExpression. Take a look there
        """

        assert self.is_pointer_type()

        if self == DataTypeToken.BOOL_POINTER:
            return DataTypeToken.BOOL
        elif self == DataTypeToken.CHAR_POINTER:
            return DataTypeToken.CHAR
        elif self == DataTypeToken.INT_POINTER:
            return DataTypeToken.INT
        elif self == DataTypeToken.FLOAT_POINTER:
            return DataTypeToken.FLOAT
        else:
            raise NotImplementedError

    @staticmethod
    def is_richer_than(datatype1, datatype2):

        assert isinstance(datatype1, DataTypeToken) and isinstance(datatype2, DataTypeToken)
        assert not (datatype1.is_pointer_type() or datatype2.is_pointer_type())
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


class TypeAttributeToken(NamedEnum):
    CONST = 'const'

    @staticmethod
    def from_str(name: str):

        if name == 'const':
            return TypeAttributeToken.CONST
        else:
            return None


class IfStatementToken(NamedEnum):
    IF = 'if'
    ELSE_IF = 'else if'
    ELSE = 'else'

    @staticmethod
    def from_str(name: str):

        if name == 'if':
            return IfStatementToken.IF
        elif name == 'else if':
            return IfStatementToken.ELSE_IF
        elif name == 'else if':
            return IfStatementToken.ELSE
        else:
            return None


class UnaryArithmeticExprToken(NamedEnum):
    PLUS = '+'
    MINUS = '-'

    @staticmethod
    def from_str(name: str):

        if name == '+':
            return UnaryArithmeticExprToken.PLUS
        elif name == '-':
            return UnaryArithmeticExprToken.MINUS
        else:
            return None


class PointerExprToken(NamedEnum):
    DEREFERENCE = '*'
    ADDRESS = '&'

    @staticmethod
    def from_str(name: str):

        if name == '*':
            return PointerExprToken.PLUS
        elif name == '&':
            return PointerExprToken.MINUS
        else:
            return None


class BinaryArithmeticExprToken(NamedEnum):
    ADD = '+'
    SUB = '-'
    MUL = '*'
    DIV = '/'
    MOD = '%'

    @staticmethod
    def from_str(name: str):

        if name == '+':
            return BinaryArithmeticExprToken.ADD
        elif name == '-':
            return BinaryArithmeticExprToken.SUB
        elif name == '*':
            return BinaryArithmeticExprToken.MUL
        elif name == '/':
            return BinaryArithmeticExprToken.DIV
        elif name == '%':
            return BinaryArithmeticExprToken.MOD
        else:
            return None


class LogicalExprToken(NamedEnum):
    OR = '||'
    AND = '&&'
    NOT = '!'

    @staticmethod
    def from_str(name: str):
        if name == '||':
            return LogicalExprToken.OR
        elif name == '&&':
            return LogicalExprToken.AND
        elif name == '!':
            return LogicalExprToken.NOT
        else:
            return None


class BitwiseExprToken(NamedEnum):
    OR = '|'
    AND = '&'

    @staticmethod
    def from_str(name: str):
        if name == '|':
            return BitwiseExprToken.OR
        elif name == '&':
            return BitwiseExprToken.AND
        else:
            return None


class RelationalExprToken(NamedEnum):
    GREATER_THAN = '>'
    GREATER_THAN_OR_EQUALS = '>='
    LESS_THAN = '<'
    LESS_THAN_OR_EQUALS = '<='
    EQUALS = '=='
    NOT_EQUALS = '!='

    @staticmethod
    def from_str(name: str):
        if name == '>':
            return RelationalExprToken.GREATER_THAN
        elif name == '>=':
            return RelationalExprToken.GREATER_THAN_OR_EQUALS
        elif name == '<':
            return RelationalExprToken.LESS_THAN
        elif name == '<=':
            return RelationalExprToken.LESS_THAN_OR_EQUALS
        elif name == '==':
            return RelationalExprToken.EQUALS
        elif name == '!=':
            return RelationalExprToken.NOT_EQUALS
        else:
            return None


class ControlFlowToken(NamedEnum):
    BREAK = 'break'
    CONTINUE = 'continue'
    RETURN = 'return'

    @staticmethod
    def from_str(name: str):
        if name == 'break':
            return ControlFlowToken.BREAK
        elif name == 'continue':
            return ControlFlowToken.CONTINUE
        elif name == 'return':
            return ControlFlowToken.RETURN
        else:
            return None
