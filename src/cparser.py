import ply.yacc as yacc
from lexer import *
import ply.lex as lex
import sys
lex.lex()

import pydot
graph = pydot.Dot(graph_type='graph')

# todo: Check for ASCII value of character
# todo: Add support for Struct
# todo: Run Good4, Good5, All Bads
# todo: Struct Address Dereference

# Symbol Table is a list of hash tables
# Each Hash table is of the form, symbol_table[scope_level]['A'] = [type, 'Function or not']
# It also has the attributes symbol_stable[scope_level]['parent_scope_name'] = 'name of parent scope', 
# symbol_stable[scope_level]['scope_name'] = 'current score name'
symbol_table = []
full_symbol_table = []
symbol_table.append({'parent_scope_name':'','scope_name':'s0'})
current_scope_name = 's0'
scope_level = 0
scopeNo = 0
current_function = ''
current_struct = ''
# Checks if the 'Compound Statement' is associated with a function or not
current_function_used = False

def add_edge(node_parent,node_child):
  graph.add_edge(pydot.Edge(node_parent, node_child))


def newScopeName():
  global scopeNo
  scopeNo += 1
  newScope = "s"+str(scopeNo) 
  return newScope


k = 0
def add_node(p):
  global k
  node = pydot.Node(k,label = p)
  graph.add_node(node)
  k = k + 1
  return node

