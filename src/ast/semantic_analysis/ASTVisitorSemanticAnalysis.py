from src.ast.ASTBaseVisitor import ASTBaseVisitor
from src.ast.ASTs import *
from src.ast.ASTTokens import *
from src.ast.semantic_analysis.SymbolTable import *


class SemanticError(Exception):
    pass


class AlreadyDeclaredError(SemanticError):
    pass


class UndeclaredError(SemanticError):
    pass


class UninitializedError(SemanticError):
    pass


class IncompatibleTypesError(Exception):
    pass


class ASTVisitorResultingDataType(ASTBaseVisitor):
    """
    This visitor is used whenever the semantic analysis visitor needs to decide what the data type of the result
    of a (binary) expression is.

    PRE-CONDITION: all variables within the tree should exist and be defined. This can be checked using the unavailable variable usage visitor
    """

    def __init__(self, last_symbol_table: SymbolTable):
        self.last_symbol_table = last_symbol_table
        # This becomes the actual data type after doing some lookups of the
        # variables and their data types and the literals entered as well
        self.resulting_data_type = None
        assert last_symbol_table is not None

    def update_current_data_type(self, other_data_type):
        """
        Checks if the other data type given is richer than the current type and replaces it, otherwise do nothing
        """

        # TODO raise a semantic error if the data types are incomparable

        if self.resulting_data_type is None:
            self.resulting_data_type = other_data_type
        else:
            if DataTypeToken.is_richer_than(other_data_type, self.resulting_data_type):
                self.resulting_data_type = other_data_type

    def visit_ast_literal(self, ast: ASTLiteral):
        if ast.get_token() == LiteralToken.CHAR_LITERAL:
            self.update_current_data_type(DataTypeToken.CHAR)
        elif ast.get_token() == LiteralToken.INT_LITERAL:
            self.update_current_data_type(DataTypeToken.INT)
        elif ast.get_token() == LiteralToken.FLOAT_LITERAL:
            self.update_current_data_type(DataTypeToken.FLOAT)
        else:
            raise NotImplementedError(f"Token type '{ast.get_token()}' not recognized as literal")

    def visit_ast_identifier(self, ast: ASTIdentifier):
        variable = self.last_symbol_table.lookup_variable(ast.get_content())
        assert variable.is_initialized()
        self.update_current_data_type(variable.data_type)


class ASTVisitorUndeclaredVariableUsed(ASTBaseVisitor):
    """
    Used by the semantical analysis visitor to check if a certain AST contains undeclared variables
    """

    def __init__(self, last_symbol_table: SymbolTable):
        """ The symbol table at the top of the stack in the semantical analysis vistor"""
        self.last_symbol_table = last_symbol_table
        self.undeclared_variables_used = list()
        assert last_symbol_table is not None

    def visit_ast_identifier(self, ast: ASTIdentifier):
        table_element = self.last_symbol_table.lookup(ast.get_content())
        if not table_element:
            self.undeclared_variables_used.append(ast)


class ASTVisitorUninitializedVariableUsed(ASTBaseVisitor):
    """
    Used by the semantical analysis visitor to check if a certain AST contains an unitialized variables
    """

    def __init__(self, last_symbol_table: SymbolTable):
        """ The symbol table at the top of the stack in the semantical analysis vistor"""
        self.last_symbol_table = last_symbol_table
        self.uninitialized_variables_used = list()
        assert last_symbol_table is not None

    def visit_ast_identifier(self, ast: ASTIdentifier):
        super().visit_ast_identifier(ast)
        table_element = self.last_symbol_table.lookup(ast.get_content())
        if table_element:
            assert isinstance(table_element, Symbol)
            assert isinstance(table_element, VariableSymbol)
            if not table_element.is_initialized():
                self.uninitialized_variables_used.append(ast)


