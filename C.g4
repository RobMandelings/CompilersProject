grammar C;
prog: stat+;
stat: expr ';';
expr: add value
    | expr mult expr
    | expr add expr
    | value
    ;
value: ID
     | DOUBLE
     | '(' expr ')'
     ;
add: '+' | '-';
mult: '*' | '/';

ID  :   [a-zA-Z]+ [0-9]* ;      // match identifiers
DOUBLE :   [0-9]+ ('.' [0-9]+)? ;
WS : [ \r\t\n]+ -> skip ;
