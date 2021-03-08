grammar C;
program: statement+;
statement:
    varDeclaration ';'
    | varAssignment ';'
    | expr ';'
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
    multExpr '*' finalExpr
    | multExpr '/' finalExpr
    | finalExpr
    ;
finalExpr: ID
     | DOUBLE
     | INTEGER
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
INTEGER: [0-9]+ ;
DOUBLE :   [0-9]+'.'[0-9]+ ;
WS : [ \r\t\n]+ -> skip ;