class ast_node(object):
  def __init__(self, name='', value='', type='', children='', modifiers='', dims=0, arraylen=[], sym_entry='',
   lineno=0,tag = '',pydot_Node = None, is_var = False, scope_name = ''):
    self.name = name
    self.value = value
    self.type = type
    self.dims = dims
    self.lineno = lineno
    self.sym_entry = sym_entry
    self.pydot_Node = None
    self.is_var = is_var
    self.scope_name = scope_name
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
  def traverse_tree(self):
    global scope_level
    global symbol_table
    global current_function
    global current_function_used
    global current_struct
    global current_scope_name
    if self.name == 'VarAccess':
      found = False
      self.scope_name = current_scope_name
      for i in range(0,scope_level+1):
        if self.value in symbol_table[i].keys():
          found = True
          self.type = symbol_table[i][self.value][0]
          break
      if found == False:
        print self.lineno, 'COMPILATION ERROR: Trying to access undeclared variable ' + self.value
        sys.exit()

    if self.name.startswith('VarDecl'):
      self.scope_name = current_scope_name
      if self.value.split('=')[0] in symbol_table[scope_level].keys():
        print self.lineno, 'COMPILATION ERROR : Variable ' + self.value.split('=')[0] + ' already declared'
        sys.exit()
      else:
        symbol_table[scope_level][self.value.split('=')[0]] = [self.type,'',self.lineno]
        if self.type == 'void' and scope_level != 0:
          print self.lineno, 'COMPILATION ERROR : Variable ' + self.value.split('=')[0] + ' declared void'
          sys.exit()

    if self.name == 'struct_variable_declaration':
      if self.value in symbol_table[scope_level].keys():
        print self.lineno, 'COMPILATION ERROR : Variable in Struct ' + self.value.split('=')[0] + ' already declared'
        sys.exit()
      else:
        symbol_table[scope_level][self.value] = [self.type,'',self.lineno]
        if self.type == 'void' and scope_level != 0:
          print self.lineno, 'COMPILATION ERROR : Variable ' + self.value + ' declared void'
          sys.exit()

    if self.name == 'Struct Declaration':
      # checking at level 0 for redeclaration
      if self.value in symbol_table[0].keys():
        print self.lineno, 'COMPILATION ERROR : struct ' + self.value + ' already declared'
        sys.exit()
      symbol_table[0][self.value] = ['struct', '',self.lineno]
      current_struct = self.value

    if self.name == 'paramater':
      if self.value in symbol_table[scope_level].keys():
        print self.lineno, 'COMPILATION ERROR : Variable ' + self.value + ' already declared'
        sys.exit()
      else:
        # symbol_table[scope_level - 1][self.value][0] = p[2].type    Correct version todo : try to use p[2].type
        symbol_table[scope_level][self.value] = [self.type,'',self.lineno]

    if self.name == 'Function_definition':
      # Method names belong in the hashtable for the outermost scope NOT in the same table as the method's variables
      symbol_table[scope_level][self.value] = [self.type, 'Function',self.lineno]
      scope_level = scope_level + 1
      new_hash_table = {}
      new_hash_table = {'parent_scope_name':current_scope_name}
      current_scope_name = newScopeName()
      new_hash_table['scope_name'] = current_scope_name
      current_function = self.value
      symbol_table.append(new_hash_table)
      current_function_used = False

    if self.name == 'Compound Statement':
      # add a new scope if the 'compound statement' corresponding to the 'function definition' is used
      if current_function_used == True:
        scope_level = scope_level + 1
        new_hash_table = {'parent_scope_name':current_scope_name}
        current_scope_name = newScopeName()
        new_hash_table['scope_name'] = current_scope_name
        symbol_table.append(new_hash_table)
      if current_function_used == False:
        current_function_used = True

    if self.name == 'struct_declaration_list':
      # add a new scope if the 'compound statement' corresponding to the 'function definition' is used
      scope_level = scope_level + 1
      new_hash_table = {}
      new_hash_table = {'parent_scope_name':current_scope_name}
      current_scope_name = newScopeName()
      new_hash_table['scope_name'] = current_scope_name
      symbol_table.append(new_hash_table)

    if len(self.children) > 0 :
      for child in self.children :
        if child is not None: 
          child.traverse_tree()

    if self.name == 'Compound Statement':
      if len(full_symbol_table) > scope_level + 1:
        full_symbol_table[scope_level].append(symbol_table[scope_level])
      else:
        full_symbol_table.append([symbol_table[scope_level]])
      current_scope_name = symbol_table[scope_level]['parent_scope_name']
      del symbol_table[scope_level]
      scope_level = scope_level - 1

    if self.name == 'struct_declaration_list':
      symbol_table[0][current_struct].append(symbol_table[scope_level])
      current_struct = ''
      if len(full_symbol_table) > scope_level + 1:
        full_symbol_table[scope_level].append(symbol_table[scope_level])
      else:
        full_symbol_table.append([symbol_table[scope_level]])
      del symbol_table[scope_level]
      scope_level = scope_level - 1

    if self.name == 'Assignment' or self.name == 'VarDecl and Initialise':
      type_lhs = fetch_type_from_symbol_table(self.children[0])
      type_rhs = fetch_type_from_symbol_table(self.children[1])
      valid = ['double','float','int','unsigned int']
      if type_rhs in valid and type_lhs in valid:
        # todo: properly check these comments
        # if valid.index(type_lhs) > valid.index(type_rhs):
        #   print 'lineno',self.lineno,'-COMPILATION TERMINATED: type checking failed in assignment. '+
        #   self.children[0].value +': ' + type_lhs + ', ' + self.children[1].value + ': ' + type_rhs
        #   sys.exit(0)
        pass
      elif type_lhs[-1:] == '*':
        if type_rhs == type_lhs:
          pass
        elif type_rhs not in ['int','unsigned int']:
          print 'lineno',self.lineno,'-COMPILATION TERMINATED: type checking failed in assignment. '+ \
            self.children[0].value +': ' + type_lhs + ', ' + self.children[1].value + ': ' + type_rhs
          sys.exit(0)
        else:
          print 'lineno',self.lineno,'-WARNING: initialization makes pointer from integer without a cast'
      elif type_lhs != type_rhs:
        print 'lineno',self.lineno,'-COMPILATION TERMINATED: type checking failed in assignment. '+ \
         self.children[0].value +': ' + type_lhs + ', ' + self.children[1].value + ': ' + type_rhs
        sys.exit(0)
      self.type = fetch_type_from_symbol_table(self.children[0])

    if self.name == 'Multiplication':
      type_children_0 = fetch_type_from_symbol_table(self.children[0])
      type_children_1 = fetch_type_from_symbol_table(self.children[1])
      valid = ['double','float','int','unsigned int']
      if (type_children_0 in valid) and (type_children_1 in valid):
        _type = valid[min([valid.index(type_children_0), valid.index(type_children_1)])]
        self.type = _type
      else:
        print 'lineno',self.lineno,'-COMPILATION TERMINATED: error in multiplication types'
        sys.exit()

    if self.name == 'Modulus Operation':
      type_children_0 = fetch_type_from_symbol_table(self.children[0])
      type_children_1 = fetch_type_from_symbol_table(self.children[1])
      valid = ['int','unsigned int']      
      if (type_children_0 in valid) and (type_children_1 in valid):
        self.type = 'unsigned int'
      else:
        print 'lineno',self.lineno,'-COMPILATION TERMINATED: error in multiplication types'
        sys.exit()

    if self.name == 'Addition':
      type_children_0 = fetch_type_from_symbol_table(self.children[0])
      type_children_1 = fetch_type_from_symbol_table(self.children[1])
      valid = ['double','float','int','unsigned int']
      if (type_children_0 in valid) and (type_children_1 in valid):
        _type = valid[min([valid.index(type_children_0), valid.index(type_children_1)])]
        self.type = _type
      elif type_children_0[-1:] == '*' or type_children_1[-1:] == '*':
        if type_children_0 == type_children_1:
          print 'lineno',self.lineno,'-COMPILATION TERMINATED: Addition not permit for 2 pointers '
          sys.exit(0)
        elif type_rhs in ['int','unsigned int'] or type_lhs in ['int','unsigned int']:
          print 'lineno',self.lineno,'-WARNING: initialization makes pointer from integer without a cast'
      else:
        print 'lineno',self.lineno,'-COMPILATION TERMINATED: error in addition types'
        sys.exit()

    if self.name == 'Shift':
      type_children_0 = fetch_type_from_symbol_table(self.children[0])
      type_children_1 = fetch_type_from_symbol_table(self.children[1])
      valid = ['int','unsigned int']
      if (type_children_0 in valid) and (type_children_1 in valid):
        _type = self.children[0].type
        self.type = _type
      else:
        print 'lineno',self.lineno,'-COMPILATION TERMINATED: error in shift types'
        sys.exit()

    if self.name == 'Relation':
      type_children_0 = fetch_type_from_symbol_table(self.children[0])
      type_children_1 = fetch_type_from_symbol_table(self.children[1])
      valid = ['double','float','int','unsigned int']
      if (type_children_0 in valid) and (type_children_1 in valid):
        _type = 'BOOL'
        self.type = _type
      else:
        print 'lineno',self.lineno,'-COMPILATION TERMINATED: error in Relation types'
        sys.exit()

    if self.name == 'UnaryOperator':
      type_children_0 = fetch_type_from_symbol_table(self.children[0])
      if type_children_0 not in {'int','float','double','unsigned int'}:
        print 'lineno',self.lineno,'-COMPILATION TERMINATED: invalid use of Unary Operator'
        sys.exit()
      else:
        self.type = type_children_0

    if self.name == 'EqualityExpression':
      type_children_0 = fetch_type_from_symbol_table(self.children[0])
      type_children_1 = fetch_type_from_symbol_table(self.children[1])
      valid = ['double','float','int','unsigned int','BOOL']
      if (type_children_0 in valid) and (type_children_1 in valid):
        _type = 'BOOL'
        self.type = _type
      else:
        print 'lineno',self.lineno,'-COMPILATION TERMINATED: error in Equality expression types'
        sys.exit()

    if self.name == ('AND' or 'Exclusive OR' or'Inclusive OR'):
      type_children_0 = fetch_type_from_symbol_table(self.children[0])
      type_children_1 = fetch_type_from_symbol_table(self.children[1])
      valid = ['int','unsigned int','BOOL']
      if (type_children_0 in valid) and (type_children_1 in valid):
        _type = valid[min([valid.index(type_children_0), valid.index(type_children_1)])]
        self.type = _type
      else:
        print 'lineno',self.lineno,'-COMPILATION TERMINATED: error in logical operation types'
        sys.exit()

    if self.name == ('Logical AND' or'Logical OR'):
      type_children_0 = fetch_type_from_symbol_table(self.children[0])
      type_children_1 = fetch_type_from_symbol_table(self.children[1])
      valid = ['double','float','int','unsigned int','BOOL']
      if (type_children_0 in valid) and (type_children_1 in valid):
        _type = 'BOOL'
        self.type = _type
      else:
        print 'lineno',self.lineno,'-COMPILATION TERMINATED: error in logical operation types'
        sys.exit()

    if self.name == 'ArrayAccess':
      if fetch_type_from_symbol_table(self.children[1]) not in ['int','unsigned int']: 
        print 'lineno',self.lineno,'-COMPILATION TERMINATED: error in logical ArrayAccess'
        sys.exit()

    if self.name == 'ArrayDeclaration':
       if fetch_type_from_symbol_table(self.children[0]) not in ['int','unsigned int']: 
        print 'lineno',self.lineno,'-COMPILATION TERMINATED: error in logical ArrayDeclaration'
        sys.exit()

    if self.name == 'InitializerList':
      for child in self.children:
        if child.name != '':
          if child.type != self.type:
            print 'lineno',self.lineno,'-COMPILATION TERMINATED: error in logical InitializerList'
            sys.exit()

    if self.name == 'RETURN_EXPRESSION':
      if fetch_type_from_symbol_table(self.children[0]) != symbol_table[0][current_function][0]:
        print 'lineno',self.lineno,'-COMPILATION TERMINATED: Return type of function('+ \
         str(symbol_table[0][current_function][0])+') does not match variable type('+str(fetch_type_from_symbol_table(self.children[0]))+')'
        sys.exit()

    if self.name == 'Ternary Operation':
      if fetch_type_from_symbol_table(self.children[0]) not in ['BOOL','int','unsigned int','float','double']:
        print 'COMPILAION TERMINATED: tyepcheck error in ternary operator'
        sys.exit()       

    if self.name == 'StructReference':
      # Checking if 'Declarated variable' is a struct or not
      if fetch_type_from_symbol_table(self.children[0]).startswith('struct'):
        pass
      else:
        print fetch_type_from_symbol_table(self.children[0])
        print 'lineno',self.lineno,'-COMPILATION TERMINATED: '+ self.children[0].value +' is no struct'
        sys.exit()
      if self.children[1].value not in symbol_table[0][fetch_type_from_symbol_table(self.children[0]).split(' ')[1]][2].keys():
        print 'lineno',self.lineno,'-COMPILATION TERMINATED Struct has no field: ', self.children[1].value
        sys.exit()
      self.type = symbol_table[0][fetch_type_from_symbol_table(self.children[0]).split(' ')[1]][2][self.children[1].value][0]


    if self.name == 'Pointer Dereference':
      self.type = fetch_type_from_symbol_table(self.children[0]).split(' ')[0]

    if self.name == 'Address Of Operation':
      self.type = fetch_type_from_symbol_table(self.children[0])+' *'

  def print_tree(self,depth):
    output = ''
    if self.name is not '':
      for i in range(0,depth-1):
        print '-',
      print '+',
      depth = depth + 1
      if len(self.arraylen) != 0:
        output = self.name + ' ' + self.type+' '+str(self.value)+' '+str(self.arraylen)
      else:
        output = self.name + ' ' + self.type+' '+str(self.value)+' '+self.scope_name
      print (output)
    self.pydot_Node = add_node(output)
    if len(self.children) > 0 :
      for child in self.children :
        if child is not None:  
          child.print_tree(depth)
          add_edge(self.pydot_Node,child.pydot_Node)
        else : 
          print '[DEBUG] CHILD NONE WARNING'    

  def set_type(self,t):
    self.type = t
    if len(self.children) > 0 :
      for child in self.children : 
        if hasattr(child,'name'):
          if child.name != 'ConstantLiteral':
              child.set_type(t)

