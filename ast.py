import sys
import values

class Program(object):

    env = { }

    # decls is a dictionary of the form { 'id', 'typename' }
    def __init__(self, decls, stmts, declList):
        self.decls = decls
        self.stmts = stmts
        self.declList = declList

        # add each declaration to the environment
        for d in self.decls:
            Program.env[d] = None

    # evaluation all statements
    def eval(self):
        for stmt in self.stmts:
          stmt.eval()



    # combining all object strings
    def __str__(self):
        str = "int main () { \n"
        for d in self.declList:
                str = str + '\t' + self.decls[d] + " " + d + ';' + '\n'

        for s in self.stmts:
            str = str + s.__str__()
            str = str + "\n"

        return str + "}"


########## Statements #############

class Stmt(object):
    indent_level = 1
    def __init__(self):
        Stmt.indent_level = 1


class Assign(Stmt):
    # id and expression of assignment
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr
        self.indent_level = Stmt.indent_level

    # assignment into str
    def __str__(self):
        indent = "\t" * self.indent_level

        return indent + "{0} = {1};".format(self.id, self.expr)

    # adding expressions to the environment
    def eval(self):
        Program.env[self.id] = self.expr.eval()

class IfState(Stmt):
    #expression and statement of if statement
    def __init__(self, expr, stmt):
        self.expr = expr
        self.stmt = stmt
        self.indent_level = Stmt.indent_level


    # putting IfState into str
    def __str__(self):

        indent = "\t" * self.indent_level
        self.indent_level += 1
        statementindent = "\t" * self.indent_level

        return indent + "if {0}\n".format(self.expr) + statementindent + "{0}\n".format(self.stmt)

    #evaluates statement according to bool value of expression
    def eval(self):
        if self.expr.eval() == True:
            return self.stmt.eval()


class WhileState(Stmt):
    #expression and statement of whilestatement
    def __init__(self, expr, stmt):
        self.expr = expr
        self.stmt = stmt
        self.indent_level = Stmt.indent_level
    #putting whilestatement into str
    def __str__(self):
        indent = "\t" * self.indent_level
        self.indent_level += 1

        return indent + "while {0}\n".format(self.expr) +"{0}".format(self.stmt)

    #evaluates statement according to bool value of expression
    def eval(self):
        while self.expr.eval() == True:
            self.stmt.eval()


class PrintState(Stmt):
    #expression of printstatement
    def __init__(self, expr):
        self.expr = expr
        self.indent_level = Stmt.indent_level
    #putting printstatement into str
    def __str__(self):
        indent = "\t" * self.indent_level

        return indent + "print {0};".format(self.expr)
    #prints statement in printstatement
    def eval(self):
        print(self.expr.eval())

class Semi(Stmt):
    '''
    semi col object
    '''
    def __init__(self):
        pass
    # returns string of object
    def __str__(self):
        return ''

    def eval(self):
        return

class Block(Stmt):
    '''
    block object
    '''
    def __init__(self, stmts):
        self.stmts = stmts
        self.indent_level = Stmt.indent_level
    # returns string of object
    def __str__(self):
        indent = "\t" * self.indent_level

        block = indent + "{\n"
        for stmt in self.stmts:
            block = block + indent + str(stmt)
        block = block + '\n' + indent +"}"
        return block
    #evaluates all statements within block
    def eval(self):
        for stmt in self.stmts:
            stmt.eval()


######### Expressions ############

class Expr(object):
    def __init__(self):
        pass

class IdentExpr(Expr):
    '''
    Identifier Expression object
    '''
    def __init__(self, ident):
        self.ident = ident
    # returns string of object
    def __str__(self):
        return self.ident

    def eval(self):
        if Program.env[self.ident] == None:
            raise CliteRuntimeError(self.ident + " not defined")

        return Program.env[self.ident]

    def typeof(self):
        '''
        Lookup the type of the identifier in the
        declarations
        :return:
        '''
        return Program.decls[self.ident]

class IntLitExpr(Expr):
    '''
    Integer literal expression object
    '''
    def __init__(self, intlit):
        self.intlit = intlit
    # returns string of object
    def __str__(self):
        return str(self.intlit)

    def eval(self):
        return int(self.intlit)

    def typeof(self):
        '''
        Returns the type of the CLite value as a string
        :return:
        '''
        return "int"

class FloatLitExpr(Expr):
    '''
    Float Literal expression object
    '''

    def __init__(self, floatlit):
        self.floatlit = floatlit
    # returns string of object
    def __str__(self):
        return str(self.floatlit)

    def eval(self):
        return float(self.floatlit)

    def typeof(self):
        '''
        Returns the type of the CLite value as a string
        :return:
        '''
        return "float"

class BoolExpr(Expr):
    '''
    Bool Expression object
    '''
    def __init__(self, boollit):
        self.boollit = boollit
        self.value = "true"
    # returns string of object
    def __str__(self):
        return str(self.boollit)

    def eval(self):
        return self.value == self.boollit

    def typeof(self):
        '''
        Returns the type of the CLite value as a string
        :return:
        '''
        return "bool"

class BinaryExpr(Expr):
    '''
    Binary expression object
    '''

    def __init__(self, left, right):
        self.left = left
        self.right = right

