grammar C;
program:
    statement+
;

statement:
    singleLineStatement ';' |
    scopedStatement
    ;

singleLineStatement:
    expression |
    varDeclaration |
    controlFlowStatement |
    printfStatement
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

// TODO Should be checked semantically that break and continue is only allowed in loops or switch statements
controlFlowStatement: BREAK | CONTINUE | RETURN ;
printfStatement:
    'printf' '(' (ID|CHAR_LITERAL|INT_LITERAL|DOUBLE_LITERAL) ')'
    ;
varDeclaration:
    // Declaration and initialization
    varDeclarationAndInit |
    typeDeclaration1 ID
    ;

typeDeclaration1:
    // TODO instead of 'const int' also support 'int const'?
    constDeclaration typeDeclaration2
    | typeDeclaration2
    ;

typeDeclaration2: INT | CHAR | FLOAT ;
constDeclaration: CONST ;

varDeclarationAndInit: typeDeclaration1 varAssignment ;
varAssignment: ID '=' expression ;

expression:
    varDeclarationAndInit |
    varAssignment |
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
finalExpression: enclosedExpression | ID | CHAR_LITERAL | INT_LITERAL | DOUBLE_LITERAL ;

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
