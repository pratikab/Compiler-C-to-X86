#!/usr/bin/python
import sys
import cparser
import three_addr_code_generation
fout = open("../test/a.s", "wb")
with open ("../test/lib.s", 'r') as myfile:
      data=myfile.read()
fout.write(data)

root, symbol_table = three_addr_code_generation.main()

for temp in symbol_table:
  print temp, '\n'

def get_argc_symbol_table(variable,scope_name):
  for hash_table in symbol_table:
    if hash_table['scope_name'] == scope_name:
      if variable in hash_table.keys():
        return hash_table[variable][1].split(' ')[1]
      elif scope_name == 's0':
        print 'Variable not found in symbol table exiting'
        sys.exit()
      else:
        return get_argc_symbol_table(variable,hash_table['parent_scope_name'])

def get_allo_symbol_table(variable,scope_name):
  for hash_table in symbol_table:
    if hash_table['scope_name'] == scope_name:
      if variable in hash_table.keys():
        k = hash_table[variable][1].split(' ')[2]
        return k
      elif scope_name == 's0':
        print 'Variable not found in symbol table exiting'
        sys.exit()
      else:
        return get_allo_symbol_table(variable,hash_table['parent_scope_name'])


def get_offset_symbol_table(variable,scope_name):
  for hash_table in symbol_table:
    if hash_table['scope_name'] == scope_name:
      if variable in hash_table.keys():
        if(hash_table[variable][1].startswith('Function')):
          return ''
        return hash_table[variable][8]
      elif scope_name == 's0':
        print 'Variable not found in symbol table exiting'
        sys.exit()
      else:
        return get_offset_symbol_table(variable,hash_table['parent_scope_name'])

def set_address_symbol_table(variable,scope_name,address):
  for index,hash_table in enumerate(symbol_table):
    if hash_table['scope_name'] == scope_name:
      if variable in hash_table.keys():
        symbol_table[index][variable].append(address)
        # print symbol_table[index][variable]
      elif scope_name == 's0':
        print 'Variable not found in symbol table exiting'
        sys.exit()
      else:
        set_address_symbol_table(variable,hash_table['parent_scope_name'],address)
def get_array_symbol_table(variable,scope_name):
  for hash_table in symbol_table:
    if hash_table['scope_name'] == scope_name:
      if variable in hash_table.keys():
        return hash_table[variable][7]
      elif scope_name == 's0':
        print 'Variable not found in symbol table exiting'
        sys.exit()
      else:
        return get_array_symbol_table(variable,hash_table['parent_scope_name'])
count_label = 0
count_temp = 0
data = ''


class label(object):
  def __init__(self,_id = 0,name=''):
    global count_label
    self._id = count_label;
    if name == '':
      name = 'L' + str(count_label) 
      count_label = count_label + 1;
    self.name = name
  def __repr__(self):
    return (self.name+':')

class newtemp(object):
  def __init__(self,_id = 0):
    global count_temp
    self.count = count_temp
    self._id = count_temp;
    count_temp = count_temp + 1;
  def __repr__(self):
    p = 'T' + str(self.count)
    return p

