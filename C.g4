grammar C;
program:
instructions
| function+
| ;
function:
    ifStatement
   ;

// Everything to do with loops
loop:
    'while' '(' expr ')' scope |
    'for' '(' expr ';' expr ';' expr ')' scope
    ;

// Handles if, else if and else statement
ifStatement:
    'if' '(' expr ')' scope |
    'if' '(' expr ')' scope elseStatement
    ;
elseStatement:
    'else' ifStatement scope |
    'else' scope
    ;

// Handles scoping
scope: '{' program '}' ;

instructions: instruction+ ';';
instruction:
    varDeclaration
    | varAssignment
    | expr
    | controlFlowInstruction
    | printfInstruction
    ;

// TODO Should be checked semantically that break and continue is only allowed in loops or switch statements
controlFlowInstruction:
    BREAK |
    CONTINUE |
    RETURN
    ;
printfInstruction:
    'printf' '(' (ID|CHAR_LITERAL|INT_LITERAL|DOUBLE_LITERAL) ')'
    ;
varDeclaration:
    // Declaration and initialization
    typeDeclaration1 varAssignment
    | typeDeclaration1 ID
    ;
varAssignment:
    ID '=' expr
    ;
expr: compareExpr;
compareExpr:
    compareExpr '>' addExpr
    | compareExpr '<' addExpr
    | compareExpr '==' addExpr
    | addExpr
    ;
addExpr:
    addExpr '+' multExpr
    | addExpr '-' multExpr
    | multExpr
    ;
multExpr:
    multExpr '*' unaryExpr
    | multExpr '/' unaryExpr
    | unaryExpr
    ;
unaryExpr:
    '+' pointerExpr
    | '-' pointerExpr
    | pointerExpr
    ;
pointerExpr:
    '*' finalExpr
    | '&' finalExpr
    | finalExpr
    ;
finalExpr: ID
     | CHAR_LITERAL
     | INT_LITERAL
     | DOUBLE_LITERAL
     | '(' expr ')'
     ;
typeDeclaration1:
    // TODO instead of 'const int' also support 'int const'?
    constDeclaration typeDeclaration2
    | typeDeclaration2
    ;
typeDeclaration2:
    'int'
    | 'char'
    | 'float'
    ;
constDeclaration:
    'const'
    ;

// Reserved words
BREAK: 'break';
CONTINUE: 'continue';
RETURN: 'return';

IF: 'if';
ELSE: 'else';
WHILE: 'while';

CONST: 'const';
CHAR: 'char';
INT: 'int';
FLOAT: 'float';

ID  :   [a-zA-Z_]+ [0-9_]* ;      // match identifiers
CHAR_LITERAL: '\''.'\'' ;
INT_LITERAL: [0-9]+ ;
DOUBLE_LITERAL :   [0-9]+'.'[0-9]+ ;
LineComment: '//' ~[\r\n]* -> channel(HIDDEN);
BlockComment: '/*' .*? '*/' -> channel(HIDDEN);
WS : [ \r\t\n]+ -> skip ;
