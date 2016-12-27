# Name: Qixiang Chen
# ID#108605598
# HW#4


import string
import ply.lex as lex
import ply.yacc as yacc
import sys
import fileinput
import os

tokens = (

    'NAME','INT','REAL','STR',

    'PLUS','MINUS','FLDIVIDE','EXP','MOD','TIMES','DIVIDE','EQUALS',

    'LPAREN','RPAREN', 'LLSPAREN','RLSPAREN',
    
    'LESS','LESSTHAN','EEQUALS','NOTEQUALS','GREAT','GREATTHAN',

    'NOT','AND','OR', "IN",'COMMA',

    'EXIT', #FOR CONTRAL ONLY

    )

 

# Tokens

t_PLUS    = r'\+'

t_MINUS   = r'\-'

t_FLDIVIDE = r'\/\/'

t_EXP     = r'\*\*'

t_MOD     = r'\%'

t_TIMES   = r'\*'

t_DIVIDE  = r'/'

t_EQUALS  = r'='

t_LPAREN  = r'\('

t_RPAREN  = r'\)'

t_LLSPAREN  = r'\['

t_RLSPAREN  = r'\]'

t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'

t_LESS    = r'\<'

t_LESSTHAN = r'\<='

t_EEQUALS = r'\=='

t_NOTEQUALS = r'\<>'

t_GREAT   = r'\>'

t_GREATTHAN = r'\>='

t_COMMA = r'\,'

def t_IN(t):
    r'in'
    t.value = str(t.value)
    return t

def t_EXIT(t):
    r'exit'
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


def t_STR(t):
    # r'(\"([^\\"]|(\\.))*\")|(\'([^\\"]|(\\.))*\')'
    # es = 0
    # str = t.value[1:-1]
    # newstr = ""
    # for i in range(0, len(str)):
    #     c = str[i]
    #     if es:
    #         if c == "n":
    #             c = "\n"
    #         elif c == "t":
    #             c = "\t"
    #         newstr += c
    #         es = 0
    #     else:
    #         if c == "\\":
    #             es = 1
    #         else:
    #             newstr += c
    # t.value = newstr
    r'(\"([^\\\n]|(\\.))*?\") | (\'([^\\\n]|(\\.))*?\')'
    t.value = t.value[1:-1]
    return t

def t_REAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    
    return t
    

    
# Ignored characters

t_ignore = " \t"

 

def t_newline(t):

    r'\n+'

    t.lexer.lineno += t.value.count("\n")

   

def t_error(t):

    print("Illegal character '%s'" % t.value[0])

    #t.lexer.skip(1)

   

# Build the lexer


lexer = lex.lex()

 

# Parsing rules

precedence = (
    ('left','COMMA'),

    ('left','EQUALS'),

    ('left','OR'),

    ('left','AND'),

    ('left','NOT'),
    
    ('left','LESS','GREAT','EEQUALS','NOTEQUALS','GREATTHAN','LESSTHAN'),

    ('left','IN'),

    ('left','PLUS','MINUS'),

    ('left','FLDIVIDE'),
    
    ('left','EXP'),

    ('left','MOD'),

    ('left','TIMES','DIVIDE'),

    ('left','LPAREN','RPAREN', 'LLSPAREN','RLSPAREN'),

    ('right','UMINUS'),

    ('left','EXIT'),

)

 

# dictionary of names

names = { }

 
def p_statement_assign(t):

    'statement : NAME EQUALS expression'

    names[t[1]] = t[3]

def p_statement_expr(t):

    'statement : expression'

    if not (t[1] == None):
        print(t[1])

def p_expression_binop(t):

    '''expression : expression PLUS expression

                  | expression MINUS expression

                  | expression FLDIVIDE expression

                  | expression EXP expression

                  | expression MOD expression

                  | expression TIMES expression

                  | expression DIVIDE expression'''

    try:
        if t[2] == '+'  :              
                if type(t[1]) == type('string') and type(t[3]) == type('string'):
                    t[1] = str(t[1][1:len(t[1])-1])
                    t[3] = str(t[3][1:len(t[3])-1])
                    t[0] = '\'' + t[1] + t[3] + '\''
                elif type(t[2]) == type([]):
                    t[0]=t[1]
                else:
                    t[0] = t[1]+t[3]

        elif t[2] == '-': t[0] = t[1] - t[3]

        elif t[2] == '//': t[0] = t[1] // t[3]

        elif t[2] == '**': t[0] = t[1] ** t[3]

        elif t[2] == '%': t[0] = t[1] % t[3]

        elif t[2] == '*': t[0] = t[1] * t[3]

        elif t[2] == '/': t[0] = t[1] / t[3]
    except TypeError:
        print("SEMANTIC ERROR")

    except ZeroDivisionError:
        print("ZeroDivision ERROR")

