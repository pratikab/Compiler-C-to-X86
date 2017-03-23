import ply.yacc as yacc
from lexer import *
import ply.lex as lex
import sys
lex.lex()

import pydot
graph = pydot.Dot(graph_type='graph')

# Symbol Table is a list of hash tables
symbol_table = []
symbol_table.append({})
scope_level = 0

def add_edge(node_parent,node_child):
  graph.add_edge(pydot.Edge(node_parent, node_child))

k = 0
def add_node(p):
  global k
  node = pydot.Node(k,label = p)
  graph.add_node(node)
  k = k + 1
  return node

class ast_node(object):
  def __init__(self, name="", value="", type="", children="", modifiers="", dims=0, arraylen="", sym_entry="", lineno=0,tag = "",pydot_Node = None):
    self.name = name
    self.value = value
    self.type = type
    self.dims = dims
    self.lineno = lineno
    self.sym_entry = sym_entry
    self.pydot_Node = None
    if modifiers:
        self.modifiers = modifiers
    else:
        self.modifiers = [ ]
    if children :
      self.children = children
    else:
      self.children = [ ]
    if arraylen:
      self.arraylen = arraylen
    else:
      self.arraylen = [ ]
  def print_tree(self,depth):
    output = ""
    if self.name is not "":
      for i in range(0,depth-1):
        print "-",
      print "+",
      depth = depth + 1
      output = self.name + " " + self.type+" "+str(self.value)
      print (output)
    self.pydot_Node = add_node(output)
    if len(self.children) > 0 :
      for child in self.children : 
        child.print_tree(depth)
        add_edge(self.pydot_Node,child.pydot_Node)

  def set_type(self,t):
    self.type = t
    if len(self.children) > 0 :
      for child in self.children : 
        child.set_type(t)

start = ast_node("START",value = "",type ="" ,children = [])
def p_primary_expression(p):
  '''primary_expression   : identifier
                          '''
  # found = False
  # for i in range(0,scope_level+1):
  #   if p[1].value in symbol_table[scope_level].keys():
  #     found = True
  #     print symbol_table
  #     break
  # if found == False:
  #   print "COMPILATION ERROR: Trying to access undeclared variable " + p[1].value
  #   print symbol_table
  #   sys.exit()
  p[0] = ast_node("VarAccess",value = p[1].value,type ="",children = [])
def p_primary_expression_1(p):
  '''primary_expression   : constant
                          '''
  p[0] = p[1]
def p_primary_expression_2(p):
  '''primary_expression   : string
                          '''
  p[0] = p[1]
def p_primary_expression_3(p):
  '''primary_expression   : '(' expression ')'
                          '''
  p[0] = p[2]
def p_identifier(p):
  '''identifier   : IDENTIFIER
                   '''
  p[0] = ast_node("",value = p[1],type ="",children = []) 
def p_constant(p):
  '''constant             : ICONST
                          '''
  p[0] = ast_node("ConstantLiteral",value = p[1],type ="int",children = [])  
def p_constant_1(p):
  '''constant             : FCONST
                          '''
  p[0] = ast_node("ConstantLiteral",value = p[1],type ="float",children = [])  
def p_constant_2(p):
  '''constant             : CCONST
                          '''
  p[0] = ast_node("ConstantLiteral",value = p[1],type ="char",children = [])  

def p_string(p):
  '''string               : STRING_LITERAL
                           '''
  p[0] = ast_node("StringLiteral",value = p[1],type ="string",children = [])  

def p_postfix_expression(p):
  '''postfix_expression   : primary_expression
                          '''
  p[0] = p[1]

def p_postfix_expression_1(p):
  '''postfix_expression   : postfix_expression '[' expression ']'
                          '''
  p[0] = ast_node("ArrayAccess",value = p[1].value,type =p[1].type,arraylen = p[3].value,children = [p[1],p[3]])  

def p_postfix_expression_2(p):
  '''postfix_expression   : postfix_expression '(' ')'
                          '''                          
  p[0] = ast_node("FuncCall",value = p[1].value,type = p[1].type,children =[p[1]])                          
def p_postfix_expression_3(p):
  '''postfix_expression   : postfix_expression '(' argument_expression_list ')'
                          '''
  p[0] = ast_node("FuncCallwithArgs",value = p[1].value,type = p[1].type,children =[p[1],p[3]])  
