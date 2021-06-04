grammar C;
program:
    // We start with a global scope which may contain statements
    includeStdio?
    statement*
;

functionDeclaration: dataType ID '(' ((multiVarDeclaration ',')* multiVarDeclaration)? ')';
functionDefinition: functionDeclaration scope ;

includeStdio: '#include <stdio.h>';


/**
 * Statements
 */
statement:
    singleLineStatement ';' |
    scopedStatement
    ;

// Single line
singleLineStatement:
    functionDeclaration |
    multiVarDeclaration |
    //varDeclarationAndInit |
    controlFlowStatement |
    expression
    ;

controlFlowStatement: BREAK | CONTINUE | returnStatement ;
returnStatement: RETURN expression?;

// Scoped statements
scopedStatement:
    functionDefinition |
    loop |
    ifStatement |
    scope
    ;

loop:
    whileLoop |
    forLoop
    ;

whileLoop: WHILE enclosedExpression scope ;
forLoop: FOR '(' (expression | singleVarDeclaration) ';' expression ';' expression ')' scope ;

ifStatement:
    IF enclosedExpression scope |
    IF enclosedExpression scope elseStatement
    ;
elseStatement:
    ELSE IF enclosedExpression scope elseStatement |
    ELSE IF enclosedExpression scope |
    ELSE scope
    ;

scope: '{' statement* '}' ;

/**
 * Declarations and initializations
 */

multiVarDeclaration: typeDeclaration (singleVarDeclaration ',')* singleVarDeclaration ;

singleVarDeclaration: ID arrayDeclaration? varInitialization? ;
arrayDeclaration: '[' INT_LITERAL ']' ;
varInitialization: '=' expression ;

normalVarDeclaration: typeDeclaration ID ;
arrayVarDeclaration: typeDeclaration ID '[' INT_LITERAL ']' ;

typeDeclaration:
    // TODO instead of 'const int' also support 'int const'?
    typeAttributes dataType
    | dataType
    ;

// Used in combinations with string initialization
charTypeDeclaration:
    typeAttributes CHAR |
    CHAR
    ;

varDeclarationAndInit:
    normalVarDeclarationAndInit |
    arrayVarDeclarationAndInit
;

normalVarDeclarationAndInit: typeDeclaration ID '=' expression ;

arrayVarDeclarationAndInit:
    typeDeclaration ID '[' INT_LITERAL ']' '=' braceInitializer |
    charTypeDeclaration ID '['INT_LITERAL ']' '=' STRING ;

braceInitializer: '{' ((value ',')* value)? '}' ;

/**
 * Expressions
 */

expression:
    compareExpression
    ;

functionCallExpression: ID '(' ((expression ',')* expression)? ')' ;
accessArrayVarExpression: ID '[' expression ']' ;

compareExpression:
    compareExpression '>' assignmentExpression
    | compareExpression '<' assignmentExpression
    | compareExpression '==' assignmentExpression
    | compareExpression '>=' assignmentExpression
    | compareExpression '<=' assignmentExpression
    | compareExpression '!=' assignmentExpression
    | assignmentExpression
    ;
assignmentExpression:
    assignmentExpression '=' addExpression
    | assignmentExpression '+=' addExpression
    | assignmentExpression '-=' addExpression
    | assignmentExpression '*=' addExpression
    | assignmentExpression '/=' addExpression
    | addExpression
    ;
addExpression:
    addExpression '+' multExpression
    | addExpression '-' multExpression
    | multExpression
    ;
multExpression:
    multExpression '%' unaryExpression
    | multExpression '*' unaryExpression
    | multExpression '/' unaryExpression
    | unaryExpression
    ;
unaryExpression:
    '+' unaryExpression
    | '-' unaryExpression
    | pointerExpression
    ;
pointerExpression:
    '*' pointerExpression
    | '&' pointerExpression
    | finalExpression
    ;

enclosedExpression: '(' expression ')';
finalExpression:
    enclosedExpression
    | identifierExpression
    | accessArrayVarExpression
    | functionCallExpression
    ;
identifierExpression:
    value |
    (ID | enclosedExpression) INCREMENT |
    (ID | enclosedExpression) DECREMENT |
    INCREMENT (ID | enclosedExpression) |
    DECREMENT (ID | enclosedExpression)
    ;

/**
 * Value wrappers
 */
typeAttributes: CONST ;
dataType: (CHAR | INT | FLOAT | VOID) ('*')*  ;
value: ID | CHAR_LITERAL | INT_LITERAL | DOUBLE_LITERAL | STRING;

/**
 * Lexer rules
 */
// Reserved words

INCREMENT: '++' ;
DECREMENT: '--' ;

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
STRING: '"' ( '\\"' | . )*? '"' ;
CHAR_LITERAL: '\''.'\'' ;
INT_LITERAL: [0-9]+ ;
DOUBLE_LITERAL :   [0-9]+'.'[0-9]+ ;

// Comments
LineComment: '//' ~[\r\n]* -> channel(HIDDEN);
BlockComment: '/*' .*? '*/' -> channel(HIDDEN);

// Skip whitespace
WS : [ \r\t\n]+ -> skip ;
