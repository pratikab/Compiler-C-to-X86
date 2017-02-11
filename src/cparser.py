import ply.yacc as yacc
from lexer import *
import ply.lex as lex
import sys
lex.lex()

import pydot
graph = pydot.Dot(graph_type='graph')

def add_edge(node_parent,node_child):
  graph.add_edge(pydot.Edge(node_parent, node_child))

k = 0
def add_node(p):
  global k
  node = pydot.Node(k,label = p)
  graph.add_node(node)
  k = k + 1
  return node

def draw_graph(p):
    for x in range (1,len(p)):
        add_edge(p[0],p[x])


def p_primary_expression(p):
  '''primary_expression   : IDENTIFIER
                          | ICONST
                          | FCONST
                          | CCONST
                          | STRING_LITERAL
                          | '(' expression ')'
                          '''
  parent = add_node("primary_expression")
  if len(p) == 2:
    c1 = add_node(str(p[1]))
    t = [parent,c1]
  else:
    c1 = add_node(str(p[1]))
    c2 = add_node(str(p[3]))
    t = [parent,c1,p[2],c2]
  p[0] = parent
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
  parent = add_node("postfix_expression")
  if len(p) == 2:
    t = [parent,p[1]]
  elif len(p) == 3:
    if p[2] == "++":
      c1 = add_node(str(p[2]))
      t = [parent,p[1],c1]
    else:
      c1 = add_node(str(p[2]))
      t = [parent,p[1],c1]
  else:
    if p[2] == "[":
      c1 = add_node(str(p[2]))
      c2 = add_node(str(p[4]))
      t = [parent,p[1],c1,p[3],c2]
    elif p[2] == "(":
      if len(p) == 4:
        c1 = add_node(str(p[2]))
        c2 = add_node(str(p[3]))
        t = [parent,p[1],c1,c2]
      else : 
        c1 = add_node(str(p[2]))
        c2 = add_node(str(p[4]))
        t = [parent,p[1],c1,p[3],c2]
    elif p[2] == ".":
      c1 = add_node(str(p[2]))
      t = [parent,p[1],c1,p[3]]
    elif p[2] == "->":
      c1 = add_node(str(p[2]))
      t = [parent,p[1],c1,p[3]]
  p[0] = parent
  draw_graph(t)

def p_argument_expression_list(p):
  '''argument_expression_list   : assignment_expression
                                | argument_expression_list ',' assignment_expression
                                '''
  parent = add_node("argument_expression_list")
  if len(p) == 2:
    t = [parent,p[1]]
  else:
    c1 = add_node("\,")
    t = [parent,p[1],c1,p[3]]
  p[0] = parent
  draw_graph(t)

def p_unary_expression(p):
  '''unary_expression   : postfix_expression
                        | INC_OP unary_expression
                        | DEC_OP unary_expression
                        | unary_operator cast_expression
                        | SIZEOF unary_expression
                        '''
  parent = add_node("unary_expression")
  if len(p) == 2:
    t = [parent,p[1]]
  else:
    if p[1] == "++":
      c1 = add_node(str(p[1]))
      t = [parent,c1,p[2]]
    elif p[1] == "--":
      c1 = add_node(str(p[1]))
      t = [parent,c1,p[2]]
    elif p[1] == "sizeof":
      c1 = add_node(str(p[1]))
      t = [parent,c1,p[2]]
    else :
      t = [parent,p[1],p[2]]
  p[0] = parent
  draw_graph(t)

def p_unary_operator(p):
  '''unary_operator : '&'
                    | '*'
                    | '+'
                    | '-'
                    | '~'
                    | '!'
                    '''
  parent = add_node("unary_operator")
  c1 = add_node(str(p[1]))
  t = [parent,c1]
  p[0] = parent
  draw_graph(t)

def p_cast_expression(p):
  '''cast_expression  : unary_expression
                      '''
  parent = add_node("cast_expression")
  t = [parent,p[1]]
  p[0] = parent
  draw_graph(t)