class Assignment():
  """docstring for Assignment"""
  def __init__(self,source='',sourceadd='', destination='',destinationadd=''):
    global data
    self.source = source
    self.destination = destination
    
    if sourceadd.startswith('array'):
      k = sourceadd.split(" ")[1]
      data = data + '\tmov eax, '+k+'\n'   
    if destinationadd != '':
      if destinationadd.startswith("array"):
        y = destinationadd.split(" ")[1]
        data = data + '\tmov edx, '+y+'\n'
        data = data + '\tmov ecx, [edx]\n'
      else:
        data = data + '\tmov ecx, '+destinationadd+'\n'
    else:
      data = data + '\tmov ecx, '+destination+'\n'
    if sourceadd.startswith('array'):
      data = data + '\tmov [eax]'+', ecx'+'\n'
    else:
      data = data + '\tmov '+sourceadd+', ecx'+'\n'
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
  def __init__(self,destination='',source_1='',source_1add='',operand='',source_2='',source_2add=''):
    global data
    self.source_1 = source_1
    self.source_2 = source_2
    self.operand = operand
    self.destination = destination
    source1 = source_1
    source2 = source_2
    if source_1add != '':
      source1 = source_1add
    if source_2add != '':
      source2 = source_2add
    # print source1,source2
    if source1.startswith("array"):
      k = source1.split(" ")[1]
      data = data + '\tmov eax, '+k+'\n'
      data = data + '\tmov eax, [eax]\n'
    else:
      data = data + '\tmov eax, ' + str(source1)+'\n'
    if source2.startswith("array"):
      k = source2.split(" ")[1]
      data = data + '\tmov ecx, '+k+'\n'
      data = data + '\tmov ecx, [ecx]\n'
    else:
      data = data + '\tmov ecx, ' + str(source2)+'\n'
    if operand == '+':
      
      data = data + '\tadd eax, ecx\n'
    if operand == '-':
      data = data + '\tsub eax, ecx\n'
    if operand == '*':
      data = data + '\timul eax, ecx\n'
    if operand == '/':
      data = data + '\tcdq\n'
      data = data + '\tidiv ecx\n'
    if operand == '%':
      data = data + '\tcdq\n'
      data = data + '\tidiv ecx\n'
    if operand == '==':
      data = data + '\tcmp eax, ecx\n'
      data = data + '\tsete al\n'
      data = data + '\tmovzx eax, '+'al'+'\n'
    if operand == '<':
      data = data + '\tcmp eax, ecx\n'
      data = data + '\tsetl al\n'
      data = data + '\tmovzx eax, '+'al'+'\n'
    if operand == '>':
      data = data + '\tcmp eax, ecx\n'
      data = data + '\tsetg al\n'
      data = data + '\tmovzx eax, '+'al'+'\n'
    if operand == '<=':
      data = data + '\tcmp eax, ecx\n'
      data = data + '\tsetle al\n'
      data = data + '\tmovzx eax, '+'al'+'\n'
    if operand == '>=':
      data = data + '\tcmp eax, ecx\n'
      data = data + '\tsetge al\n'
      data = data + '\tmovzx eax, '+'al'+'\n'
    if operand == '&':
      data = data + '\tand eax, ecx\n'
    if operand == '|':
      data = data + '\tor eax, ecx\n'
    if operand == '^':
      data = data + '\txor eax, ecx\n'
    if operand == '&&':
      data = data + '\tmovzx eax, al'+'\n'
    if operand == '||':
      data = data + '\tmovzx eax, al'+'\n'

    data = data + '\tmov '+destination+', eax'+'\n'


  def __repr__(self):
    return self.destination + ' = ' + self.source_1 + self.operand + self.source_2

def Jump(arg, arg2):
  global data
  if(arg2 == 'je'):
    data = data + '\tje '+str(arg).rstrip(':')+'\n'
  if(arg2 == 'jmp'):
    data = data + '\tjmp '+str(arg).rstrip(':')+'\n'
  if(arg2 == 'jne'):
    data = data + '\tjne '+str(arg).rstrip(':')+'\n'


def Compare(arg1,add1,arg2,add2):
  global data
  a1 = arg1
  a2 = arg2
  data = data + '\txor ebx, ebx'+'\n'
  data = data + '\txor ecx, ecx'+'\n'

  if add1 != '':
      a1 = add1
  if add2 != '':
      a2 = add2
  if a1.startswith("array"):
    k = a1.split(" ")[1]
    data = data + '\tmov ebx, '+k+'\n'
    data = data + '\tmov ebx, [ebx]\n'
  else:
    data = data + '\tmov ebx, ' + str(a1)+'\n'
  if a2.startswith("array"):
    k = a2.split(" ")[1]
    data = data + '\tmov ecx, '+k+'\n'
    data = data + '\tmov ecx, [ecx]\n'
  else:
    data = data + '\tmov ecx, ' + str(a2)+'\n'
  data = data + '\tcmp ebx, ecx\n'


