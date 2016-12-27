# Name: Qixiang Chen
# ID#108605598
# HW#5

import ply.lex as lex
import ply.yacc as yacc
import sys

global names
names = {}

class Node:
    def __init__(self):
        print("Node")

    def evaluate(self):
        print("Evaluate")
        return 0

    def execute(self):
        print("Execute")

class VarNode(Node):
    def __init__(self, v):
        self.value = v
        # print("VarNode")

    def evaluate(self):
        # print("Evaluate VarNode")
        if self.value in names:
            return names[self.value]
        else:
            print("Semantic Error:Undefined name '%s'" % self.value)

    def execute(self):
        # print("Execute VarNode")
        self.evaluate()

class AssignNode(Node):
    def __init__(self,n,v):
        self.name = n
        self.value = v
        # print("AssignNode")

    def evaluate(self):
        # print("Evaluate AssignNode")
        # print("Assign value: " +str(self.value.evaluate()))
        names[self.name] = self.value.evaluate()
        return 0

    def execute(self):
        # print("Execute AssignNode")
        self.evaluate()

class ArrayAssignNode(Node):
    def __init__(self,a,i, v):
        self.name = a
        self.index = i
        self.value = v
        # print("ArrayAssignNode")

    def evaluate(self):
        # print("Evaluate ArrayAssignNode")
        # print("ArrayAssign value: " +str(self.index.evaluate()))
        # print("ArrayAssign name: " + str(self.name.evaluate()))
        self.name.evaluate()[self.index.evaluate()] = self.value.evaluate()
        return 0


    def execute(self):
        # print("Execute ArrayAssignNode")
        self.evaluate()

class UminusNode(Node):
    def __init__(self, v):
        self.value = v.evaluate()
    def evaluate(self):
        # print("Evaluate UminusNNode")
        try:
            return - self.value
        except:
            print("TypeError")

    def execute(self):
        # print("Execute UminusNode")
        return self.evaluate()

class RealNumberNode(Node):
    def __init__(self, v):
        self.value = float(v)
        # print("RealNumberNode")

    def evaluate(self):
        # print("Evaluate RealNumberNode")
        return self.value

    def execute(self):
        # print("Execute RealNumberNode")
        return self.value

class IntNumberNode(Node):
    def __init__(self, v):
        self.value = int(v)
        # print("IntNumberNode")

    def evaluate(self):
        # print("Evaluate IntNumberNode")
        return self.value

    def execute(self):
        # print("Execute IntNumberNode")
        return self.value

class StringNode(Node):
    def __init__(self, v):
        self.value = str(v)
        self.value = self.value[1:-1]  # to eliminate the left and right double quotes
        # print("StringNode")

    def evaluate(self):
        # print("Evaluate StringNode")
        return self.value

    def execute(self):
        # print("Execute StringNode")
        print("'"+self.value+"'")

class ListNode(Node):
    def __init__(self,v):
        self.value = v
        # print("ListNode")

    def evaluate(self):
        # print("Evaluate ListNode")
        return self.value

    def execute(self):
        # print("Execute ListNode")
        print(self.value)

class IndexNode(Node):
    def __init__(self,l,i):
        self.list = l
        self.indexlist = i
        # print("IndexNode")

    def evaluate(self):
        # print("Evaluate IndexNode")
        try:
            value = self.list.evaluate()
            value = value[self.indexlist.evaluate()]
            return value
        except TypeError:
            print("SEMANTIC ERROR")
        except IndexError:
            print("IndexError")
    def execute(self):
        # print("Execute IndexNode")
        self.evaluate()


class PrintNode(Node):
    def __init__(self, v):
        self.value = v
        # print("PrintNode")

    def evaluate(self):
        # print("Evaluate PrintNode")
        return 0

    def execute(self):
        # print("Execute NumberNode")
        if(self.value.evaluate() != None):
            print(self.value.evaluate())

