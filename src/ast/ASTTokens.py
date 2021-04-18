import src.enum_utils as enum_utils


class TypeAttributeToken(enum_utils.NamedEnum):
    CONST = 'const'

    @staticmethod
    def from_str(name: str):

        if name == 'const':
            return TypeAttributeToken.CONST
        else:
            return None


class IfStatementToken(enum_utils.NamedEnum):
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


class UnaryArithmeticExprToken(enum_utils.NamedEnum):
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


class BinaryArithmeticExprToken(enum_utils.NamedEnum):
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


class LogicalExprToken(enum_utils.NamedEnum):
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


class BitwiseExprToken(enum_utils.NamedEnum):
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


class RelationalExprToken(enum_utils.NamedEnum):
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


class ControlFlowToken(enum_utils.NamedEnum):
    """
    Control flow tokens break and continue are placed here, not the control flow token return
    because it can also take a return value
    """
    BREAK = 'break'
    CONTINUE = 'continue'

    @staticmethod
    def from_str(name: str):
        if name == 'break':
            return ControlFlowToken.BREAK
        elif name == 'continue':
            return ControlFlowToken.CONTINUE
        else:
            return None
