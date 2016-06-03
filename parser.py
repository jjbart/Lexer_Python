import Lexer
import ast
import values

class Parser(object):
    '''
    Parser class will encapsulate all of our parsing functions.
    There will be one public function called parse().
    '''

    def __init__(self, filename):
        self.filename = filename
        self.lex_gen = Lexer.Lexer(filename)
        self.lex_gen = self.lex_gen.token_generator()


        # get the ball rolling looking at the first token
        self.curr_tok = self.lex_gen.__next__()


    def parse(self):
        '''
        Parse a Clite file
        :return: Expr
        '''

        tree = self.program()
        if self.curr_tok != values.END_OF_FILE:
            raise CliteSyntaxError("Extra symbols in input")

        return tree

    def program(self):
        '''
        Program -> int  main ( ) { Declarations Statements }

        :return: Program object
        '''

        # match int main ( ) open brace
        if self.curr_tok[0] != values.INT:
            raise CliteSyntaxError("Keyword 'int' expected")
        self.curr_tok = self.lex_gen.__next__()

        if self.curr_tok[0] != values.MAIN:
            raise CliteSyntaxError("Keyword 'main' expected")
        self.curr_tok = self.lex_gen.__next__()

        if self.curr_tok[0] != values.PARENL:
            raise CliteSyntaxError(" ( expected")
        self.curr_tok = self.lex_gen.__next__()

        if self.curr_tok[0] != values.PARENR:
            raise CliteSyntaxError(" ) expected")
        self.curr_tok = self.lex_gen.__next__()

        if self.curr_tok[0] != values.LBRACE:
            raise CliteSyntaxError(" { expected")
        self.curr_tok = self.lex_gen.__next__()


        self.decls = self.declarations()
        self.stmts = self.statements()


        prog = ast.Program(self.decls, self.stmts, self.declList)



        if self.curr_tok[0] != values.RBRACE:
            raise CliteSyntaxError(" } expected")
        self.curr_tok = self.lex_gen.__next__()

        return prog

    def declarations(self):
        '''
        Declarations -> { Declaration }
        :return: list of declarations
        '''
        decldict = {}
        self.declList = []

        while self.curr_tok[0] == values.INT or self.curr_tok[0] == values.BOOL \
                or self.curr_tok[0] == values.FLOAT or self.curr_tok[0] == values.CHAR:
            decl = self.declaration()
            id = decl[0][1]
            typename = decl[1][1]


            # what kind of error checking can we do here?
            if id in decldict:
                raise CliteSyntaxError('Identifier already declared')

            decldict[id] = typename
            self.declList.append(id)

        return decldict



    def declaration(self):
        '''
        Declaration -> Type  Identifier  ;
        :return: type and identifier tuple
        '''
        tmptype = self.curr_tok
        self.curr_tok = self.lex_gen.__next__()

        if self.curr_tok[0] != values.ID:
            raise CliteSyntaxError("Identifier expected")

        tmpid = self.curr_tok

        # consume ident
        self.curr_tok = self.lex_gen.__next__()


        # match a semicolon
        if self.curr_tok[0] != values.SEMI:
            raise CliteSyntaxError("Semicolon expected")

        self.curr_tok = self.lex_gen.__next__()

        return (tmpid, tmptype)


    def statements(self):
        '''
        Statements -> { Statement }
        :return: list of statements
        '''

        first_set = {values.SEMI, values.WHILE, values.IF, values.PRINT, values.LBRACE, values.ID}

        stmts = []

        while self.curr_tok[0] in first_set:
            # do not consume the token yet
            stmts.append(self.statement())

        return stmts

    def statement(self):
        '''
        Statement ->  ; | Block | Assignment | IfStatement
                       | WhileStatement | PrintStatement
        :return: a Semi object or a tree of objects consisting of the documentation above
        '''

        if self.curr_tok[0] == values.SEMI:
            self.curr_tok = self.lex_gen.__next__()
            return ast.Semi()
        elif self.curr_tok[0] == values.LBRACE:
            return self.block()
        elif self.curr_tok[0] == values.ID:
            return self.assignment()
        elif self.curr_tok[0] == values.IF:
            return self.ifStatement()
        elif self.curr_tok[0] == values.WHILE:
            return self.whileStatement()
        elif self.curr_tok[0] == values.PRINT:
            return self.printStatement()

    def block(self):
        '''
        Block -> '{' Statements '}'
        :return: a Block object
        '''
        # match/consume the opening brace
        self.curr_tok = self.lex_gen.__next__()


        stmts = self.statements()


        if self.curr_tok[0] != values.RBRACE:
            raise CliteSyntaxError('} expected' )

        self.curr_tok = self.lex_gen.__next__()

        return ast.Block(stmts)

    def assignment(self):
        '''
        Assignment -> Identifier = Expression;
        :return: an Assign object
        '''

        # save and match identifier
        idtok = self.curr_tok
        self.curr_tok = self.lex_gen.__next__()

        if self.curr_tok[0] != values.ASSIGN:
            raise CliteSyntaxError("= expected")

        # what is true here? Match an =
        self.curr_tok = self.lex_gen.__next__()

        expr = self.expression()

        # we should be looking at a semicolon
        if self.curr_tok[0] != values.SEMI:
            raise CliteSyntaxError("; expected")
        self.curr_tok = self.lex_gen.__next__()

        # error checking? make sure idtok is declared
        if idtok[1] not in self.decls:
            raise CliteSyntaxError("Identifier is not declared")

        return ast.Assign(idtok[1], expr)

    def ifStatement(self):
        '''
        IfStatement ->  if ( Expression ) Statement [ else Statement ]
        :return: an IfState object
        '''
        self.curr_tok = self.lex_gen.__next__()

        if self.curr_tok[0] == values.PARENL:
            self.curr_tok = self.lex_gen.__next__()

            expr = self.expression()

            if self.curr_tok[0] == values.PARENR:

                self.curr_tok = self.lex_gen.__next__()
                stmt = self.statement()
            else:
                raise CliteSyntaxError("Missing right parenthesis")
        else:
            raise CliteSyntaxError("Left parenthesis expected")

        return ast.IfState(expr, stmt)

    def whileStatement(self):
        '''
        WhileStatement -> while ( Expression ) Statement
        :return: a WhileState object
        '''
        self.curr_tok = self.lex_gen.__next__()

        if self.curr_tok[0] == values.PARENL:
            self.curr_tok = self.lex_gen.__next__()

            expr = self.expression()

            if self.curr_tok[0] == values.PARENR:
                self.curr_tok = self.lex_gen.__next__()
                stmt = self.statement()
            else:
                raise CliteSyntaxError("Missing right parenthesis")
        else:
            raise CliteSyntaxError("Left parenthesis expected")

        return ast.WhileState(expr, stmt)

    def printStatement(self):
        '''
        PrintStatement -> print( Expression )
        :return: a PrintState object
        '''

        self.curr_tok = self.lex_gen.__next__()

        if self.curr_tok[0] == values.PARENL:
            self.curr_tok = self.lex_gen.__next__()

            expr = self.expression()

            if self.curr_tok[0] == values.PARENR:
                self.curr_tok = self.lex_gen.__next__()
                if self.curr_tok[0] == values.SEMI:
                    self.curr_tok = self.lex_gen.__next__()
                    return ast.PrintState(expr)
                else:
                    raise CliteSyntaxError("; expected")
            else:
                raise CliteSyntaxError("Missing right parenthesis")
        else:
            raise CliteSyntaxError("Left parenthesis expected")



    def expression(self):
        '''
        Expression -> Conjunction { ||  Conjunction }
        :return: a BinaryDBarExpr object
        '''

        left_tree = self.conjunction()

        while self.curr_tok[0] == values.DBAR:
            self.curr_tok = self.lex_gen.__next__()
            right_tree = self.conjunction()
            left_tree = ast.BinaryDBarExpr(left_tree, right_tree)

        return left_tree

    def conjunction(self):
        '''
        Conjunction -> Equality { && Equality }
        :return: a BinaryDampExpre object
        '''

        left_tree = self.equality()

        while self.curr_tok[0] == values.DAMP:
            self.curr_tok = self.lex_gen.__next__()
            right_tree = self.equality()
            left_tree = ast.BinaryDampExpr(left_tree, right_tree)

        return left_tree

    def equality(self):
        '''
        Equality -> Relation [ EquOp Relation ]
        :return: a BinaryEqualityExpr object
        '''
        left_tree = self.relation()

        while self.curr_tok[0] == values.EQUALTO or self.curr_tok[0]==values.NEQUALTO:
            # we "matched" an equop (== or !=) so "consume"
            # it and get the next one
            tmp_val = self.curr_tok[0]
            self.curr_tok = self.lex_gen.__next__()
            right_tree = self.relation()
            left_tree = ast.BinaryEqualityExpr(left_tree, right_tree, tmp_val)

        return left_tree

    def relation(self):
        '''
        Relation -> Addition [ RelOp Addition ]
        :return: a Binary RelationExpr object
        '''
        left_tree = self.addition()

        while self.curr_tok[0] == values.LESSEQ or self.curr_tok[0]== values.GREATEREQ or \
                self.curr_tok[0] == values.LESS or self.curr_tok[0]== values.GREATER:
            # we "matched" an relop (< or > or <= or >=) so "consume"
            # it and get the next one
            tmp_val = self.curr_tok[0]
            self.curr_tok = self.lex_gen.__next__()
            right_tree = self.addition()
            left_tree = ast.BinaryRelationExpr(left_tree, right_tree, tmp_val)

        return left_tree

    def addition(self):
        '''
        Addition -> Term { AddOp Term }

        :return: None on a valid parse
        :raise CliteSyntaxError
        '''

        left_tree = self.term()

        while self.curr_tok[0] == values.PLUS or self.curr_tok[0]==values.MINUS:
            # we "matched" an addop (+ or -) so "consume"
            # it and get the next one
            tmp_val = self.curr_tok[0]
            self.curr_tok = self.lex_gen.__next__()
            right_tree = self.term()
            left_tree = ast.BinaryPlusExpr(left_tree, right_tree, tmp_val)

        return left_tree

    def term(self):
        '''
        Term -> Factor { MulOp Factor }
        :return: a BinaryTimesExpr object
        '''
        left_tree = self.factor()

        while self.curr_tok[0] == values.TIMES or self.curr_tok[0] == values.DIVIDE or \
                                                  self.curr_tok[0] == values.MOD:
            tmp_val = self.curr_tok[0]
            self.curr_tok = self.lex_gen.__next__()
            right_tree = self.factor()
            left_tree = ast.BinaryTimesExpr(left_tree, right_tree, tmp_val)

        return left_tree

    def factor(self):
        '''
        Factor -> [ UnaryOp ] Primary
        :return: primary
        '''

        if self.curr_tok[0] == values.MINUS or self.curr_tok[0] == values.BANG:
            #tmp_val = self.curr_tok[0]
            # you need to build a UnaryExpr object
            self.curr_tok = self.lex_gen.__next__()

        tree = self.primary()

        return tree

    def primary(self):
        '''
        Primary -> Identifier | IntLit | FloatLit | ( Expression ) | true | false

            should be Expression when implementing full expressions
        :return: Expr
        '''

        if self.curr_tok[0] == values.ID:
            tmp_id = self.curr_tok[1]

            # check to see if the identifier was declared

            if tmp_id not in self.decls:
                raise CliteSyntaxError("Identifier not declared")

            self.curr_tok = self.lex_gen.__next__()
            return ast.IdentExpr(tmp_id)

        elif self.curr_tok[0] == values.INTLIT:
            tmp_int = self.curr_tok[1]
            self.curr_tok = self.lex_gen.__next__()
            return ast.IntLitExpr(tmp_int)

        elif self.curr_tok[0] == values.FLOATLIT:
            tmp_float = self.curr_tok[1]
            self.curr_tok = self.lex_gen.__next__()
            return ast.FloatLitExpr(tmp_float)

        elif self.curr_tok[0] == values.PARENL:
            self.curr_tok = self.lex_gen.__next__()
            tree = self.expression()


            if self.curr_tok[0] == values.PARENR:
                self.curr_tok = self.lex_gen.__next__()
                return tree
            else:
                raise CliteSyntaxError("Missing right parenthesis")

        elif self.curr_tok[0] == values.TRUE or self.curr_tok[0] == values.FALSE:
            tmp_bool = self.curr_tok[1]
            self.curr_tok = self.lex_gen.__next__()
            return ast.BoolExpr(tmp_bool)

        else:
            raise CliteSyntaxError("Unexpected symbol {0}".format(self.curr_tok[1]))



class CliteSyntaxError(Exception):
    def __init__(self, msg):
        Exception.__init__(self)  # same as super.__init__()
        self.msg = msg
    def __str__(self):
        return self.msg