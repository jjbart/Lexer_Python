'''
List of all the token types of the Lexer
'''

UNRECOGNIZED_TOKEN = (0, "unrecog tok")
CANNOT_OPEN_FILE   = (1, "can't open file")
INTLIT             = (2, "integer lit")
PLUS               = (3, "plus")
MINUS              = (4, "minus")
TIMES              = (5, "multiply")
DIVIDE             = (6, "divide")
MOD                = (7, "mod")
BANG               = (8, "bang")
PARENL             = (9, "Left paren")
PARENR             = (10, "Right paren")
ID                 = (11, "identifier")
KEYWORD            = (12, "Keyword")
FLOATLIT           = (13, "float")
LBRACE             = (14, "Left brace")
RBRACE             = (15, "Right brace")
DBAR               = (16, "double bar")
GREATEREQ          = (17, "great-equal")
LESSEQ             = (18, "less-equal")
LESS               = (19, "less")
GREATER            = (20, "greater")
EQUALTO            = (21, "equal-equal")
NEQUALTO           = (22, "bang-equal")
DAMP               = (23, "dub amp")
SEMI               = (24, "semi-colon")
COMMA              = (25, "comma")
ASSIGN             = (26, "assignment")
BRACKETL           = (27, "Left brack")
BRACKETR           = (28, "Right brack")
COLON              = (29, "colon")
END_OF_FILE        = (30, "End of file")
BOOL               = (31, "keyword: bool")
ELSE               = (32, "keyword: else")
FALSE              = (33, "keyword: false")
TRUE               = (34, "keyword: true")
IF                 = (35, "keyword: if")
FLOAT              = (36, "keyword: float")
INT                = (37, "keyword: int")
MAIN               = (38, "keyword: main")
WHILE              = (39, "keyword: while")
PRINT              = (40, "keyword: print")
CHAR               = (41, "keyword: char")