class ASTVisitorOptimizer(ASTBaseVisitor):
    """
    Pre-condition: The variables used in these expressions must exist (checks must be done beforehand in the semantical analyser)
    """

    def __init__(self, last_symbol_table: SymbolTable):
        self.last_symbol_table = last_symbol_table
        self.optimized_ast = None

    def replace_identifier_if_applicable(self, ast: ASTIdentifier):
        assert isinstance(ast, ASTIdentifier)

    def do_constant_propagation(self, ast: AST):

        if isinstance(ast, ASTBinaryExpression):
            ast.left = self.do_constant_propagation(ast.left)
            ast.right = self.do_constant_propagation(ast.right)
        elif isinstance(ast, ASTUnaryExpression):
            ast.value_applied_to = self.do_constant_propagation(ast.value_applied_to)
        elif isinstance(ast, ASTIdentifier):
            variable = self.last_symbol_table.lookup_variable(ast.get_content())
            # The variable in the symbol table still has a reaching definition, so we can replace this variable with the reaching definition
            if variable.has_reaching_defintion():
                # Return the reaching definition instead of the variable
                return variable.get_reaching_definition()

        return ast

    def do_constant_folding(self, ast: AST):

        if isinstance(ast, ASTBinaryExpression):

            ast.left = self.do_constant_folding(ast.left)
            ast.right = self.do_constant_folding(ast.right)

            if isinstance(ast.left, ASTLiteral) and isinstance(ast.right, ASTLiteral):

                # The richest token will be the new literal token
                if DataTypeToken.is_richer_than(ast.left.token, ast.right.token):
                    new_literal_token = ast.left.token
                else:
                    new_literal_token = ast.right.token

                left_value = ast.left.get_content_depending_on_literal_token()
                right_value = ast.right.get_content_depending_on_literal_token()

                result = None
                if isinstance(ast, ASTBinaryArithmeticExpression):
                    if ast.get_token() == BinaryArithmeticExprToken.ADD_EXPRESSION:
                        result = left_value + right_value
                    elif ast.get_token() == BinaryArithmeticExprToken.SUB_EXPRESSION:
                        result = left_value - right_value
                    elif ast.get_token() == BinaryArithmeticExprToken.DIV_EXPRESSION:
                        result = left_value / right_value
                    elif ast.get_token() == BinaryArithmeticExprToken.MUL_EXPRESSION:
                        result = left_value * right_value
                    else:
                        raise NotImplementedError

                elif isinstance(ast, ASTBinaryCompareExpression):
                    if ast.get_token() == BinaryCompareExprToken.EQUALS_EXPRESSION:
                        result = left_value == right_value
                    elif ast.get_token() == BinaryCompareExprToken.LESS_THAN_EXPRESSION:
                        result = left_value < right_value
                    elif ast.get_token() == BinaryCompareExprToken.GREATER_THAN_EXPRESSION:
                        result = left_value > right_value
                    else:
                        raise NotImplementedError

                assert result is not None
                return ASTLiteral(new_literal_token, str(result)).set_parent(ast.parent)

        elif isinstance(ast, ASTUnaryExpression):

            ast.value_applied_to = self.do_constant_folding(ast.value_applied_to)

            if isinstance(ast.value_applied_to, ASTLiteral):
                if ast.get_token() == UnaryExprToken.UNARY_PLUS_EXPRESSION:
                    factor = 1
                elif ast.get_token() == UnaryExprToken.UNARY_MINUS_EXPRESSION:
                    factor = -1
                else:
                    raise NotImplementedError

                return ASTLiteral(ast.value_applied_to.token,
                                  str(
                                      factor * ast.value_applied_to.get_content_depending_on_literal_token())).set_parent(
                    ast.parent)

        return ast

    def optimize(self, ast: AST):
        self.optimized_ast = ast
        self.optimized_ast = self.do_constant_propagation(self.optimized_ast)
        self.optimized_ast = self.do_constant_folding(self.optimized_ast)

    def visit_ast_binary_expression(self, ast: ASTBinaryExpression):
        self.optimize(ast)

    def visit_ast_unary_expression(self, ast: ASTUnaryExpression):
        self.optimize(ast)

    def visit_ast_identifier(self, ast: ASTIdentifier):
        self.optimize(ast)

    def visit_ast_literal(self, ast: ASTLiteral):
        # Do nothing, literals can't be optimized
        self.optimized_ast = ast


