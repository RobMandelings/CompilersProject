import copy

from src.ast.ASTBaseVisitor import ASTBaseVisitor
from src.ast.ASTs import *
from src.semantic_analysis.SymbolTableSemanticAnalyser import *


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
        Checks if the other data type given is richer than the current type
        and replaces it if this is the case, otherwise do nothing
        """

        assert isinstance(other_data_type, DataType.DataType)

        # TODO raise a semantic error if the data types are incomparable

        if self.resulting_data_type is None:
            self.resulting_data_type = other_data_type
        else:

            other_richer = other_data_type > self.resulting_data_type

            if other_richer:
                self.resulting_data_type = other_data_type
            else:
                if other_richer is None:
                    raise SemanticError(
                        f'Cannot get resulting data type: data types '
                        f'{self.resulting_data_type.get_name()} and '
                        f'{other_data_type.get_name()} are incompatible')

    def visit_ast_literal(self, ast: ASTLiteral):
        if ast.get_data_type() == DataType.NORMAL_CHAR:
            self.update_current_data_type(DataType.NORMAL_CHAR)
        elif ast.get_data_type() == DataType.NORMAL_INT:
            self.update_current_data_type(DataType.NORMAL_INT)
        elif ast.get_data_type() == DataType.NORMAL_FLOAT:
            self.update_current_data_type(DataType.NORMAL_FLOAT)
        elif ast.get_data_type() == DataType.NORMAL_DOUBLE:
            self.update_current_data_type(DataType.NORMAL_DOUBLE)
        else:
            raise NotImplementedError(f"Token type '{ast.get_data_type()}' not recognized as literal")

    def visit_ast_array_init(self, ast: ASTArrayInit):
        self.update_current_data_type(ast.get_data_type())

    def visit_ast_function_call(self, ast: ASTFunctionCall):
        function_symbol = self.last_symbol_table.lookup(ast.get_function_called_id())
        assert isinstance(function_symbol, FunctionSymbol)
        self.update_current_data_type(function_symbol.get_return_type())

    def visit_ast_identifier(self, ast: ASTIdentifier):
        variable = self.last_symbol_table.lookup_variable(ast.get_content())

        if isinstance(variable, IHasDataType):
            self.update_current_data_type(variable.get_data_type())
        else:
            raise SemanticError(
                'Identifier does not correspond to a variable with a data type. Cannot get resulting data type')

    def visit_ast_dereference(self, ast: ASTDereference):

        # Create a sub visitor to get the value of the data type being dereference
        # Dereference afterwards
        sub_visitor = ASTVisitorResultingDataType(self.last_symbol_table)
        ast.get_value_to_dereference().accept(sub_visitor)

        result_data_type = sub_visitor.get_resulting_data_type()

        if not result_data_type.is_pointer():
            raise SemanticError(f"Cannot dereference a non-pointer ('{result_data_type.get_name()}' invalid)")

        self.update_current_data_type(
            DataType.DataType(result_data_type.get_token(), result_data_type.get_pointer_level() - 1))

    def visit_ast_access_element(self, ast: ASTAccessArrayVarExpression):
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

    def visit_ast_identifier(self, ast: ASTIdentifier):
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

    def visit_ast_identifier(self, ast: ASTIdentifier):
        super().visit_ast_identifier(ast)
        table_element = self.last_symbol_table.lookup(ast.get_content())
        if table_element:
            assert isinstance(table_element, Symbol)
            if isinstance(table_element, VariableSymbol):
                if not table_element.is_initialized():
                    self.uninitialized_variables_used.append(ast)


class ASTVisitorOptimizer(ASTBaseVisitor):
    """
    Pre-condition: The variables used in these expressions must exist (checks must be done beforehand in the semantical analyser)
    """

    def __init__(self, last_symbol_table: SymbolTableSemanticAnalyser):
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
        elif isinstance(ast, ASTDereference):
            propagated_ast = self.do_constant_propagation(ast.get_value_to_dereference())
            if isinstance(propagated_ast, ASTLiteral):
                return propagated_ast
            else:
                return ast
        elif isinstance(ast, ASTIdentifier):
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

                resulting_data_type = DataType.DataType.get_resulting_data_type(ast.left.get_data_type(),
                                                                                ast.right.get_data_type())

                left_value = ast.left.get_content_depending_on_data_type()
                right_value = ast.right.get_content_depending_on_data_type()

                result = None
                if isinstance(ast, ASTBinaryArithmeticExpression):
                    if ast.get_token() == BinaryArithmeticExprToken.ADD:
                        result = left_value + right_value
                    elif ast.get_token() == BinaryArithmeticExprToken.SUB:
                        result = left_value - right_value
                    elif ast.get_token() == BinaryArithmeticExprToken.DIV:
                        if resulting_data_type == DataType.NORMAL_CHAR or resulting_data_type == DataType.NORMAL_INT:
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

                return ASTLiteral(ast.value_applied_to.get_data_type(),
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

    def visit_ast_identifier(self, ast: ASTIdentifier):
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

    def check_resulting_data_type(self, ast: AST):
        """
        Calculates the resulting data type using a visitor for the AST. This is necessary because some variables
        need to be looked up in a symbol table for it to determine the resulting (richest) data type
        """

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

    def check_for_narrowing_result(self, declared_data_type: DataType.DataType, rhs: AST):
        """
        Checks if the result would be narrowed down into another data type (e.g. float to int). If so, warn to the log
        PRE-CONDITION: All variables need to be declared and initialized in order for lookups to work
        """
        resulting_data_type = self.check_resulting_data_type(rhs)

        # This is the data type that was declared in the input program

        if declared_data_type != resulting_data_type:

            if declared_data_type.get_pointer_level() == resulting_data_type.get_pointer_level():

                if DataType.DataTypeToken.is_richer_than(resulting_data_type.get_token(),
                                                         declared_data_type.get_token()) and (
                        not resulting_data_type == DataType.NORMAL_DOUBLE and declared_data_type == DataType.NORMAL_FLOAT):
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
        self.check_resulting_data_type(ast)
        if not self.check_resulting_data_type(ast.left) == self.check_resulting_data_type(ast.right):
            raise SemanticError(
                f'Incompatible datatypes: {self.check_resulting_data_type(ast.left).get_name()} and {self.check_resulting_data_type(ast.right).get_name()}'
            )

    def visit_ast_binary_compare_expression(self, ast: ASTRelationalExpression):

        self.check_undeclared_variable_usage(ast)
        self.check_uninitialized_variable_usage(ast)

        if isinstance(ast.left, ASTExpression):
            self.check_resulting_data_type(ast.left)
        if isinstance(ast.right, ASTExpression):
            self.check_resulting_data_type(ast.right)

        if isinstance(ast.left, ASTIdentifier) and isinstance(ast.right, ASTIdentifier):
            lookup_left = self.get_last_symbol_table().lookup(ast.left.get_name())
            lookup_right = self.get_last_symbol_table().lookup(ast.right.get_name())

            if isinstance(lookup_left, ArraySymbol) and isinstance(lookup_right, ArraySymbol):
                print("Warning: array comparison always evaluates to false")
            elif isinstance(lookup_left, ArraySymbol) or isinstance(lookup_right, ArraySymbol):
                print(
                    f"Warning: comparison between {lookup_left.get_data_type().get_name()}* and {lookup_right.get_data_type().get_token().get_name()}")
            elif isinstance(lookup_left, VariableSymbol) and isinstance(lookup_right, VariableSymbol):
                self.check_resulting_data_type(ast)
            else:
                raise NotImplementedError

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
        ast.get_left().accept(self)
        ast.get_right().accept(self)

        if isinstance(ast.get_left(), ASTIdentifier):
            symbol = symbol_table.lookup_variable(ast.get_left().get_content())

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
                    # otherwise there is no reaching definition anymore
                    # (intervening assignment has been encountered)
                    if symbol.has_reaching_defintion() and not symbol.is_const():
                        symbol.reaching_definition_ast = None

                # Warn in case the result will be narrowed down into another data type
            elif isinstance(symbol, ArraySymbol):
                if self.optimize:
                    ast.right = self.optimize_expression(ast.get_right())

            self.check_for_narrowing_result(
                DataType.DataType(symbol.data_type.get_token(), symbol.get_data_type().get_pointer_level() - 1),
                ast.get_right())

        else:

            data_type = self.check_resulting_data_type(ast.get_left())

            # if not data_type.is_pointer():
            #     raise SemanticError('Cannot assign value: too many dereferences')

    def visit_ast_var_declaration(self, ast: ASTVarDeclaration):
        assert isinstance(ast, ASTVarDeclaration)
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
            # The variables are automatically stored as pointers.
            # This is because values 'assigned' to it are STORED in the variable, the symbol always points to the
            # underlying data type
            symbol_table.insert_symbol(var_name,
                                       VariableSymbol(ast.var_name_ast.get_content(),
                                                      DataType.DataType(ast.get_data_type().get_token(),
                                                                        ast.get_data_type().get_pointer_level() + 1),
                                                      ast.is_const(), False))
        else:
            raise SemanticError(
                f"Variable with name '{ast.var_name_ast.get_content()}' has already been declared in this scope!")

    def visit_ast_array_declaration(self, ast: ASTArrayVarDeclaration):
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
            # Pointer level + 1 because its stored internally as a pointer
            symbol_table.insert_symbol(var_name,
                                       ArraySymbol(var_name, DataType.DataType(ast.get_data_type().get_token(),
                                                                               ast.get_data_type().get_pointer_level() + 1),
                                                   ast.get_array_size().get_content()))
        else:
            raise SemanticError(
                f"Array with name '{var_name}' has already been declared in this scope!"
            )

    def visit_ast_var_declaration_and_init(self, ast: ASTVarDeclarationAndInit):
        self.visit_ast_var_declaration(ast.get_var_declaration())
        variable_symbol = self.get_last_symbol_table().lookup_variable(
            ast.get_var_declaration().get_var_name_ast().get_content())

        # Do some semantic checks
        self.check_undeclared_variable_usage(ast.initial_value)
        self.check_uninitialized_variable_usage(ast.initial_value)

        variable_symbol.initialized = True

        if self.optimize:
            ast.initial_value = self.optimize_expression(ast.initial_value)
        variable_symbol.reaching_definition_ast = ast.initial_value

        self.check_for_narrowing_result(ast.get_data_type(), ast.initial_value)

    def on_scope_entered(self, scope_type: SymbolTable.ScopeType):

        new_symbol_table = SymbolTableSemanticAnalyser(scope_type)
        if len(self.symbol_table_stack) > 0:
            new_symbol_table.set_parent(self.get_last_symbol_table())

        self.symbol_table_stack.append(new_symbol_table)

    def on_scope_exit(self):
        self.symbol_table_stack.pop()

    def visit_ast_scope(self, ast: ASTScope):
        # Only the global scope will directly visit ast scope
        self.on_scope_entered(SymbolTable.ScopeType.GLOBAL)
        super().visit_ast_scope(ast)
        self.on_scope_exit()

    def on_function_entered(self, function_symbol: FunctionSymbol):
        self.current_function = function_symbol

    def on_function_exit(self):
        self.current_function = None

    def visit_ast_return_statement(self, ast: ASTReturnStatement):

        if self.get_current_function() is None:
            raise SemanticError(f'You cannot put a return value outside of a function')

        return_value = ast.get_return_value()

        if self.get_current_function().get_return_type() != self.check_resulting_data_type(return_value):
            raise SemanticError(
                f"The return type of the function '{self.get_current_function().symbol_name}' "
                f"(data type '{self.get_current_function().get_return_type()}') and "
                f"return type of the return value (data type '{return_value.get_data_type()}') aren't equal")

        super().visit_ast_return_statement(ast)

    def visit_conditional_statement(self, ast: ASTConditionalStatement):
        condition_ast = ast.get_condition()

        if not isinstance(condition_ast, ASTRelationalExpression) and condition_ast is not None:

            condition_resulting_data_type = self.check_resulting_data_type(condition_ast)
            if condition_resulting_data_type != DataType.NORMAL_BOOL:
                print("WARN: the result of an expression does not return boolean type")

        # Skip the visit AST scope as we need to pass in a custom SymbolTable.ScopeType
        self.on_scope_entered(SymbolTable.ScopeType.CONDITIONAL)
        super().visit_ast_scope(ast.get_execution_body())
        self.on_scope_exit()

    def check_function_call_with_format_arg(self, function_call_ast: ASTFunctionCall):
        """
        Checks the array which represents the format for functions like scanf and printf
        returns the symbol type specifications collected
        """

        format_argument = function_call_ast.get_arguments()[0]
        format_array = None
        is_array_format = False
        if isinstance(format_argument, ASTArrayInit):
            is_array_format = True
            format_array = format_argument
        else:
            if isinstance(format_argument, ASTIdentifier):
                lookup = self.get_last_symbol_table().lookup(format_argument.get_name())

                if isinstance(lookup, ArraySymbol):
                    print('WARN: only inline printf format strings are currently checked for proper format.')
                    is_array_format = True

        if not is_array_format:
            raise SemanticError('Printf function call: first argument must be an array')

        if isinstance(format_argument, ASTArrayInit):

            symbol_type_specifications = list()

            for i in range(len(format_argument.get_values())):
                literal = format_argument.get_values()[i]
                if i == len(format_argument.get_values()) - 1:
                    next_literal = format_argument.get_values()[i]
                else:
                    next_literal = format_argument.get_values()[i + 1]

                if not isinstance(literal, ASTLiteral) or not isinstance(next_literal, ASTLiteral):
                    raise SemanticError('Printf, Element of format array is not a literal')
                elif literal.get_data_type() != DataType.NORMAL_CHAR or \
                        next_literal.get_data_type() != DataType.NORMAL_CHAR:
                    raise SemanticError('Printf, Format array: found literal not of type char')

                char = chr(int(literal.get_content()))

                if char == '%':
                    type_specification = chr(int(next_literal.get_content()))

                    if function_call_ast.get_function_called_id() == 'printf':
                        pointer_level = 0
                    elif function_call_ast.get_function_called_id() == 'scanf':
                        pointer_level = 1
                    else:
                        raise NotImplementedError(
                            f"Function {function_call_ast.get_function_called_id()} not recognized for format checking")

                    if type_specification == 'd':
                        symbol_type_specifications.append(DataType.DataType(DataType.DataTypeToken.INT, pointer_level))
                    elif type_specification == 'c':
                        symbol_type_specifications.append(DataType.DataType(DataType.DataTypeToken.CHAR, pointer_level))
                    elif type_specification == 's':
                        symbol_type_specifications.append(DataType.DataType(DataType.DataTypeToken.CHAR, 0, array=True))
                    elif type_specification == 'f':
                        symbol_type_specifications.append(
                            DataType.DataType(DataType.DataTypeToken.FLOAT, pointer_level))
                    else:
                        raise SemanticError(f'Could not deduce format %{type_specification}')

            # The first argument is the format argument, which doesn't code as a given parameter
            if len(symbol_type_specifications) != len(function_call_ast.get_arguments()) - 1:
                raise SemanticError(
                    f'Number of placeholder symbols ({len(symbol_type_specifications)}) '
                    f'does not match the number of arguments after the format ({len(function_call_ast.get_arguments()) - 1})')

            return symbol_type_specifications

    def check_io_function_call(self, ast: ASTFunctionCall):
        """
        Semantically checks the printf and scanf functions
        """

        if ast.get_function_called_id() == 'printf' or ast.get_function_called_id() == 'scanf':
            if len(ast.get_arguments()) == 0:
                raise SemanticError(f'No arguments provided for {ast.get_function_called_id()} function')

            symbol_type_specifications = self.check_function_call_with_format_arg(ast)

            if symbol_type_specifications is not None:

                # Printf contains formats such as '%d'. These are parsed and with the other arguments
                for i in range(1, len(symbol_type_specifications) + 1):
                    symbol_type_specification = symbol_type_specifications[i - 1]

                    resulting_data_type = self.check_resulting_data_type(ast.get_arguments()[i])

                    if symbol_type_specification != resulting_data_type:

                        if (symbol_type_specification.get_token().is_floating_point() and
                                resulting_data_type.get_token().is_floating_point()):
                            # If both types are floating point, its okay
                            continue

                        raise SemanticError(
                            f'{ast.get_function_called_id()} placeholder symbol data type ({symbol_type_specification}) '
                            f'does not match the data type of the argument given ({resulting_data_type})')

            else:
                print("WARN: format array cannot be deduced at compile time, not checking the format")

    def visit_ast_function_call(self, ast: ASTFunctionCall):
        function_identifier = ast.get_function_called_id()

        is_io_function_call = function_identifier == 'scanf' or function_identifier == 'printf'

        param_data_types = list()

        if is_io_function_call:
            self.check_io_function_call(ast)
            if function_identifier == 'scanf':
                for i in range(1, len(ast.get_arguments())):
                    arg = ast.get_arguments()[i]
                    if not isinstance(arg, ASTIdentifier):
                        raise SemanticError(f'Scanf function, argument {i}: An identifier must be provided')

                    else:
                        lookup = self.get_last_symbol_table().lookup(arg.get_name())

                        if not isinstance(lookup, VariableSymbol):
                            raise SemanticError(f'Scanf function, argument provided must be a variable symbol')
                        else:
                            # We set it to initialized as this is what we expect with the scanf function
                            lookup.initialized = True

        for arg in ast.get_arguments():
            self.check_undeclared_variable_usage(arg)
            self.check_uninitialized_variable_usage(arg)
            arg.accept(self)
            resulting_data_type_visitor = ASTVisitorResultingDataType(self.get_last_symbol_table())
            arg.accept(resulting_data_type_visitor)
            param_data_types.append(resulting_data_type_visitor.get_resulting_data_type())

        function_lookup = self.get_last_symbol_table().lookup(function_identifier)

        if function_lookup is None:
            raise SemanticError(f'Function {function_identifier} not found! Cannot call this function')
        else:
            assert isinstance(function_lookup, FunctionSymbol)

            if function_identifier != "printf" and function_identifier != "scanf":
                if len(function_lookup.get_params()) != len(ast.get_arguments()):
                    if len(function_lookup.get_params()) < len(ast.get_arguments()):
                        raise SemanticError(
                            f'Cannot call function {function_identifier}: to many arguments provided (is {len(ast.get_arguments())}, must be {len(function_lookup.get_params())})')
                    else:
                        if len(function_lookup.get_params()) > len(ast.get_arguments()):
                            raise SemanticError(
                                f'Cannot call function {function_identifier}: not enough arguments provided (is {len(ast.get_arguments())}, must be {len(function_lookup.get_params())})')
                else:

                    for i in range(len(function_lookup.get_params())):

                        data_type_param = function_lookup.get_params()[i].get_data_type()
                        data_type_argument = self.check_resulting_data_type(ast.get_arguments()[i])

                        if data_type_param != data_type_argument:
                            raise SemanticError(
                                f"Cannot call function: types don't match. ({data_type_param.get_name()} and {data_type_argument.get_name()})")

                    if not function_lookup.is_defined():
                        print(
                            f'warn: Function declaration {function_identifier} found but no definition for this function at the time of calling!')

    def visit_ast_function_declaration(self, ast: ASTFunctionDeclaration):
        """
        Basically takes over the scope thing a little bit because of the parameters
        """

        if self.get_last_symbol_table().get_scope_type() != SymbolTable.ScopeType.GLOBAL:
            raise SemanticError(
                f'Function declaration cannot be placed within scope {self.get_last_symbol_table().get_scope_type().name}')

        function_identifier = ast.get_identifier()
        param_data_types = list()

        param_names = list()
        for p in ast.get_params():
            if p.get_var_name() not in param_names:
                param_names.append(p.get_var_name())
            else:
                raise SemanticError(f'Multiple parameter declaration in declaration of {function_identifier}')

        for param in ast.get_params():
            param_data_types.append(param.get_data_type())

        function_symbol = self.get_last_symbol_table().lookup(function_identifier)
        if function_symbol is not None:

            assert isinstance(function_symbol, FunctionSymbol)

            if not len(function_symbol.get_params()) == len(ast.get_params()):
                raise SemanticError(
                    f'Wrong amount of parameters given for {function_identifier}: {len(function_symbol.get_params())} != {len(ast.get_params())}'
                )

            for i in range(len(function_symbol.get_params())):
                if function_symbol.get_params()[i].get_data_type() == ast.get_params()[i].get_data_type():
                    raise SemanticError(
                        f'Conflicting types'
                    )

            if function_symbol.get_return_type() != ast.get_return_type_ast().get_data_type():
                raise SemanticError(
                    f'Declaration of function with same name but different return types: {function_symbol.get_return_type()} and {ast.get_return_type_ast()}')
            else:
                print(f"Redundant declaration of function {function_identifier}")

        else:
            function_symbol = FunctionSymbol(function_identifier,
                                             ast.get_params(),
                                             ast.get_return_type_ast().get_data_type(), False)

            self.get_last_symbol_table().insert_symbol(
                function_symbol.get_name(), function_symbol)

        # Skip the on_scope entered thing because it is already done

    def visit_ast_function_definition(self, ast: ASTFunctionDefinition):
        if self.get_last_symbol_table().get_scope_type() != SymbolTable.ScopeType.GLOBAL:
            raise SemanticError(
                f'Function definition cannot be placed within scope {self.get_last_symbol_table().get_scope_type().name}')
        function_identifier = ast.get_function_declaration().get_identifier()
        param_data_types = list()

        param_names = list()
        function_declaration = ast.get_function_declaration()
        for p in function_declaration.get_params():
            if p.get_var_name() not in param_names:
                param_names.append(p.get_var_name())
            else:
                raise SemanticError(f'Multiple parameter declaration in declaration of {function_identifier}')

        for param in ast.get_function_declaration().get_params():
            param_data_types.append(param.get_data_type())

        function_symbol = self.get_last_symbol_table().lookup(function_identifier)

        if function_symbol is not None:
            assert isinstance(function_symbol, FunctionSymbol)

            if not len(function_symbol.get_params()) == len(ast.get_function_declaration().get_params()):
                raise SemanticError(
                    f'Wrong amount of parameters given for {function_identifier}: {len(function_symbol.get_params())} != {len(ast.get_function_declaration().get_params())}'
                )

            for i in range(len(function_symbol.get_params())):
                if function_symbol.get_params()[i].get_data_type() != ast.get_function_declaration().get_params()[
                    i].get_data_type():
                    raise SemanticError(
                        f'Conflicting types'
                    )

            if not function_symbol.get_return_type() == ast.get_function_declaration().get_return_type_ast().get_data_type():
                raise SemanticError(f'conflicting return types for {function_identifier}')

            if not function_symbol.is_defined():
                function_symbol.defined = True
            else:
                raise SemanticError(f'Redefinition of function {function_identifier}!')
        else:
            function_symbol = FunctionSymbol(function_identifier,
                                             ast.get_function_declaration().get_params(),
                                             ast.get_function_declaration().get_return_type_ast().get_data_type(),
                                             True)
            self.get_last_symbol_table().insert_symbol(
                function_symbol.get_name(), function_symbol)

        self.on_function_entered(function_symbol)
        self.on_scope_entered(SymbolTable.ScopeType.FUNCTION)
        for param in ast.get_function_declaration().get_params():
            # A little bit different then with normal variable declarations, which is why we handle it ourselves
            # The variable symbol will be set on initialized in the symbol table as it is a parameter, so values
            # are passed in
            assert isinstance(param, ASTVarDeclaration)
            var_name = param.get_var_name()
            self.get_last_symbol_table().insert_symbol(var_name,
                                                       VariableSymbol(param.get_var_name_ast().get_content(),
                                                                      DataType.DataType(
                                                                          param.get_data_type().get_token(),
                                                                          param.get_data_type().get_pointer_level() + 1),
                                                                      param.is_const(), True))

        # Skip the on_scope entered thing because it is already done
        super().visit_ast_scope(ast.get_execution_body())
        self.on_scope_exit()
        self.on_function_exit()

    def visit_ast_include(self, ast: ASTInclude):
        # Just simple placeholder params
        params = list()

        printf_symbol = FunctionSymbol("printf", params, DataType.NORMAL_INT, True)
        scanf_symbol = FunctionSymbol("scanf", params, DataType.NORMAL_INT, True)

        self.get_last_symbol_table().insert_symbol(printf_symbol.get_name(), printf_symbol)
        self.get_last_symbol_table().insert_symbol(scanf_symbol.get_name(), scanf_symbol)

    def visit_ast_access_element(self, ast: ASTAccessArrayVarExpression):
        variable_accessed = ast.get_variable_accessed().get_name()
        lookup = self.get_last_symbol_table().lookup(variable_accessed)

        if not isinstance(lookup, ArraySymbol):
            raise SemanticError(f'Type mismatch: variable {variable_accessed} trying to access is not an array!')

    def visit_ast_dereference(self, ast: ASTDereference):
        self.check_resulting_data_type(ast)

    def visit_ast_control_flow_statement(self, ast: ASTControlFlowStatement):
        if not self.get_last_symbol_table().get_scope_type() == SymbolTable.ScopeType.CONDITIONAL:
            raise SemanticError(
                f"Control flow statement '{ast.get_content()}' not placed within conditional scope (currently {self.get_last_symbol_table().get_scope_type().name.lower()} scope)")