def PushParam(arg1,add1):
  global data
  a1 = arg1

  if add1 != '':
      a1 = add1
  if a1.startswith("array"):
    k = a1.split(" ")[1]
    data = data + '\tmov eax, '+k+'\n'
    data = data + '\tmov eax, [eax]\n'
  else:
    data = data + '\tmov eax, ' + str(a1)+'\n'

  data = data + '\tpush eax'+'\n'

def FuncCall(arg1,add1):
  global data
  k = int(get_argc_symbol_table(str(arg1.value),'s0'))
  # print "+++",get_argc_symbol_table(str(arg1.value),'s0')
  data = data + '\tcall ' + str(arg1.value) + '\n'
  for i in range(0,k):
    data = data + '\tpop edx'+'\n'
  data = data + '\tmov '+add1+ ', eax\n'
def BeginFunc(offset):
  global data
  data = data + '\tpush ebp'+'\n'
  data = data + '\tmov ebp, esp'+'\n'
  data = data + '\tsub esp, '+ str(offset)+'\n'
def EndFunc(offset):
  global data
  data = data + '\tadd esp, '+ str(offset)+'\n'
  data = data + '\tpop ebp'+'\n'
  data = data + '\tret'+'\n'
def Ret(arg1, add1,offset):
  global data
  if add1 == '':
    data = data + '\tmov eax, '+ arg1+'\n'
  else:
    data = data + '\tmov eax, '+ add1+'\n'
  EndFunc(offset)