def p_postfix_expression_4(p):
  '''postfix_expression   : postfix_expression '.' identifier
                          | postfix_expression PTR_OP identifier
                          '''
  p[0] = ast_node("StructReference",value = p[1].value,type = p[3].value,children =[p[1]])                          
def p_postfix_expression_5(p):
  '''postfix_expression   : postfix_expression INC_OP
                          | postfix_expression DEC_OP
                         '''
  p[0] = ast_node("UnaryOperator",value = p[1].value, type = p[1].type, children =[p[1]])
def p_postfix_expression_6(p):
  '''postfix_expression   : '(' type_name ')' '{' initializer_list '}'
                          | '(' type_name ')' '{' initializer_list ',' '}'
                          '''
  p[0] = ast_node("Compound Literal")
def p_argument_expression_list(p):
  '''argument_expression_list   : assignment_expression
                                | argument_expression_list ',' assignment_expression
                                '''
  if len(p) == 2:
    p[0] = ast_node('Argument List',value = '', type = p[1].type, children = [p[1]])
  else:
    if p[1].name != 'Argument List':
      p[1] = ast_node('Argument List',value = '', type = p[3].type, children = [])
    p[1].children.append(p[3])
    p[0] = p[1] 
def p_unary_expression(p):
  '''unary_expression   : postfix_expression
                        '''
  p[0] = p[1]

def p_unary_expression_1(p):
  '''unary_expression   : INC_OP unary_expression
                        | DEC_OP unary_expression
                        | unary_operator cast_expression
                        '''
  p[0] = ast_node("Unary Operator",value = p[2].value, type = p[2].type, children =[p[2]])

def p_unary_expression_3(p):
  '''unary_expression   : SIZEOF '(' unary_expression ')'
                        | SIZEOF '(' struct_or_union_specifier ')'
                        '''
  p[0] = ast_node("Size Of", value = p[3].value, type = p[3].type, children =[p[3]])  

def p_unary_operator(p):
  '''unary_operator : '&'
                    | '*'
                    | '+'
                    | '-'
                    | '~'
                    | '!'
                    '''
  p[0] = p[1]
def p_cast_expression(p):
  '''cast_expression  : unary_expression
                      | '(' type_name ')' cast_expression
                      '''
  if len(p) == 2:
    p[0] = p[1]
  else: 
    p[0] = ast_node("Type Cast", value = p[2].value, type = p[2].type, children =[p[2],p[4]])

def p_multiplicative_expression(p):
  '''multiplicative_expression  : cast_expression
                                | multiplicative_expression '*' cast_expression
                                | multiplicative_expression '/' cast_expression
                                | multiplicative_expression '%' cast_expression
                                '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    p[0] = ast_node("Multiplication", value = "", type = '', children =[p[1],p[3]])                      

def p_additive_expression(p):
  '''additive_expression  : multiplicative_expression
                          | additive_expression '+' multiplicative_expression
                          | additive_expression '-' multiplicative_expression
                          '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    p[0] = ast_node("Addition", value = "", type = '', children =[p[1],p[3]])
  
def p_shift_expression(p):
  '''shift_expression   : additive_expression
                        | shift_expression LEFT_OP additive_expression
                        | shift_expression RIGHT_OP additive_expression
                        '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    p[0] = ast_node("Shift", value = "", type = '', children =[p[1],p[3]])
  
def p_relational_expression(p):
  '''relational_expression  : shift_expression
                            | relational_expression '<' shift_expression
                            | relational_expression '>' shift_expression
                            | relational_expression LE_OP shift_expression
                            | relational_expression GE_OP shift_expression
                            '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    p[0] = ast_node("Relation", value = "", type = '', children =[p[1],p[3]])

def p_equality_expression(p):
  '''equality_expression  : relational_expression
                          | equality_expression EQ_OP relational_expression
                          | equality_expression NE_OP relational_expression
                          '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    p[0] = ast_node("EqualityExpression", value = "", type = '', children =[p[1],p[3]])

def p_and_expression(p):
  '''and_expression   : equality_expression
                      | and_expression '&' equality_expression
                      '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    p[0] = ast_node("AND", value = "", type = '', children =[p[1],p[3]])

