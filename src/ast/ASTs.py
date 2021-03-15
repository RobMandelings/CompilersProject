from abc import abstractmethod

from src.ast.ASTTokens import *
from src.ast.IAstVisitor import IASTVisitor


class AST:

    def __init__(self, content: str):
        self.parent = None
        self.content = content

    def __str__(self):
        return self.get_content()

    def set_parent(self, parent):
        assert isinstance(parent, AST) and not isinstance(parent, ASTLeaf)
        self.parent = parent
        return self

    def is_root(self):
        return self.parent is None

    def accept(self, visitor: IASTVisitor):
        raise NotImplementedError('Generic method')

    def get_content(self):
        assert isinstance(self.content, str)
        return self.content


class Tokenable:
    """
    Interface which provides a get_token method for the ASTs which contain tokens
    """

    @abstractmethod
    def get_token(self):
        pass


class ASTLeaf(AST):

    def __init__(self, content: str):
        super().__init__(content)

    def accept(self, visitor: IASTVisitor):
        assert isinstance(visitor, IASTVisitor)
        visitor.visit_ast_leaf(self)


class ASTLiteral(ASTLeaf, Tokenable):

    def __init__(self, token: LiteralToken, content: str):
        super().__init__(content)
        self.token = token

    def get_token(self):
        assert isinstance(self.token, LiteralToken)
        return self.token

    def accept(self, visitor: IASTVisitor):
        assert isinstance(visitor, IASTVisitor)
        visitor.visit_ast_literal(self)


class ASTDataType(ASTLeaf, Tokenable):

    def __init__(self, token: DataTypeToken):
        content = None
        if token == DataTypeToken.CHAR:
            content = 'char'
        elif token == DataTypeToken.INT:
            content = 'int'
        elif token == DataTypeToken.FLOAT:
            content = 'float'
        elif token == DataTypeToken.CONST_TYPE:
            content = 'const'
        assert content is not None
        super().__init__(content)
        self.token = token

    def get_token(self):
        assert isinstance(self.token, DataTypeToken)
        return self.token

    def accept(self, visitor: IASTVisitor):
        assert isinstance(visitor, IASTVisitor)
        visitor.visit_ast_data_type(self)


class ASTTypeAttribute(ASTLeaf, Tokenable):

    def __init__(self, token: TypeAttributeToken):
        content = None
        if token == TypeAttributeToken.CONST:
            content = 'const'
        assert content is not None
        super().__init__(content)
        self.token = token

    def get_token(self):
        assert isinstance(self.token, TypeAttributeToken)
        return self.token

    def accept(self, visitor: IASTVisitor):
        assert isinstance(visitor, IASTVisitor)
        visitor.visit_ast_data_type(self)


class ASTIdentifier(ASTLeaf):

    def __init__(self, content: str):
        super().__init__(content)

    def accept(self, visitor: IASTVisitor):
        visitor.visit_ast_identifier(self)


class ASTInternal(AST):

    def __init__(self, content: str):
        super().__init__(content)
        self.children = list()

    def accept(self, visitor: IASTVisitor):
        visitor.visit_ast_internal(self)

    def add_child(self, child):
        assert child is not None

        if isinstance(child, list):
            for sub_child in child:
                self.add_child(sub_child)
        else:
            child.parent = self
            self.children.append(child)


class ASTUnaryExpression(AST, Tokenable):

    def __init__(self, token: UnaryExprToken, value_applied_to: AST):
        if token == UnaryExprToken.UNARY_PLUS_EXPRESSION:
            content = '+'
        elif token == UnaryExprToken.UNARY_MINUS_EXPRESSION:
            content = '-'
        elif token == UnaryExprToken.DEREFERENCE_EXPRESSION:
            content = '*'
        elif token == UnaryExprToken.ADDRESS_EXPRESSION:
            content = '&'
        else:
            raise NotImplementedError

        super().__init__(content)
        # The value this unary expression is applied to
        self.value_applied_to = value_applied_to
        self.value_applied_to.parent = self
        self.token = token

    def get_token(self):
        assert isinstance(self.token, UnaryExprToken)
        return self.token

    def accept(self, visitor: IASTVisitor):
        visitor.visit_ast_unary_expression(self)


