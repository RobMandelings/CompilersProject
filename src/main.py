from CSTVisitors import CSTVisitorToDot
from src.ast.ASTVisitorConstantFolding import ASTVisitorConstantFolding
from src.ast.CSTtoASTConverter import *
from src.ast.ASTVisitorDot import ASTVisitorDot
from src.syntacticalAnalysis import CSTErrorListener
from src.ast.semantic_analysis.ASTVisitorSemanticAnalysis import ASTVisitorSemanticAnalysis, SemanticError


# TODO support for unary operations ('-5' for example)
def main(argv):
    input_stream = FileStream(argv[1])
    lexer = CLexer(input_stream)

    stream = CommonTokenStream(lexer)
    parser = CParser(stream)

    parser.removeErrorListeners()
    parser.addErrorListener(CSTErrorListener())

    try:
        tree = parser.program()

        cst_visitor_to_dot = CSTVisitorToDot()
        tree.accept(cst_visitor_to_dot)
        cst_visitor_to_dot.graph.render('output/cst.gv', view=False)

        ast = create_ast_from_concrete_syntax_tree(tree, lexer)
        ast_visitor_dot = ASTVisitorDot()
        ast.accept(ast_visitor_dot)
        ast_visitor_dot.graph.render('output/ast.gv', view=False)

        # ast_visitor_folding = ASTVisitorConstantFolding()
        # ast.accept(ast_visitor_folding)

        ast_visitor_dot = ASTVisitorDot()
        ast.accept(ast_visitor_dot)
        ast_visitor_dot.graph.render('output/astfolded.gv', view=False)

        ast_visitor_semantic_analysis = ASTVisitorSemanticAnalysis()
        try:
            ast.accept(ast_visitor_semantic_analysis)
        except SemanticError as e:
            print("A semantic error occurred: ")
            print(e)
            print("Stopping the compiler...")
            sys.exit(0)
        print(argv[1])

    except SyntaxError:
        print("Exiting program...", file=sys.stderr)
        sys.exit()


if __name__ == '__main__':
    main(sys.argv)
