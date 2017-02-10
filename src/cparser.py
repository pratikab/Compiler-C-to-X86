import ply.yacc as yacc
from lexer import *
import ply.lex as lex
import sys
sys.path.insert(0, "../..")

if sys.version_info[0] >= 3:
    raw_input = input
lex.lex()

import pydot
graph = pydot.Dot(graph_type='graph')

def add_edge(node_parent,node_child):
  graph.add_edge(pydot.Edge(node_parent, node_child))

def add_node(p):
  node = pydot.Node(p)
  return node

def draw_graph(p):
  parent = add_node(p[0])
  for x in (1,len(p)-1):
    child = add_node(p[x])
    add_edge(parent,child)

def p_primary_expression(p):
  '''primary_expression   : IDENTIFIER
                          | ICONST
                          | FCONST
                          | CCONST
                          | STRING_LITERAL
                          | '(' expression ')'
                          '''
  if len(p) == 2:
    t = ["primary_expression",p[1]]
  else:
    t = ["primary_expression","(",p[2],")"]
  #parent = add_node("primary_expression")
  draw_graph(t)


def p_postfix_expression(p):
  '''postfix_expression   : primary_expression
                          | postfix_expression '[' expression ']'
                          | postfix_expression '(' ')'
                          | postfix_expression '(' argument_expression_list ')'
                          | postfix_expression '.' IDENTIFIER
                          | postfix_expression PTR_OP IDENTIFIER
                          | postfix_expression INC_OP
                          | postfix_expression DEC_OP
                          '''
  if len(p) == 2:
    t = ["postfix_expression",p[1]]
  elif len(p) == 3:
    if p[2] == "++":
      t = ["postfix_expression",p[1],"++"]
    else:
      t = ["postfix_expression",p[1],"--"]
  else:
    if p[2] == "[":
      t = ["postfix_expression",p[1],"[",p[3],"]"]
    elif p[2] == "(":
      if len(p) == 4:
        t = ["postfix_expression",p[1],"(",")"]
      else : 
        t = ["postfix_expression",p[1],"(",p[3],")"]
    elif p[2] == ".":
      t = ["postfix_expression",p[1],".",p[3]]
    elif p[2] == "->":
      t = ["postfix_expression",p[1],"->",p[3]]
  draw_graph(t)

def p_argument_expression_list(p):
  '''argument_expression_list   : assignment_expression
                                | argument_expression_list ',' assignment_expression
                                '''
  if len(p) == 2:
    t = ["primary_expression",p[1]]
  else:
    t = ["primary_expression",p[1],",",p[3]]
  draw_graph(t)

def p_unary_expression(p):
  '''unary_expression   : postfix_expression
                        | INC_OP unary_expression
                        | DEC_OP unary_expression
                        | unary_operator cast_expression
                        | SIZEOF unary_expression
                        '''
  if len(p) == 2:
    t = ["unary_expression",p[1]]
  else:
    if p[1] == "++":
      t = ["unary_expression","++",p[2]]
    elif p[1] == "--":
      t = ["unary_expression","--",p[2]]
    elif p[1] == "sizeof":
      t = ["unary_expression","sizeof",p[2]]
    else :
      t = ["unary_expression",p[1],p[2]]
  draw_graph(t)

def p_unary_operator(p):
  '''unary_operator : '&'
                    | '*'
                    | '+'
                    | '-'
                    | '~'
                    | '!'
                    '''
  t = ["unary_operator",p[1]]
  draw_graph(t)

def p_cast_expression(p):
  '''cast_expression  : unary_expression
                      '''
  t = ["cast_expression",p[1]]
  draw_graph(t)

def p_multiplicative_expression(p):
  '''multiplicative_expression  : cast_expression
                                | multiplicative_expression '*' cast_expression
                                | multiplicative_expression '/' cast_expression
                                | multiplicative_expression '%' cast_expression
                                '''
  if len(p) == 2:
    t = ["multiplicative_expression",p[1]]
  else:
    if p[2] == "*":
      t = ["multiplicative_expression",p[1],"*",p[3]]
    elif p[2] == "/":
      t = ["multiplicative_expression",p[1],"/",p[3]]
    else : 
      t = ["multiplicative_expression",p[1],"%",p[3]]
  draw_graph(t)