def p_exclusive_or_expression(p):
  '''exclusive_or_expression  : and_expression
                              | exclusive_or_expression '^' and_expression
                              '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    p[0] = ast_node("Exclusive OR", value = "", type = '', children =[p[1],p[3]])

def p_inclusive_or_expression(p):
  '''inclusive_or_expression  : exclusive_or_expression
                              | inclusive_or_expression '|' exclusive_or_expression
                              '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    p[0] = ast_node("Inclusive OR", value = "", type = '', children =[p[1],p[3]])
  

def p_logical_and_expression(p):
  '''logical_and_expression   : inclusive_or_expression
                              | logical_and_expression AND_OP inclusive_or_expression
                              '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    p[0] = ast_node("Logical AND", value = "", type = '', children =[p[1],p[3]])
  
def p_logical_or_expression(p):
  '''logical_or_expression  : logical_and_expression
                            | logical_or_expression OR_OP logical_and_expression
                            '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    p[0] = ast_node("Logical OR", value = "", type = '', children =[p[1],p[3]])

def p_conditional_expression(p):
  '''conditional_expression   : logical_or_expression
                              | logical_or_expression '?' expression ':' conditional_expression
                                '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    p[0] = ast_node("Ternary Operation", value = "", type = '', children =[p[1],p[3],p[5]])

def p_assignment_expression(p):
  '''assignment_expression  : conditional_expression
                            | unary_expression assignment_operator assignment_expression
                            '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    p[0] = ast_node("Assignment", value = "", type = p[1].type, children =[p[1],p[3]])
  
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
  p[0] = p[1]

def p_expression(p):
  '''expression   : assignment_expression
                  | expression ',' assignment_expression
                  '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    p[0] = p[1]
    p[0].children.append(p[3])
def p_constant_expression(p):
  '''constant_expression  : conditional_expression
                          '''
  p[0] = p[1] 
def p_declaration(p):
  '''declaration  : declaration_specifiers ';'
                  | declaration_specifiers init_declarator_list ';'
                  | static_assert_declaration
                  '''
  if len(p) == 2:
    p[0] = p[1]
  elif len(p) == 4:
    temp = p[1].type + " "+ p[2].type
    p[0] = ast_node("Declaration Statement",value = "",type =temp,children = [p[1],p[2]])
    p[0].set_type(temp)
  else:
    p[0] = p[1]

def p_declaration_specifiers(p):
  '''declaration_specifiers   : storage_class_specifier
                              | storage_class_specifier declaration_specifiers
                              | type_specifier
                              | type_specifier declaration_specifiers
                              | type_qualifier
                              | type_qualifier declaration_specifiers
                              '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    temp = p[1].type + " " + p[2].type
    p[0] = ast_node("Declaration Specifier",value = p[1].value,type =temp,children = [p[1],p[2]])

def p_init_declarator_list(p):
  '''init_declarator_list   : init_declarator
                            | init_declarator_list ',' init_declarator
                            '''
  if len(p) == 2:
    p[0] = ast_node('Initializer List',value = '', type = p[1].type, children = [p[1]])
  else:
    if p[1].name != 'Initializer List':
      p[1] = ast_node('Initializer List',value = '', type = p[3].type, children = [])
    p[1].children.append(p[3])
    p[0] = p[1] 
def p_init_declarator(p):
  '''init_declarator  : declarator
                      | declarator '=' initializer
                      '''
  # global scope_level
  # global symbol_table
  # if p[1].value in symbol_table[scope_level].keys():
  #   print "COMPILATION ERROR : Variable " + p[1].value + " already declared"
  #   print symbol_table
  #   sys.exit()
  # else:
  #   symbol_table[scope_level][p[1].value] = p[1].type
  if len(p) == 2:
    p[0] = ast_node("VarDecl", value = p[1].value,type =p[1].type,children = [p[1]])
  else:
    p[0] = ast_node("VarDecl and Initialise",value = (p[1].value + "=" +p[3].value),type =p[1].type,children = [p[1],p[3]])  