def p_multiplicative_expression(p):
  '''multiplicative_expression  : cast_expression
                                | multiplicative_expression '*' cast_expression
                                | multiplicative_expression '/' cast_expression
                                | multiplicative_expression '%' cast_expression
                                '''
  parent = add_node("multiplicative_expression")
  if len(p) == 2:
    t = [parent,p[1]]
  else:
    c1 = add_node(str(p[2]))
    t = [parent,p[1],c1,p[3]]
  p[0] = parent
  draw_graph(t)

def p_additive_expression(p):
  '''additive_expression  : multiplicative_expression
                          | additive_expression '+' multiplicative_expression
                          | additive_expression '-' multiplicative_expression
                          '''
  parent = add_node("additive_expression")
  if len(p) == 2:
    t = [parent,p[1]]
  else:
    c1 = add_node(str(p[2]))
    t = [parent,p[1],c1,p[3]]
  p[0] = parent
  draw_graph(t)

def p_shift_expression(p):
  '''shift_expression   : additive_expression
                        | shift_expression LEFT_OP additive_expression
                        | shift_expression RIGHT_OP additive_expression
                        '''
  parent = add_node("shift_expression")
  if len(p) == 2:
    t = [parent,p[1]]
  else:
    c1 = add_node(str(p[2]))
    t = [parent,p[1],c1,p[3]]
  p[0] = parent
  draw_graph(t)

def p_relational_expression(p):
  '''relational_expression  : shift_expression
                            | relational_expression '<' shift_expression
                            | relational_expression '>' shift_expression
                            | relational_expression LE_OP shift_expression
                            | relational_expression GE_OP shift_expression
                            '''
  parent = add_node("relational_expression")
  if len(p) == 2:
    t = [parent,p[1]]
  else:
    c1 = add_node(str(p[2]))
    t = [parent,p[1],c1,p[3]]
  p[0] = parent
  draw_graph(t)

def p_equality_expression(p):
  '''equality_expression  : relational_expression
                          | equality_expression EQ_OP relational_expression
                          | equality_expression NE_OP relational_expression
                          '''
  parent = add_node("equality_expression")
  if len(p) == 2:
    t = [parent,p[1]]
  else:
    c1 = add_node(str(p[2]))
    t = [parent,p[1],c1,p[3]]
  p[0] = parent
  draw_graph(t)

def p_and_expression(p):
  '''and_expression   : equality_expression
                      | and_expression '&' equality_expression
                      '''
  parent = add_node("and_expression")
  if len(p) == 2:
    t = [parent,p[1]]
  else:
    c1 = add_node(str(p[2]))
    t = [parent,p[1],c1,p[3]]
  p[0] = parent
  draw_graph(t)

def p_exclusive_or_expression(p):
  '''exclusive_or_expression  : and_expression
                              | exclusive_or_expression '^' and_expression
                              '''
  parent = add_node("exclusive_or_expression")
  if len(p) == 2:
    t = [parent,p[1]]
  else:
    c1 = add_node(str(p[2]))
    t = [parent,p[1],c1,p[3]]
  p[0] = parent
  draw_graph(t)

def p_inclusive_or_expression(p):
  '''inclusive_or_expression  : exclusive_or_expression
                              | inclusive_or_expression '|' exclusive_or_expression
                              '''
  parent = add_node("inclusive_or_expression")
  if len(p) == 2:
    t = [parent,p[1]]
  else:
    c1 = add_node(str(p[2]))
    t = [parent,p[1],c1,p[3]]
  p[0] = parent
  draw_graph(t)


def p_logical_and_expression(p):
  '''logical_and_expression   : inclusive_or_expression
                              | logical_and_expression AND_OP inclusive_or_expression
                              '''
  parent = add_node("logical_and_expression")
  if len(p) == 2:
    t = [parent,p[1]]
  else:
    c1 = add_node(str(p[2]))
    t = [parent,p[1],c1,p[3]]
  p[0] = parent
  draw_graph(t)

