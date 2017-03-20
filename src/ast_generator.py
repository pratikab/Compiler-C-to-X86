# ------------------------------------------------------------
#	This code generates the following :-				
# 	1. Global Symbol Tables								
#	2. Local Symbol Tables for indivisual functions		
#	3. Abstract Syntax Tree (AST) 						
#-------------------------------------------------------------

class Node(object):
	# List of all the attributes
	attributes = []
# 	"""docstring for Node"""
# 	# Constructing nodes
# 	def __init__(self, arg):
# 		super(Node, self).__init__()
# 		self.arg = arg

# 	# Display the nodes hanging on the sub-tree of the "node"

# class Visitor(object):
# 	# Will contain methods to traverse different type of nodes



class ArrayDecl(Node):
#    __slots__ = ('type', 'dim', 'dim_quals', 'coord', '__weakref__')
    def __init__(self, type, dim, dim_quals):
        self.type = type
        self.dim = dim
        self.dim_quals = dim_quals


    attr_names = ['dim_quals']

class ArrayRef(Node):
#    __slots__ = ('name', 'subscript', 'coord', '__weakref__')
    def __init__(self, name, subscript):
        self.name = name
        self.subscript = subscript

    attr_names = []

class Assignment(Node):
#    __slots__ = ('op', 'lvalue', 'rvalue', 'coord', '__weakref__')
    def __init__(self, op, lvalue):
        self.op = op
        self.lvalue = lvalue
        self.rvalue = rvalue
        # self.coord = coord
    attr_names = ['op']

class BinaryOp(Node):
#    __slots__ = ('op', 'left', 'right', 'coord', '__weakref__')
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    attr_names = ['op']

class Break(Node):
#    __slots__ = ('coord', '__weakref__')
    # def __init__(self):

    attr_names = []

class Case(Node):
#    __slots__ = ('expr', 'stmts', 'coord', '__weakref__')
    def __init__(self, expr, stmts):
        self.expr = expr
        self.stmts = stmts

    attr_names = []

class Cast(Node):
#    __slots__ = ('to_type', 'expr', 'coord', '__weakref__')
    def __init__(self, to_type, expr):
        self.to_type = to_type
        self.expr = expr

    attr_names = []

class Compound(Node):
#    __slots__ = ('block_items', 'coord', '__weakref__')
    def __init__(self, block_items):
        self.block_items = block_items

    attr_names = []

class CompoundLiteral(Node):
#    __slots__ = ('type', 'init', 'coord', '__weakref__')
    def __init__(self, type, init):
        self.type = type
        self.init = init

    attr_names = []

class Constant(Node):
#    __slots__ = ('type', 'value', 'coord', '__weakref__')
    def __init__(self, type, value):
        self.type = type
        self.value = value
        # self.coord = coord
    attr_names = ['type', 'value']

class Continue(Node):
#    __slots__ = ('coord', '__weakref__')
    # def __init__(self):

    attr_names = []

class Decl(Node):
#	__slots__ = ('name', 'quals', 'storage', 'funcspec', 'type', 'init', 'bitsize', 'coord', '__weakref__')
	def __init__(self, name, quals, storage, funcspec, type, init, bitsize):
		self.name = name
		self.quals = quals
		self.storage = storage
		self.funcspec = funcspec
		self.type = type
		self.init = init
		self.bitsize = bitsize

	attr_names = ['name', 'quals', 'storage', 'funcspec']

class DeclList(Node):
#    __slots__ = ('decls', 'coord', '__weakref__')
    def __init__(self, decls):
        self.decls = decls

    attr_names = []

class Default(Node):
#    __slots__ = ('stmts', 'coord', '__weakref__')
    def __init__(self, stmts):
        self.stmts = stmts

    attr_names = []

class DoWhile(Node):
#    __slots__ = ('cond', 'stmt', 'coord', '__weakref__')
    def __init__(self, cond, stmt):
        self.cond = cond
        self.stmt = stmt

    attr_names = []

class EllipsisParam(Node):
#    __slots__ = ('coord', '__weakref__')
    # def __init__(self):

    attr_names = []

class EmptyStatement(Node):
#    __slots__ = ('coord', '__weakref__')
    # def __init__(self):

    attr_names = []

class Enum(Node):
#    __slots__ = ('name', 'values', 'coord', '__weakref__')
    def __init__(self, name, values):
        self.name = name
        self.values = values

    attr_names = ['name']

class Enumerator(Node):
#    __slots__ = ('name', 'value', 'coord', '__weakref__')
    def __init__(self, name, value):
        self.name = name
        self.value = value

    attr_names = ['name']

class EnumeratorList(Node):
#    __slots__ = ('enumerators', 'coord', '__weakref__')
    def __init__(self, enumerators):
        self.enumerators = enumerators

    attr_names = []

class ExprList(Node):
#    __slots__ = ('exprs', 'coord', '__weakref__')
    def __init__(self, exprs):
        self.exprs = exprs
    attr_names = []

class FileAST(Node):
#    __slots__ = ('ext', 'coord', '__weakref__')
    def __init__(self, ext):
        self.ext = ext

    attr_names = []

