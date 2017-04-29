#!/usr/bin/python
import sys
import cparser


root, symbol_table = cparser.main()
# print symbol_table
for temp in symbol_table:
  print temp

def get_offset_symbole_table(variable,scope_name):
  for hash_table in symbol_table:
    if hash_table['scope_name'] == symbol_table:
      if variable in hash_table.keys():
        return hash_table[variable][5]
      elif scope_name == 's0':
        print 'Variable not found in symbol table exiting'
        sys.exit()
      else:
        return get_offset_symbole_table(variable,hash_table['parent_scope_name'])

def set_address_symbole_table(variable,scope_name,address):
  for index,hash_table in enumerate(symbol_table):
    if hash_table['scope_name'] == symbol_table:
      if variable in hash_table.keys():
        symbol_table[index][variable].append(address)
      elif scope_name == 's0':
        print 'Variable not found in symbol table exiting'
        sys.exit()
      else:
        set_address_symbole_table(variable,hash_table['parent_scope_name'],address)

count_label = 0
count_temp = 0
code = ''
class label(object):
  def __init__(self,_id = 0,name=''):
    global count_label
    # self.code = code
    self._id = count_label;
    if name == '':
      name = 'L' + str(count_label) 
      count_label = count_label + 1;
    self.name = name
  def __repr__(self):
    return self.name

class newtemp(object):
  def __init__(self,_id = 0):
    global count_temp
    self.count = count_temp
    self._id = count_temp;
    count_temp = count_temp + 1;
  def __repr__(self):
    return  'T' + str(self.count)

class Assignment():
  """docstring for Assignment"""
  def __init__(self,source='',destination=''):
    self.source = source
    self.destination = destination
  def __repr__(self):
    return self.source + ' = ' + self.destination

class Function_definition():
  """docstring for Function_definition"""
  def __init__(self,name=''):
    self.name = name
  def __repr__(self):
    return self.name

class BinOp():
  """docstring for BinOp"""
  def __init__(self,destination='',source_1='',operand='',source_2=''):
    self.source_1 = source_1
    self.source_2 = source_2
    self.operand = operand
    self.destination = destination
  def __repr__(self):
    return self.destination + ' = ' + self.source_1 + self.operand + self.source_2

def Jump(arg):
  global code
  code = code + '\tJMP ' + str(arg) + '\n'
def Compare(arg1, arg2):
  global code
  code = code + '\tCMP ' + str(arg1) +', ' + str(arg2) + '\n'
def PushParam(arg1):
  global code
  code = code + '\tPUSH ' + str(arg1)+ '\n'
def FuncCall(arg1):
  global code
  code = code + '\tCALL ' + str(arg1)+ '\n'
def Decl(arg1):
  global code
  code = code + '\tDecl ' + str(arg1)+ '\n'
def Ret():
  global code
  code = code + '\tRET '+ '\n'


