import copy

from src.ast.ASTBaseVisitor import ASTBaseVisitor
from src.ast.ASTs import *
from src.semantic_analysis.SymbolTableSemanticAnalyser import *


class SemanticError(Exception):
    pass


class ASTVisitorResultingDataType(ASTBaseVisitor):
    """
    This visitor is used whenever the semantic analysis visitor needs to decide what the data type of the result
    of a (binary) expression is.

    PRE-CONDITION: all variables within the tree should exist and be defined.
    This can be checked using the unavailable variable usage visitor
    """

    def __init__(self, last_symbol_table: SymbolTableSemanticAnalyser):
        self.last_symbol_table = last_symbol_table
        # This becomes the actual data type after doing some lookups of the
        # variables and their data types and the literals entered as well
        self.resulting_data_type = None
        assert last_symbol_table is not None

    def get_resulting_data_type(self):
        assert isinstance(self.resulting_data_type, DataType.DataType)
        return self.resulting_data_type

    def update_current_data_type(self, other_data_type):
        """
        Checks if the other data type given is richer than the current type and replaces it, otherwise do nothing
        """

        assert isinstance(other_data_type, DataType.DataType)

        # TODO raise a semantic error if the data types are incomparable

        if self.resulting_data_type is None:
            self.resulting_data_type = other_data_type
        else:

            # Doesn't matter which one you pick, the pointer levels are the same
            if self.resulting_data_type.get_pointer_level() == other_data_type.get_pointer_level() == 0:
                if DataType.DataTypeToken.is_richer_than(other_data_type.get_token(),
                                                         self.get_resulting_data_type().get_token()):
                    self.resulting_data_type = other_data_type
            else:
                if self.resulting_data_type != other_data_type:
                    raise SemanticError(
                        f'Cannot get resulting data type: pointer types '
                        f'{self.resulting_data_type.get_name()} and '
                        f'{other_data_type.get_name()} are incompatible')

    def visit_ast_literal(self, ast: ASTLiteral):
        if ast.get_data_type() == DataType.NORMAL_CHAR:
            self.update_current_data_type(DataType.NORMAL_CHAR)
        elif ast.get_data_type() == DataType.NORMAL_INT:
            self.update_current_data_type(DataType.NORMAL_INT)
        elif ast.get_data_type() == DataType.NORMAL_FLOAT:
            self.update_current_data_type(DataType.NORMAL_FLOAT)
        else:
            raise NotImplementedError(f"Token type '{ast.get_data_type()}' not recognized as literal")

    def visit_ast_identifier(self, ast: ASTVariable):
        variable = self.last_symbol_table.lookup_variable(ast.get_content())
        assert variable.is_initialized(), "Variable should be initialized"
        self.update_current_data_type(variable.data_type)

        # The resulting data type is the data type you get when you apply the amount of derefencing
        variable_data_type_with_derefencing = DataType.DataType(variable.get_data_type().get_token(),
                                                                variable.get_data_type().get_pointer_level() - ast.get_dereference_count())
        self.update_current_data_type(variable_data_type_with_derefencing)

    def visit_ast_access_element(self, ast: ASTArrayAccessElement):
        access_element = self.last_symbol_table.lookup_variable(ast.get_content())
        self.update_current_data_type(access_element.data_type)


class ASTVisitorUndeclaredVariableUsed(ASTBaseVisitor):
    """
    Used by the semantical analysis visitor to check if a certain AST contains undeclared variables
    """

    def __init__(self, last_symbol_table: SymbolTableSemanticAnalyser):
        """ The symbol table at the top of the stack in the semantical analysis vistor"""
        self.last_symbol_table = last_symbol_table
        self.undeclared_variables_used = list()
        assert last_symbol_table is not None

    def visit_ast_identifier(self, ast: ASTVariable):
        table_element = self.last_symbol_table.lookup(ast.get_content())
        if not table_element:
            self.undeclared_variables_used.append(ast)