def p_storage_class_specifier(p):
  '''storage_class_specifier  : TYPEDEF
                              | EXTERN
                              | STATIC
                              | AUTO
                              | REGISTER
                              '''
  p[0] = ast_node("Storage Specifier",value = "",type =p[1],children = []) 
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
                      '''
  p[0] = ast_node("",value = "",type =p[1],children = [])

def p_type_specifier_1(p):
  '''type_specifier   : struct_or_union_specifier
                      | enum_specifier
                      '''
  p[0] = ast_node("",value = p[1].value,type =p[1].type,children = [p[1]])

def p_struct_or_union_specifier(p):
  '''struct_or_union_specifier  : struct_or_union identifier '{' struct_declaration_list '}'
                                '''
  p[0] = ast_node("Struct Declaration",value = "",type =(p[1]+" "+p[2].value),children = [p[4]])

def p_struct_or_union_specifier_1(p):
  '''struct_or_union_specifier  : struct_or_union '{' struct_declaration_list '}'
                                '''
  p[0] = ast_node("Struct Declaration",value = "",type =(p[1]),children = [p[3]])

def p_struct_or_union_specifier_2(p):
  '''struct_or_union_specifier  : struct_or_union identifier
                                '''
  p[0] = ast_node("Struct Declaration",value = "",type =(p[1]+" "+p[2].value),children = [])

def p_struct_or_union_(p):
  '''struct_or_union  : STRUCT
                      | UNION
                      '''
  p[0] = p[1]


def p_struct_declaration_list(p):
  '''struct_declaration_list  : struct_declaration
                              | struct_declaration_list struct_declaration
                              '''
  if len(p) == 2:
    p[0] = ast_node('struct_declaration_list',value = '', type = p[1].type, children = [p[1]])
  else:
    if p[1].name != 'struct_declaration_list':
      p[1] = ast_node('struct_declaration_list',value = '', type = p[3].type, children = [])
    p[1].children.append(p[2])
    p[0] = p[1] 

def p_struct_declaration(p):
  '''struct_declaration   : specifier_qualifier_list ';'
                          | specifier_qualifier_list struct_declarator_list ';' 
                          | static_assert_declaration  
                          '''
  if len(p) == 2:
    p[0] = p[1]
  elif len(p) == 4:
    p[0] = ast_node("struct declarations",value = "",type =p[1].type ,children = [p[1],p[2]])
    #p[0].set_type(p[1].type)
  else:
    p[0] = p[1]
def p_specifier_qualifier_list(p):
  '''specifier_qualifier_list   : type_specifier specifier_qualifier_list
                                | type_specifier
                                | type_qualifier specifier_qualifier_list
                                | type_qualifier
                                '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    temp = p[1].type + " " + p[2].type
    p[0] = ast_node("Declaration Specifier",value = p[1].value,type = temp ,children = [p[1],p[2]])

def p_struct_declarator_list(p):
  '''struct_declarator_list   : struct_declarator
                              | struct_declarator_list ',' struct_declarator
                              '''
  if len(p) == 2:
    p[0] = ast_node('struct_declarator_list',value = '', type = p[1].type, children = [p[1]])
  else:
    if p[1].name != 'struct_declarator_list':
      p[1] = ast_node('struct_declarator_list',value = '', type = p[3].type, children = [])
    p[1].children.append(p[3])
    p[0] = p[1] 
def p_struct_declarator(p):
  '''struct_declarator  : declarator
                        | ':' constant_expression
                        | declarator ':' constant_expression
                        '''
  if len(p) == 2:
    p[0] = p[1]
  elif len(p) == 3:
    pass
  else: 
    pass
def p_enum_specifier(p):
  '''enum_specifier     : ENUM '{' enumerator_list '}'
                        '''
def p_enum_specifier_1(p):
  '''enum_specifier     : ENUM '{' enumerator_list ',' '}'
                        '''
def p_enum_specifier_2(p):
  '''enum_specifier     : ENUM identifier '{' enumerator_list '}'
                        '''
def p_enum_specifier_3(p):
  '''enum_specifier     : ENUM identifier '{' enumerator_list ',' '}'
                       '''
def p_enum_specifier_4(p):
  '''enum_specifier     : ENUM identifier
                        '''
def p_enumerator_list(p):
  '''enumerator_list  : enumerator
                      | enumerator_list ',' enumerator
                      '''
  if len(p) == 2:
    p[0] = p[1]
  else: 
    pass
def p_enumerator(p):
  '''enumerator   : identifier
                  | identifier '=' constant_expression
                  '''
  if len(p) == 2:
    p[0] = p[1]
  else: 
    pass
