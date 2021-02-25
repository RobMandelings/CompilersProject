grammar C;
prog: stat+;
stat: expr ';';
expr: addExpr;
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
     | '(' expr ')'
     ;
ID  :   [a-zA-Z]+ [0-9]* ;      // match identifiers
DOUBLE :   [0-9]+ ('.' [0-9]+)? ;
WS : [ \r\t\n]+ -> skip ;