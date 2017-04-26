import sys
import cparser

root, symbol_table = cparser.main()
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

class  LogicalOP(object):
  """docstring for  LogicalOP"""
  def __init__(self,source_1='',operand='',source_2=''):
    self.source_1 = source_1
    self.source_2 = source_2
    self.operand = operand
  def __repr__(self):
    return 'if ' + self.source_1 + ' ' + self.operand + ' ' + self.source_2 + ' jmp'

class ShiftOP(object):
  """docstring for  ShiftOP"""
  def __init__(self,destination, source_1='',operand='',source_2=''):
    self.source_1 = source_1
    self.source_2 = source_2
    self.operand = operand
    self.destination = destination
  def __repr__(self):
    return self.destination + ' = ' + self.source_1 + ' ' + self.operand + ' ' + self.source_2
    

def Jump(arg):
  code = code + '\t JMP ' + arg + '\n'


def traverse_tree(ast_node):
  global code
  arg = ''
  # if ast_node.name == 'VarAccess':

  if ast_node.name == 'IF Statement':
    E_start = label(name = ast_node.value)
    E_true = label(name = ast_node.value)
    E_next = label(name = ast_node.value)
    code = code + str(E_start) + '\n'
    arg1 = traverse_tree(ast_node.children[0])
    code = code + '\t if ' + str(arg1) + ' JMP' + '\n'
    code = code + str(E_true) + '\n'
    traverse_tree(ast_node.children[1])
    code = code + str(E_next) + '\n'

  elif ast_node.name == 'IF-Else Statement':
    E_start = label(name = ast_node.value)
    E_true = label(name = ast_node.value)
    E_false = label(name = ast_node.value)
    E_next = label(name = ast_node.value)

    code = code + str(E_start) + '\n'
    arg1 = traverse_tree(ast_node.children[0])
    code = code + '\tif ' + str(arg1) + ' JMP' + '\n'

    code = code + str(E_true) + '\n'
    traverse_tree(ast_node.children[1])

    code = code + str(E_false) + '\n'
    traverse_tree(ast_node.children[2])

    code = code + str(E_next) + '\n'

  elif ast_node.name == 'VarDecl and Initialise':
    if ast_node.children[1] is not None: 
      arg1 = traverse_tree(ast_node.children[1])
    if arg1 == '':
      arg1 = ast_node.children[1].value
    arg3 = Assignment(ast_node.children[0].value,arg1)
    code = code +'\t' + str(arg3) +'\n'
  # elif ast_node.name == 'struct_variable_declaration':

  # elif ast_node.name == 'Struct Declaration':

  # elif ast_node.name == 'paramater':
  elif ast_node.name == 'Function_definition':
    arg1 = label(name = ast_node.value)
    code = code + str(arg1) + '\n'
    if len(ast_node.children) > 0 :
      for child in ast_node.children :
        if child is not None: 
         traverse_tree(child)

  elif ast_node.name == 'Compound Statement':
    if len(ast_node.children) > 0 :
      for child in ast_node.children :
        traverse_tree(child)
    # E_true = label(name = ast_node.value)
    # code = code + str(E_true) + '\n'

  # elif ast_node.name == 'struct_declaration_list':

  elif ast_node.name == 'Assignment':
    arg1 = traverse_tree(ast_node.children[1])
    if arg1 == '':
      arg1 = ast_node.children[1].value
    arg3 = BinOp(ast_node.children[0].value, arg1, '','')
    code = code +'\t' + str(arg3) +'\n'

  elif ast_node.name == 'Multiplication':
    arg1 = traverse_tree(ast_node.children[0])
    if arg1 == '':
      arg1 = ast_node.children[0].value
    arg2 = traverse_tree(ast_node.children[1])
    if arg2 == '':
      arg2 = ast_node.children[1].value
    arg = str(newtemp())
    arg3 = BinOp(str(arg),str(arg1),ast_node.children[2].value,str(arg2))
    code = code +'\t' + str(arg3) +'\n'

  elif ast_node.name == 'Modulus Operation':
    arg1 = traverse_tree(ast_node.children[0])
    if arg1 == '':
      arg1 = ast_node.children[0].value
    arg2 = traverse_tree(ast_node.children[1])
    if arg2 == '':
      arg2 = ast_node.children[1].value
    arg = str(newtemp())
    arg3 = BinOp(str(arg),str(arg1),ast_node.children[2].value,str(arg2))
    code = code +'\t' + str(arg3) +'\n'

  elif ast_node.name == 'Addition':
    arg1 = traverse_tree(ast_node.children[0])
    if arg1 == '':
      arg1 = ast_node.children[0].value
    arg2 = traverse_tree(ast_node.children[1])
    if arg2 == '':
      arg2 = ast_node.children[1].value
    arg = str(newtemp())
    arg3 = BinOp(str(arg),str(arg1),ast_node.children[2].value,str(arg2))
    code = code +'\t' + str(arg3) +'\n'

  elif ast_node.name == 'Shift':
    arg1 = traverse_tree(ast_node.children[0])
    if arg1 == '':
      arg1 = ast_node.children[0].value
    arg2 = traverse_tree(ast_node.children[1])
    if arg2 == '':
      arg2 = ast_node.children[1].value
    arg = str(newtemp())
    arg3 = ShiftOP(str(arg) ,str(arg1) , ast_node.children[2].value, str(arg2))
    code = code +'\t' + str(arg3) +'\n'

  # elif ast_node.name == 'Relation':
  #   if ast_node.children[1] is not None: 
  #     traverse_tree(ast_node.children[1])
  #   arg = newtemp()
  #   arg1 = BinOp(str(arg),ast_node.children[0].value,ast_node.children[2].value,ast_node.children[1].value)
  #   code = code +'\t' + str(arg1) +'\n'

  # elif ast_node.name == 'UnaryOperator':

  elif ast_node.name == 'EqualityExpression':
    arg2 = traverse_tree(ast_node.children[1])
    if arg2 == '':
      arg2 = ast_node.children[1].value
    arg = newtemp()
    arg3 = BinOp(str(arg), ast_node.children[0].value, ast_node.children[2].value, arg2)
    code = code +'\t' + str(arg3) +'\n'

  # elif ast_node.name == ('AND' or 'Exclusive OR' or'Inclusive OR'):
  #   if ast_node.children[1] is not None: 
  #     traverse_tree(ast_node.children[1])
  #   arg = newtemp()
  #   arg1 = BinOp(arg,ast_node.children[0].value,'*//',ast_node.children[1].value)
  #   code = code +'\t' + str(arg1) +'\n'

  # elif ast_node.name == ('Logical AND' or'Logical OR'):
  #   if ast_node.children[1] is not None: 
  #     traverse_tree(ast_node.children[1])
  #   arg = newtemp()
  #   arg1 = BinOp(arg,ast_node.children[0].value,'*//',ast_node.children[1].value)
  #   code = code +'\t' + str(arg1) +'\n'

  # elif ast_node.name == 'ArrayAccess':

  # elif ast_node.name == 'ArrayDeclaration':

  # elif ast_node.name == 'InitializerList':

  # elif ast_node.name == 'RETURN_EXPRESSION':

  # elif ast_node.name == 'Ternary Operation':

  # elif ast_node.name == 'StructReference':

  # elif ast_node.name == 'Pointer Dereference':

  # elif ast_node.name == 'Address Of Operationx':
  else:
    if len(ast_node.children) > 0 :
      for child in ast_node.children :
        if child is not None:
          traverse_tree(child)
  return str(arg)

traverse_tree(root)
print code