def p_type_qualifier(p):
  '''type_qualifier   : CONST
                      | VOLATILE
                      | RESTRICT
                      '''
  p[0] = ast_node("Qualifier Declaration",value = "",type =p[1],children = [])  

def p_declarator(p):
  '''declarator   : pointer direct_declarator
                  | direct_declarator
                  '''
  if len(p) == 2:
    p[0] = p[1]
  else: 
    p[0] = ast_node("PointerDeclaration",value = p[2].value,type =p[1].type+p[2].type,children = [])                

def p_direct_declarator(p):
  '''direct_declarator  : identifier
                        '''
  p[0] = p[1]
def p_direct_declarator_1(p):
  '''direct_declarator  : '(' declarator ')'
                        '''
  p[0] = p[2]
def p_direct_declarator_2(p):
  '''direct_declarator  : direct_declarator '[' ']'
                        '''
  p[0] = ast_node("ArrayIntialize",value = p[1].value,type =p[1].type,arraylen = 0,children = [p[1]]) 
# def p_direct_declarator_3(p):
#   '''direct_declarator  : direct_declarator '[' '*' ']'
#                         '''
#   p[0] = p[1]
# def p_direct_declarator_4(p):
#   '''direct_declarator  : direct_declarator '[' STATIC type_qualifier_list assignment_expression ']'
#                         | direct_declarator '[' STATIC assignment_expression ']'
#                         '''

# def p_direct_declarator_5(p):
#   '''direct_declarator  : direct_declarator '[' type_qualifier_list '*' ']'
#                         '''
# def p_direct_declarator_7(p):
#   '''direct_declarator  : direct_declarator '[' type_qualifier_list STATIC assignment_expression ']'
#                         '''
# def p_direct_declarator_8(p):
#   '''direct_declarator  : direct_declarator '[' type_qualifier_list assignment_expression ']'
#                         '''
# def p_direct_declarator_9(p):
#   '''direct_declarator  : direct_declarator '[' type_qualifier_list ']'
#                        '''
def p_direct_declarator_3(p):
  '''direct_declarator  : direct_declarator '[' assignment_expression ']'
                        '''
  p[0] = ast_node("Array Declaration",value = p[1].value,type ="", arraylen = p[3].value,children = [p[3]]) 
def p_direct_declarator_4(p):
  '''direct_declarator  : direct_declarator '(' parameter_type_list ')'
                        '''
  p[0] = ast_node("Function Arguments",value = p[1].value,type ="",children = [p[1],p[3]])
def p_direct_declarator_5(p):
  '''direct_declarator  : direct_declarator '(' ')'
                        '''
  p[0] = p[1] # blank function declare e.g int main()
def p_direct_declarator_6(p):
  '''direct_declarator  : direct_declarator '(' identifier_list ')'
                        '''
  p[0] = ast_node("Function Arguments",value = p[1].value,type ="",children = [p[1],p[3]])
def p_pointer(p):
  '''pointer  : '*'
              '''
  p[0] = ast_node("",value = "",type =p[1],children = [])
def p_pointer_1(p):
  '''pointer  : '*' type_qualifier_list
              '''
  p[0] = ast_node("",value = "",type =p[1]+" "+p[2].type,children = [])
def p_pointer_2(p):
  '''pointer  : '*' pointer
              '''
  p[0] = ast_node("",value = "",type =p[1]+" "+p[2].type,children = [])
def p_pointer_3(p):
  '''pointer  : '*' type_qualifier_list pointer
              '''
  p[0] = ast_node("",value = "",type =p[1]+" "+p[2].type+p[3].type,children = [])

def p_type_qualifier_list(p):
  '''type_qualifier_list  : type_qualifier
                          | type_qualifier_list type_qualifier
                          '''
  if len(p) == 2:
    p[0] = p[1]
  else: 
    p[0] = p[2]
    p[0].type = p[1].type + " " + p[2].type

def p_parameter_type_list(p):
  '''parameter_type_list  : parameter_list
                          '''
  p[0] = p[1] 
def p_parameter_list(p):
  '''parameter_list   : parameter_declaration
                      | parameter_list ',' parameter_declaration
                      '''
  if len(p) == 2:
    p[0] = ast_node('paramater_list',value = '', type = "", children = [p[1]])
  else:
    if p[1].name != 'paramater_list':
      p[1] = ast_node('paramater_list',value = '', type = "", children = [])
    p[1].children.append(p[3])
    p[0] = p[1]