def p_additive_expression(p):
  '''additive_expression  : multiplicative_expression
                          | additive_expression '+' multiplicative_expression
                          | additive_expression '-' multiplicative_expression
                          '''
  if len(p) == 2:
    t = ["additive_expression",p[1]]
  else:
    if p[2] == "+":
      t = ["additive_expression",p[1],"+",p[3]]
    else : 
      t = ["additive_expression",p[1],"-",p[3]]
  draw_graph(t)

def p_shift_expression(p):
  '''shift_expression   : additive_expression
                        | shift_expression LEFT_OP additive_expression
                        | shift_expression RIGHT_OP additive_expression
                        '''
  if len(p) == 2:
    t = ["shift_expression",p[1]]
  else:
    if p[2] == "<<":
      t = ["shift_expression",p[1],"<<",p[3]]
    else : 
      t = ["shift_expression",p[1],">>",p[3]]
  draw_graph(t)

def p_relational_expression(p):
  '''relational_expression  : shift_expression
                            | relational_expression '<' shift_expression
                            | relational_expression '>' shift_expression
                            | relational_expression LE_OP shift_expression
                            | relational_expression GE_OP shift_expression
                            '''
  if len(p) == 2:
    t = ["relational_expression",p[1]]
  else:
    if p[2] == "<":
      t = ["relational_expression",p[1],"<",p[3]]
    elif p[2] == ">":
      t = ["relational_expression",p[1],">",p[3]]
    elif p[2] == "<=":
      t = ["relational_expression",p[1],"<=",p[3]]
    else : 
      t = ["relational_expression",p[1],">=",p[3]]
  draw_graph(t)

def p_equality_expression(p):
  '''equality_expression  : relational_expression
                          | equality_expression EQ_OP relational_expression
                          | equality_expression NE_OP relational_expression
                          '''
  if len(p) == 2:
    t = ["equality_expression",p[1]]
  else:
    if p[2] == "==":
      t = ["equality_expression",p[1],"==",p[3]]
    else : 
      t = ["equality_expression",p[1],"!=",p[3]]
  draw_graph(t)

def p_and_expression(p):
  '''and_expression   : equality_expression
                      | and_expression '&' equality_expression
                      '''
  if len(p) == 2:
    t = ["and_expression",p[1]]
  else:
    t = ["and_expression",p[1],"&",p[3]]
  draw_graph(t)

def p_exclusive_or_expression(p):
  '''exclusive_or_expression  : and_expression
                              | exclusive_or_expression '^' and_expression
                              '''
  if len(p) == 2:
    t = ["exclusive_or_expression",p[1]]
  else:
    t = ["exclusive_or_expression",p[1],"^",p[3]]
  draw_graph(t)

def p_inclusive_or_expression(p):
  '''inclusive_or_expression  : exclusive_or_expression
                              | inclusive_or_expression '|' exclusive_or_expression
                              '''
  if len(p) == 2:
    t = ["inclusive_or_expression",p[1]]
  else:
    t = ["inclusive_or_expression",p[1],"|",p[3]]
  draw_graph(t)


def p_logical_and_expression(p):
  '''logical_and_expression   : inclusive_or_expression
                              | logical_and_expression AND_OP inclusive_or_expression
                              '''
  if len(p) == 2:
    t = ["logical_and_expression",p[1]]
  else:
    t = ["logical_and_expression",p[1],"&&",p[3]]
  draw_graph(t)

def p_logical_or_expression(p):
  '''logical_or_expression  : logical_and_expression
                            | logical_or_expression OR_OP logical_and_expression
                            '''
  if len(p) == 2:
    t = ["logical_or_expression",p[1]]
  else:
    t = ["logical_or_expression",p[1],"||",p[3]]
  draw_graph(t)

def p_conditional_expression(p):
  '''conditional_expression   : logical_or_expression
                              | logical_or_expression '?' expression ':' conditional_expression
                              '''
  if len(p) == 2:
    t = ["conditional_expression",p[1]]
  else:
    t = ["conditional_expression",p[1],"?",p[3],":",p[5]]
  draw_graph(t)