class IfNode(Node):
    def __init__(self, c, t, e):

        self.condition = c

        self.thenBlock = t

        self.elseBlock = e

        # print("IfNode")

    def evaluate(self):

        # print("Evaluate IfNode")

        return 0

    def execute(self):

        # print("Execute IfNode")
        # print(self.condition.evaluate())

        if (self.condition.evaluate()):

            self.thenBlock.execute()

        else:
            if(self.elseBlock == None):
                pass
            else:
                self.elseBlock.execute()

class WhileNode(Node):
    def __init__(self, c, b):
        self.condition = c
        self.bodyBlock = b
        # print("WhileNode")

    def evaluate(self):
        # print("Evaluate WhileNode")
        return 0

    def execute(self):
        # print("Execute WhileNode")
        if(self.condition.evaluate() >= 1):
            self.bodyBlock.execute()
            self.execute()



class BolNode(Node):
    def __init__(self,l,op,r):
        self.f1 = l
        self.f2 = r
        self.o = op
        self.r = 0
        # print("BolNode")

    def evaluate(self):
        # print("Evaluate BolNode")
        try:

            if self.o == '<':
                if self.f1.evaluate() < self.f2.evaluate():
                    self.r = 1
                else:
                    self.r = 0
            elif self.o == '<=':
                if self.f1.evaluate() <= self.f2.evaluate():
                    self.r = 1
                else:
                    self.r = 0
            elif self.o == '==':
                if self.f1.evaluate() < self.f2.evaluate():
                    self.r = 1
                else:
                    self.r = 0
            elif self.o == '<>':
                if self.f1.evaluate() != self.f2.evaluate():
                    self.r = 1
                else:
                    self.r = 0
            elif self.o == '>':
                if self.f1.evaluate() > self.f2.evaluate():
                    self.r = 1
                else:
                    self.r = 0
            elif self.o == '>=':
                if self.f1.evaluate() >= self.f2.evaluate():
                    self.r = 1
                else:
                    self.r = 0
            elif self.o == 'in':
                if self.f1.evaluate() in self.f2.evaluate():
                    self.r = 1
                else:
                    self.r = 0
            elif self.o == 'and':
                if self.f1.evaluate() and self.f2.evaluate():
                    self.r = 1
                else:
                    self.r = 0
            elif self.o == 'or':
                if self.f1.evaluate() or self.f2.evaluate():
                    self.r = 1
                else:
                    self.r = 0
            elif self.o == 'not':
                if self.f1.evaluate():
                    self.r = 0
                else:
                    self.r = 1
            return self.r
        except TypeError:
            print("SEMANTIC ERROR")

    def execute(self):
        # print("Execute BoltNode")
        return self.evaluate()

class OperationNode(Node):
    def __init__(self,l,op,r):
        self.f1 = l
        self.f2 = r
        self.o = op
        self.r = None
        # print("OperationNode")

    def evaluate(self):
        # print("Evaluate OperationNode")
        try:

            if self.o == '+' :
                self.r = self.f1.evaluate() + self.f2.evaluate()

            elif self.o == '-':
                self.r = self.f1.evaluate() - self.f2.evaluate()

            elif self.o == '//':
                self.r = self.f1.evaluate() // self.f2.evaluate()

            elif self.o == '**':
                self.r = self.f1.evaluate() ** self.f2.evaluate()

            elif self.o == '%':
                self.r = self.f1.evaluate() % self.f2.evaluate()

            elif self.o == '*':
                self.r = self.f1.evaluate() * self.f2.evaluate()

            elif self.o == '/':
                self.r = self.f1.evaluate() / self.f2.evaluate()
            return self.r
        except TypeError:
            print("SEMANTIC ERROR")
        except ZeroDivisionError:
            print("ZeroDivision ERROR")

    def execute(self):
        # print("Execute OperationNode")
        if(type(self.evaluate()) == type(" ")):
            print("'" + self.r +"'")
        else:
            print(self.evaluate())

class BlockNode(Node):
    def __init__(self, sl):
        self.statementNodes = sl
        # print("BlockNode")
        # print(sl)

    def evaluate(self):
        # print("Evaluate BlockNode")
        return 0

    def execute(self):
        # print(self.statementNodes)
        # print("Execute BlockNode")
        for statement in self.statementNodes:
                statement.execute()


