import ply.yacc as yacc
from lexer import *
import ply.lex as lex

lex.lex()

# dictionary of names (for storing variables)
names = { }

def p_statement_assign(p):
    'statement : ID EQUAL expression'
    names[p[1]] = p[3]

def p_statement_expr(p):
    'statement : expression'
    print(p[1])

def p_expression_binop(p):
    print "here"
    '''expression : expression PLUS expression 
                | expression MINUS expression 
                | expression MUL expression 
                | expression DIVIDE expression'''
    if p[2] == '+'  : p[0] = p[1] + p[3]
    elif p[2] == '-': p[0] = p[1] - p[3]
    elif p[2] == '*': p[0] = p[1] * p[3]
    elif p[2] == '/': p[0] = p[1] / p[3]

def p_expression_group(p):
    'expression : OPEN_PAR expression CLOSE_PAR'
    p[0] = p[2]

def p_expression_number(p):
    'expression : CONSTANT'
    p[0] = p[1]

def p_expression_name(p):
    'expression : ID'
    try:
        p[0] = names[p[1]]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0

def p_error(p):
    print("Syntax error at '%s'" % p.value)

parser = yacc.yacc()

while True:
   try:
       s = raw_input('calc > ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print(result)