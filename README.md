# CompilersProject

## TODO

### Dereferencing node

From the slides, it will be easier to compiler into llvm

#### y = x

#### *y = x

#### *y = &x

(for example)

### Implement char data type

## TO FIX

### Error 1

This gives an assertion error: char c = 'a';

### Error 2

If you put this in the inputfile.txt, the compiler says there is a token recognition error but continues anyway:

int i = 6;

const int a = 28.999; char c = 'a';

Improved semantic analysing on scopes: variables may be redeclared in another (deeper) scope, just not in the exact same
scope. Do a lookup_lookal instead of lookup to find the redeclaration of a variable

# Fixessss

Already declared errors with for loops event though not already declared