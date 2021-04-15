grammar C;
program:
    // We start with a global scope which may contain statements
    functionDeclaration+
;

functionDeclaration: dataType ID '(' ((varDeclaration ',')* varDeclaration)? ')' scope ;

statement:
    singleLineStatement ';' |
    scopedStatement
    ;

singleLineStatement:
    functionCall |
    varDeclaration |
    controlFlowStatement |
    printfStatement |
    expression
    ;

scopedStatement:
    scope |
    loop |
    ifStatement
    ;

// Everything to do with loops
loop:
    WHILE enclosedExpression scope |
    FOR '(' expression ';' expression ';' expression ')' scope
    ;

// Handles if, else if and else statement
ifStatement:
    IF enclosedExpression scope |
    IF enclosedExpression scope elseStatement
    ;
elseStatement:
    ELSE IF enclosedExpression scope elseStatement |
    ELSE IF enclosedExpression scope |
    ELSE scope
    ;

// Handles scoping
scope:
    '{' '}' |
    '{' statement+ '}';

functionCall: ID '(' ((value ',')* value)? ')' ;

// TODO Should be checked semantically that break and continue is only allowed in loops or switch statements
controlFlowStatement: BREAK | CONTINUE | returnStatement ;
returnStatement: RETURN value ;

printfStatement: 'printf' '(' value ')' ;
varDeclaration: (typeDeclaration ID) | arrayDeclaration ;
arrayDeclaration: typeDeclaration ID '[' INT_LITERAL ']' ;

typeDeclaration:
    // TODO instead of 'const int' also support 'int const'?
    CONST dataType
    | dataType
    ;

varDeclarationAndInit: (typeDeclaration ID '=' expression) | arrayDeclarationAndInit ;
assignment: (ID | accessArrayElement) '=' expression ;
arrayDeclarationAndInit: arrayDeclaration '=' '{' ((value ',')* value)? '}' ;
accessArrayElement: ID '[' INT_LITERAL ']' ;

expression:
    varDeclarationAndInit |
    assignment |
    compareExpression
    ;
compareExpression:
    compareExpression '>' addExpression
    | compareExpression '<' addExpression
    | compareExpression '==' addExpression
    | addExpression
    ;
addExpression:
    addExpression '+' multExpression
    | addExpression '-' multExpression
    | multExpression
    ;
multExpression:
    multExpression '*' unaryExpression
    | multExpression '/' unaryExpression
    | unaryExpression
    ;
unaryExpression:
    '+' unaryExpression
    | '-' unaryExpression
    | pointerExpression
    ;
pointerExpression:
    '*' finalExpression
    | '&' finalExpression
    | finalExpression
    ;
enclosedExpression: '(' expression ')';
finalExpression: enclosedExpression | value ;

dataType: ((CHAR | INT | FLOAT) ('*')*) | (VOID ('*')+)  ;
value: ID | CHAR_LITERAL | INT_LITERAL | DOUBLE_LITERAL;
// Reserved words
BREAK: 'break';
CONTINUE: 'continue';
RETURN: 'return';

IF: 'if';
ELSE: 'else';
WHILE: 'while';
FOR: 'for';

CONST: 'const';

CHAR: 'char';
INT: 'int';
FLOAT: 'float';

VOID: 'void' ;

// These nodes will be skipped when creating the AST as they have no purpose after conversion
TO_SKIP: '{' | '}' | '(' | ')' | ';' ;

// Literals and identifiers
ID  :   [a-zA-Z_]+ [0-9_]* ;
CHAR_LITERAL: '\''.'\'' ;
INT_LITERAL: [0-9]+ ;
DOUBLE_LITERAL :   [0-9]+'.'[0-9]+ ;

// Comments
LineComment: '//' ~[\r\n]* -> channel(HIDDEN);
BlockComment: '/*' .*? '*/' -> channel(HIDDEN);

// Skip whitespace
WS : [ \r\t\n]+ -> skip ;
