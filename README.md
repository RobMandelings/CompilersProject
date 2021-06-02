# Testing our code

Run the main.py script using the following command: python main.py "input file". Our compiler will automatically produce
the following:

- Parsed Concrete Syntax Tree pdf
- Converted Abstract Syntax Tree pdf
- LLVM Output (.ll extension)
- MIPS Output (.asm extension)

## Features

We have implemented everything of the mandatory features, except support for arrays in MIPS. Due to lack of time,
considering we had the deadline on the 30th of may whilst also having the Computer Networking exam two days later, we
were not able to implement this final feature.

We have however, implemented some optional features from before which work both for MIPS and LLVM. These optional
features are:

- Constant Folding (see optimizations)
- Constant Propagation (see optimizations)
- Identifier Expressions (i++, --i,...)
- Fully sophisticated comparisons: <=, >= !=, < and >
- Multi variable declaration and initialization in one line / statement (see benchmark prime.c for example)

### Optimization

In order to facilitate the optimization feature, run the previous command but with a true after the filename.

The command would look like this:

python main.py "input file" true

# Bugs to solve

Float initialized with integer literal gives no semantical error anymore, and an integer is stored into floating point
variable. MIPS doesn't output anything for this.