tokens = (
            'NAME', 'INT', 'REAL', 'STR',
            'PLUS', 'MINUS', 'FLDIVIDE', 'EXP', 'MOD', 'TIMES', 'DIVIDE', 'EQUALS',
            'LBRACE', 'RBRACE', 'LLSPAREN', 'RLSPAREN','LCBRACE', 'RCBRACE',
            'LESS', 'LESSTHAN', 'EEQUALS', 'NOTEQUALS', 'GREAT', 'GREATTHAN',
            'NOT', 'AND', 'OR', "IN", 'COMMA',
            'PRINT', 'SEMI', 'IF','ELSE', 'WHILE',
        )


# Tokens

t_SEMI = '\;'

t_PLUS = r'\+'

t_MINUS = r'\-'

t_FLDIVIDE = r'\/\/'

t_EXP = r'\*\*'

t_MOD = r'\%'

t_TIMES = r'\*'

t_DIVIDE = r'/'

t_EQUALS = r'='

t_LBRACE = r'\('

t_RBRACE = r'\)'

t_LLSPAREN = r'\['

t_RLSPAREN  = r'\]'

t_LCBRACE = r'\{'

t_RCBRACE = r'\}'

t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

t_LESS = r'\<'

t_LESSTHAN = r'\<='

t_EEQUALS = r'\=='

t_NOTEQUALS = r'\<>'

t_GREAT = r'\>'

t_GREATTHAN = r'\>='

t_COMMA = r'\,'


def t_REAL(t):
    r'\d+\.\d+'
    t.value = RealNumberNode(t.value)
    return t

def t_INT(t):
    r'\d+'
    t.value = IntNumberNode(t.value)
    return t

def t_STR(t):
    r'(\"([^\\\n]|(\\.))*?\") | (\'([^\\\n]|(\\.))*?\')'
    t.value = StringNode(t.value)
    return t

def t_IN(t):
    r'in'
    t.value = str(t.value)
    return t

def t_NOT(t):
    r'not'
    t.value = str(t.value)
    return t

def t_AND(t):
    r'and'
    t.value = str(t.value)
    return t

def t_OR(t):
    r'or'
    t.value = str(t.value)
    return t

def t_PRINT(t):
    r'print'
    t.value = str(t.value)
    return t

def t_IF(t):
    r'if'
    t.value = str(t.value)
    return t

def t_ELSE(t):
    r'else'
    t.value = str(t.value)
    return t

def t_WHILE(t):
    r'while'
    t.value = str(t.value)
    return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

# Parsing rules

precedence = (

    ('left', 'PRINT','IF','ELSE'),

    ('left', 'COMMA'),

    ('right', 'EQUALS'),

    ('left', 'OR'),

    ('left', 'AND'),

    ('left', 'NOT'),

    ('left', 'LESS', 'GREAT', 'EEQUALS', 'NOTEQUALS', 'GREATTHAN', 'LESSTHAN'),

    ('left', 'IN'),

    ('left', 'PLUS', 'MINUS'),

    ('left', 'FLDIVIDE'),

    ('right', 'EXP'),

    ('left', 'MOD'),

    ('left', 'TIMES', 'DIVIDE'),

    ('left', 'LBRACE', 'RBRACE', 'LLSPAREN', 'RLSPAREN'),

    ('right', 'UMINUS'),

)


def p_statement_block(t):
    ''' statement : LCBRACE block RCBRACE '''

    t[0] = BlockNode(t[2])

def p_block_expression(t):
    '''block : blockstate SEMI block'''
    t[0] = [t[1]] + t[3]

def p_block_if_exipresssion(t):
    '''block : blockstateCon block'''
    t[0] = [t[1]] + t[2]

def p_if_expression(t):
    '''blockstateCon : IF LBRACE expression RBRACE LCBRACE block RCBRACE'''
    t[0] = IfNode(t[3], BlockNode(t[6]),None)