def p_logical_or_expression(p):
  '''logical_or_expression  : logical_and_expression
                            | logical_or_expression OR_OP logical_and_expression
                            '''
  parent = add_node("logical_or_expression")
  if len(p) == 2:
    t = [parent,p[1]]
  else:
    c1 = add_node(str(p[2]))
    t = [parent,p[1],c1,p[3]]
  p[0] = parent
  draw_graph(t)

def p_conditional_expression(p):
  '''conditional_expression   : logical_or_expression
                              | logical_or_expression '?' expression ':' conditional_expression
                              '''
  parent = add_node("conditional_expression")
  if len(p) == 2:
    t = [parent,p[1]]
  else:
    c1 = add_node(str(p[2]))
    c2 = add_node(str(p[4]))
    t = [parent,p[1],c1,p[3],c2,p[5]]
  p[0] = parent
  draw_graph(t)

def p_assignment_expression(p):
  '''assignment_expression  : conditional_expression
                            | unary_expression assignment_operator assignment_expression
                            '''
  parent = add_node("assignment_expression")
  if len(p) == 2:
    t = [parent,p[1]]
  else:
    t = [parent,p[1],p[2],p[3]]
  p[0] = parent
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
  parent = add_node("assignment_operator")
  c1 = add_node(str(p[1]))
  t = [parent,c1]
  p[0] = parent
  draw_graph(t)

def p_expression(p):
  '''expression   : assignment_expression
                  | expression ',' assignment_expression
                  '''
  parent = add_node("expression")
  if len(p) == 2:
    t = [parent,p[1]]
  else:
    c1 = add_node(str(p[2]))
    t = [parent,p[1],c1,p[3]]
  p[0] = parent
  draw_graph(t)

def p_constant_expression(p):
  '''constant_expression  : conditional_expression
                          '''
  parent = add_node("constant_expression")
  t = [parent,p[1]]  
  p[0] = parent
  draw_graph(t)

def p_declaration(p):
  '''declaration  : declaration_specifiers ';'
                  | declaration_specifiers init_declarator_list ';'
                  '''
  parent = add_node("declaration")
  if len(p) == 3:
    c1 = add_node(str(p[2]))
    t = [parent,p[1],c1]
  else:
    c1 = add_node(str(p[3]))
    t = [parent,p[1],p[2],c1]
  p[0] = parent
  draw_graph(t)

def p_declaration_specifiers(p):
  '''declaration_specifiers   : storage_class_specifier
                              | storage_class_specifier declaration_specifiers
                              | type_specifier
                              | type_specifier_1
                              | type_specifier declaration_specifiers
                              | type_specifier_1 declaration_specifiers
                              | type_qualifier
                              | type_qualifier declaration_specifiers
                              '''
  parent = add_node("declaration_specifiers")
  if len(p) == 2:
    t = [parent,p[1]]
  else:
    t = [parent,p[1],p[2]]
  p[0] = parent
  draw_graph(t)

def p_init_declarator_list(p):
  '''init_declarator_list   : init_declarator
                            | init_declarator_list ',' init_declarator
                            '''
  parent = add_node("init_declarator_list")
  if len(p) == 2:
    t = [parent,p[1]]
  else:
    c1 = add_node("\,")
    t = [parent,p[1],c1,p[3]]
  draw_graph(t)
  p[0] = parent

def p_init_declarator(p):
  '''init_declarator  : declarator
                      | declarator '=' initializer
                      '''
  parent = add_node("init_declarator")
  if len(p) == 2:
    t = [parent,p[1]]
  else:
    c1 = add_node(str(p[2]))
    t = [parent,p[1],c1,p[3]]
  draw_graph(t)
  p[0] = parent

def p_storage_class_specifier(p):
  '''storage_class_specifier  : TYPEDEF
                              | EXTERN
                              | STATIC
                              | AUTO
                              | REGISTER
                              '''
  parent = add_node("storage_class_specifier")
  c1 = add_node(str(p[1]))
  t = [parent,c1]  
  draw_graph(t)
  p[0] = parent

