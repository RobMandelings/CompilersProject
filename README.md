# Testing our compiler

Run the main.py script using the following command: python main.py "input file". Our compiler will automatically produce
the following:

- Parsed Concrete Syntax Tree pdf
- Converted Abstract Syntax Tree pdf
- LLVM Output (.ll extension)
- MIPS Output (.asm extension)

In order to run our compiler, run one of following commands:

python main.py <optimize: true/false><br>

This will run the compiler against all files present in the benchmark: CorrectCode and SemanticErrors, and produce the
output in subfolders (asts/ and compiled_code/). This will most likely be the most helpful one for evaluation. It
generates a

- benchmarks.log: file which includes all encountered errors (semantic/syntax/something else from our compiler)
  so you can easily see what went wrong when compiling each file. If successful, nothing is outputted to this log for
  the current c file.

- summary_benchmarks.log file: shows a summary of how many compilations were succesful, how many attempted compilations
  with syntax errors,... It also includes the percentage of success

As you will notice, in the SemanticErrors summary, there are a few SyntaxErrors instead of SemanticErrors. This is
because some things might have been catched earlier, before needing to semantically check it. E.g: int a[0.5] will never
work, as you may only give the size of a static array at compilation time instead of runtime, and you cannot enter a
floating point as array access element.

python main.py <filepath> <optimize: true/false>

Compiles the code present in the file and generates the output. Must be a file with a .c extension

### Optimization

In order to facilitate the optimization feature, run the previous command but with a true after the filename.

The command would look like this:

python main.py "input file" true

## Removed/adjusted in benchmark

In order to make the compiler work fully with our implemented features, we have removed/adjusted some files as these
were optionals that we did not implement:

comparisons1.c<br>
floatToIntConversion.c<br>
intToFloatConversion.c<br>
if.c: replaced && 1 with a nested if statement, as we don't support logical operators<br>
ifElse.c: replaced && 1 with a nested if as we don't support logical operators<br>

# Features

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
   6.4. Identifiers appearing in expressions 7.Pointer operations: *, &
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
7. Efficient register retrieval<br>
   7.1. Depending on register and address descriptors<br>
   7.2. Storing and loading only registers that are used in function

## Added since intermediate presentation

Lots of bug fixes and improvements. Benchmark now running as it should.

Features that were not yet implemented:

1. Arrays and Global variables added
2. Scanf