# Works for both cases : when the child is variable and when it's a constant
def fetch_type_from_symbol_table(child):
  if child.name ==  "StringLiteral":
    return 'string'
  _type = ''
  if child.name == 'Pointer Dereference' or child.name == 'Address Of Operation':
    return child.type
  for i in range(0,scope_level+1):
    if child.value in symbol_table[i].keys():
      _type = symbol_table[i][child.value][0]
      return _type
    if child.is_var == False:
      _type = child.type
  return _type



start = ast_node('START',value = '',type ='' ,children = [])
def p_primary_expression(p):
  '''primary_expression   : identifier
                          '''
  p[0] = ast_node('VarAccess',value = p[1].value,type =p[1].type,children = [],is_var = p[1].is_var,lineno = p[1].lineno)
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
  p[0] = ast_node('',value = p[1],type ='',children = [],is_var=True, lineno = p.lineno(1)) 
def p_constant(p):
  '''constant             : CONSTANT
                          '''
  if p[1].isdigit():
    p[0] = ast_node('ConstantLiteral',value = p[1],type ='int',children = [], lineno = p.lineno(1))  
  else:
    p[0] = ast_node('ConstantLiteral',value = p[1],type ='float',children = [], lineno = p.lineno(1))  
def p_constant_2(p):
  '''constant             : CCONST
                          '''
  p[0] = ast_node('ConstantLiteral',value = p[1],type ='char',children = [], lineno = p.lineno(1))  

