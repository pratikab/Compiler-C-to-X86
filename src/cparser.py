import ply.yacc as yacc
from lexer import *
import ply.lex as lex

lex.lex()

while True:
   try:
       s = raw_input('calc > ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print(result)