def p_assignment_expression(p):
  '''assignment_expression  : conditional_expression
                            | unary_expression assignment_operator assignment_expression
                            '''
  if len(p) == 2:
    t = ["assignment_expression",p[1]]
  else:
    t = ["assignment_expression",p[1],p[2],p[3]]
  draw_graph(t)

def p_assignment_operator(p):
  '''assignment_operator  : '='
                          | MUL_ASSIGN
                          | DIV_ASSIGN
                          | MOD_ASSIGN
                          | ADD_ASSIGN
                          | SUB_ASSIGN
                          | LEFT_ASSIGN
                          | RIGHT_ASSIGN
                          | AND_ASSIGN
                          | XOR_ASSIGN
                          | OR_ASSIGN
                          '''
  t = ["assignment_operator",p[1]]
  draw_graph(t)

def p_expression(p):
  '''expression   : assignment_expression
                  | expression ',' assignment_expression
                  '''
  if len(p) == 2:
    t = ["expression",p[1]]
  else:
    t = ["expression",p[1],",",p[3]]
  draw_graph(t)

def p_constant_expression(p):
  '''constant_expression  : conditional_expression
                          '''
  t = ["constant_expression",p[1]]  
  draw_graph(t)

def p_declaration(p):
  '''declaration  : declaration_specifiers ';'
                  | declaration_specifiers init_declarator_list ';'
                  '''
  if len(p) == 3:
    t = ["declaration",p[1],";"]
  else:
    t = ["declaration",p[1],p[2],";"]
  draw_graph(t)

def p_declaration_specifiers(p):
  '''declaration_specifiers   : storage_class_specifier
                              | storage_class_specifier declaration_specifiers
                              | type_specifier
                              | type_specifier declaration_specifiers
                              | type_qualifier
                              | type_qualifier declaration_specifiers
                              '''
  if len(p) == 2:
    t = ["declaration_specifiers",p[1]]
  else:
    t = ["declaration_specifiers",p[1],p[2]]
  draw_graph(t)

def p_init_declarator_list(p):
  '''init_declarator_list   : init_declarator
                            | init_declarator_list ',' init_declarator
                            '''
  if len(p) == 2:
    t = ["init_declarator_list",p[1]]
  else:
    t = ["init_declarator_list",p[1],",",p[3]]
  draw_graph(t)

def p_init_declarator(p):
  '''init_declarator  : declarator
                      | declarator '=' initializer
                      '''
  if len(p) == 2:
    t = ["init_declarator",p[1]]
  else:
    t = ["init_declarator",p[1],"=",p[3]]
  draw_graph(t)

def p_storage_class_specifier(p):
  '''storage_class_specifier  : TYPEDEF
                              | EXTERN
                              | STATIC
                              | AUTO
                              | REGISTER
                              '''
  t = ["storage_class_specifier",p[1]]  
  draw_graph(t)

def p_type_specifier(p):
  '''type_specifier   : VOID
                      | CHAR
                      | SHORT
                      | INT
                      | LONG
                      | FLOAT
                      | DOUBLE
                      | SIGNED
                      | UNSIGNED
                      | struct_or_union_specifier
                      | enum_specifier
                      '''
  t = ["type_specifier",p[1]]
  draw_graph(t)


def p_struct_or_union_specifier(p):
  '''struct_or_union_specifier  : struct_or_union IDENTIFIER '{' struct_declaration_list '}'
                                | struct_or_union '{' struct_declaration_list '}'
                                | struct_or_union IDENTIFIER
                                '''
  if len(p) == 3 :
    t = ["struct_or_union_specifier",p[1],p[2]]
  elif len(p) == 5:
    t = ["struct_or_union_specifier",p[1],"{",p[3],"}"]
  else :
    t = ["struct_or_union_specifier",p[1],p[2],"{",p[4],"}"]    
  draw_graph(t)


def p_struct_or_union_(p):
  '''struct_or_union  : STRUCT
                      | UNION
                      '''
  t = ["struct_or_union",p[1]]  
  draw_graph(t)