def p_if_else_expression(t):
    '''blockstateCon : IF LBRACE expression RBRACE LCBRACE block RCBRACE ELSE LCBRACE block RCBRACE'''
    t[0] = IfNode(t[3],BlockNode(t[6]),BlockNode(t[10]))

def p_while_expression(t):
    '''blockstateCon : WHILE LBRACE expression RBRACE LCBRACE block RCBRACE'''
    t[0] = WhileNode(t[3], BlockNode(t[6]))

def p_block_empty(t):
    'block : '
    t[0] = []

def p_blockstate_print(t):
    ''' blockstate : PRINT LBRACE expression RBRACE '''
    t[0] = PrintNode(t[3])  # create nodes in the tree instead of executing the current expression

def p_statement_expression(t):

    'blockstate : expression'
    t[0] = t[1]

def p_expression_array_assign(t):
    'expression : expression LLSPAREN expression RLSPAREN EQUALS expression'
    t[0] = ArrayAssignNode(t[1],t[3],t[6])

def p_expression_assign(t):

    'expression : NAME EQUALS expression'
    t[0] = AssignNode(t[1],t[3])


def p_expression_name(t):

    'expression : NAME'
    t[0] = VarNode(t[1])

def p_expression_group(t):
    'expression : LBRACE expression RBRACE'
    t[0] = t[2]

def p_expression_binop(t):

    '''expression : expression PLUS expression

                  | expression MINUS expression

                  | expression FLDIVIDE expression

                  | expression EXP expression

                  | expression MOD expression

                  | expression TIMES expression

                  | expression DIVIDE expression'''

    t[0] = OperationNode(t[1],t[2],t[3])

def p_expression_uminus(t):

    'expression : MINUS expression %prec UMINUS'
    t[0] = UminusNode(t[2])


def p_expression_compare(t):
    '''expression : expression LESS expression

                  | expression LESSTHAN expression

                  | expression EEQUALS expression

                  | expression NOTEQUALS expression

                  | expression GREAT expression

                  | expression GREATTHAN expression

    '''
    t[0] = BolNode(t[1],t[2],t[3])


def p_expression_boolean(t):
    '''expression : NOT expression

                  | expression AND expression

                  | expression OR expression

                  | expression IN expression

    '''
    if(t[1]=='not'):
        t[0] = BolNode(t[2],t[1],None)
    else:
        t[0] = BolNode(t[1],t[2],t[3])

def p_expression_index(t):
    '''expression : expression LLSPAREN expression RLSPAREN'''
    t[0] = IndexNode(t[1],t[3])



def p_expression_list(t):
    'expression : LLSPAREN expression list_tail'
    if(t[3] == []):
        t[0] = [t[2].evaluate()]
    else:
        t[0] = [t[2].evaluate()]+t[3]
    t[0] = ListNode(t[0])

def p_list_tail(t):
    'list_tail : COMMA expression list_tail'
    t[0] = [t[2].evaluate()]+t[3]

def p_list_start2(t):
    'list_tail : RLSPAREN'
    t[0] = []

def p_expresion_basic(t):
    '''expression : REAL
                  | INT
                  | STR '''
    t[0] = t[1]

def p_error(t):
    print("SYNTAX ERROR7")
    t.lexer.skip(-1)

# def p_empty(t):
#     'empty : '



# execute the abstract syntax tree for the whole program that you read from the file
parser = yacc.yacc()

# while 1:
#     try:
#         allFileCode = input('TrueSeawolf>> ')
#     except EOFError:
#         break
#     #yacc.parse(allFileCode)
#     ast = yacc.parse(allFileCode)
#     try:
#         ast.execute()
#     except:
#         pass

def main():
    argv = sys.argv
    inputFile = argv[1]
    try:
        file = open(inputFile,"r")
    except IOError:
        raise RuntimeError("File does not exit")
        exit()
    AllFileCode = ""
    for line in file:
        try:
            s = line
        except:
            print("EOFError")
        if(s == '\n'):
            pass
        else:
            AllFileCode = AllFileCode + s
    # print(AllFileCode)
    ast = yacc.parse(AllFileCode)
    try:
        ast.execute()
    except:
        pass


main()