def p_type_specifier(p):
  '''type_specifier   : VOID
                      | CHAR
                      | SHORT
                      | INT
                      | BOOL
                      | LONG
                      | FLOAT
                      | DOUBLE
                      | SIGNED
                      | UNSIGNED
                      '''
  parent = add_node("type_specifier")
  c1 = add_node(str(p[1]))
  t = [parent,c1]
  draw_graph(t)
  p[0] = parent

def p_type_specifier_1(p):
  '''type_specifier_1   : struct_or_union_specifier
                        | enum_specifier
                        '''
  parent = add_node("type_specifier_1")
  t = [parent,p[1]]
  draw_graph(t)
  p[0] = parent


def p_struct_or_union_specifier(p):
  '''struct_or_union_specifier  : struct_or_union IDENTIFIER '{' struct_declaration_list '}'
                                | struct_or_union '{' struct_declaration_list '}'
                                | struct_or_union IDENTIFIER
                                '''
  parent = add_node("struct_or_union_specifier")
  if len(p) == 3 :
    c1 = add_node(str(p[2]))
    t = [parent,p[1],c1]
  elif len(p) == 5:
    c1 = add_node(str(p[2]))
    c2 = add_node(str(p[4]))
    t = [parent,p[1],c1,p[3],c2]
  else :
    c1 = add_node(str(p[2]))
    c2 = add_node(str(p[3]))
    c3 = add_node(str(p[5]))
    t = [parent,p[1],c1,c2,p[4],c3]    
  draw_graph(t)
  p[0] = parent


def p_struct_or_union_(p):
  '''struct_or_union  : STRUCT
                      | UNION
                      '''
  parent = add_node("struct_or_union")
  c1 = add_node(str(p[1]))
  t = [parent,c1]  
  draw_graph(t)
  p[0] = parent


def p_struct_declaration_list(p):
  '''struct_declaration_list  : struct_declaration
                              | struct_declaration_list struct_declaration
                              '''
  parent = add_node("struct_declaration_list")
  if len(p) == 2:
    t = [parent,p[1]]
  else :
    t = [parent,p[1],p[2]]    
  draw_graph(t)
  p[0] = parent

def p_struct_declaration(p):
  '''struct_declaration   : specifier_qualifier_list struct_declarator_list ';' '''
  parent = add_node("struct_declaration")
  c1 = add_node(str(p[3]))
  t = [parent,p[1],p[2],c1]
  draw_graph(t)
  p[0] = parent


def p_specifier_qualifier_list(p):
  '''specifier_qualifier_list   : type_specifier specifier_qualifier_list
                                | type_specifier
                                | type_specifier_1 specifier_qualifier_list
                                | type_specifier_1
                                | type_qualifier specifier_qualifier_list
                                | type_qualifier
                                '''
  parent = add_node("specifier_qualifier_list")
  if len(p) == 2:
    t = [parent,p[1]]
  else :
    t = [parent,p[1],p[2]]
  draw_graph(t)
  p[0] = parent

def p_struct_declarator_list(p):
  '''struct_declarator_list   : struct_declarator
                              | struct_declarator_list ',' struct_declarator
                              '''
  parent = add_node("struct_declarator_list")
  if len(p) == 2:
    t = [parent,p[1]]
  else:
    c1 = add_node("\,")
    t = [parent,p[1],c1,p[3]]
  draw_graph(t)
  p[0] = parent

def p_struct_declarator(p):
  '''struct_declarator  : declarator
                        | ':' constant_expression
                        | declarator ':' constant_expression
                        '''
  parent = add_node("struct_declarator")
  if len(p) == 2:
    t = [parent,p[1]]
  elif len(p) == 3 :
    c1 = add_node(str(p[1]))
    t = [parent,c1,p[2]]
  else :
    c1 = add_node(str(p[2]))
    t = [parent,p[1],c1,p[3]]
  draw_graph(t)
  p[0] = parent

