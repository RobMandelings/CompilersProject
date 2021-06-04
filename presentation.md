## Mandatory features

1. Binary operations: +, -, *, /, >, <, == <br>
2. Unary operations: +, -
3. Brackets (overwriting order of operations)
4. Supported data types: char, int, float and pointers (e.g. float**)
5. Special reserved words: const, if, else, while, for, break, continue, return and void
6. Variables<br>
   6.0. Local and global variables<br>
   6.1. Declaration<br>
   6.2. Definition<br>
   6.3. Assignments<br>

6.4. Identifiers appearing in expressions

7.Pointer operations: *, &

8. Comments: single-line, multi-line
9. Printf and Scanf functions
10. Scoping
11. Functions<br>
    11.1. Passing parameters by value and by reference (pointers)
12. Optimizations: unreachable and dead code not implemented
13. Arrays
14. Import <stdio.h> (printf, scanf)

## Optional features

1. Constant folding
2. Constant propagation: works with the reaching definition principle
3. Modulo operation: %
4. Comparison operations: <=, >=, !=
5. Identifier operations: ++, --
6. (Multiple variable declaration and/or initializations in one line, see benchmark prime.c for example)

## Added since intermediate presentation

Lots of bug fixes and improvements. Benchmark now running as it should.

Features that were not yet implemented:

1. Arrays and Global variables added
2. Scanf