def p_string(p):
  '''string               : STRING_LITERAL
                           '''
  p[0] = ast_node('StringLiteral',value = p[1],type ='string',children = [], lineno = p.lineno(1))  

def p_postfix_expression(p):
  '''postfix_expression   : primary_expression
                          '''
  p[0] = p[1]

def p_postfix_expression_1(p):
  '''postfix_expression   : postfix_expression '[' expression ']'
                          '''
  p[0] = ast_node('ArrayAccess',value = p[1].value,type =p[1].type,children = [p[1],p[3]], lineno = p[1].lineno)  
def p_postfix_expression_2(p):
  '''postfix_expression   : postfix_expression '(' ')'
                          '''                          
  p[0] = ast_node('FuncCall',value = p[1].value,type = p[1].type,children =[p[1]], lineno = p[1].lineno)
def p_postfix_expression_3(p):
  '''postfix_expression   : postfix_expression '(' argument_expression_list ')'
                          '''
  p[0] = ast_node('FuncCallwithArgs',value = p[1].value,type = p[1].type,children =[p[1],p[3]], lineno = p[1].lineno)  
def p_postfix_expression_4(p):
  '''postfix_expression   : postfix_expression '.' identifier
                          | postfix_expression PTR_OP identifier
                          '''
  p[0] = ast_node('StructReference',value = p[3].value,type = p[3].type,children =[p[1],p[3]], lineno = p[1].lineno)
def p_postfix_expression_5(p):
  '''postfix_expression   : postfix_expression INC_OP
                          | postfix_expression DEC_OP
                         '''
  temp = ast_node('',value=p[2], lineno=p[1].lineno)
  p[0] = ast_node('UnaryOperator',value = p[1].value, type = p[1].type, children =[p[1],temp], lineno = p[1].lineno)
def p_postfix_expression_6(p):
  '''postfix_expression   : '(' type_name ')' '{' initializer_list '}'
                          | '(' type_name ')' '{' initializer_list ',' '}'
                          '''
  p[0] = ast_node('Compound Literal')
def p_argument_expression_list(p):
  '''argument_expression_list   : assignment_expression
                                | argument_expression_list ',' assignment_expression
                                '''
  if len(p) == 2:
    p[0] = ast_node('Argument List',value = '', type = p[1].type, children = [p[1]], lineno = p[1].lineno)
  else:
    if p[1].name != 'Argument List':
      p[1] = ast_node('Argument List',value = '', type = p[3].type, children = [], lineno = p[1].lineno)
    p[1].children.append(p[3])
    p[0] = p[1] 
def p_unary_expression(p):
  '''unary_expression   : postfix_expression
                        '''
  p[0] = p[1]

def p_unary_expression_1(p):
  '''unary_expression   : INC_OP unary_expression
                        | DEC_OP unary_expression
                        '''
  p[0] = ast_node('Unary Operator',value = p[2].value, type = p[2].type, children =[p[2]], lineno = p.lineno(1))

def p_unary_expression_2(p):
  '''unary_expression   : unary_operator cast_expression
                        '''
  if p[1] == '*':
    p[0] = ast_node('Pointer Dereference',value = p[2].value, type = p[2].type, children =[p[2]], lineno = p.lineno(1))
  elif p[1] == '&':
    p[0] = ast_node('Address Of Operation',value = p[2].value, type = p[2].type, children =[p[2]], lineno = p.lineno(1))
  else:
    p[0] = ast_node('Unary Operator',value = p[2].value, type = p[2].type, children =[p[2]], lineno = p.lineno(1))    

