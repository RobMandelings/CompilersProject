grammar C;
program:
    body
;

// Everything that you can do within a scope as well as outside a scope. May also contain whitespaces
body:
    instruction+ ';' |
    loop+ |
    ifStatement+ |
    WS
    ;

// Everything to do with loops
loop:
    WHILE enclosedExpression scope |
    FOR '(' expr ';' expr ';' expr ')' scope
    ;

// Handles if, else if and else statement
ifStatement:
    IF enclosedExpression scope |
    IF enclosedExpression scope elseStatement
    ;
elseStatement:
    ELSE IF enclosedExpression scope elseStatement |
    ELSE scope
    ;

// Handles scoping
scope: '{' body '}' ;

instruction:
    varDeclaration
    | varAssignment
    | expr
    | controlFlowInstruction
    | printfInstruction
    ;

// TODO Should be checked semantically that break and continue is only allowed in loops or switch statements
controlFlowInstruction:
    BREAK |
    CONTINUE |
    RETURN
    ;
printfInstruction:
    'printf' '(' (ID|CHAR_LITERAL|INT_LITERAL|DOUBLE_LITERAL) ')'
    ;
varDeclaration:
    // Declaration and initialization
    typeDeclaration1 varAssignment
    | typeDeclaration1 ID
    ;

varAssignment:
    ID '=' expr
    ;

typeDeclaration1:
    // TODO instead of 'const int' also support 'int const'?
    constDeclaration typeDeclaration2
    | typeDeclaration2
    ;
typeDeclaration2: INT | CHAR | FLOAT ;
constDeclaration: CONST ;

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
    multExpr '*' unaryExpr
    | multExpr '/' unaryExpr
    | unaryExpr
    ;
unaryExpr:
    '+' pointerExpr
    | '-' pointerExpr
    | pointerExpr
    ;
pointerExpr:
    '*' finalExpr
    | '&' finalExpr
    | finalExpr
    ;
enclosedExpression:
    '(' expr ')';
finalExpr: ID
     | CHAR_LITERAL
     | INT_LITERAL
     | DOUBLE_LITERAL
     | enclosedExpression
     ;

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

ID  :   [a-zA-Z_]+ [0-9_]* ;      // match identifiers
CHAR_LITERAL: '\''.'\'' ;
INT_LITERAL: [0-9]+ ;
DOUBLE_LITERAL :   [0-9]+'.'[0-9]+ ;
LineComment: '//' ~[\r\n]* -> channel(HIDDEN);
BlockComment: '/*' .*? '*/' -> channel(HIDDEN);
WS : [ \r\t\n]+ -> skip ;