def p_struct_declaration_list(p):
  '''struct_declaration_list  : struct_declaration
                              | struct_declaration_list struct_declaration
                              '''
  if len(p) == 2:
    t = ["struct_declaration_list",p[1]]
  else :
    t = ["struct_declaration_list",p[1],p[2]]    
  draw_graph(t)

def p_struct_declaration(p):
  '''struct_declaration   : specifier_qualifier_list struct_declarator_list ';' '''
  t = ["struct_declaration",p[1],p[2],";"]
  draw_graph(t)


def p_specifier_qualifier_list(p):
  '''specifier_qualifier_list   : type_specifier specifier_qualifier_list
                                | type_specifier
                                | type_qualifier specifier_qualifier_list
                                | type_qualifier
                                '''
  if len(p) == 2:
    t = ["specifier_qualifier_list",p[1]]
  else :
    t = ["specifier_qualifier_list",p[1],p[2]]
  draw_graph(t)

def p_struct_declarator_list(p):
  '''struct_declarator_list   : struct_declarator
                              | struct_declarator_list ',' struct_declarator
                              '''
  if len(p) == 2:
    t = ["struct_declarator_list",p[1]]
  else :
    t = ["struct_declarator_list",p[1],",",p[3]]
  draw_graph(t)

def p_struct_declarator(p):
  '''struct_declarator  : declarator
                        | ':' constant_expression
                        | declarator ':' constant_expression
                        '''
  if len(p) == 2:
    t = ["struct_declarator",p[1]]
  elif len(p) == 3 :
    t = ["struct_declarator",":",p[2]]
  else :
    t = ["struct_declarator",p[1],":",p[3]]
  draw_graph(t)

def p_enum_specifier(p):
  '''enum_specifier   : ENUM '{' enumerator_list '}'
                      | ENUM IDENTIFIER '{' enumerator_list '}'
                      | ENUM IDENTIFIER
                      '''
  if len(p) == 3:
    t = ["enum_specifier",p[1],p[2]]
  elif len(p) == 5 :
    t = ["enum_specifier",p[1],"{",p[3],"}"]
  else :
    t = ["enum_specifier",p[1],p[2],"{",p[4],"}"]
  draw_graph(t)

def p_enumerator_list(p):
  '''enumerator_list  : enumerator
                      | enumerator_list ',' enumerator
                      '''
  if len(p) == 2:
    t = ["enumerator_list",p[1]]
  else :
    t = ["enumerator_list",p[1],",",p[3]]
  draw_graph(t)

def p_enumerator(p):
  '''enumerator   : IDENTIFIER
                  | IDENTIFIER '=' constant_expression
                  '''
  if len(p) == 2:
    t = ["enumerator",p[1]]
  else :
    t = ["enumerator",p[1],"=",p[3]]
  draw_graph(t)

def p_type_qualifier(p):
  '''type_qualifier   : CONST
                      | VOLATILE
                      '''
  t = ["type_qualifier",p[1]]
  draw_graph(t)

def p_declarator(p):
  '''declarator   : pointer direct_declarator
                  | direct_declarator
                  '''
  if len(p) == 2:
    t = ["declarator",p[1]]
  else :
    t = ["declarator",p[1],p[2]]
  draw_graph(t)

def p_direct_declarator(p):
  '''direct_declarator  : IDENTIFIER
                        | '(' declarator ')'
                        | direct_declarator '[' constant_expression ']'
                        | direct_declarator '[' ']'
                        | direct_declarator '(' parameter_type_list ')'
                        | direct_declarator '(' identifier_list ')'
                        | direct_declarator '(' ')'
                        '''
  if len(p) == 2:
    t = ["direct_declarator",p[1]]
  elif len(p) == 4:
    if p[1] == "(":
      t = ["direct_declarator","(",p[2],")"]
    elif p[2] == "[":
      t = ["direct_declarator",p[1],"[","]"]
    else:
      t = ["direct_declarator",p[1],"(",")"]     
  else:
    if p[2] == "[":
      t = ["direct_declarator",p[1],"[",p[3],"]"]
    elif p[2] == "(":
      t = ["direct_declarator",p[1],"(",p[3],")"]
  draw_graph(t)

