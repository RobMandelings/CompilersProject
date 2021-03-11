from enum import Enum, auto
from .ASTVisitors import ASTVisitor


class TokenType(Enum):
    PROGRAM = auto()
    INSTRUCTIONS = auto()
    INSTRUCTION = auto()

    UNARY_EXPRESSION = auto()
    UNARY_PLUS_OPERATOR = auto()
    UNARY_MINUS_OPERATOR = auto()
    DEREFERENCE_OPERATOR = auto()
    ADDRESS_OPERATOR = auto()

    ADD_EXPRESSION = auto()
    SUB_EXPRESSION = auto()
    MULT_EXPRESSION = auto()
    DIV_EXPRESSION = auto()
    GREATER_THAN_EXPRESSION = auto()
    LESS_THAN_EXPRESSION = auto()
    EQUALS_EXPRESSION = auto()
    ASSIGNMENT_EXPRESSION = auto()

    IDENTIFIER = auto()

    DOUBLE_LITERAL = auto()
    INT_LITERAL = auto()

    VARIABLE_DECLARATION = auto()
    VARIABLE_DECLARATION_AND_INIT = auto()
    INT_TYPE = auto()
    FLOAT_TYPE = auto()
    CHAR_TYPE = auto()
    CONST_TYPE = auto()


class ASTToken:

    def __init__(self, token_type, content=None):

        self.token_type = token_type
        if content is not None:
            self.content = content
        else:
            self.content = self.token_type.name.lower().replace("_", " ")


class AST:

    def __init__(self, token: ASTToken):
        self.parent = None
        self.token = token

    def isRoot(self):
        return self.parent is None

    def accept(self, visitor):
        raise NotImplementedError('Generic method')

    def get_token(self):
        assert isinstance(self.token, ASTToken)
        return self.token

    def get_token_content(self):
        token_content = self.get_token().content
        assert isinstance(token_content, str)
        return token_content


class ASTLeaf(AST):

    def __init__(self, token: ASTToken):
        super().__init__(token)

    def accept(self, visitor: ASTVisitor):
        assert isinstance(visitor, ASTVisitor)
        visitor.visit_ast_leaf(self)


class ASTInternal(AST):

    def __init__(self, token: ASTToken):
        super().__init__(token)
        self.children = list()

    def accept(self, visitor: ASTVisitor):
        for child in self.children:
            assert isinstance(child, AST)
            child.accept(visitor)
        visitor.visit_ast_internal(self)

    def addChild(self, child):
        assert child is not None

        if isinstance(child, list):
            for sub_child in child:
                self.addChild(sub_child)
        else:
            child.parent = self
            self.children.append(child)


class ASTVariableDeclaration(AST):

    def __init__(self, type_attributes: list, name: ASTLeaf):
        super().__init__(ASTToken(TokenType.VARIABLE_DECLARATION))
        self.type_attributes = list()
        # Performs a recursion to make sure the list only consists of ast elements within instead of other lists
        self.set_type_attributes(type_attributes)
        for attribute in self.type_attributes:
            attribute.parent = self

        self.var_name = name
        self.var_name.parent = self

    def __str__(self):
        return self.get_token_content()

    def set_type_attributes(self, type_attributes: list):
        for attribute in type_attributes:
            if isinstance(attribute, list):
                self.set_type_attributes(attribute)
            else:
                self.type_attributes.append(attribute)

    def accept(self, visitor: ASTVisitor):
        for attribute in self.type_attributes:
            attribute.accept(visitor)
        self.var_name.accept(visitor)
        visitor.visit_ast_variable_declaration(self)


class ASTVariableDeclarationAndInit(ASTVariableDeclaration):

    def __init__(self, type_attributes: list, name: ASTLeaf, value: AST):
        super().__init__(type_attributes, name)
        self.token = ASTToken(TokenType.VARIABLE_DECLARATION_AND_INIT)
        self.value = value
        self.value.parent = self

    def accept(self, visitor):
        for attribute in self.type_attributes:
            attribute.accept(visitor)
        self.var_name.accept(visitor)
        self.value.accept(visitor)
        visitor.visit_ast_variable_declaration_and_init(self)
