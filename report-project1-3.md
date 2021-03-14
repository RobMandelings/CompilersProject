# Report: assignments 1 - 3

## Assignment 1

We implemented all mandatory features of this assignment and only one optional so far. An AST can be constructed from
the Parse Tree using the class CSTToASTConverter. This class recursively iterates through each node in the Concrete
Syntax Tree to decide which node in the AST will be created (if any). Our grammar is able to parse basic expressions.

The optional feature we already implemented was constant folding, as it seemed easier to work with.

## Assignment 2

All mandatory features of this assignment are implemented as well. No optionals have been implemented so far due to lack
of time. Our grammar is able to fully parse types, reserved words, variables and pointer operations. Using the
ErrorListener, we can print all syntax errors the ANTLR generated parser has encountered and stop the compiler
accordingly. We also implemented a visitor for the abstract syntax tree to detect semantical errors and lets the user
know what went wrong. We might want to add some line numbers here as well, which will be added in the future.

## Assignment 3

For this assignment, we added comments and printf to our grammar so far. We again used the visitor design patten to
generate our LLVM code from an abstract syntax tree, in which the visitor uses an LLVMBuilder class to construct the
actual LLVM IR. In this builder, we use a new symbol table to keep track of the current variables in the scope (
currently only global though). These variables are mapped on a register in LLVM. We currently only support assignments
and binary expressions for integers, but can be expanded very easily. Unfortunately, due to some setbacks we weren't
able to fully complete this assignment.