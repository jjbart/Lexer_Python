import re

class Lexer(object):

    def __init__(self,filename):
        '''
        :param filename: name of the file being tokenized
        '''
        self.filename = filename

    def token_generator(self):
        '''
        tokenizes the file based on desired splitting characters
        :return: a tuple consisting of the type of token, the token, and the line number (type, token, linecount)
        '''

        CANNOT_OPEN_FILE = (1, "can't open file")
        END_OF_FILE = 30

        try:
            file = open(self.filename)
        except IOError:
            print("Cannot open file {0}".format(self.filename))
            return (CANNOT_OPEN_FILE, self.filename )

        linecount = 1

        while True:
            line = file.readline()
            if not line:
                break


            tokens = re.split("\s+|(\+)|(\-)|(\<=)|(\>=)|(\<)|(\>)|(\!=)|(\==)|(\:)"
                              "|(\=)|(\;)|(\,)|(\{)|(\})|(\[)|(\])|(\()|(\))|(\//)|(\/)", line)


            for tok in tokens:
                if tok == '' or tok == None:
                    continue

                if tok == "//":
                    break


                yield (self.ruless(tok),tok,linecount)

            linecount += 1

        while True:
            yield (END_OF_FILE, "End of file")

    def ruless(self,tok):

        '''
        :param tok: an individual token from the current line of the text
        :return: the type of token
        '''

        UNRECOGNIZED_TOKEN = (0, "unrecog tok")
        INTLIT             = (2, "integer lit")
        PLUS               = (3, "plus")
        MINUS              = (4, "minus")
        MULT               = (5, "multiply")
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

        keywords ={ "bool": BOOL, "else": ELSE, "false": FALSE,"true": TRUE,"if": IF, "float": FLOAT,
                   "int": INT, "main": MAIN, "while": WHILE, "print": PRINT, "char": CHAR}

        rules = {'^[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?$': FLOATLIT, '\+': PLUS,
                 '\-': MINUS, '\*': MULT, '^\/$': DIVIDE, '\%': MOD, '\!': BANG, '\(': PARENL, '\)': PARENR,
                 '^[a-zA-Z_]\w*$': ID, '\{': LBRACE, '\}': RBRACE, '\|\|': DBAR,'\>=': GREATEREQ,
                 '\<=': LESSEQ, '\<': LESS, '\>': GREATER, '\==': EQUALTO, '\!=': NEQUALTO, '\&&': DAMP,
                 '\;': SEMI, '\,': COMMA, '\=': ASSIGN, '\[': BRACKETL, '\]': BRACKETR, '\:': COLON}

        for key in keywords:
            if tok == key:
                return (keywords[key])

        for key in rules:
            if re.match('^[+-]?\d+$', tok):
                return INTLIT
            if re.match(key, tok):
                return rules[key]

        return (UNRECOGNIZED_TOKEN)


def is_float(flo):
    '''
    :param flo: the token in string format
    :return: True or False depending on whether the token is a floating point
    '''
    if re.match('^[+-]?\d+$', flo):
        return False
    else:
        if re.match('^[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?$', flo):
            return True
        else:
            return False