def p_parameter_declaration(p):
  '''parameter_declaration  : declaration_specifiers declarator
                            '''
  # global scope_level
  # global symbol_table
  # if p[2].value in symbol_table[scope_level].keys():
  #   print "COMPILATION ERROR : Variable " + p[2].value + " already declared"
  #   print symbol_table
  #   sys.exit()
  # else:
  #   symbol_table[scope_level - 1][p[2].value] = p[2].type
  p[0] = ast_node('paramater',value = p[2].value, type = p[1].type, children = [])
def p_parameter_declaration_1(p):
  '''parameter_declaration  : declaration_specifiers abstract_declarator
                            | declaration_specifiers
                            '''
  if len(p) == 2:
    p[0] = p[1]
  else: 
    pass 
def p_identifier_list(p):
  '''identifier_list  : identifier
                      | identifier_list ',' identifier
                      '''
  if len(p) == 2:
    p[0] = ast_node('identifier_list',value = p[1].value, type = "", children = [p[1]])
  else:
    if p[1].name != 'identifier_list':
      p[1] = ast_node('identifier_list',value = "", type = "", children = [])
    p[1].children.append(p[3])
    p[0] = p[1]

def p_type_name(p):
  '''type_name        : specifier_qualifier_list abstract_declarator
                      | specifier_qualifier_list
                      '''
  if len(p) == 2:
    p[0] = p[1]
  else: 
    pass 

def p_abstract_declarator(p):
  '''abstract_declarator  : pointer
                          | direct_abstract_declarator
                          | pointer direct_abstract_declarator
                          '''
  if len(p) == 2:
    p[0] = p[1]
  else: 
    pass 

def p_direct_abstract_declarator(p):
  '''direct_abstract_declarator   : '(' abstract_declarator ')'
                                  '''
def p_direct_abstract_declarator_1(p):
  '''direct_abstract_declarator   : '[' ']'
                                  '''
# def p_direct_abstract_declarator_2(p):
#   '''direct_abstract_declarator   : '[' '*' ']'
#                                   '''
# def p_direct_abstract_declarator_3(p):
#   '''direct_abstract_declarator   : '[' STATIC type_qualifier_list assignment_expression ']'
#                                   '''
# def p_direct_abstract_declarator_4(p):
#   '''direct_abstract_declarator   : '[' STATIC assignment_expression ']'
#                                    '''
# def p_direct_abstract_declarator_5(p):
#   '''direct_abstract_declarator   : '[' type_qualifier_list STATIC assignment_expression ']'
#                                   '''
# def p_direct_abstract_declarator_6(p):
#   '''direct_abstract_declarator   : '[' type_qualifier_list assignment_expression ']'
#                                   '''
# def p_direct_abstract_declarator_7(p):
#   '''direct_abstract_declarator   : '[' type_qualifier_list ']'
#                                   '''
def p_direct_abstract_declarator_2(p):
  '''direct_abstract_declarator   : '[' assignment_expression ']'
                                  '''
def p_direct_abstract_declarator_3(p):
  '''direct_abstract_declarator   : direct_abstract_declarator '[' ']'
                                  '''
# def p_direct_abstract_declarator_4(p):
#    '''direct_abstract_declarator   : direct_abstract_declarator '[' '*' ']'
#                                   '''
# def p_direct_abstract_declarator_11(p):
#   '''direct_abstract_declarator   : direct_abstract_declarator '[' STATIC type_qualifier_list assignment_expression ']'
#                                   '''
# def p_direct_abstract_declarator_12(p):
#   '''direct_abstract_declarator   : direct_abstract_declarator '[' STATIC assignment_expression ']'
#                                   '''
# def p_direct_abstract_declarator_13(p):
#   '''direct_abstract_declarator   : direct_abstract_declarator '[' type_qualifier_list assignment_expression ']'
#                                   '''
# def p_direct_abstract_declarator_14(p):
#   '''direct_abstract_declarator   : direct_abstract_declarator '[' type_qualifier_list STATIC assignment_expression ']'
#                                   '''
# def p_direct_abstract_declarator_15(p):
#   '''direct_abstract_declarator   : direct_abstract_declarator '[' type_qualifier_list ']'
#                                   '''
def p_direct_abstract_declarator_5(p):
  '''direct_abstract_declarator   : direct_abstract_declarator '[' assignment_expression ']'
                                  '''
