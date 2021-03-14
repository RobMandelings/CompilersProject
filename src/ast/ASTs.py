from .ASTToken import ASTToken, TokenType
from src.ast.IAstVisitor import IASTVisitor


class AST:

    def __init__(self, token: ASTToken):
        self.parent = None
        self.token = token

    def __str__(self):
        return self.get_token_content()

    def set_parent(self, parent):
        assert isinstance(parent, AST) and not isinstance(parent, ASTLeaf)
        self.parent = parent
        return self

    def is_root(self):
        return self.parent is None

    def accept(self, visitor):
        raise NotImplementedError('Generic method')

    def get_token(self):
        assert isinstance(self.token, ASTToken)
        return self.token

    def get_token_type(self):
        assert isinstance(self.token, ASTToken)
        assert isinstance(self.token.token_type, TokenType)
        return self.token.token_type

    def get_token_content(self):
        token_content = self.get_token().content
        assert isinstance(token_content, str)
        return token_content


class ASTLeaf(AST):

    def __init__(self, token: ASTToken):
        super().__init__(token)

    def accept(self, visitor: IASTVisitor):
        assert isinstance(visitor, IASTVisitor)
        visitor.visit_ast_leaf(self)


class ASTInternal(AST):

    def __init__(self, token: ASTToken):
        super().__init__(token)
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


class ASTBinaryExpression(AST):

    def __init__(self, token: ASTToken, left: AST, right: AST):
        super().__init__(token)
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self
        assert isinstance(self.left, AST) and isinstance(self.right, AST)
        if self.token.token_type == TokenType.ASSIGNMENT_EXPRESSION:
            assert isinstance(self.left, ASTLeaf) and self.left.token.token_type == TokenType.IDENTIFIER

    def accept(self, visitor: IASTVisitor):
        visitor.visit_ast_binary_expression(self)

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right


class ASTAssignmentExpression(ASTBinaryExpression):

    def __init__(self, left: ASTLeaf, right: AST):
        super().__init__(ASTToken(TokenType.ASSIGNMENT_EXPRESSION, '='), left, right)
        assert isinstance(left, ASTLeaf)

    def accept(self, visitor: IASTVisitor):
        visitor.visit_ast_assignment_expression(self)

    def get_left(self):
        """
        Inherits get_left from ASTBinaryExpression to do an extra check: the left must be a leaf in this case
        """
        assert isinstance(self.left, ASTLeaf) and self.left.get_token_type() == TokenType.IDENTIFIER
        return self.left


class ASTVariableDeclaration(AST):

    def __init__(self, type_attributes: list, name: ASTLeaf):
        super().__init__(ASTToken(TokenType.VARIABLE_DECLARATION))
        self.type_attributes = list()
        self.set_type_attributes(type_attributes)
        for attribute in self.type_attributes:
            attribute.parent = self

        self.var_name = name
        self.var_name.parent = self

    def __str__(self):
        return self.get_token_content()

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
        self.token = ASTToken(TokenType.VARIABLE_DECLARATION_AND_INIT)
        self.value = value
        self.value.parent = self

    def accept(self, visitor):
        visitor.visit_ast_variable_declaration_and_init(self)