def p_enum_specifier(p):
  '''enum_specifier   : ENUM '{' enumerator_list '}'
                      | ENUM IDENTIFIER '{' enumerator_list '}'
                      | ENUM IDENTIFIER
                      '''
  parent = add_node("enum_specifier")
  if len(p) == 3:
    c1 = add_node(str(p[1]))
    c2 = add_node(str(p[2]))
    t = [parent,c1,c2]
  elif len(p) == 5 :
    c1 = add_node(str(p[1]))
    c2 = add_node(str(p[2]))
    c3 = add_node(str(p[4]))
    t = [parent,c1,c2,p[3],c3]
  else :
    c1 = add_node(str(p[1]))
    c2 = add_node(str(p[2]))
    c3 = add_node(str(p[3]))
    c4 = add_node(str(p[5]))
    t = [parent,c1,c2,c3,p[4],c4]
  draw_graph(t)
  p[0] = parent

def p_enumerator_list(p):
  '''enumerator_list  : enumerator
                      | enumerator_list ',' enumerator
                      '''
  parent = add_node("enumerator_list")
  if len(p) == 2:
    t = [parent,p[1]]
  else:
    c1 = add_node("\,")
    t = [parent,p[1],c1,p[3]]
  draw_graph(t)
  p[0] = parent

def p_enumerator(p):
  '''enumerator   : IDENTIFIER
                  | IDENTIFIER '=' constant_expression
                  '''
  parent = add_node("enumerator")
  if len(p) == 2:
    c1 = add_node(str(p[1]))
    t = [parent,c1]
  else:
    c1 = add_node(str(p[1]))
    c2 = add_node(str(p[2]))
    t = [parent,c1,c2,p[3]]
  draw_graph(t)
  p[0] = parent

def p_type_qualifier(p):
  '''type_qualifier   : CONST
                      | VOLATILE
                      '''
  parent = add_node("type_qualifier")
  c1 = add_node(str(p[1]))
  t = [parent,c1]
  draw_graph(t)
  p[0] = parent

def p_declarator(p):
  '''declarator   : pointer direct_declarator
                  | direct_declarator
                  '''
  parent = add_node("declarator")
  if len(p) == 2:
    t = [parent,p[1]]
  else :
    t = [parent,p[1],p[2]]
  draw_graph(t)
  p[0] = parent

def p_direct_declarator(p):
  '''direct_declarator  : IDENTIFIER
                        | '(' declarator ')'
                        | direct_declarator '[' constant_expression ']'
                        | direct_declarator '[' ']'
                        | direct_declarator '(' parameter_type_list ')'
                        | direct_declarator '(' identifier_list ')'
                        | direct_declarator '(' ')'
                        '''
  parent = add_node("direct_declarator")
  p[0] = parent
  if len(p) == 2:
    c1 = add_node(str(p[1]))
    t = [parent,c1]
  elif len(p) == 4:
    if p[1] == "(":
      c1 = add_node(str(p[1]))
      c2 = add_node(str(p[3]))
      t = [parent,c1,p[2],c2]
    else:
      c1 = add_node(str(p[2]))
      c2 = add_node(str(p[3]))
      t = [parent,p[1],c1,c2]     
  else:
    c1 = add_node(str(p[2]))
    c2 = add_node(str(p[4]))
    t = [parent,p[1],c1,p[3],c2]
  draw_graph(t)
  p[0] = parent

def p_pointer(p):
  '''pointer  : '*'
              | '*' type_qualifier_list
              | '*' pointer
              | '*' type_qualifier_list pointer
              '''
  parent = add_node("pointer")
  c1 = add_node(str(p[1]))
  if len(p) == 2:
    t = [parent,c1]
  elif len(p) == 3:
    t = [parent,c1,p[2]]
  else:
    t = [parent,c1,p[2],p[3]]
  draw_graph(t)
  p[0] = parent