class For(Node):
#    __slots__ = ('init', 'cond', 'next', 'stmt', 'coord', '__weakref__')
    def __init__(self, init, cond, next, stmt):
        self.init = init
        self.cond = cond
        self.next = next
        self.stmt = stmt

    attr_names = []

class FuncCall(Node):
#    __slots__ = ('name', 'args', 'coord', '__weakref__')
    def __init__(self, name, args):
        self.name = name
        self.args = args

    attr_names = []

class FuncDecl(Node):
#    __slots__ = ('args', 'type', 'coord', '__weakref__')
    def __init__(self, args, type):
        self.args = args
        self.type = type

    attr_names = []

class FuncDef(Node):
#    __slots__ = ('decl', 'param_decls', 'body', 'coord', '__weakref__')
    def __init__(self, decl, param_decls, body):
        self.decl = decl
        self.param_decls = param_decls
        self.body = body

    attr_names = []

class Goto(Node):
#    __slots__ = ('name', 'coord', '__weakref__')
    def __init__(self, name):
        self.name = name

    attr_names = ['name']

class ID(Node):
#    __slots__ = ('name', 'coord', '__weakref__')
    def __init__(self, name):
        self.name = name
        # self.coord = coord
    attr_names = ['name']

class IdentifierType(Node):
#    __slots__ = ('names', 'coord', '__weakref__')
    def __init__(self, names):
        self.names = names

    attr_names = ['names']

class If(Node):
#    __slots__ = ('cond', 'iftrue', 'iffalse', 'coord', '__weakref__')
    def __init__(self, cond, iftrue, iffalse):
        self.cond = cond
        self.iftrue = iftrue
        self.iffalse = iffalse

    attr_names = []

class InitList(Node):
#    __slots__ = ('exprs', 'coord', '__weakref__')
    def __init__(self, exprs):
        self.exprs = exprs

    attr_names = []

class Label(Node):
#    __slots__ = ('name', 'stmt', 'coord', '__weakref__')
    def __init__(self, name, stmt):
        self.name = name
        self.stmt = stmt

    attr_names = ['name']

class NamedInitializer(Node):
#    __slots__ = ('name', 'expr', 'coord', '__weakref__')
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    attr_names = []

class ParamList(Node):
#    __slots__ = ('params', 'coord', '__weakref__')
    def __init__(self, params):
        self.params = params

    attr_names = []

class PtrDecl(Node):
#    __slots__ = ('quals', 'type', 'coord', '__weakref__')
    def __init__(self, quals, type):
        self.quals = quals
        self.type = type

    attr_names = ['quals']

class Return(Node):
#    __slots__ = ('expr', 'coord', '__weakref__')
    def __init__(self, expr):
        self.expr = expr

    attr_names = []

class Struct(Node):
#    __slots__ = ('name', 'decls', 'coord', '__weakref__')
    def __init__(self, name, decls):
        self.name = name
        self.decls = decls

    attr_names = ['name']

class StructRef(Node):
#    __slots__ = ('name', 'type', 'field', 'coord', '__weakref__')
    def __init__(self, name, type, field):
        self.name = name
        self.type = type
        self.field = field

    attr_names = ['type']

class Switch(Node):
#    __slots__ = ('cond', 'stmt', 'coord', '__weakref__')
    def __init__(self, cond, stmt):
        self.cond = cond
        self.stmt = stmt

    attr_names = []

class TernaryOp(Node):
#    __slots__ = ('cond', 'iftrue', 'iffalse', 'coord', '__weakref__')
    def __init__(self, cond, iftrue, iffalse):
        self.cond = cond
        self.iftrue = iftrue
        self.iffalse = iffalse

    attr_names = []

class TypeDecl(Node):
#    __slots__ = ('declname', 'quals', 'type', 'coord', '__weakref__')
    def __init__(self, declname, quals, type):
        self.declname = declname
        self.quals = quals
        self.type = type

    attr_names = ['declname', 'quals']

class Typedef(Node):
#    __slots__ = ('name', 'quals', 'storage', 'type', 'coord', '__weakref__')
    def __init__(self, name, quals, storage, type):
        self.name = name
        self.quals = quals
        self.storage = storage
        self.type = type

    attr_names = ['name', 'quals', 'storage']

class Typename(Node):
#    __slots__ = ('name', 'quals', 'type', 'coord', '__weakref__')
    def __init__(self, name, quals, type):
        self.name = name
        self.quals = quals
        self.type = type

    attr_names = ['name', 'quals']

class UnaryOp(Node):
#    __slots__ = ('op', 'expr', 'coord', '__weakref__')
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    attr_names = ['op']

class Union(Node):
#    __slots__ = ('name', 'decls', 'coord', '__weakref__')
    def __init__(self, name, decls):
        self.name = name
        self.decls = decls

    attr_names = ['name']

class While(Node):
#    __slots__ = ('cond', 'stmt', 'coord', '__weakref__')
    def __init__(self, cond, stmt):
        self.cond = cond
        self.stmt = stmt

    attr_names = []

class Pragma(Node):
#    __slots__ = ('string', 'coord', '__weakref__')
    def __init__(self, string):
        self.string = string

    attr_names = ['string']
	"""docstring for Node"""
	# Constructing nodes
	def __init__(self, arg):
		super(Node, self).__init__()
		self.arg = arg

	# Display the nodes hanging on the sub-tree of the "node"