offset = 0;
def traverse_tree(ast_node, nextlist ,breaklist):
  global data,offset
  arg = ''
  add = ''
  if ast_node.name == 'VarAccess':
    arg = ast_node.value
    add = get_offset_symbol_table(ast_node.value,ast_node.scope_name)
    # pass
  elif ast_node.name == 'ConstantLiteral':
    arg = ast_node.value
  if ast_node.name == 'IF Statement':
    E_next = label(name = ast_node.value)
    E_true = label(name = ast_node.value)
    
    arg1,add1 = traverse_tree(ast_node.children[0], nextlist ,breaklist)
    Compare(arg1,add1,'0','')
    Jump(E_next, "je")
    
    data = data + str(E_true) + '\n'

    traverse_tree(ast_node.children[1], nextlist ,breaklist)
    Jump(E_next,"jmp")
    
    data = data + str(E_next) + '\n'


  elif ast_node.name == 'IF-Else Statement':
    E_next = label(name = ast_node.value)
    E_true = label(name = ast_node.value)
    E_false = label(name = ast_node.value)

    arg1,add1 = traverse_tree(ast_node.children[0], nextlist ,breaklist)
    Compare(arg1,add1,'0','')
    Jump(E_false,"je")
    
    data = data + str(E_true) + '\n'

    traverse_tree(ast_node.children[1], nextlist ,breaklist)
    Jump(E_next,"jmp")

    data = data + str(E_false) + '\n'

    traverse_tree(ast_node.children[2], nextlist ,breaklist)

    data = data + str(E_next) + '\n'

  elif ast_node.name == 'While Statement':
    E_next = label(name = ast_node.value)
    E_begin = label(name = ast_node.value)

    data = data + str(E_begin) + '\n'
    
    arg1,add1 = traverse_tree(ast_node.children[0], nextlist ,breaklist)
    Compare(arg1,add1,'0','')
    Jump(E_next,"je")
    
    traverse_tree(ast_node.children[1], E_begin ,E_next)
    Jump(E_begin,"jmp")

    data = data + str(E_next) + '\n'

  elif ast_node.name == 'BREAK':
    Jump(breaklist,"jmp")
  elif ast_node.name == 'CONTINUE':
    Jump(nextlist,"jmp")

  elif ast_node.name == 'ForStatement3Exp':
    traverse_tree(ast_node.children[0], nextlist ,breaklist)

    E_next = label(name = ast_node.value)
    E_begin = label(name = ast_node.value)
    E_end = label(name = ast_node.value)

    data = data + str(E_begin) + '\n'

    arg1,add1 = traverse_tree(ast_node.children[1], nextlist ,breaklist)
    Compare(arg1,add1,'0','')
    Jump(E_next,"je")

    traverse_tree(ast_node.children[3], E_end ,E_next)

    data = data + str(E_end) + '\n'

    traverse_tree(ast_node.children[2], nextlist ,breaklist)
    Jump(E_begin,"jmp")

    data = data + str(E_next) + '\n'

  elif ast_node.name == 'VarDecl and Initialise':
    add2 = get_offset_symbol_table(ast_node.children[0].value,ast_node.scope_name)
    arg1= ''
    add1= ''
    if ast_node.children[1] is not None: 
      arg1,add1 = traverse_tree(ast_node.children[1], nextlist ,breaklist)
    Assignment(ast_node.children[0].value,add2,arg1,add1)

  elif ast_node.name == 'Argument List':
    if len(ast_node.children) > 0 :
      for child in ast_node.children[::-1]:
        if child is not None: 
          arg1,add1 = traverse_tree(child, nextlist ,breaklist)
          PushParam(arg1,add1)

  elif ast_node.name == 'FuncCall':
    
    arg = str(newtemp())
    add = get_offset_symbol_table(arg,'s0')
    FuncCall(ast_node.children[0],add)

  elif ast_node.name == 'FuncCallwithArgs':
    if len(ast_node.children) > 0 :
      for child in ast_node.children :
        traverse_tree(child, nextlist ,breaklist)

    arg = str(newtemp())
    add = get_offset_symbol_table(arg,'s0')
    FuncCall(ast_node.children[0],add)

  elif ast_node.name == 'Function_definition':
    offset = get_allo_symbol_table(ast_node.value,'s0')
    arg1 = label(name = ast_node.value) 

    data = data + str(arg1) + '\n'
    BeginFunc(offset)
    if len(ast_node.children) > 0 :
      for child in ast_node.children :
        if child is not None: 
          traverse_tree(child, nextlist ,breaklist)
    EndFunc(offset)
  # elif ast_node.name == 'paramater':
  #   PopParam(ast_node.value)

  elif ast_node.name == 'RETURN_EXPRESSION':
    arg1,add1 = traverse_tree(ast_node.children[0], nextlist ,breaklist)
    Ret(arg1,add1,offset)
  elif ast_node.name == 'RETURN':
    Ret(0, '',offset)

  elif ast_node.name == 'Assignment':
    arg2,add2 = traverse_tree(ast_node.children[0], nextlist ,breaklist)
    arg1,add1 = traverse_tree(ast_node.children[1], nextlist ,breaklist)
    Assignment(ast_node.children[0].value, add2, arg1, add1)
    arg = arg1
    add = add1

  elif ast_node.name in {'Addition','Multiplication','Modulus Operation',
    'Shift','Relation','EqualityExpression','AND', 'Exclusive OR','Inclusive OR'}:
    arg1,add1 = traverse_tree(ast_node.children[0], nextlist ,breaklist)
    arg2,add2 = traverse_tree(ast_node.children[1], nextlist ,breaklist)
    arg = str(newtemp())
    add = get_offset_symbol_table(arg,'s0')
    BinOp(add,str(arg1),add1,ast_node.children[2].value,str(arg2),add2)

  elif ast_node.name == 'Logical AND':
    arg1,add1 = traverse_tree(ast_node.children[0], nextlist ,breaklist)
    arg2,add2 = traverse_tree(ast_node.children[1], nextlist ,breaklist)

    arg = str(newtemp())
    add = get_offset_symbol_table(arg,'s0')

    E_next = label(name = ast_node.value)
    E_true = label(name = ast_node.value)

    Compare(arg1,add1,'0','')
    Jump(E_next,"je")
    Compare(arg2,add2,'0','')
    Jump(E_next,"je")

    data = data + "\tmov eax, 1"+'\n'
    Jump(E_true,"jmp")

    data = data + str(E_next) + '\n'
    data = data + "\tmov eax, 0"+'\n'

    data = data + str(E_true) + '\n'
    BinOp(add,str(arg1),add1,ast_node.children[2].value,str(arg2),add2)
  elif ast_node.name == 'Logical OR':
    arg1,add1 = traverse_tree(ast_node.children[0], nextlist ,breaklist)
    arg2,add2 = traverse_tree(ast_node.children[1], nextlist ,breaklist)

    arg = str(newtemp())
    add = get_offset_symbol_table(arg,'s0')

    E_next = label(name = ast_node.value)
    E_true = label(name = ast_node.value)
    E_false = label(name = ast_node.value)

    Compare(arg1,add1,'0','')
    Jump(E_false,"jne")
    Compare(arg2,add2,'0','')
    Jump(E_true,"je")

    data = data + str(E_false) + '\n'
    data = data + "\tmov eax, 1"+'\n'
    Jump(E_next,"jmp")
    data = data + str(E_true) + '\n'
    data = data + "\tmov eax, 0"+'\n'
    data = data + str(E_next) + '\n'

    BinOp(add,str(arg1),add1,ast_node.children[2].value,str(arg2),add2)

  elif ast_node.name == 'UnaryOperator':
    arg1,add1 = traverse_tree(ast_node.children[0], nextlist ,breaklist)
    arg = str(newtemp())
    add = get_offset_symbol_table(arg,'s0')
    if ast_node.children[1].value == '++':
      BinOp(add,str(arg1),add1, '+',str(1),'')
    elif ast_node.children[1].value == '--': 
      BinOp(add,str(arg1),add1, '-',str(1),'')
    Assignment(str(arg1), add1, str(arg), add)   


  elif ast_node.name == 'ArrayAccess':
    
    arr = get_array_symbol_table(ast_node.value,ast_node.scope_name)
    # print arr
    index = []
    mul_size = []
    for i in range (1,len(arr)):
      t = 1
      for j in range(i,len(arr)):
        t = t * arr[j]
      mul_size.append(t)
    mul_size.append(1)
    # print mul_size
    for i in range (0,len(arr)):
      k = ast_node
      for j in range (0,i):
        k = k.children[0]
      index.append(k.children[1])
    index = index[::-1]
    j = 0
    lis = []
    for i in index:
      # print i.value
      arg1 = str(newtemp())
      add1 = get_offset_symbol_table(arg1,'s0')
      add2 = get_offset_symbol_table(i.value,i.scope_name)
      if add2 == None:
        add2 = ''
      BinOp(add1,str(i.value),add2, '*',str(mul_size[j]),'')
      lis.append(add1)
      j = j+1
    arg2 = lis[0]
    for i in range (1,len(index)):
      arg1 = str(newtemp())
      add1 = get_offset_symbol_table(arg1,'s0')
      BinOp(add1,'',arg2, '+','',lis[i])
      arg2 = add1
    p = cparser.get_size(ast_node.type)
    arg1 = str(newtemp())
    add1 = get_offset_symbol_table(arg1,'s0')
    BinOp(add1,'',arg2, '*',str(p),'')
    f = get_offset_symbol_table(ast_node.value,ast_node.scope_name)
    f = f.split('-')[1].split(']')[0]
    print f,add1
    data = data + '\tmov edx, ebp\n'
    data = data + '\tsub edx, '+ f +'\n'
    data = data + '\tadd edx, '+add1+ '\n'

    arg1 = str(newtemp())
    add1 = get_offset_symbol_table(arg1,'s0')

    data = data + '\tmov '+add1+', edx\n'
    add = "array "+ add1
    arg = ''

    # add = ast_node.value + '+'+str(arg1)

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
  return str(arg), add

traverse_tree(root, None,None)

fout.write(data)