class ASTVisitorUninitializedVariableUsed(ASTBaseVisitor):
    """
    Used by the semantical analysis visitor to check if a certain AST contains an unitialized variables
    """

    def __init__(self, last_symbol_table: SymbolTableSemanticAnalyser):
        """ The symbol table at the top of the stack in the semantical analysis vistor"""
        self.last_symbol_table = last_symbol_table
        self.uninitialized_variables_used = list()
        assert last_symbol_table is not None

    def visit_ast_identifier(self, ast: ASTVariable):
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

    def __init__(self, last_symbol_table: SymbolTableSemanticAnalyser):
        self.last_symbol_table = last_symbol_table
        self.optimized_ast = None

    def replace_identifier_if_applicable(self, ast: ASTVariable):
        assert isinstance(ast, ASTVariable)

    def do_constant_propagation(self, ast: AST):

        if isinstance(ast, ASTBinaryExpression):
            ast.left = self.do_constant_propagation(ast.left)
            ast.right = self.do_constant_propagation(ast.right)
        elif isinstance(ast, ASTUnaryExpression):
            ast.value_applied_to = self.do_constant_propagation(ast.value_applied_to)
        elif isinstance(ast, ASTVariable):
            variable = self.last_symbol_table.lookup_variable(ast.get_content())
            # The variable in the symbol table still has a reaching definition, so we can
            # replace this variable with the reaching definition
            if variable.has_reaching_defintion():
                # Return the reaching definition instead of the variable
                # We need to make a deep copy so that they are not seen as one node anymore
                # (changes to one node doesn't make changes to the other)
                # Otherwise this would also break visualisation because the DotVisitor uses the IDs of the Nodes
                # Also the parent is different

                return copy.deepcopy(variable.get_reaching_definition()).set_parent(ast.parent)

        return ast

    def do_constant_folding(self, ast: AST):

        if isinstance(ast, ASTBinaryExpression):

            ast.left = self.do_constant_folding(ast.left)
            ast.right = self.do_constant_folding(ast.right)

            if isinstance(ast.left, ASTLiteral) and isinstance(ast.right, ASTLiteral):

                resulting_data_type = DataType.DataType.get_resulting_data_type(ast.left, ast.right)

                left_value = ast.left.get_content_depending_on_data_type()
                right_value = ast.right.get_content_depending_on_data_type()

                result = None
                if isinstance(ast, ASTBinaryArithmeticExpression):
                    if ast.get_token() == BinaryArithmeticExprToken.ADD:
                        result = left_value + right_value
                    elif ast.get_token() == BinaryArithmeticExprToken.SUB:
                        result = left_value - right_value
                    elif ast.get_token() == BinaryArithmeticExprToken.DIV:
                        if resulting_data_type == DataType.DataTypeToken.CHAR or resulting_data_type == DataType.DataTypeToken.INT:
                            result = int(left_value / right_value)
                        else:
                            result = float(left_value / right_value)
                    elif ast.get_token() == BinaryArithmeticExprToken.MUL:
                        result = left_value * right_value
                    else:
                        raise NotImplementedError

                elif isinstance(ast, ASTRelationalExpression):
                    if ast.get_token() == RelationalExprToken.EQUALS:
                        result = left_value == right_value
                    elif ast.get_token() == RelationalExprToken.LESS_THAN:
                        result = left_value < right_value
                    elif ast.get_token() == RelationalExprToken.GREATER_THAN:
                        result = left_value > right_value
                    else:
                        raise NotImplementedError

                assert result is not None
                return ASTLiteral(resulting_data_type, str(result)).set_parent(ast.parent)

        elif isinstance(ast, ASTUnaryArithmeticExpression):

            ast.value_applied_to = self.do_constant_folding(ast.value_applied_to)

            if isinstance(ast.value_applied_to, ASTLiteral):
                if ast.get_token() == UnaryArithmeticExprToken.PLUS:
                    factor = 1
                elif ast.get_token() == UnaryArithmeticExprToken.MINUS:
                    factor = -1
                else:
                    raise NotImplementedError

                return ASTLiteral(ast.value_applied_to.get_data_type_token(),
                                  str(
                                      factor * ast.value_applied_to.get_content_depending_on_data_type())).set_parent(
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

    def visit_ast_identifier(self, ast: ASTVariable):
        self.optimize(ast)

    def visit_ast_literal(self, ast: ASTLiteral):
        # Do nothing, literals can't be optimized
        self.optimized_ast = ast


class ASTVisitorSemanticAnalysis(ASTBaseVisitor):

    def __init__(self, optimize=False):
        super().__init__()
        self.symbol_table_stack = list()
        self.current_function = None
        self.optimize = optimize

    def get_current_function(self):
        assert self.current_function is None or isinstance(self.current_function, FunctionSymbol)
        return self.current_function

    def get_resulting_data_type(self, ast: AST):
        """
        Calculates the resulting data type using a visitor for the AST. This is necessary because some variables
        need to be looked up in a symbol table for it to determine the resulting (richest) data type
        """

        last_symbol_table = self.get_last_symbol_table()
        resulting_data_type_visitor = ASTVisitorResultingDataType(self.get_last_symbol_table())
        ast.accept(resulting_data_type_visitor)
        return resulting_data_type_visitor.get_resulting_data_type()

    def get_last_symbol_table(self):
        """
        Retrieve the symbol table that was last created (top of the stack)
        This corresponds the scope you are currently in
        """
        symbol_table = self.symbol_table_stack[-1]
        assert isinstance(symbol_table, SymbolTableSemanticAnalyser)
        return symbol_table

    def check_for_narrowing_result(self, declared_data_type: DataType.DataType, ast: AST):
        """
        Checks if the result would be narrowed down into another data type (e.g. float to int). If so, warn to the log
        PRE-CONDITION: All variables need to be declared and initialized in order for lookups to work
        """
        resulting_data_type = self.get_resulting_data_type(ast)

        # This is the data type that was declared in the input program

        if declared_data_type != resulting_data_type:

            if declared_data_type.get_pointer_level() == resulting_data_type.get_pointer_level():

                if DataType.DataTypeToken.is_richer_than(resulting_data_type, declared_data_type):
                    raise SemanticError(
                        "The result would be narrowed, and we do not yet support explicit or implicit casting")
            else:

                raise SemanticError(
                    f'Cannot get resulting data type: pointer types '
                    f'{resulting_data_type.get_name()} and '
                    f'{declared_data_type.get_name()} are incompatible')

    def check_r_value_assignment(self, bin_expr: ASTAssignmentExpression):
        # TODO Needs to be improved with derefencing and all that stuff

        if isinstance(bin_expr.left, ASTLiteral):
            raise SemanticError(
                f"Assignment to an R-VALUE of type {bin_expr.left.get_data_type_token().token_name} "
                f"(value is {bin_expr.left.get_content()})")

    def check_undeclared_variable_usage(self, ast: AST):

        undeclared_var_usage = ASTVisitorUndeclaredVariableUsed(self.get_last_symbol_table())
        ast.accept(undeclared_var_usage)

        if len(undeclared_var_usage.undeclared_variables_used) != 0:
            error_text = ""

            for variable in undeclared_var_usage.undeclared_variables_used:
                error_text += f"Variable with name '{variable.get_content()}' is undeclared! \n"

            raise SemanticError(error_text)

    def check_uninitialized_variable_usage(self, ast: AST):

        uninitialized_var_usage = ASTVisitorUninitializedVariableUsed(self.get_last_symbol_table())
        ast.accept(uninitialized_var_usage)

        if len(uninitialized_var_usage.uninitialized_variables_used) != 0:
            error_text = ""

            for variable in uninitialized_var_usage.uninitialized_variables_used:
                error_text += f"Variable with name '{variable.get_content()}' is found but uninitialized! \n"

            raise SemanticError(error_text)

    def check_const_assignment(self, bin_expr: ASTAssignmentExpression):
        """
        Checks if a variable being assigned a new value is const, and if so, raise a semantic error
        PRE-CONDITION: Variable must exist (check must have gone before)
        """
        variable = self.get_last_symbol_table().lookup_variable(bin_expr.left.get_content())

        if isinstance(variable, VariableSymbol):
            if variable.const:
                raise SemanticError(f"Cannot assign value to const variable '{bin_expr.left.get_content()}'")

    def visit_ast_binary_expression(self, ast: ASTBinaryExpression):
        # Do nothing, just some optimization
        self.check_undeclared_variable_usage(ast)
        self.check_uninitialized_variable_usage(ast)

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
        self.check_undeclared_variable_usage(ast.left)
        self.visit_ast_binary_expression(ast.get_right())

        symbol = symbol_table.lookup_variable(ast.left.get_content())

        if isinstance(symbol, VariableSymbol):
            self.check_const_assignment(ast)
            if self.optimize:
                ast.right = self.optimize_expression(ast.get_right())

            if not symbol.is_initialized():
                symbol.initialized = True
                # Set its reaching definition as it has just been initialized
                symbol.reaching_definition_ast = ast.get_right()

            else:

                # Const variables can not be reassigned so the keep their reaching definition,
                # otherwise there is no reaching definition anymore (intervening assignment has been encountered)
                if symbol.has_reaching_defintion() and not symbol.is_const():
                    symbol.reaching_definition_ast = None

            # Warn in case the result will be narrowed down into another data type
            self.check_for_narrowing_result(symbol.data_type, ast)
        elif isinstance(symbol, ArraySymbol):
            if self.optimize:
                ast.right = self.optimize_expression(ast.get_right())
            self.check_for_narrowing_result(symbol.data_type, ast)
        else:
            raise NotImplementedError

    def visit_ast_variable_declaration(self, ast: ASTVariableDeclaration):
        symbol_table = self.get_last_symbol_table()

        if ast.is_const():
            raise SemanticError(
                f"Variable '{ast.var_name_ast.get_content()}' declared const must be initialized with its declaration")

        if symbol_table.lookup_local(ast.var_name_ast.get_content()) is None:
            if symbol_table.lookup(ast.var_name_ast.get_content()) is not None:
                print(
                    f"[SemanticAnalysis] Warning: declaration of '{ast.var_name_ast.get_content()}'"
                    f" shadows a local variable. You might want to rename it")
            var_name = ast.var_name_ast.get_content()
            # The variables are automatically stored as pointers. You need to dereference in order to the the underlying data type.
            symbol_table.insert_symbol(var_name,
                                       VariableSymbol(ast.var_name_ast.get_content(),
                                                      DataType.DataType(ast.get_data_type().get_token(),
                                                                        ast.get_data_type().get_pointer_level() + 1),
                                                      ast.is_const(), False))
        else:
            raise SemanticError(
                f"Variable with name '{ast.var_name_ast.get_content()}' has already been declared in this scope!")

    def visit_ast_array_declaration(self, ast: ASTArrayDeclaration):
        symbol_table = self.get_last_symbol_table()
        var_name = ast.var_name_ast.get_content()
        if ast.is_const():
            raise SemanticError(
                f"Array '{var_name}' declared const must be initialized with its declaration")

        if symbol_table.lookup_local(var_name) is None:
            if symbol_table.lookup(var_name) is not None:
                print(
                    f"[SemanticAnalysis] Warning: declaration of '{var_name}'"
                    f" shadows a local variable. You might want to rename it")
            symbol_table.insert_symbol(var_name, ArraySymbol(var_name, ast.get_data_type(), ast.get_size().get_content()))
        else:
            raise SemanticError(
                f"Array with name '{var_name}' has already been declared in this scope!"
            )

    def visit_ast_variable_declaration_and_init(self, ast: ASTVariableDeclarationAndInit):
        self.visit_ast_variable_declaration(ast)
        variable_symbol = self.get_last_symbol_table().lookup_variable(ast.var_name_ast.get_content())

        # Do some semantic checks
        self.check_undeclared_variable_usage(ast.value)
        self.check_uninitialized_variable_usage(ast.value)

        variable_symbol.initialized = True

        if self.optimize:
            ast.value = self.optimize_expression(ast.value)
        variable_symbol.reaching_definition_ast = ast.value

        self.check_for_narrowing_result(ast.get_data_type(), ast.value)

    # TODO implement this!
    def visit_ast_printf_instruction(self, ast: ASTPrintfInstruction):
        super().visit_ast_printf_instruction(ast)

    def on_scope_entered(self):

        new_symbol_table = SymbolTableSemanticAnalyser()
        if len(self.symbol_table_stack) > 0:
            new_symbol_table.set_parent(self.get_last_symbol_table())

        self.symbol_table_stack.append(new_symbol_table)

    def on_scope_exit(self):
        self.symbol_table_stack.pop()

    def visit_ast_scope(self, ast: ASTScope):
        self.on_scope_entered()
        super().visit_ast_scope(ast)
        self.on_scope_exit()

    def get_function_name_for_symbol_table(self, function_identifier: str, param_data_types: list):
        """
        Creates an appropriate function name to put as key in the symbol table, taking into account which functions
        can be overloaded and which not
        function_identifier: the identifier of the function
        param_data_types: DataTypes of the parameters
        """
        name = f'{function_identifier}('

        for i in range(0, len(param_data_types)):
            param_data_type = param_data_types[i]
            name += param_data_type.get_var_name()
            if i != len(param_data_types) - 1:
                name += ','

        name += ')'
        return name

    def on_function_entered(self, function_symbol: FunctionSymbol):
        self.current_function = function_symbol

    def on_function_exit(self):
        self.current_function = None

    def visit_ast_return_statement(self, ast: ASTReturnStatement):

        if self.get_current_function() is None:
            raise SemanticError(f'You cannot put a return value outside of a function')

        return_value = ast.get_return_value()

        if self.get_current_function().get_return_type() != self.get_resulting_data_type(return_value):
            raise SemanticError(
                f"The return type of the function '{self.get_current_function().symbol_name}' "
                f"(data type '{self.get_current_function().get_return_type()}') and "
                f"return type of the return value (data type '{return_value.get_data_type()}') aren't equal")

        super().visit_ast_return_statement(ast)

    def visit_conditional_statement(self, ast: ASTConditionalStatement):
        condition_ast = ast.get_condition()

        boolean_result = False

        if isinstance(condition_ast, ASTLiteral):
            if condition_ast.get_data_type() == DataType.NORMAL_BOOL:
                boolean_result = True
        elif isinstance(condition_ast, ASTVariable):
            variable_symbol = self.get_last_symbol_table().lookup_variable(condition_ast.get_content())

            if variable_symbol.get_data_type() == DataType.NORMAL_BOOL:
                boolean_result = True

        if not boolean_result:
            print("WARN: the result of an expression does not return boolean type")

    def visit_ast_function_call(self, ast: ASTFunctionCall):

        function_identifier = ast.get_function_called().get_var_name()

        param_data_types = list()

        for param in ast.get_arguments():
            self.check_undeclared_variable_usage(param)
            self.check_uninitialized_variable_usage(param)

            resulting_data_type_visitor = ASTVisitorResultingDataType(self.get_last_symbol_table())
            param.accept(resulting_data_type_visitor)
            param_data_types.append(resulting_data_type_visitor.get_resulting_data_type())

        function_name_for_symbol_table = self.get_function_name_for_symbol_table(function_identifier, param_data_types)
        function_lookup = self.get_last_symbol_table().lookup(function_name_for_symbol_table)

        if function_lookup is None:
            raise SemanticError(f'Function {function_name_for_symbol_table} is not declared! Cannot call this function')

    def visit_ast_function_declaration(self, ast: ASTFunctionDeclaration):
        """
        Basically takes over the scope thing a little bit because of the parameters
        """

        function_identifier = ast.get_name()
        param_data_types = list()

        for param in ast.get_params():
            param_data_types.append(param.get_data_type())

        function_name_for_symbol_table = self.get_function_name_for_symbol_table(function_identifier, param_data_types)

        function_symbol = FunctionSymbol(function_name_for_symbol_table,
                                         ast.get_params(),
                                         ast.get_return_type().get_data_type())
        if self.get_last_symbol_table().lookup(
                function_name_for_symbol_table) is not None:
            raise SemanticError(
                f'function {function_name_for_symbol_table} already declared!\n')

        self.get_last_symbol_table().insert_symbol(
            function_symbol.get_name(), function_symbol)

        self.on_function_entered(function_symbol)
        self.on_scope_entered()
        for param in ast.get_params():
            # A little bit different then with normal variable declarations, which is why we handle it ourselves
            # The variable symbol will be set on initialized in the symbol table as it is a parameter, so values
            # are passed in
            assert isinstance(param, ASTVariableDeclaration)
            var_name = param.get_var_name()
            self.get_last_symbol_table().insert_symbol(var_name,
                                                       VariableSymbol(param.get_var_name_ast().get_content(),
                                                                      param.get_data_type(),
                                                                      param.is_const(), True))

        # Skip the on_scope entered thing because it is already done
        super().visit_ast_scope(ast.get_execution_body())
        self.on_scope_exit()
        self.on_function_exit()