def p_type_qualifier_list(p):
  '''type_qualifier_list  : type_qualifier
                          | type_qualifier_list type_qualifier
                          '''
  parent = add_node("type_qualifier_list")
  if len(p) == 2:
    t = [parent,p[1]]
  else:
    t = [parent,p[1],p[2]]
  draw_graph(t)
  p[0] = parent

def p_parameter_type_list(p):
  '''parameter_type_list  : parameter_list
                          | parameter_list ',' ELLIPSIS
                          '''
  parent = add_node("parameter_type_list")
  if len(p) == 2:
    t = [parent,p[1]]
  else:
    c1 = add_node("\,")
    c2 = add_node(str(p[3]))
    t = [parent,p[1],c1,c2]
  draw_graph(t)
  p[0] = parent

def p_parameter_list(p):
  '''parameter_list   : parameter_declaration
                      | parameter_list ',' parameter_declaration
                      '''
  parent = add_node("parameter_list")
  if len(p) == 2:
    t = [parent,p[1]]
  else:
    c1 = add_node("\,")
    t = [parent,p[1],c1,p[3]]
  draw_graph(t)
  p[0] = parent

def p_parameter_declaration(p):
  '''parameter_declaration  : declaration_specifiers declarator
                            | declaration_specifiers abstract_declarator
                            | declaration_specifiers
                            '''
  parent = add_node("parameter_declaration")
  if len(p) == 2:
    t = [parent,p[1]]
  else:
    t = [parent,p[1],p[2]]
  draw_graph(t)
  p[0] = parent

def p_identifier_list(p):
  '''identifier_list  : IDENTIFIER
                      | identifier_list ',' IDENTIFIER
                      '''
  parent = add_node("identifier_list")
  if len(p) == 2:
    c1 = add_node(str(p[1]))
    t = [parent,c1]
  else:
    c1 = add_node("\,")
    c2 = add_node(str(p[3]))
    t = [parent,p[1],c1,c2]
  draw_graph(t)
  p[0] = parent

def p_abstract_declarator(p):
  '''abstract_declarator  : pointer
                          | direct_abstract_declarator
                          | pointer direct_abstract_declarator
                          '''
  parent = add_node("abstract_declarator")
  if len(p) == 2:
    t = [parent,p[1]]
  else:
    t = [parent,p[1],p[2]]
  draw_graph(t)
  p[0] = parent

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
  parent = add_node("direct_abstract_declarator")
  if len(p) == 3:
    c1 = add_node(str(p[1]))
    c2 = add_node(str(p[2]))
    t = [parent,c1,c2]
  elif len(p) == 4:
    if p[1] == "(" :
      c1 = add_node(str(p[1]))
      c2 = add_node(str(p[3]))
      t = [parent,c1,p[2],c2]
    elif p[1] == "[":
      c1 = add_node(str(p[1]))
      c2 = add_node(str(p[3]))
      t = [parent,c1,p[2],c2]
    else :
      c1 = add_node(str(p[2]))
      c2 = add_node(str(p[3]))
      t = [parent,p[1],c1,c2]
  else:
    c1 = add_node(str(p[2]))
    c2 = add_node(str(p[4]))
    t = [parent,p[1],c1,p[3],c2]
  draw_graph(t)
  p[0] = parent

def p_initializer(p):
  '''initializer  : assignment_expression
                  | '{' initializer_list '}'
                  | '{' initializer_list ',' '}'
                  '''
  parent = add_node("initializer")
  if len(p) == 2:
    t = [parent,p[1]]
  elif len(p) == 4:
    c1 = add_node(str(p[1]))
    c2 = add_node(str(p[3]))
    t = [parent,c1,p[2],c2]
  else:
    c1 = add_node(str(p[1]))
    c2 = add_node("\,")
    c3 = add_node(str(p[4]))
    t = [parent,c1,p[2],c2,c3]    
  draw_graph(t)
  p[0] = parent