class ASTVisitorSemanticAnalysis(ASTBaseVisitor):

    def __init__(self):
        super().__init__()
        self.symbol_table_stack = list()
        # TODO needs to be removed once the concept of 'blocks' is introduced
        self.create_symbol_table()

    def create_symbol_table(self):
        if len(self.symbol_table_stack) == 0:
            # First symbol table created
            self.symbol_table_stack.append(SymbolTable())
        else:
            parent_symbol_table = self.symbol_table_stack[-1]
            new_symbol_table = SymbolTable()
            new_symbol_table.parent = parent_symbol_table
            self.symbol_table_stack.append(new_symbol_table)

    def get_last_symbol_table(self):
        """
        Retrieve the symbol table that was last created (top of the stack)
        This corresponds the scope you are currently in
        """
        symbol_table = self.symbol_table_stack[-1]
        assert isinstance(symbol_table, SymbolTable)
        return symbol_table

    def check_for_narrowing_result(self, declared_data_type: DataTypeToken, ast: AST):
        """
        Checks if the result would be narrowed down into another data type (e.g. float to int). If so, warn to the log
        PRE-CONDITION: All variables need to be declared and initialized in order for lookups to work
        """
        resulting_data_type_visitor = ASTVisitorResultingDataType(self.get_last_symbol_table())
        ast.accept(resulting_data_type_visitor)
        assert resulting_data_type_visitor.resulting_data_type is not None

        # This is the data type that was declared in the input program

        if declared_data_type != resulting_data_type_visitor.resulting_data_type and not DataTypeToken.is_richer_than(
                declared_data_type, resulting_data_type_visitor.resulting_data_type):
            print(
                "WARN: narrowing result of expression from datatype '" +
                resulting_data_type_visitor.resulting_data_type.name + "' to datatype '" + declared_data_type.name + "'")

    def check_r_value_assignment(self, bin_expr: ASTAssignmentExpression):
        # TODO Needs to be improved with derefencing and all that stuff

        if isinstance(bin_expr.left, ASTLiteral):
            raise SemanticError(
                f"Assignment to an R-VALUE of type {bin_expr.left.token.name} (value is {bin_expr.left.get_content()})")

    def check_undeclared_variable_usage(self, ast: AST):

        undeclared_var_usage = ASTVisitorUndeclaredVariableUsed(self.get_last_symbol_table())
        ast.accept(undeclared_var_usage)

        if len(undeclared_var_usage.undeclared_variables_used) != 0:
            error_text = ""

            for variable in undeclared_var_usage.undeclared_variables_used:
                error_text += "Variable with name '" + variable.get_content() + "' is undeclared! \n"

            raise SemanticError(error_text)

    def check_uninitialized_variable_usage(self, ast: AST):

        uninitialized_var_usage = ASTVisitorUninitializedVariableUsed(self.get_last_symbol_table())
        ast.accept(uninitialized_var_usage)

        if len(uninitialized_var_usage.uninitialized_variables_used) != 0:
            error_text = ""

            for variable in uninitialized_var_usage.uninitialized_variables_used:
                error_text += "Variable with name '" + variable.get_content() + "' is found but uninitialized! \n"

            raise SemanticError(error_text)

    def check_const_assignment(self, bin_expr: ASTAssignmentExpression):
        """
        Checks if a variable being assigned a new value is const, and if so, raise a semantic error
        PRE-CONDITION: Variable must exist (check must have gone before)
        """

        variable = self.get_last_symbol_table().lookup_variable(bin_expr.left.get_content())

        if variable.const:
            raise SemanticError("Cannot assign value to const variable '" + bin_expr.left.get_content() + "'")

    def visit_ast_binary_expression(self, ast: ASTBinaryExpression):
        # Do nothing, just some optimization
        pass

    def optimize_expression(self, ast: AST):
        """
        Optimizes an expression using constant propagation and constant folding
        Constant propagation: replaces the variables, if possible, with their corresponding literals (reaching definition)
        Constant folding: folds literal expressions with nodes containing the results
        """

        optimizer_visitor = ASTVisitorOptimizer(self.get_last_symbol_table())
        ast.accept(optimizer_visitor)
        return optimizer_visitor.optimized_ast

    def visit_ast_assignment_expression(self, ast: ASTAssignmentExpression):
        symbol_table = self.get_last_symbol_table()

        # Do some semantic checks. If all checks don't raise any errors, continue on with the new value
        self.check_undeclared_variable_usage(ast.right)
        self.check_undeclared_variable_usage(ast.left)
        self.check_uninitialized_variable_usage(ast.right)

        self.check_const_assignment(ast)

        ast.right = self.optimize_expression(ast.get_right())

        variable = symbol_table.lookup_variable(ast.left.get_content())
        if not variable.is_initialized():
            variable.initialized = True
            # Set its reaching definition as it has just been initialized
            variable.reaching_definition_ast = ast.get_right()

        else:

            # Const variables can not be reassigned so the keep their reaching definition,
            # otherwise there is no reaching definition anymore (intervening assignment has been encountered)
            if variable.has_reaching_defintion() and not variable.is_const():
                variable.reaching_definition_ast = None

        # Warn in case the result will be narrowed down into another data type
        self.check_for_narrowing_result(variable.data_type, ast)

    def visit_ast_variable_declaration(self, ast: ASTVariableDeclaration):
        symbol_table = self.get_last_symbol_table()

        if ast.is_const():
            raise SemanticError(
                f"Variable '{ast.var_name_ast.get_content()}' declared const must be initialized with its declaration")

        if symbol_table.lookup(ast.var_name_ast.get_content()) is None:
            symbol_table.insert_symbol(
                VariableSymbol(ast.var_name_ast.get_content(), ast.get_data_type(), ast.is_const(), False))
        else:
            raise AlreadyDeclaredError(
                "Variable with name '" + str(ast.var_name_ast) + "' has already been declared in this scope!")

    def visit_ast_variable_declaration_and_init(self, ast: ASTVariableDeclarationAndInit):
        self.visit_ast_variable_declaration(ast)
        variable_symbol = self.get_last_symbol_table().lookup_variable(ast.var_name_ast.get_content())

        # Do some semantic checks
        self.check_undeclared_variable_usage(ast.value)
        self.check_uninitialized_variable_usage(ast.value)

        variable_symbol.initialized = True

        ast.value = self.optimize_expression(ast.value)
        variable_symbol.reaching_definition_ast = ast.value

        self.check_for_narrowing_result(ast.get_data_type(), ast.value)

    # TODO implement this!
    def visit_ast_printf_instruction(self, ast: ASTPrintfInstruction):
        super().visit_ast_printf_instruction(ast)