def p_direct_abstract_declarator_6(p):
  '''direct_abstract_declarator   : '(' ')'
                                  '''
def p_direct_abstract_declarator_7(p):
  '''direct_abstract_declarator   : '(' parameter_type_list ')'
                                  '''
def p_direct_abstract_declarator_8(p):
  '''direct_abstract_declarator   : direct_abstract_declarator '(' ')'
                                  '''
def p_direct_abstract_declarator_9(p):
  '''direct_abstract_declarator   : direct_abstract_declarator '(' parameter_type_list ')'
                                  '''
def p_initializer(p):
  '''initializer  : assignment_expression
                  '''
  p[0] = p[1]
def p_initializer_1(p):
  '''initializer  : '{' initializer_list '}'
                  | '{' initializer_list ',' '}'
                  '''
  p[0] = p[2]
def p_initializer_list(p):
  '''initializer_list   : initializer
                        | initializer_list ',' initializer
                        '''
  if len(p) == 2:
    p[0] = ast_node("Initializer List",value = '',type = p[1].type, children = [p[1]])
  else:
    if p[1].name != 'Initializer List':
      p[1] = ast_node('Initializer List',value = '', type = p[3].type, children = [])
    p[1].children.append(p[3])
    p[0] = p[1] 

def p_initializer_list_2(p):
  '''initializer_list   : designation initializer
                        '''
def p_initializer_list_3(p):
  '''initializer_list   : initializer_list ',' designation initializer
                        '''

def p_designation(p):
  '''designation   : designator_list '='
                  ''' 
def p_designator_list(p):
  '''designator_list    : designator
                        | designator_list designator
                        '''
  if len(p) == 2:
    p[0] = p[1]
  else: 
    pass  
def p_designator(p):
  '''designator    : '[' constant_expression ']'
                   | '.' identifier
                  '''
  if len(p) == 3:
    pass
  else: 
    pass  
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
  p[0] = p[1]

def p_labeled_statement(p):
  '''labeled_statement  : identifier ':' statement
                        '''
  ast_node('Label statement',value = '', type = '', children = [p[3]])
def p_labeled_statement_1(p):
  '''labeled_statement  : CASE constant_expression ':' statement
                        '''
  ast_node('Case statement',value = '', type = '', children = [p[2],p[4]])

def p_labeled_statement_2(p):
  '''labeled_statement  : DEFAULT ':' statement
                        '''
  ast_node('Default statement',value = '', type = '', children = [p[3]])

def p_compound_statement(p):
  '''compound_statement   : '{' '}'
                          | '{'  block_item_list '}'
                          '''
  if len(p) == 3:
    pass  
  else: 
    p[0] = p[2]

def p_block_item_list(p):
  '''block_item_list    : block_item
                        | block_item_list block_item
                          '''
  
  if len(p) == 2:
    p[0] = ast_node("Compound Statement",value = '',type = '', children = [p[1]])
  else:
    if p[1].name != 'Compound Statement':
      p[1] = ast_node('Compound Statement',value = '', type = '', children = [])
    p[1].children.append(p[2])
    p[0] = p[1] 
# todo : Add the concept of 'scope' in each blocks ('{' ... '}')
def p_block_item(p):
  '''block_item     : declaration
                    | statement
                    '''
  p[0] = p[1]
def p_expression_statement(p):
  '''expression_statement   : ';'
                            | expression ';'
                            '''
  if len(p) == 2:
    pass
  else:
    p[0] = p[1]
def p_selection_statement(p):
  '''selection_statement  : IF '(' expression ')' statement
                          '''
  p[0] = ast_node("IF Statement", value = '', type = '', children = [p[3],p[5]])
def p_selection_statement_1(p):
  '''selection_statement  : IF '(' expression ')' statement ELSE statement
                          '''
  p[0] = ast_node("IF-Else Statement", value = '', type = '', children = [p[3],p[5],p[7]])
def p_selection_statement_2(p):
  '''selection_statement  : SWITCH '(' expression ')' statement
                          '''
  p[0] = ast_node("Switch Statement", value = '', type = '', children = [p[3],p[5]])
