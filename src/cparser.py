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
                          | constant
                          | string
                          | '(' expression ')'
                          | generic_selection
                          '''
def p_constant(p):
  '''constant             : ICONST
                          | FCONST
                          | CCONST
                          '''
def p_string(p):
  '''string               : STRING_LITERAL
                          | FUNC_NAME
                           '''
def p_generic_selection(p):
  '''generic_selection    :  GENERIC '(' assignment_expression ',' generic_assoc_list ')'
                          '''
          
def p_generic_assoc_list(p):
  '''generic_assoc_list   : generic_association
                          | generic_assoc_list ',' generic_association
                          '''
def p_generic_association(p):
  '''generic_association  : type_name ':' assignment_expression
                          | DEFAULT ':' assignment_expression
                          '''
def p_postfix_expression(p):
  '''postfix_expression   : primary_expression
                          | postfix_expression '[' expression ']'
                          | postfix_expression '(' ')'
                          | postfix_expression '(' argument_expression_list ')'
                          | postfix_expression '.' IDENTIFIER
                          | postfix_expression PTR_OP IDENTIFIER
                          | postfix_expression INC_OP
                          | postfix_expression DEC_OP
                          | '(' type_name ')' '{' initializer_list '}'
                          | '(' type_name ')' '{' initializer_list ',' '}'
                          '''

def p_argument_expression_list(p):
  '''argument_expression_list   : assignment_expression
                                | argument_expression_list ',' assignment_expression
                                '''

def p_unary_expression(p):
  '''unary_expression   : postfix_expression
                        | INC_OP unary_expression
                        | DEC_OP unary_expression
                        | unary_operator cast_expression
                        | SIZEOF '(' unary_expression ')'
                        | SIZEOF '(' struct_or_union_specifier ')'
                        | ALIGNOF '(' type_name ')'
                        '''

def p_unary_operator(p):
  '''unary_operator : '&'
                    | '*'
                    | '+'
                    | '-'
                    | '~'
                    | '!'
                    '''

def p_cast_expression(p):
  '''cast_expression  : unary_expression
                      | '(' type_name ')' cast_expression
                      '''
 
def p_multiplicative_expression(p):
  '''multiplicative_expression  : cast_expression
                                | multiplicative_expression '*' cast_expression
                                | multiplicative_expression '/' cast_expression
                                | multiplicative_expression '%' cast_expression
                                '''

def p_additive_expression(p):
  '''additive_expression  : multiplicative_expression
                          | additive_expression '+' multiplicative_expression
                          | additive_expression '-' multiplicative_expression
                          '''
  
def p_shift_expression(p):
  '''shift_expression   : additive_expression
                        | shift_expression LEFT_OP additive_expression
                        | shift_expression RIGHT_OP additive_expression
                        '''
  
def p_relational_expression(p):
  '''relational_expression  : shift_expression
                            | relational_expression '<' shift_expression
                            | relational_expression '>' shift_expression
                            | relational_expression LE_OP shift_expression
                            | relational_expression GE_OP shift_expression
                            '''

def p_equality_expression(p):
  '''equality_expression  : relational_expression
                          | equality_expression EQ_OP relational_expression
                          | equality_expression NE_OP relational_expression
                          '''

def p_and_expression(p):
  '''and_expression   : equality_expression
                      | and_expression '&' equality_expression
                      '''

def p_exclusive_or_expression(p):
  '''exclusive_or_expression  : and_expression
                              | exclusive_or_expression '^' and_expression
                              '''

def p_inclusive_or_expression(p):
  '''inclusive_or_expression  : exclusive_or_expression
                              | inclusive_or_expression '|' exclusive_or_expression
                              '''
  

def p_logical_and_expression(p):
  '''logical_and_expression   : inclusive_or_expression
                              | logical_and_expression AND_OP inclusive_or_expression
                              '''
  
def p_logical_or_expression(p):
  '''logical_or_expression  : logical_and_expression
                            | logical_or_expression OR_OP logical_and_expression
                            '''

def p_conditional_expression(p):
  '''conditional_expression   : logical_or_expression
                              | logical_or_expression '?' expression ':' conditional_expression
                              '''

def p_assignment_expression(p):
  '''assignment_expression  : conditional_expression
                            | unary_expression assignment_operator assignment_expression
                            '''
  
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

def p_expression(p):
  '''expression   : assignment_expression
                  | expression ',' assignment_expression
                  '''

def p_constant_expression(p):
  '''constant_expression  : conditional_expression
                          '''
 
def p_declaration(p):
  '''declaration  : declaration_specifiers ';'
                  | declaration_specifiers init_declarator_list ';'
                  | static_assert_declaration
                  '''
 
def p_declaration_specifiers(p):
  '''declaration_specifiers   : storage_class_specifier
                              | storage_class_specifier declaration_specifiers
                              | type_specifier
                              | type_specifier declaration_specifiers
                              | type_qualifier
                              | type_qualifier declaration_specifiers
                              | function_specifier declaration_specifiers
                              | function_specifier
                              | alignment_specifier declaration_specifiers
                              | alignment_specifier
                              '''
 
def p_init_declarator_list(p):
  '''init_declarator_list   : init_declarator
                            | init_declarator_list ',' init_declarator
                            '''

def p_init_declarator(p):
  '''init_declarator  : declarator
                      | declarator '=' initializer
                      '''

def p_storage_class_specifier(p):
  '''storage_class_specifier  : TYPEDEF
                              | EXTERN
                              | STATIC
                              | AUTO
                              | REGISTER
                              '''
 
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
                      | COMPLEX
                      | IMAGINARY
                      | struct_or_union_specifier
                      | enum_specifier
                      '''