def p_initializer_list(p):
  '''initializer_list   : initializer
                        | initializer_list ',' initializer
                        '''
  parent = add_node("initializer_list")
  if len(p) == 2:
    t = [parent,p[1]]
  else:
    c1 = add_node("\,")
    t = [parent,p[1],c1,p[3]]
  draw_graph(t)
  p[0] = parent


def p_statement(p):
  '''statement    : labeled_statement
                  | compound_statement
                  | expression_statement
                  | selection_statement
                  | iteration_statement
                  | iteration_statement_1
                  | jump_statement
                  | jump_statement_1
                  '''
  parent = add_node("statement")
  t = [parent,p[1]]
  draw_graph(t)
  p[0] = parent

def p_labeled_statement(p):
  '''labeled_statement  : IDENTIFIER ':' statement
                        | CASE constant_expression ':' statement
                        | DEFAULT ':' statement
                        '''
  parent = add_node("labeled_statement")
  if len(p) == 4:
    c1 = add_node(str(p[1]))
    c2 = add_node(str(p[2]))
    t = [parent,c1,c2,p[3]]
  else:
    c1 = add_node(str(p[1]))
    c2 = add_node(str(p[3]))
    t = [parent,c1,p[2],c2,p[4]]
  draw_graph(t)
  p[0] = parent

def p_compound_statement(p):
  '''compound_statement   : '{' '}'
                          | '{' statement_list '}'
                          | '{' declaration_list '}'
                          | '{' declaration_list statement_list '}'
                          '''
  parent = add_node("compound_statement")
  if len(p) == 3:
    c1 = add_node(str(p[1]))
    c2 = add_node(str(p[2]))
    t = [parent,c1,c2]
  elif len(p) == 4:
    c1 = add_node(str(p[1]))
    c2 = add_node(str(p[3]))
    t = [parent,c1,p[2],c2]
  else:
    c1 = add_node(str(p[1]))
    c2 = add_node(str(p[4]))
    t = [parent,c1,p[2],p[3],c2]
  draw_graph(t)
  p[0] = parent

def p_declaration_list(p):
  '''declaration_list   : declaration
                        | declaration_list declaration
                        '''
  parent = add_node("declaration_list")
  if len(p) == 2:
    t = [parent,p[1]]
  else:
    t = [parent,p[1],p[2]]
  draw_graph(t)
  p[0] = parent

def p_statement_list(p):
  '''statement_list   : statement
                      | statement_list statement
                      '''
  parent = add_node("statement_list")
  if len(p) == 2:
    t = [parent,p[1]]
  else:
    t = [parent,p[1],p[2]]
  draw_graph(t)
  p[0] = parent

def p_expression_statement(p):
  '''expression_statement   : ';'
                            | expression ';'
                            '''
  parent = add_node("expression_statement")
  if len(p) == 2 :
    c1 = add_node(str(p[1]))
    t = [parent,c1]
  else :
    c1 = add_node(str(p[2]))
    t = [parent,p[1],c1]
  draw_graph(t)
  p[0] = parent

def p_selection_statement(p):
  '''selection_statement  : IF '(' expression ')' statement
                          | IF '(' expression ')' statement ELSE statement
                          | SWITCH '(' expression ')' statement
                          '''
  parent = add_node("selection_statement")
  if len(p) == 6:
    c1 = add_node(str(p[1]))
    c2 = add_node(str(p[2]))
    c3 = add_node(str(p[4]))
    t = [parent,c1,c2,p[3],c3,p[5]]
  else:
    c1 = add_node(str(p[1]))
    c2 = add_node(str(p[2]))
    c3 = add_node(str(p[4]))
    c4 = add_node(str(p[6]))
    t = [parent,c1,c2,p[3],c3,p[5],c4,p[7]]
  draw_graph(t)
  p[0] = parent

