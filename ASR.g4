grammar ASR;		
fragment DIGIT : [0-9] ;
FLOAT         : DIGIT+ '.' DIGIT+ ;
INTEGER : DIGIT+;
STRING : '"' ([a-zA-Z])+ '"';
BOOL : BOOLT | BOOLF;
BOOLT : 'true';
BOOLF : 'false';

// Keywords
PARAMKW : 'param';
COMPONENTKW : 'component'; 
TYPE : 'int'|'float'|'string'|'bool'|'id';

ASSIGN : '=';
EQ : '==';
LT : '<=';
DOT: '.';
LSQUARE: '[';
RSQUARE: ']';
variable: ID;
arrayaccess: LSQUARE (INTEGER|variable) RSQUARE;
componentfield: variable DOT ID DOT ID;
valueholder: (variable | componentfield) (arrayaccess)?;
literal : FLOAT | INTEGER | STRING | BOOL;
lexpr: valueholder;
rexpr: valueholder | literal;
assignexpr: lexpr ASSIGN rexpr;
expr: assignexpr NEWLINE*;
param: PARAMKW ID (literal)? NEWLINE+;         // match keyword hello followed by an identifier
component: COMPONENTKW ID '{' NEWLINE* componentfielddecl* NEWLINE* '}' NEWLINE*;
componentfielddecl: ID TYPE (literal)? NEWLINE+;
r  : param* component* expr* EOF;

DEFAULTVALUE: FLOAT 
| INTEGER 
| STRING;
ID : [a-z]+([a-z][0-9])* ;             // match lower-case identifiers
WS : [ \t]+ -> skip ; // skip spaces, tabs
NEWLINE             : '\r'? '\n';