def p_struct_or_union_specifier(p):
  '''struct_or_union_specifier  : struct_or_union IDENTIFIER '{' struct_declaration_list '}'
                                | struct_or_union '{' struct_declaration_list '}'
                                | struct_or_union IDENTIFIER
                                '''
 

def p_struct_or_union_(p):
  '''struct_or_union  : STRUCT
                      | UNION
                      '''


def p_struct_declaration_list(p):
  '''struct_declaration_list  : struct_declaration
                              | struct_declaration_list struct_declaration
                              '''
 
def p_struct_declaration(p):
  '''struct_declaration   : specifier_qualifier_list ';'
                          | specifier_qualifier_list struct_declarator_list ';' 
                          | static_assert_declaration  
                          '''
 

def p_specifier_qualifier_list(p):
  '''specifier_qualifier_list   : type_specifier specifier_qualifier_list
                                | type_specifier
                                | type_qualifier specifier_qualifier_list
                                | type_qualifier
                                '''

def p_struct_declarator_list(p):
  '''struct_declarator_list   : struct_declarator
                              | struct_declarator_list ',' struct_declarator
                              '''
 

def p_struct_declarator(p):
  '''struct_declarator  : declarator
                        | ':' constant_expression
                        | declarator ':' constant_expression
                        '''
 
def p_enum_specifier(p):
  '''enum_specifier     : ENUM '{' enumerator_list '}'
                        | ENUM '{' enumerator_list ',' '}'
                        | ENUM IDENTIFIER '{' enumerator_list '}'
                        | ENUM IDENTIFIER '{' enumerator_list ',' '}'
                        | ENUM IDENTIFIER
                        '''


def p_enumerator_list(p):
  '''enumerator_list  : enumerator
                      | enumerator_list ',' enumerator
                      '''

def p_enumerator(p):
  '''enumerator   : IDENTIFIER
                  | IDENTIFIER '=' constant_expression
                  '''

def p_type_qualifier(p):
  '''type_qualifier   : CONST
                      | VOLATILE
                      | RESTRICT
                      '''
def p_function_specifier(p):
  '''function_specifier   : INLINE
                          | NORETURN
                          '''
def p_alignment_specifier(p):
  '''alignment_specifier   : ALIGNAS '(' type_name ')'
                          | ALIGNAS '(' constant_expression ')'
                          '''
def p_declarator(p):
  '''declarator   : pointer direct_declarator
                  | direct_declarator
                  '''


def p_direct_declarator(p):
  '''direct_declarator  : IDENTIFIER
                        | '(' declarator ')'
                        | direct_declarator '[' ']'
                        | direct_declarator '[' '*' ']'
                        | direct_declarator '[' STATIC type_qualifier_list assignment_expression ']'
                        | direct_declarator '[' STATIC assignment_expression ']'
                        | direct_declarator '[' type_qualifier_list '*' ']'
                        | direct_declarator '[' type_qualifier_list STATIC assignment_expression ']'
                        | direct_declarator '[' type_qualifier_list assignment_expression ']'
                        | direct_declarator '[' type_qualifier_list ']'
                        | direct_declarator '[' assignment_expression ']'
                        | direct_declarator '(' parameter_type_list ')'
                        | direct_declarator '(' ')'
                        | direct_declarator '(' identifier_list ')'
                        '''
 

def p_pointer(p):
  '''pointer  : '*'
              | '*' type_qualifier_list
              | '*' pointer
              | '*' type_qualifier_list pointer
              '''

def p_type_qualifier_list(p):
  '''type_qualifier_list  : type_qualifier
                          | type_qualifier_list type_qualifier
                          '''

def p_parameter_type_list(p):
  '''parameter_type_list  : parameter_list
                          | parameter_list ',' ELLIPSIS
                          '''

def p_parameter_list(p):
  '''parameter_list   : parameter_declaration
                      | parameter_list ',' parameter_declaration
                      '''

def p_parameter_declaration(p):
  '''parameter_declaration  : declaration_specifiers declarator
                            | declaration_specifiers abstract_declarator
                            | declaration_specifiers
                            '''