class BinaryPlusExpr(BinaryExpr):
    '''
    Binary Plus Expression object
    '''

    def __init__(self, left, right, value):
        BinaryExpr.__init__(self, left, right)
        self.value = value
    # returns string of object
    def __str__(self):
        if self.value == values.PLUS:
            return "({0} + {1})".format(self.left.__str__(), self.right.__str__())
        else:
            return "({0} - {1})".format(self.left.__str__(), self.right.__str__())


    #returns evaluated expression
    def eval(self):
        left_val = self.left.eval()

        right_val = self.right.eval()

        #type checking for int and float
        if type(left_val) != type(1.0) and type(left_val) != type(1) or \
                type(right_val) != type(1.0) and type(right_val) != type(1):
            raise CliteTypeError("Incompatible types")

        if self.value == values.PLUS:
            return self.left.eval() + self.right.eval()
        else:
            return self.left.eval() - self.right.eval()

class BinaryDampExpr(BinaryExpr):
    '''
    Binary Double Ampersand object
    '''

    def __init__(self, left, right):
        BinaryExpr.__init__(self, left, right)
    # returns string of object
    def __str__(self):
        return \
          "({0} && {1})".format(self.left.__str__(), \
                               self.right.__str__())

    #returns value of expression
    def eval(self):
        left_val = self.left.eval()

        right_val = self.right.eval()

        #type check for bool type
        if type(left_val) != type(True) or type(right_val) != type(True) :
            raise CliteTypeError("Incompatible types")

        return self.left.eval() and self.right.eval()

class BinaryDBarExpr(BinaryExpr):
    '''
    Binary Double Bar object
    '''
    def __init__(self, left, right):
        BinaryExpr.__init__(self, left, right)
    # returns string of object
    def __str__(self):
        return \
          "({0} || {1})".format(self.left.__str__(), \
                               self.right.__str__())
    #returns value of expression
    def eval(self):
        left_val = self.left.eval()

        right_val = self.right.eval()

        #type check for bool type
        if type(left_val) != type(True) or type(right_val) != type(True) :
            raise CliteTypeError("Incompatible types with operator")

        return self.left.eval() or self.right.eval()

class BinaryEqualityExpr(BinaryExpr):
    '''
    Binaray Equality Expression object
    '''

    def __init__(self, left, right, value):
        BinaryExpr.__init__(self, left, right)
        self.value = value
    # returns string of object
    def __str__(self):
        if self.value == values.EQUALTO:
            return "({0} == {1})".format(self.left.__str__(),self.right.__str__())
        else:
            return "({0} != {1})".format(self.left.__str__(),self.right.__str__())
    #returns bool value of the expression
    def eval(self):
        if self.value == values.EQUALTO:
            return self.left.eval() == self.right.eval()
        else:
            return self.left.eval() != self.right.eval()

class BinaryRelationExpr(BinaryExpr):
    '''
    Binary Relation Expression object
    '''

    def __init__(self, left, right, value):
        BinaryExpr.__init__(self, left, right)
        self.value = value

    # returns string of object
    def __str__(self):
        if self.value == values.LESS:
            return "({0} < {1})".format(self.left.__str__(),self.right.__str__())
        elif self.value == values.LESSEQ:
            return "({0} <= {1})".format(self.left.__str__(),self.right.__str__())
        elif self.value == values.GREATER:
            return "({0} > {1})".format(self.left.__str__(),self.right.__str__())
        else:
            return "({0} >= {1})".format(self.left.__str__(),self.right.__str__())

    #returns evaluated expression
    def eval(self):
        left_val = self.left.eval()

        right_val = self.right.eval()

        #type checking for int and float
        if type(left_val) != type(1.0) and type(left_val) != type(1) or \
                type(right_val) != type(1.0) and type(right_val) != type(1):
            raise CliteTypeError("Incompatible types")

        if self.value == values.LESS:
            return self.left.eval() < self.right.eval()
        elif self.value == values.LESSEQ:
            return self.left.eval() <= self.right.eval()
        elif self.value == values.GREATER:
            return self.left.eval() > self.right.eval()
        else:
            return self.left.eval() >= self.right.eval()

class BinaryTimesExpr(BinaryExpr):
    '''
    Binary Times Expression object
    '''

    def __init__(self, left, right, value):
        BinaryExpr.__init__(self, left, right)
        self.value = value
    # returns string of object
    def __str__(self):
        if self.value == values.TIMES:
            return "{0} * {1}".format(self.left.__str__(), self.right.__str__())
        elif self.value == values.DIVIDE:
            return "{0} / {1}".format(self.left.__str__(), self.right.__str__())
        else:
            return "{0} % {1}".format(self.left.__str__(), self.right.__str__())

    #returns evaluated expression
    def eval(self):
        left_val = self.left.eval()

        right_val = self.right.eval()

        #type checking for int and float
        if type(left_val) != type(1.0) and type(left_val) != type(1) or \
                type(right_val) != type(1.0) and type(right_val) != type(1):
            raise CliteTypeError("Incompatible types")

        if self.value == values.TIMES:
            return self.left.eval() * self.right.eval()
        elif self.value == values.DIVIDE:
            return self.left.eval() / self.right.eval()
        else:
            return self.left.eval() % self.right.eval()

class CliteRuntimeError(Exception):
    def __init__(self, msg):
        Exception.__init__(self)  # same as super.__init__()
        self.msg = msg
    def __str__(self):
        return self.msg

class CliteTypeError(CliteRuntimeError):
    def __init__(self, msg):
        CliteRuntimeError.__init__(self, msg)  # same as super.__init__()
    def __str__(self):
        return super.msg