def p_unary_expression_3(p):
  '''unary_expression   : SIZEOF '(' unary_expression ')'
                        | SIZEOF '(' struct_or_union_specifier ')'
                        '''
  p[0] = ast_node('Size Of', value = p[3].value, type = p[3].type, children =[p[3]], lineno = p.lineno(1))  

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
    p[0] = ast_node('Type Cast', value = p[2].value, type = p[2].type, children =[p[2],p[4]], lineno = p.lineno(1))

def p_multiplicative_expression(p):
  '''multiplicative_expression  : cast_expression
                                | multiplicative_expression '*' cast_expression
                                | multiplicative_expression '/' cast_expression
                                '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    temp = ast_node(value=p[2], lineno=p[1].lineno)
    p[0] = ast_node('Multiplication', value = '', type = '', children =[p[1],p[3],temp], lineno = p[1].lineno)

def p_multiplicative_expression_1(p):
  '''multiplicative_expression  : multiplicative_expression '%' cast_expression
                                '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    temp = ast_node(value=p[2], lineno=p[1].lineno)
    p[0] = ast_node('Modulus Operation', value = '', type = '', children =[p[1],p[3],temp], lineno = p[1].lineno)

def p_additive_expression(p):
  '''additive_expression  : multiplicative_expression
                          | additive_expression '+' multiplicative_expression
                          | additive_expression '-' multiplicative_expression
                          '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    temp = ast_node(value=p[2], lineno=p[1].lineno)
    p[0] = ast_node('Addition', value = '', type = '', children =[p[1],p[3],temp], lineno = p[1].lineno)
  
def p_shift_expression(p):
  '''shift_expression   : additive_expression
                        | shift_expression LEFT_OP additive_expression
                        | shift_expression RIGHT_OP additive_expression
                        '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    temp = ast_node(value=p[2], lineno=p[1].lineno)
    p[0] = ast_node('Shift', value = '', type = '', children =[p[1],p[3],temp], lineno = p[1].lineno)
  
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
    temp = ast_node(value=p[2], lineno=p[1].lineno)
    p[0] = ast_node('Relation', value = '', type = '', children =[p[1],p[3],temp], lineno = p[1].lineno)

def p_equality_expression(p):
  '''equality_expression  : relational_expression
                          | equality_expression EQ_OP relational_expression
                          | equality_expression NE_OP relational_expression
                          '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    temp = ast_node(value=p[2], lineno=p[1].lineno)
    p[0] = ast_node('EqualityExpression', value = '', type = '', children =[p[1],p[3],temp], lineno = p[1].lineno)

def p_and_expression(p):
  '''and_expression   : equality_expression
                      | and_expression '&' equality_expression
                      '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    temp = ast_node(value=p[2], lineno=p[1].lineno)
    p[0] = ast_node('AND', value = '', type = '', children =[p[1],p[3],temp], lineno = p[1].lineno)

def p_exclusive_or_expression(p):
  '''exclusive_or_expression  : and_expression
                              | exclusive_or_expression '^' and_expression
                              '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    temp = ast_node(value=p[2], lineno=p[1].lineno)
    p[0] = ast_node('Exclusive OR', value = '', type = '', children =[p[1],p[3],temp], lineno = p[1].lineno)

def p_inclusive_or_expression(p):
  '''inclusive_or_expression  : exclusive_or_expression
                              | inclusive_or_expression '|' exclusive_or_expression
                              '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    temp = ast_node(value=p[2], lineno=p[1].lineno)
    p[0] = ast_node('Inclusive OR', value = '', type = '', children =[p[1],p[3],temp], lineno = p[1].lineno)
  

def p_logical_and_expression(p):
  '''logical_and_expression   : inclusive_or_expression
                              | logical_and_expression AND_OP inclusive_or_expression
                              '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    temp = ast_node(value=p[2], lineno=p[1].lineno)
    p[0] = ast_node('Logical AND', value = '', type = '', children =[p[1],p[3],temp], lineno = p[1].lineno)
  
def p_logical_or_expression(p):
  '''logical_or_expression  : logical_and_expression
                            | logical_or_expression OR_OP logical_and_expression
                            '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    temp = ast_node(value=p[2], lineno=p[1].lineno)
    p[0] = ast_node('Logical OR', value = '', type = '', children =[p[1],p[3],temp], lineno = p[1].lineno)

def p_conditional_expression(p):
  '''conditional_expression   : logical_or_expression
                              | logical_or_expression '?' expression ':' conditional_expression
                                '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    p[0] = ast_node('Ternary Operation', value = '', type = '', children =[p[1],p[3],p[5]], lineno = p[1].lineno)

def p_assignment_expression(p):
  '''assignment_expression  : conditional_expression
                            | unary_expression assignment_operator assignment_expression
                            '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    p[0] = ast_node('Assignment', value = '', type = p[1].type, children =[p[1],p[3]], lineno = p[1].lineno)
  
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
    if p[2].type == '':
      temp = p[1].type
    else:
      temp = p[1].type + ' '+ p[2].type
    p[0] = ast_node('Declaration Statement',value = '',type =temp,children = [p[1],p[2]], lineno = p[1].lineno)
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
    temp = p[1].type + ' ' + p[2].type
    p[0] = ast_node('Declaration Specifier',value = p[1].value,type =temp,children = [p[1],p[2]], lineno = p[1].lineno)