def p_identifier_list(p):
  '''identifier_list  : IDENTIFIER
                      | identifier_list ',' IDENTIFIER
                      '''

def p_type_name(p):
  '''type_name        : specifier_qualifier_list abstract_declarator
                      | specifier_qualifier_list
                      '''

def p_abstract_declarator(p):
  '''abstract_declarator  : pointer
                          | direct_abstract_declarator
                          | pointer direct_abstract_declarator
                          '''


def p_direct_abstract_declarator(p):
  '''direct_abstract_declarator   : '(' abstract_declarator ')'
                                  | '[' ']'
                                  | '[' '*' ']'
                                  | '[' STATIC type_qualifier_list assignment_expression ']'
                                  | '[' STATIC assignment_expression ']'
                                  | '[' type_qualifier_list STATIC assignment_expression ']'
                                  | '[' type_qualifier_list assignment_expression ']'
                                  | '[' type_qualifier_list ']'
                                  | '[' assignment_expression ']'
                                  | direct_abstract_declarator '[' ']'
                                  | direct_abstract_declarator '[' '*' ']'
                                  | direct_abstract_declarator '[' STATIC type_qualifier_list assignment_expression ']'
                                  | direct_abstract_declarator '[' STATIC assignment_expression ']'
                                  | direct_abstract_declarator '[' type_qualifier_list assignment_expression ']'
                                  | direct_abstract_declarator '[' type_qualifier_list STATIC assignment_expression ']'
                                  | direct_abstract_declarator '[' type_qualifier_list ']'
                                  | direct_abstract_declarator '[' assignment_expression ']'
                                  | '(' ')'
                                  | '(' parameter_type_list ')'
                                  | direct_abstract_declarator '(' ')'
                                  | direct_abstract_declarator '(' parameter_type_list ')'
                                  '''

def p_initializer(p):
  '''initializer  : assignment_expression
                  | '{' initializer_list '}'
                  | '{' initializer_list ',' '}'
                  '''

def p_initializer_list(p):
  '''initializer_list   : initializer
                        | initializer_list ',' initializer
                        | designation initializer
                        | initializer_list ',' designation initializer
                        '''
def p_designation(p):
  '''designation   : designator_list '='
                        ''' 

def p_designator_list(p):
  '''designator_list    : designator
                        | designator_list designator
                        ''' 
def p_designator(p):
  '''designator    : '[' constant_expression ']'
                   | '.' IDENTIFIER
                  ''' 
def p_static_assert_declaration(p):
  '''static_assert_declaration    : STATIC_ASSERT '(' constant_expression ',' STRING_LITERAL ')' ';'
                                  ''' 

def p_statement(p):
  '''statement    : labeled_statement
                  | compound_statement
                  | expression_statement
                  | selection_statement
                  | iteration_statement
                  | jump_statement
                  '''

def p_labeled_statement(p):
  '''labeled_statement  : IDENTIFIER ':' statement
                        | CASE constant_expression ':' statement
                        | DEFAULT ':' statement
                        '''

def p_compound_statement(p):
  '''compound_statement   : '{' '}'
                          | '{'  block_item_list '}'
                          '''

def p_block_item_list(p):
  '''block_item_list    : block_item
                        | block_item_list block_item
                          '''
def p_block_item(p):
  '''block_item     : declaration
                    | statement
                    '''

def p_expression_statement(p):
  '''expression_statement   : ';'
                            | expression ';'
                            '''

def p_selection_statement(p):
  '''selection_statement  : IF '(' expression ')' statement
                          | IF '(' expression ')' statement ELSE statement
                          | SWITCH '(' expression ')' statement
                          '''

def p_iteration_statement(p):
  '''iteration_statement  : WHILE '(' expression ')' statement
                          | DO statement WHILE '(' expression ')' ';'
                          | FOR '(' expression_statement expression_statement ')' statement
                          | FOR '(' expression_statement expression_statement expression ')' statement
                          | FOR '(' declaration expression_statement ')' statement
                          | FOR '(' declaration expression_statement expression ')' statement
                          '''

def p_jump_statement(p):
  '''jump_statement   : GOTO IDENTIFIER ';'
                      | CONTINUE ';'
                      | BREAK ';'
                      | RETURN ';'
                      | RETURN expression ';'
                      '''

def p_translation_unit(p):
  '''translation_unit   : external_declaration
                        | translation_unit external_declaration
                        '''

def p_external_declaration(p):
  '''external_declaration   : function_definition
                            | declaration
                            '''

def p_function_definition(p):
  '''function_definition  : declaration_specifiers declarator declaration_list compound_statement
                          | declaration_specifiers declarator compound_statement
                          '''
def p_declaration_list(p):
  '''declaration_list   : declaration_list declaration
                        | declaration
                        '''
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
  yacc.yacc( start='translation_unit')
  yacc.parse("");
  print("Please provide file to be parsed")