def p_iteration_statement(p):
  '''iteration_statement  : WHILE '(' expression ')' statement
                          | DO statement WHILE '(' expression ')' ';'
                          '''
  parent = add_node("iteration_statement")
  if len(p) == 6:
    c1 = add_node(str(p[1]))
    c2 = add_node(str(p[2]))
    c3 = add_node(str(p[4]))
    t = [parent,c1,c2,p[3],c3,p[5]]
  else:
    c1 = add_node(str(p[1]))
    c2 = add_node(str(p[3]))
    c3 = add_node(str(p[4]))
    c4 = add_node(str(p[6]))
    c5 = add_node(str(p[7]))
    t = [parent,c1,p[2],c2,c3,p[5],c4,c5]
  draw_graph(t)
  p[0] = parent

def p_iteration_statement_1(p):
  '''iteration_statement_1  : FOR '(' expression_statement expression_statement ')' statement
                            | FOR '(' expression_statement expression_statement expression ')' statement
                            '''
  parent = add_node("iteration_statement_1")
  if len(p) == 7:
    c1 = add_node(str(p[1]))
    c2 = add_node(str(p[2]))
    c3 = add_node(str(p[5]))
    t = [parent,c1,c2,p[3],p[4],c3,p[6]]
  else:
    c1 = add_node(str(p[1]))
    c2 = add_node(str(p[2]))
    c3 = add_node(str(p[6]))
    t = [parent,c1,c2,p[3],p[4],p[5],c3,p[7]]
  draw_graph(t)
  p[0] = parent

def p_jump_statement(p):
  '''jump_statement   : GOTO IDENTIFIER ';'
                      | CONTINUE ';'
                      | BREAK ';'
                      | RETURN ';'
                      '''
  parent = add_node("jump_statement")
  if len(p) == 3:
    c1 = add_node(str(p[1]))
    c2 = add_node(str(p[2]))
    t = [parent,c1,c2]
  else:
    c1 = add_node(str(p[1]))
    c2 = add_node(str(p[2]))
    c2 = add_node(str(p[3]))
    t = [parent,c1,c2,c3]
  draw_graph(t)
  p[0] = parent

def p_jump_statement_1(p):
  '''jump_statement_1   : RETURN expression ';' 
                        '''
  parent = add_node("jump_statement_1")
  c1 = add_node(str(p[1]))
  c2 = add_node(str(p[3]))
  t = [parent,c1,p[2],c2]
  draw_graph(t)
  p[0] = parent

def p_translation_unit(p):
  '''translation_unit   : external_declaration
                        | translation_unit external_declaration
                        '''
  parent = add_node("translation_unit")
  if len(p) == 2:
    t = [parent,p[1]]
  else:
    t = [parent,p[1],p[2]]
  draw_graph(t)
  p[0] = parent

def p_external_declaration(p):
  '''external_declaration   : function_definition
                            | declaration
                            '''
  parent = add_node("external_declaration")
  t = [parent,p[1]]
  draw_graph(t)
  p[0] = parent

def p_function_definition(p):
  '''function_definition  : declaration_specifiers declarator declaration_list compound_statement
                          | declaration_specifiers declarator compound_statement
                          | declarator declaration_list compound_statement
                          | declarator compound_statement
                          '''
  parent = add_node("function_definition")
  if len(p) == 3:
    t = [parent,p[1],p[2]]
  elif len(p) == 4:
    t = [parent,p[1],p[2],p[3]]
  else:
    t = [parent,p[1],p[2],p[3],p[4]]
  draw_graph(t)
  p[0] = parent


def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

if len(sys.argv) >= 2:
  fd = sys.argv[1]
  if len(sys.argv) == 3 :
    fd_2 = "../test/" + sys.argv[2]
  else : 
    fd_2 = "../test/graph.png"
  yacc.yacc( start='translation_unit')
  with open (fd, "r") as myfile:
    data=myfile.read()
  print("File read complete")
  yacc.parse(data)
  print ("Parsed successfully, writing graph to" + fd_2)
  graph.write_png(fd_2)
  print ("Write successful")
else :
  print("Please provide file to be parsed")