def p_pointer(p):
  '''pointer  : '*'
              | '*' type_qualifier_list
              | '*' pointer
              | '*' type_qualifier_list pointer
              '''
  if len(p) == 2:
    t = ["pointer","*"]
  elif len(p) == 3:
    t = ["pointer","*",p[2]]
  else:
    t = ["pointer","*",p[2],p[3]]
  draw_graph(t)

def p_type_qualifier_list(p):
  '''type_qualifier_list  : type_qualifier
                          | type_qualifier_list type_qualifier
                          '''
  if len(p) == 2:
    t = ["type_qualifier_list",p[1]]
  else:
    t = ["type_qualifier_list",p[1],p[2]]
  draw_graph(t)

def p_parameter_type_list(p):
  '''parameter_type_list  : parameter_list
                          | parameter_list ',' ELLIPSIS
                          '''
  if len(p) == 2:
    t = ["parameter_type_list",p[1]]
  else:
    t = ["parameter_type_list",p[1],",",p[3]]
  draw_graph(t)

def p_parameter_list(p):
  '''parameter_list   : parameter_declaration
                      | parameter_list ',' parameter_declaration
                      '''
  if len(p) == 2:
    t = ["parameter_list",p[1]]
  else:
    t = ["parameter_list",p[1],",",p[3]]
  draw_graph(t)

def p_parameter_declaration(p):
  '''parameter_declaration  : declaration_specifiers declarator
                            | declaration_specifiers abstract_declarator
                            | declaration_specifiers
                            '''
  if len(p) == 2:
    t = ["parameter_declaration",p[1]]
  else:
    t = ["parameter_declaration",p[1],p[2]]
  draw_graph(t)

def p_identifier_list(p):
  '''identifier_list  : IDENTIFIER
                      | identifier_list ',' IDENTIFIER
                      '''
  if len(p) == 2:
    t = ["identifier_list",p[1]]
  else:
    t = ["identifier_list",p[1],",",p[3]]
  draw_graph(t)

def p_abstract_declarator(p):
  '''abstract_declarator  : pointer
                          | direct_abstract_declarator
                          | pointer direct_abstract_declarator
                          '''
  if len(p) == 2:
    t = ["abstract_declarator",p[1]]
  else:
    t = ["abstract_declarator",p[1],p[2]]
  draw_graph(t)

def p_direct_abstract_declarator(p):
  '''direct_abstract_declarator   : '(' abstract_declarator ')'
                                  | '[' ']'
                                  | '[' constant_expression ']'
                                  | direct_abstract_declarator '[' ']'
                                  | direct_abstract_declarator '[' constant_expression ']'
                                  | '(' ')'
                                  | '(' parameter_type_list ')'
                                  | direct_abstract_declarator '(' ')'
                                  | direct_abstract_declarator '(' parameter_type_list ')'
                                  '''
  if len(p) == 3:
    t = ["direct_abstract_declarator",p[1],p[2]]
  elif len(p) == 4:
    t = ["direct_abstract_declarator",p[1],p[2],p[3]]
  else:
    t = ["direct_abstract_declarator",p[1],p[2],p[3],p[4]]
  draw_graph(t)

def p_initializer(p):
  '''initializer  : assignment_expression
                  | '{' initializer_list '}'
                  | '{' initializer_list ',' '}'
                  '''
  if len(p) == 2:
    t = ["identifier_list",p[1]]
  elif len(p) == 4:
    t = ["identifier_list","{",p[2],"}"]
  else:
    t = ["identifier_list","{",p[2],",","}"]    
  draw_graph(t)

def p_initializer_list(p):
  '''initializer_list   : initializer
                        | initializer_list ',' initializer
                        '''
  if len(p) == 2:
    t = ["initializer_list",p[1]]
  else:
    t = ["initializer_list",p[1],",",p[3]]
  draw_graph(t)


def p_statement(p):
  '''statement    : labeled_statement
                  | compound_statement
                  | expression_statement
                  | selection_statement
                  | iteration_statement
                  | jump_statement
                  '''
  t = ["statement",p[1]]
  draw_graph(t)

def p_labeled_statement(p):
  '''labeled_statement  : IDENTIFIER ':' statement
                        | CASE constant_expression ':' statement
                        | DEFAULT ':' statement
                        '''
  if len(p) == 4:
    t = ["labeled_statement",p[1],p[2],p[3]]
  else:
    t = ["labeled_statement",p[1],p[2],p[3],p[4]]
  draw_graph(t)