def p_init_declarator_list(p):
  '''init_declarator_list   : init_declarator
                            | init_declarator_list ',' init_declarator
                            '''
  if len(p) == 2:
    p[0] = ast_node('Initializer List',value = '', type = p[1].type, children = [p[1]], lineno = p[1].lineno)
  else:
    if p[1].name != 'Initializer List':
      p[1] = ast_node('Initializer List',value = '', type = p[3].type, children = [])
    p[1].children.append(p[3])
    p[0] = p[1] 
def p_init_declarator(p):
  '''init_declarator  : declarator
                      | declarator '=' initializer
                      '''
  if len(p) == 2:
    p[0] = ast_node('VarDecl', value = p[1].value,type =p[1].type,children = [p[1]], lineno = p[1].lineno)
  else:
    p[0] = ast_node('VarDecl and Initialise',value = (p[1].value + '=' +p[3].value),
      type =p[1].type,children = [p[1],p[3]], lineno = p[1].lineno)
def p_storage_class_specifier(p):
  '''storage_class_specifier  : TYPEDEF
                              | EXTERN
                              | STATIC
                              | AUTO
                              | REGISTER
                              '''
  p[0] = ast_node('Storage Specifier',value = '',type =p[1],children = [], lineno = p.lineno(1)) 
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
  p[0] = ast_node('',value = '',type =p[1],children = [], lineno = p.lineno(1))

def p_type_specifier_1(p):
  '''type_specifier   : struct_or_union_specifier
                      '''
  p[0] = ast_node('',value = p[1].value,type =p[1].type,children = [p[1]], lineno = p[1].lineno)

def p_struct_or_union_specifier(p):
  '''struct_or_union_specifier  : struct_or_union identifier '{' struct_declaration_list '}'
                                '''
  p[0] = ast_node('Struct Declaration',value = p[2].value,type =(p[1]+' '+p[2].value),children = [p[4]], lineno = p.lineno(1))

def p_struct_or_union_specifier_1(p):
  '''struct_or_union_specifier  : struct_or_union '{' struct_declaration_list '}'
                                '''
  # todo
  p[0] = ast_node('Struct Declaration',value = '',type =(p[1]),children = [p[3]], lineno = p.lineno(1))

def p_struct_or_union_specifier_2(p):
  '''struct_or_union_specifier  : struct_or_union identifier
                                '''
  p[0] = ast_node('',value = '',type =(p[1]+' '+p[2].value),children = [], lineno = p.lineno(1))

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
    p[0] = ast_node('struct_declaration_list',value = '', type = '', children = [p[1]], lineno = p[1].lineno)
  else:
    if p[1].name != 'struct_declaration_list':
      p[1] = ast_node('struct_declaration_list',value = '', type = '', children = [], lineno = p[1].lineno)
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
    if p[2].type == '':
      temp = p[1].type
    else:
      temp = p[1].type + ' '+ p[2].type
    p[0] = ast_node('Struct declarations',value = '',type =temp,children = [p[1],p[2]], lineno = p[1].lineno)
    p[0].set_type(temp)
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
    temp = p[1].type + ' ' + p[2].type
    p[0] = ast_node('Declaration Specifier',value = p[1].value,type = temp ,children = [p[1],p[2]], lineno = p[1].lineno)

def p_struct_declarator_list(p):
  '''struct_declarator_list   : struct_declarator
                              | struct_declarator_list ',' struct_declarator
                              '''
  if len(p) == 2:
    p[0] = ast_node('struct_declarator_list',value = '', type = p[1].type, children = [p[1]], lineno = p[1].lineno)
  else:
    if p[1].name != 'struct_declarator_list':
      p[1] = ast_node('struct_declarator_list',value = '', type = p[3].type, children = [], lineno = p[1].lineno)
    p[1].children.append(p[3])
    p[0] = p[1] 
def p_struct_declarator(p):
  '''struct_declarator  : declarator
                        | ':' constant_expression
                        | declarator ':' constant_expression
                        '''
  if len(p) == 2:
    p[0] = ast_node('struct_variable_declaration', value = p[1].value,type = '',children = [p[1]], lineno = p[1].lineno)
  elif len(p) == 3:
    pass
  else: 
    pass

def p_type_qualifier(p):
  '''type_qualifier   : CONST
                      | VOLATILE
                      | RESTRICT
                      '''
  p[0] = ast_node('Qualifier Declaration',value = '',type =p[1],children = [], lineno = p.lineno(1))  

def p_declarator(p):
  '''declarator   : pointer direct_declarator
                  | direct_declarator
                  '''
  if len(p) == 2:
    p[0] = p[1]
  else: 
    p[0] = ast_node('PointerDeclaration',value = p[2].value,type =p[1].type+p[2].type,children = [], lineno = p[1].lineno)

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
  p[0] = ast_node('ArrayIntialize',value = p[1].value,type =p[1].type,children = [p[1]], lineno = p[1].lineno) 
  p[0].arraylen.append(0)
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
  if p[1].is_var:
    p[0] = ast_node('ArrayDeclaration',value = p[1].value,type ='',children = [p[3]],dims = p[1].dims + 1, lineno = p[1].lineno)
  else:
    p[0] = p[1]
    p[0].children.append(p[3])
    p[0].dims = p[0].dims+1
  p[0].arraylen.append(p[3].value)
