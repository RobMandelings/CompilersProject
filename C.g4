grammar C;
program: instructions;
instructions: instruction+;
instruction:
    varDeclaration ';'
    | varAssignment ';'
    | expr ';'
    | printfInstruction
    ;
printfInstruction:
    'printf' '(' (ID|CHAR|DOUBLE|INTEGER) ')' ';'
    ;
varDeclaration:
    // Declaration and initialization
    typeDeclaration1 varInit
    | typeDeclaration1 ID
    ;
varInit:
    ID '=' expr
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
    multExpr '*' finalExpr
    | multExpr '/' finalExpr
    | unaryExpr
    ;
unaryExpr:
    '*' finalExpr
    | '&' finalExpr
    | '+' finalExpr
    | '-' finalExpr
    | finalExpr
    ;
finalExpr: ID
     | CHAR
     | INTEGER
     | DOUBLE
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
ID  :   [a-zA-Z_]+ [0-9_]* ;      // match identifiers
CHAR: '\''.'\'' ;
INTEGER: [0-9]+ ;
DOUBLE :   [0-9]+'.'[0-9]+ ;
LineComment: '//' ~[\r\n]* -> channel(HIDDEN);
BlockComment: '/*' .*? '*/' -> channel(HIDDEN);
WS : [ \r\t\n]+ -> skip ;