def p_iteration_statement(p):
  '''iteration_statement  : WHILE '(' expression ')' statement
                          '''
  p[0] = ast_node("While Statement", value = '', type = '', children = [p[3],p[5]])
def p_iteration_statement_1(p):
  '''iteration_statement  : DO statement WHILE '(' expression ')' ';'
                          '''
  p[0] = ast_node("Do-While Statement", value = '', type = '', children = [p[2],p[5]])
def p_iteration_statement_2(p):
  '''iteration_statement  : FOR '(' expression_statement expression_statement ')' statement
                          '''
  p[0] = ast_node("For Statement", value = '', type = '', children = [p[3],p[4],p[6]])
def p_iteration_statement_3(p):
  '''iteration_statement  : FOR '(' expression_statement expression_statement expression ')' statement
                          '''
  p[0] = ast_node("For Statement", value = '', type = '', children = [p[3],p[4],p[5],p[7]])
def p_iteration_statement_4(p):
  '''iteration_statement  : FOR '(' declaration expression_statement ')' statement
                          '''
  p[0] = ast_node("For Statement", value = '', type = '', children = [p[3],p[4],p[6]])                          
def p_iteration_statement_5(p):
  '''iteration_statement  : FOR '(' declaration expression_statement expression ')' statement
                          '''
  p[0] = ast_node("For Statement", value = '', type = '', children = [p[3],p[4],p[5],p[7]])
def p_jump_statement(p):
  '''jump_statement   : GOTO identifier ';'
                      '''
  p[0] = ast_node("Goto", value = p[2].value, type = '', children = [])
def p_jump_statement_1(p):
  '''jump_statement   : CONTINUE ';'
                      '''
  p[0] = ast_node("CONTINUE", value = '', type = '', children = [])
def p_jump_statement_2(p):
  '''jump_statement   : BREAK ';'
                      '''
  p[0] = ast_node("BREAK", value = '', type = '', children = [])
def p_jump_statement_3(p):
  '''jump_statement   : RETURN ';'
                      '''
  p[0] = ast_node("RETURN", value = '', type = '', children = [])
def p_jump_statement_4(p):
  '''jump_statement   : RETURN expression ';'
                      '''
  p[0] = ast_node("RETURN", value = '', type = '', children = [p[2]])
def p_translation_unit(p):
  '''translation_unit   : external_declaration
                        | translation_unit external_declaration
                        '''
  if len(p) == 2:
    start.children.append(p[1])
  else:
    start.children.append(p[2])

def p_external_declaration_1(p):
  '''external_declaration   : function_definition
                            '''
  # global symbol_table
  # global scope_level
  # del symbol_table[scope_level]
  # scope_level = scope_level - 1
  p[0] = p[1]

def p_external_declaration_2(p):
  '''external_declaration   : declaration
                            '''
  p[0] = p[1]

def p_function_definition(p):
  '''function_definition  : declaration_specifiers declarator declaration_list compound_statement
                          | declaration_specifiers declarator compound_statement
                          '''
  # global symbol_table
  # global scope_level
  # # Method names belong in the hashtable for the outermost scope NOT in the same table as the method's variables
  # symbol_table[scope_level][p[2].value] = p[1].type
  # scope_level = scope_level + 1
  # new_hash_table = {}
  # symbol_table.append(new_hash_table)
  if len(p) == 4:
    p[0] = ast_node("Function_definition",value = p[2].value,type =p[1].type ,children = [p[2],p[3]])
  else:
    p[0] = ast_node("Function_definition",value = p[2].value,type =p[1].type ,children = [p[2],p[3],p[4]])
  
def p_declaration_list(p):
  '''declaration_list   : declaration_list declaration
                        | declaration
                        '''
  if len(p) == 2:
    p[0] = ast_node('Declaration List',value = '', type = '', children = [p[1]])
  else:
    if p[1].name != 'Declaration List':
      p[1] = ast_node('Declaration List',value = '', type = '', children = [])
    p[1].children.append(p[2])
    p[0] = p[1] 

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
  start.print_tree(0)
  print ("Parsed successfully, writing graph to" + fd_2)
  graph.write_png(fd_2)
  print ("Write successful")
else :
  yacc.yacc( start='translation_unit')
  yacc.parse("");
  print("Please provide file to be parsed")