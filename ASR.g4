grammar ASR;		
fragment DIGIT : [0-9] ;
fragment FLOAT         : DIGIT+ '.' DIGIT+ ;
fragment INTEGER : DIGIT+;
fragment STRING : '"' ([a-zA-Z])+ '"';

// Keywords
PARAMKW : 'param';
ENTITYKW : 'entity'; 
TYPE : 'int'|'float'|'string'|'id';
r  : param* entity* EOF;
param: PARAMKW ID DEFAULTVALUE NEWLINE+;         // match keyword hello followed by an identifier
entity: ENTITYKW ID '{' NEWLINE* entityfield* NEWLINE* '}' NEWLINE*;
entityfield: ID TYPE ('default' DEFAULTVALUE)? NEWLINE+;
DEFAULTVALUE: FLOAT 
| INTEGER 
| STRING;
ID : [a-z]+([a-z][0-9])* ;             // match lower-case identifiers
WS : [ \t]+ -> skip ; // skip spaces, tabs
NEWLINE             : '\r'? '\n';


