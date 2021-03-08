grammar C;
program: statement+;
statement:
    varDeclaration
    | varAssignment
    | expr ';'
    ;
varDeclaration:
    // Declaration and initialization
    typeDeclaration varAssignment
    typeDeclaration ID ';'
    ;
varAssignment:
    ID '=' expr ';'
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
typeDeclaration:
    | 'const' typeDeclaration
    // TODO instead of 'const int' also support 'int const'?
    | 'int'
    | 'char'
    | 'float'
    ;
ID  :   [a-zA-Z_]+ [0-9_]* ;      // match identifiers
INTEGER: [0-9]+ ;
DOUBLE :   [0-9]+'.'[0-9]+ ;
WS : [ \r\t\n]+ -> skip ;