def p_direct_declarator_4(p):
  '''direct_declarator  : direct_declarator '(' parameter_type_list ')'
                        '''
  p[0] = ast_node('Function Arguments',value = p[1].value,type ='',children = [p[1],p[3]], lineno = p[1].lineno)
def p_direct_declarator_5(p):
  '''direct_declarator  : direct_declarator '(' ')'
                        '''
  p[0] = p[1] # blank function declare e.g int main()
def p_direct_declarator_6(p):
  '''direct_declarator  : direct_declarator '(' identifier_list ')'
                        '''
  print "********"
  p[0] = ast_node('Function Arguments',value = p[1].value,type ='',children = [p[1],p[3]], lineno = p[1].lineno)
def p_pointer(p):
  '''pointer  : '*'
              '''
  p[0] = ast_node('',value = '',type =p[1],children = [], lineno = p.lineno(1))
def p_pointer_1(p):
  '''pointer  : '*' type_qualifier_list
              '''
  p[0] = ast_node('',value = '',type =p[1]+' '+p[2].type,children = [], lineno = p.lineno(1))
def p_pointer_2(p):
  '''pointer  : '*' pointer
              '''
  p[0] = ast_node('',value = '',type =p[1]+' '+p[2].type,children = [], lineno = p.lineno(1))
def p_pointer_3(p):
  '''pointer  : '*' type_qualifier_list pointer
              '''
  p[0] = ast_node('',value = '',type =p[1]+' '+p[2].type+p[3].type,children = [], lineno = p.lineno(1))

def p_type_qualifier_list(p):
  '''type_qualifier_list  : type_qualifier
                          | type_qualifier_list type_qualifier
                          '''
  if len(p) == 2:
    p[0] = p[1]
  else: 
    p[0] = p[2]
    p[0].type = p[1].type + ' ' + p[2].type

def p_parameter_type_list(p):
  '''parameter_type_list  : parameter_list
                          '''
  p[0] = p[1] 
def p_parameter_list(p):
  '''parameter_list   : parameter_declaration
                      | parameter_list ',' parameter_declaration
                      '''
  if len(p) == 2:
    p[0] = ast_node('paramater_list',value = '', type = '', children = [p[1]], lineno = p[1].lineno)
  else:
    if p[1].name != 'paramater_list':
      p[1] = ast_node('paramater_list',value = '', type = '', children = [], lineno = p[1].lineno)
    p[1].children.append(p[3])
    p[0] = p[1]

def p_parameter_declaration(p):
  '''parameter_declaration  : declaration_specifiers declarator
                            '''
  p[0] = ast_node('paramater',value = p[2].value, type = p[1].type, children = [], lineno = p[1].lineno)
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
    p[0] = ast_node('identifier_list',value = p[1].value, type = '', children = [p[1]], lineno = p[1].lineno)
  else:
    if p[1].name != 'identifier_list':
      p[1] = ast_node('identifier_list',value = '', type = '', children = [], lineno = p[1].lineno)
    p[1].children.append(p[3])
    p[0] = p[1]

