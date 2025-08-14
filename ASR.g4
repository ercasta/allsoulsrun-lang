grammar ASR;		
fragment DIGIT : [0-9] ;
fragment FLOAT         : DIGIT+ '.' DIGIT+ ;
fragment INTEGER : DIGIT+;
fragment STRING : '"' ([a-zA-Z])+ '"';
r  : param+ EOF;
param: PARAMKW ID DEFAULTVALUE NEWLINE?;         // match keyword hello followed by an identifier
DEFAULTVALUE: FLOAT 
| INTEGER 
| STRING;
PARAMKW : 'param';
ID : [a-z]+ ;             // match lower-case identifiers
WS : [ \t]+ -> skip ; // skip spaces, tabs, newlines
NEWLINE             : '\r'? '\n';

