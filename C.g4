grammar C;
prog: stat+;
stat: expr ';';
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
ID  :   [a-zA-Z]+ [0-9]* ;      // match identifiers
INTEGER: [0-9]+ ;
DOUBLE :   [0-9]+'.'[0-9]+ ;
WS : [ \r\t\n]+ -> skip ;