def traverse_tree(ast_node, nextlist ,breaklist):
  global code
  arg = ''
  if ast_node.name == 'VarAccess':
    arg = ast_node.value
    # pass
  elif ast_node.name == 'ConstantLiteral':
    arg = ast_node.value
  if ast_node.name == 'IF Statement':
    E_next = label(name = ast_node.value)
    E_true = label(name = ast_node.value)
    
    arg1 = traverse_tree(ast_node.children[0], nextlist ,breaklist)
    Compare(arg1,0)
    Jump(E_next)
    
    code = code + str(E_true) + '\n'
    traverse_tree(ast_node.children[1], nextlist ,breaklist)
    Jump(E_next)
    
    code = code + str(E_next) + '\n'


  elif ast_node.name == 'IF-Else Statement':
    E_next = label(name = ast_node.value)
    E_true = label(name = ast_node.value)
    E_false = label(name = ast_node.value)

    arg1 = traverse_tree(ast_node.children[0], nextlist ,breaklist)
    Compare(arg1,0)
    Jump(E_false)
    
    code = code + str(E_true) + '\n'
    traverse_tree(ast_node.children[1], nextlist ,breaklist)
    Jump(E_next)

    code = code + str(E_false) + '\n'
    traverse_tree(ast_node.children[2], nextlist ,breaklist)

    code = code + str(E_next) + '\n'

  elif ast_node.name == 'While Statement':
    E_next = label(name = ast_node.value)
    E_begin = label(name = ast_node.value)

    code = code + str(E_begin) + '\n'
    
    arg1 = traverse_tree(ast_node.children[0], nextlist ,breaklist)
    Compare(arg1,0)
    Jump(E_next)
    
    traverse_tree(ast_node.children[1], E_begin ,E_next)
    Jump(E_begin)

    code = code + str(E_next) + '\n'

  elif ast_node.name == 'BREAK':
    Jump(breaklist)
  elif ast_node.name == 'CONTINUE':
    Jump(nextlist)

  elif ast_node.name == 'ForStatement3Exp':
    traverse_tree(ast_node.children[0], nextlist ,breaklist)

    E_next = label(name = ast_node.value)
    E_begin = label(name = ast_node.value)
    E_end = label(name = ast_node.value)

    code = code + str(E_begin) + '\n'
    arg1 = traverse_tree(ast_node.children[1], nextlist ,breaklist)
    Compare(arg1,0)
    Jump(E_next)

    traverse_tree(ast_node.children[3], E_end ,E_next)

    code = code + str(E_end) + '\n'

    traverse_tree(ast_node.children[2], nextlist ,breaklist)
    Jump(E_begin)

    code = code + str(E_next) + '\n'

  elif ast_node.name == 'VarDecl':
    Decl(ast_node.children[0].value)
  elif ast_node.name == 'VarDecl and Initialise':
    Decl(ast_node.children[0].value)
    arg1= ''
    if ast_node.children[1] is not None: 
      arg1 = traverse_tree(ast_node.children[1], nextlist ,breaklist)
    arg3 = Assignment(ast_node.children[0].value,arg1)
    code = code +'\t' + str(arg3) +'\n'

  elif ast_node.name == 'Argument List':
    if len(ast_node.children) > 0 :
      for child in ast_node.children[::-1]:
        if child is not None: 
          arg1 = traverse_tree(child, nextlist ,breaklist)
          PushParam(arg1)

  elif ast_node.name == 'FuncCall':
    FuncCall(ast_node.children[0].value)

  elif ast_node.name == 'FuncCallwithArgs':
    if len(ast_node.children) > 0 :
      for child in ast_node.children :
        traverse_tree(child, nextlist ,breaklist)
    FuncCall(ast_node.children[0].value)

  elif ast_node.name == 'Function_definition':
    arg1 = label(name = ast_node.value)
    code = code + str(arg1) + '\n'
    if len(ast_node.children) > 0 :
      for child in ast_node.children :
        if child is not None: 
          traverse_tree(child, nextlist ,breaklist)
  # elif ast_node.name == 'paramater':
  #   PopParam(ast_node.value)

  elif ast_node.name == 'RETURN_EXPRESSION':
    arg1 = traverse_tree(ast_node.children[0], nextlist ,breaklist)
    PushParam(arg1)
    Ret()
  elif ast_node.name == 'RETURN':
    Ret()

  elif ast_node.name == 'Assignment':
    arg1 = traverse_tree(ast_node.children[1], nextlist ,breaklist)
    arg3 = BinOp(ast_node.children[0].value, arg1, '','')
    code = code +'\t' + str(arg3) +'\n'

  elif ast_node.name in {'Addition','Logical AND','Logical OR','Multiplication','Modulus Operation',
    'Shift','Relation','EqualityExpression','AND', 'Exclusive OR','Inclusive OR'}:
    arg1 = traverse_tree(ast_node.children[0], nextlist ,breaklist)
    arg2 = traverse_tree(ast_node.children[1], nextlist ,breaklist)
    arg = str(newtemp())
    arg3 = BinOp(str(arg),str(arg1),ast_node.children[2].value,str(arg2))
    code = code +'\t' + str(arg3) +'\n'

  elif ast_node.name == 'UnaryOperator':
    arg1 = traverse_tree(ast_node.children[0], nextlist ,breaklist)
    arg3 = ''
    if(ast_node.children[1].value == '++'):
      arg3 = BinOp(str(arg1),str(arg1), '+',str(1))
    else: 
      arg3 = BinOp(str(arg1),str(arg1), '-',str(1))
    code = code +'\t' + str(arg3) +'\n'
    
  # elif ast_node.name == 'ArrayAccess':

  # elif ast_node.name == 'ArrayDeclaration':

  # elif ast_node.name == 'InitializerList':

  # elif ast_node.name == 'StructReference':

  # elif ast_node.name == 'Pointer Dereference':

  elif ast_node.name == 'Address Of Operation':
    arg = ast_node.children[0].value
  else:
    if len(ast_node.children) > 0 :
      for child in ast_node.children :
        if child is not None:
          traverse_tree(child, nextlist ,breaklist)
  return str(arg)

traverse_tree(root, None,None)
print code