def p_compound_statement(p):
  '''compound_statement   : '{' '}'
                          | '{' statement_list '}'
                          | '{' declaration_list '}'
                          | '{' declaration_list statement_list '}'
                          '''
  if len(p) == 3:
    t = ["compound_statement",p[1],p[2]]
  elif len(p) == 4:
    t = ["compound_statement",p[1],p[2],p[3]]
  else:
    t = ["compound_statement",p[1],p[2],p[3],p[4]]
  draw_graph(t)

def p_declaration_list(p):
  '''declaration_list   : declaration
                        | declaration_list declaration
                        '''
  if len(p) == 2:
    t = ["declaration_list",p[1]]
  else:
    t = ["declaration_list",p[1],p[2]]
  draw_graph(t)

def p_statement_list(p):
  '''statement_list   : statement
                      | statement_list statement
                      '''
  if len(p) == 2:
    t = ["statement_list",p[1]]
  else:
    t = ["statement_list",p[1],p[2]]
  draw_graph(t)

def p_expression_statement(p):
  '''expression_statement   : ';'
                            | expression ';'
                            '''
  if len(p) == 2 :
    t = ["expression_statement",";"]
  else :
    t = ["expression_statement",p[1],";"]
  draw_graph(t)

def p_selection_statement(p):
  '''selection_statement  : IF '(' expression ')' statement
                          | IF '(' expression ')' statement ELSE statement
                          | SWITCH '(' expression ')' statement
                          '''
  if len(p) == 6:
    t = ["selection_statement",p[1],p[2],p[3],p[4],p[5]]
  else:
    t = ["selection_statement",p[1],p[2],p[3],p[4],p[5],p[6],p[7]]
  draw_graph(t)

def p_iteration_statement(p):
  '''iteration_statement  : WHILE '(' expression ')' statement
                          | DO statement WHILE '(' expression ')' ';'
                          | FOR '(' expression_statement expression_statement ')' statement
                          | FOR '(' expression_statement expression_statement expression ')' statement
                          '''
  if len(p) == 6:
    t = ["iteration_statement",p[1],p[2],p[3],p[4],p[5]]
  elif len(p) == 7:
    t = ["iteration_statement",p[1],p[2],p[3],p[4],p[5],p[6]]
  else:
    t = ["iteration_statement",p[1],p[2],p[3],p[4],p[5],p[6],p[7]]
  draw_graph(t)

def p_jump_statement(p):
  '''jump_statement   : GOTO IDENTIFIER ';'
                      | CONTINUE ';'
                      | BREAK ';'
                      | RETURN ';'
                      | RETURN expression ';'
                      '''
  if len(p) == 3:
    t = ["jump_statement",p[1],";"]
  else:
    t = ["jump_statement",p[1],p[2],";"]
  draw_graph(t)


def p_translation_unit(p):
  '''translation_unit   : external_declaration
                        | translation_unit external_declaration
                        '''
  if len(p) == 2:
    t = ["translation_unit",p[1]]
  else:
    t = ["translation_unit",p[1],p[2]]
  draw_graph(t)

def p_external_declaration(p):
  '''external_declaration   : function_definition
                            | declaration
                            '''
  t = ["external_declaration",p[1]]
  draw_graph(t)

def p_function_definition(p):
  '''function_definition  : declaration_specifiers declarator declaration_list compound_statement
                          | declaration_specifiers declarator compound_statement
                          | declarator declaration_list compound_statement
                          | declarator compound_statement
                          '''
  if len(p) == 3:
    t = ["iteration_statement",p[1],p[2]]
  elif len(p) == 4:
    t = ["iteration_statement",p[1],p[2],p[3]]
  else:
    t = ["iteration_statement",p[1],p[2],p[3],p[4]]
  draw_graph(t)


def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

yacc.yacc( start='translation_unit')

while 1:
    try:
        s = raw_input('INPUT > ')
    except EOFError:
        break
    if not s:
        continue
    yacc.parse(s)
    graph.write_png('graph.png')