def p_type_name(p):
  '''type_name        : specifier_qualifier_list abstract_declarator
                      | specifier_qualifier_list
                      '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    p[0] = ast_node('random shit',lineno = p[1].lineno)

def p_abstract_declarator(p):
  '''abstract_declarator  : pointer
                          '''
  p[0] = p[1]

def p_abstract_declarator_1(p):
  '''abstract_declarator  : direct_abstract_declarator
                          '''
  p[0] = p[1]

def p_abstract_declarator_2(p):
  '''abstract_declarator  : pointer direct_abstract_declarator
                          '''

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
    p[0] = ast_node('InitializerList',value = '',type = p[1].type, children = [p[1]], lineno = p[1].lineno)
  else:
    if p[1].name != 'InitializerList':
      p[1] = ast_node('InitializerList',value = '', type = p[3].type, children = [], lineno = p[1].lineno)
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
  p[0] = ast_node('Label statement',value = '', type = '', children = [p[3]], lineno = p[1].lineno)
def p_labeled_statement_1(p):
  '''labeled_statement  : CASE constant_expression ':' statement
                        '''
  p[0] = ast_node('Case statement',value = '', type = '', children = [p[2],p[4]], lineno = p.lineno(1))

def p_labeled_statement_2(p):
  '''labeled_statement  : DEFAULT ':' statement
                        '''
  p[0] = ast_node('Default statement',value = '', type = '', children = [p[3]], lineno = p.lineno(1))

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
    p[0] = ast_node('Compound Statement',value = '',type = '', children = [p[1]], lineno = p.lineno(1))
  else:
    if p[1].name != 'Compound Statement':
      p[1] = ast_node('Compound Statement',value = '', type = '', children = [], lineno = p[1].lineno)
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
  p[0] = ast_node('IF Statement', value = '', type = '', children = [p[3],p[5]], lineno = p.lineno(1))
def p_selection_statement_1(p):
  '''selection_statement  : IF '(' expression ')' statement ELSE statement
                          '''
  p[0] = ast_node('IF-Else Statement', value = '', type = '', children = [p[3],p[5],p[7]], lineno = p.lineno(1))
def p_selection_statement_2(p):
  '''selection_statement  : SWITCH '(' expression ')' statement
                          '''
  p[0] = ast_node('Switch Statement', value = '', type = '', children = [p[3],p[5]], lineno = p.lineno(1))
def p_iteration_statement(p):
  '''iteration_statement  : WHILE '(' expression ')' statement
                          '''
  p[0] = ast_node('While Statement', value = '', type = '', children = [p[3],p[5]], lineno = p.lineno(1))
def p_iteration_statement_1(p):
  '''iteration_statement  : DO statement WHILE '(' expression ')' ';'
                          '''
  p[0] = ast_node('Do-While Statement', value = '', type = '', children = [p[2],p[5]], lineno = p.lineno(1))
def p_iteration_statement_2(p):
  '''iteration_statement  : FOR '(' expression_statement expression_statement ')' statement
                          '''
  p[0] = ast_node('For Statement', value = '', type = '', children = [p[3],p[4],p[6]], lineno = p.lineno(1))
def p_iteration_statement_3(p):
  '''iteration_statement  : FOR '(' expression_statement expression_statement expression ')' statement
                          '''
  p[0] = ast_node('ForStatement3Exp', value = '', type = '', children = [p[3],p[4],p[5],p[7]], lineno = p.lineno(1))
def p_iteration_statement_4(p):
  '''iteration_statement  : FOR '(' declaration expression_statement ')' statement
                          '''
  p[0] = ast_node('For Statement', value = '', type = '', children = [p[3],p[4],p[6]], lineno = p.lineno(1))
def p_iteration_statement_5(p):
  '''iteration_statement  : FOR '(' declaration expression_statement expression ')' statement
                          '''
  p[0] = ast_node('For Statement', value = '', type = '', children = [p[3],p[4],p[5],p[7]], lineno = p.lineno(1))
def p_jump_statement(p):
  '''jump_statement   : GOTO identifier ';'
                      '''
  p[0] = ast_node('Goto', value = p[2].value, type = '', children = [], lineno = p.lineno(1))
def p_jump_statement_1(p):
  '''jump_statement   : CONTINUE ';'
                      '''
  p[0] = ast_node('CONTINUE', value = '', type = '', children = [], lineno = p.lineno(1))
def p_jump_statement_2(p):
  '''jump_statement   : BREAK ';'
                      '''
  p[0] = ast_node('BREAK', value = '', type = '', children = [], lineno = p.lineno(1))
def p_jump_statement_3(p):
  '''jump_statement   : RETURN ';'
                      '''
  p[0] = ast_node('RETURN', value = '', type = '', children = [], lineno = p.lineno(1))
def p_jump_statement_4(p):
  '''jump_statement   : RETURN expression ';'
                      '''
  p[0] = ast_node('RETURN_EXPRESSION', value = '', type = p[2].type, children = [p[2]], lineno = p.lineno(1))
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
  p[0] = p[1]

def p_external_declaration_2(p):
  '''external_declaration   : declaration
                            '''
  p[0] = p[1]

def p_function_definition(p):
  '''function_definition  : declaration_specifiers declarator declaration_list compound_statement
                          | declaration_specifiers declarator compound_statement
                          '''
  if len(p) == 4:
    p[0] = ast_node('Function_definition',value = p[2].value,type =p[1].type ,children = [p[2],p[3]], lineno = p[1].lineno)
  else:
    p[0] = ast_node('Function_definition',value = p[2].value,type =p[1].type ,children = [p[2],p[3],p[4]], lineno = p[1].lineno)
  
def p_declaration_list(p):
  '''declaration_list   : declaration_list declaration
                        | declaration
                        '''
  if len(p) == 2:
    p[0] = ast_node('Declaration List',value = '', type = '', children = [p[1]], lineno = p[1].lineno)
  else:
    if p[1].name != 'Declaration List':
      p[1] = ast_node('Declaration List',value = '', type = '', children = [], lineno = p[1].lineno)
    p[1].children.append(p[2])
    p[0] = p[1] 

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value+ ' at line number ' + str(p.lineno))
    else:
        print('Syntax error at EOF')
    sys.exit()

def main():
  if len(sys.argv) >= 2:
    fd = sys.argv[1]
    if len(sys.argv) == 3 :
      fd_2 = '../test/' + sys.argv[2]
    else : 
      fd_2 = '../test/graph.png'
    yacc.yacc( start='translation_unit')
    with open (fd, 'r') as myfile:
      data=myfile.read()
    print('File read complete........')
    yacc.parse(data)
    print ('Parsed successfully.......')
    start.traverse_tree()
    print ('Compiled successfully.......')
    start.print_tree(0)
    print ('Writing graph to' + fd_2)
    graph.write_png(fd_2)
    print ('Write successful')
    full_symbol_table[0] = symbol_table + full_symbol_table[0]
    return start, full_symbol_table
  else :
    yacc.yacc( start='translation_unit')
    yacc.parse('');
    print('Please provide file to be parsed')

if __name__ == '__main__':
  main()