class ASTBinaryExpression(AST):

    def __init__(self, content: str, left: AST, right: AST):
        assert isinstance(left, AST) and isinstance(right, AST)
        super().__init__(content)
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self

    def accept(self, visitor: IASTVisitor):
        visitor.visit_ast_binary_expression(self)

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right


class ASTAssignmentExpression(ASTBinaryExpression):

    def __init__(self, left: ASTLeaf, right: AST):
        assert isinstance(left, ASTLeaf)
        super().__init__('=', left, right)

    def accept(self, visitor: IASTVisitor):
        visitor.visit_ast_assignment_expression(self)

    def get_left(self):
        """
        Inherits get_left from ASTBinaryExpression to do an extra check: the left must be an identifier in this case
        """
        assert isinstance(self.left, ASTIdentifier)
        return self.left


class ASTBinaryArithmeticExpression(ASTBinaryExpression, Tokenable):

    def __init__(self, token: BinaryArithmeticExprToken, left: AST, right: AST):
        content = None
        if token == BinaryArithmeticExprToken.ADD_EXPRESSION:
            content = '+'
        elif token == BinaryArithmeticExprToken.SUB_EXPRESSION:
            content = '-'
        elif token == BinaryArithmeticExprToken.MUL_EXPRESSION:
            content = '*'
        elif token == BinaryArithmeticExprToken.DIV_EXPRESSION:
            content = '/'
        assert content is not None
        super().__init__(content, left, right)
        self.token = token

    def get_token(self):
        assert isinstance(self.token, BinaryArithmeticExprToken)
        return self.token

    def accept(self, visitor: IASTVisitor):
        visitor.visit_ast_binary_arithmetic_expression(self)


class ASTBinaryCompareExpression(ASTBinaryExpression, Tokenable):

    def __init__(self, token: BinaryCompareExprToken, left: AST, right: AST):
        content = None
        if token == BinaryCompareExprToken.LESS_THAN_EXPRESSION:
            content = '<'
        elif token == BinaryCompareExprToken.GREATER_THAN_EXPRESSION:
            content = '>'
        elif token == BinaryCompareExprToken.EQUALS_EXPRESSION:
            content = '=='
        assert content is not None
        super().__init__(content, left, right)
        self.token = token

    def get_token(self):
        assert isinstance(self.token, BinaryCompareExprToken)
        return self.token

    def accept(self, visitor: IASTVisitor):
        visitor.visit_ast_binary_compare_expression(self)


class ASTVariableDeclaration(AST):

    def __init__(self, type_attributes: list, name: ASTLeaf):
        super().__init__('variable declaration')
        self.type_attributes = list()
        self.set_type_attributes(type_attributes)
        for attribute in self.type_attributes:
            attribute.parent = self

        self.var_name = name
        self.var_name.parent = self

    def set_type_attributes(self, type_attributes: list):
        """
        Performs a recursion to make sure the list only consists of ast elements within instead of other lists
        """
        for attribute in type_attributes:
            if isinstance(attribute, list):
                self.set_type_attributes(attribute)
            else:
                self.type_attributes.append(attribute)

    def accept(self, visitor: IASTVisitor):
        visitor.visit_ast_variable_declaration(self)


class ASTVariableDeclarationAndInit(ASTVariableDeclaration):

    def __init__(self, type_attributes: list, name: ASTLeaf, value: AST):
        super().__init__(type_attributes, name)
        self.content += ' and init'
        self.value = value
        self.value.parent = self

    def accept(self, visitor):
        visitor.visit_ast_variable_declaration_and_init(self)


class ASTPrintfInstruction(AST):

    def __init__(self, value_to_print):
        super().__init__(str(value_to_print))

    def accept(self, visitor: IASTVisitor):
        visitor.visit_ast_printf_instruction(self)