def p_expression_compare(t):
    '''expression : expression LESS expression

                  | expression LESSTHAN expression

                  | expression EEQUALS expression

                  | expression NOTEQUALS expression

                  | expression GREAT expression

                  | expression GREATTHAN expression
 
    '''
    try:
        if t[2] == '<':
            if t[1] < t[3]:
                t[0] = 1
            else:
                t[0] = 0
        elif t[2] == '<=':
            if t[1] <= t[3]:
                t[0] = 1
            else:
                t[0] = 0
        elif t[2] == '==':
            if t[1] == t[3]:
                t[0] = 1
            else:
                t[0] = 0
        elif t[2] == '<>':
            if t[1]<t[3] or t[1]>t[3]:
                t[0] = 1
            else:
                t[0] = 0
        elif t[2] == '>':
            if t[1] > t[3]:
                t[0] = 1
            else:
                t[0] = 0
        elif t[2] == '>=':
            if t[1] >= t[3]:
                t[0] = 1
            else:
                t[0] = 0
    except TypeError:
        print("SEMANTIC ERROR")
            
def p_expression_boolean(t):
    '''expression : NOT expression

                  | expression AND expression

                  | expression OR expression

                  | expression IN expression

                  | EXIT

    '''
    try:
        if t[1] == 'not':
            if (not t[2]):
                t[0] = 0
            else:
                t[0] = 1
        elif t[1] == 'exit':
            exit()
            
        elif t[2] == 'and':
            if(t[1] and t[3]):           
                t[0] = 1
            else:
                t[0] = 0
        elif t[2] == 'or':
            if(t[1] or t[3]):           
                t[0] = 1
            else:
                t[0] = 0
        elif t[2] == 'in':
            
                if type(t[1]) == type('string') and type(t[3]) == type('string'):
                    t[1] = t[1][1:len(t[1])-1]
                    t[3] = t[3][1:len(t[3])-1]
                   
                t[0] = t[1] in t[3]
                if t[0]:
                    t[0] = 1
                else:
                    t[0] = 0
    except TypeError:
        print("SEMANTIC ERROR")

def p_expression_uminus(t):

    'expression : MINUS expression %prec UMINUS'

    t[0] = -t[2]

def p_expression_group(t):

    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

def p_expression_index(t):

    'expression : expression LLSPAREN index RLSPAREN'
    try:
        if type(t[1]) == type('string'):
            t[1] = t[1][1:len(t[1])-1]
            t[0] = t[1][t[3]]
            t[0] = '\'' + t[0] + '\''      
        else:    
            t[0] = t[1][t[3]]
    except TypeError:
        print("SEMANTIC ERROR")
    except IndexError:
        print("IndexError")
        
def p_expression_index_element(t):

    'index : INT'
    t[0] = t[1]



def p_list_start(t):
    'expression : LLSPAREN expression list_tail'
    if(t[3] == []):
        t[0] = [t[2]]
    else:
        t[0] = [t[2]]+t[3]

def p_list_start1(t):
    'list_tail : COMMA expression list_tail'
    t[0] = [t[2]]+t[3]

def p_list_start2(t):
    'list_tail : RLSPAREN'
    t[0] = []

        
def p_expression_int_real_str(t):

    '''expression : STR
                  | REAL
                  | INT                

    '''

    if type(t[1]) == type('string'):
        t[0] = '\'' + t[1]+ '\''
    else:
        t[0] = t[1]


def p_expression_name(t):

    'expression : NAME'

    try:

        t[0] = names[t[1]]

    except LookupError:

        print("Undefined name '%s'" % t[1])

        t[0] = 0


def p_error(t):

    print("SYNTAX ERROR")
    t.lexer.skip(2)


def p_empty(t):
    'empty : '
    pass

parser = yacc.yacc()

 
# def main():
#     argv = sys.argv
#     inputFile = argv[1]
#     try:
#         file = open(inputFile,"r")
#     except IOError:
#         raise RuntimeError("File does not exit")
#         exit()
#
#     for line in file:
#         try:
#             s = line
#         except:
#             print("EOFError")
#         if(s == '\n'):
#             pass
#         else:
#             yacc.parse(s)
# main()

while True:
    try:
        s = input('TrueSeawolf4>> ')
    except EOFError:
        break
    parser.parse(s)