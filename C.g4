grammar C;
stat: expr SEMICOLON;
expr: add value
    | expr mult expr
    | expr add expr
    | value
    ;
value: ID
     | DOUBLE
     | '(' expr ')'
     ;
end_of_line: SEMICOLON;
add: '+' | '-';
mult: '*' | '/';


MUL :   '*' ; // assigns token name to '*' used above in grammar
DIV :   '/' ;
ADD :   '+' ;
SUB :   '-' ;
SEMICOLON :   ';' ;
ID  :   [a-zA-Z]+ [0-9]* ;      // match identifiers
DOUBLE :   [0-9]+ ('.' [0-9]+)? ;
WS : [ \r\t\n]+ -> skip ;
