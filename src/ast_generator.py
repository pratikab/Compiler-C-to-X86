import cparser.py
import parsetab.py

# ------------------------------------------------------------
#	This code generates the following :-				
# 	1. Global Symbol Tables								
#	2. Local Symbol Tables for indivisual functions		
#	3. Abstract Syntax Tree (AST) 						
#-------------------------------------------------------------

class Node(object):
	# List of all the attributes
	attributes = []
	"""docstring for Node"""
	# Constructing nodes
	def __init__(self, arg):
		super(Node, self).__init__()
		self.arg = arg

	# Display the nodes hanging on the sub-tree of the "node"

class Visitor(object):
	# Will contain methods to traverse different type of nodes



class ArrayDecl(Node):
#    __slots__ = ('type', 'dim', 'dim_quals', 'coord', '__weakref__')
    def __init__(self, type, dim, dim_quals, coord=None):
        self.type = type
        self.dim = dim
        self.dim_quals = dim_quals
        self.coord = coord

    attr_names = ('dim_quals', )

class ArrayRef(Node):
#    __slots__ = ('name', 'subscript', 'coord', '__weakref__')
    def __init__(self, name, subscript, coord=None):
        self.name = name
        self.subscript = subscript
        self.coord = coord
    attr_names = ()

class Assignment(Node):
#    __slots__ = ('op', 'lvalue', 'rvalue', 'coord', '__weakref__')
    def __init__(self, op, lvalue, rvalue, coord=None):
        self.op = op
        self.lvalue = lvalue
        self.rvalue = rvalue
        self.coord = coord
    attr_names = ('op', )

class BinaryOp(Node):
#    __slots__ = ('op', 'left', 'right', 'coord', '__weakref__')
    def __init__(self, op, left, right, coord=None):
        self.op = op
        self.left = left
        self.right = right
        self.coord = coord
    attr_names = ('op', )

class Break(Node):
#    __slots__ = ('coord', '__weakref__')
    def __init__(self, coord=None):
        self.coord = coord
    attr_names = ()

class Case(Node):
#    __slots__ = ('expr', 'stmts', 'coord', '__weakref__')
    def __init__(self, expr, stmts, coord=None):
        self.expr = expr
        self.stmts = stmts
        self.coord = coord
    attr_names = ()

class Cast(Node):
#    __slots__ = ('to_type', 'expr', 'coord', '__weakref__')
    def __init__(self, to_type, expr, coord=None):
        self.to_type = to_type
        self.expr = expr
        self.coord = coord
    attr_names = ()

class Compound(Node):
#    __slots__ = ('block_items', 'coord', '__weakref__')
    def __init__(self, block_items, coord=None):
        self.block_items = block_items
        self.coord = coord
    attr_names = ()

class CompoundLiteral(Node):
#    __slots__ = ('type', 'init', 'coord', '__weakref__')
    def __init__(self, type, init, coord=None):
        self.type = type
        self.init = init
        self.coord = coord
    attr_names = ()

class Constant(Node):
#    __slots__ = ('type', 'value', 'coord', '__weakref__')
    def __init__(self, type, value, coord=None):
        self.type = type
        self.value = value
        self.coord = coord
    attr_names = ('type', 'value', )

class Continue(Node):
#    __slots__ = ('coord', '__weakref__')
    def __init__(self, coord=None):
        self.coord = coord
    attr_names = ()

class Decl(Node):
#    __slots__ = ('name', 'quals', 'storage', 'funcspec', 'type', 'init', 'bitsize', 'coord', '__weakref__')
    def __init__(self, name, quals, storage, funcspec, type, init, bitsize, coord=None):
        self.name = name
        self.quals = quals
        self.storage = storage
        self.funcspec = funcspec
        self.type = type
        self.init = init
        self.bitsize = bitsize
        self.coord = coord
    attr_names = ('name', 'quals', 'storage', 'funcspec', )

class DeclList(Node):
#    __slots__ = ('decls', 'coord', '__weakref__')
    def __init__(self, decls, coord=None):
        self.decls = decls
        self.coord = coord
    attr_names = ()

class Default(Node):
#    __slots__ = ('stmts', 'coord', '__weakref__')
    def __init__(self, stmts, coord=None):
        self.stmts = stmts
        self.coord = coord
    attr_names = ()

class DoWhile(Node):
#    __slots__ = ('cond', 'stmt', 'coord', '__weakref__')
    def __init__(self, cond, stmt, coord=None):
        self.cond = cond
        self.stmt = stmt
        self.coord = coord
    attr_names = ()

class EllipsisParam(Node):
#    __slots__ = ('coord', '__weakref__')
    def __init__(self, coord=None):
        self.coord = coord
    attr_names = ()

class EmptyStatement(Node):
#    __slots__ = ('coord', '__weakref__')
    def __init__(self, coord=None):
        self.coord = coord
    attr_names = ()

class Enum(Node):
#    __slots__ = ('name', 'values', 'coord', '__weakref__')
    def __init__(self, name, values, coord=None):
        self.name = name
        self.values = values
        self.coord = coord
    attr_names = ('name', )

class Enumerator(Node):
#    __slots__ = ('name', 'value', 'coord', '__weakref__')
    def __init__(self, name, value, coord=None):
        self.name = name
        self.value = value
        self.coord = coord
    attr_names = ('name', )

class EnumeratorList(Node):
#    __slots__ = ('enumerators', 'coord', '__weakref__')
    def __init__(self, enumerators, coord=None):
        self.enumerators = enumerators
        self.coord = coord
    attr_names = ()

class ExprList(Node):
#    __slots__ = ('exprs', 'coord', '__weakref__')
    def __init__(self, exprs, coord=None):
        self.exprs = exprs
        self.coord = coord
    attr_names = ()

class FileAST(Node):
#    __slots__ = ('ext', 'coord', '__weakref__')
    def __init__(self, ext, coord=None):
        self.ext = ext
        self.coord = coord
    attr_names = ()

class For(Node):
#    __slots__ = ('init', 'cond', 'next', 'stmt', 'coord', '__weakref__')
    def __init__(self, init, cond, next, stmt, coord=None):
        self.init = init
        self.cond = cond
        self.next = next
        self.stmt = stmt
        self.coord = coord
    attr_names = ()

class FuncCall(Node):
#    __slots__ = ('name', 'args', 'coord', '__weakref__')
    def __init__(self, name, args, coord=None):
        self.name = name
        self.args = args
        self.coord = coord
    attr_names = ()

class FuncDecl(Node):
#    __slots__ = ('args', 'type', 'coord', '__weakref__')
    def __init__(self, args, type, coord=None):
        self.args = args
        self.type = type
        self.coord = coord
    attr_names = ()

class FuncDef(Node):
#    __slots__ = ('decl', 'param_decls', 'body', 'coord', '__weakref__')
    def __init__(self, decl, param_decls, body, coord=None):
        self.decl = decl
        self.param_decls = param_decls
        self.body = body
        self.coord = coord
    attr_names = ()

class Goto(Node):
#    __slots__ = ('name', 'coord', '__weakref__')
    def __init__(self, name, coord=None):
        self.name = name
        self.coord = coord
    attr_names = ('name', )

class ID(Node):
#    __slots__ = ('name', 'coord', '__weakref__')
    def __init__(self, name, coord=None):
        self.name = name
        self.coord = coord
    attr_names = ('name', )

class IdentifierType(Node):
#    __slots__ = ('names', 'coord', '__weakref__')
    def __init__(self, names, coord=None):
        self.names = names
        self.coord = coord
    attr_names = ('names', )

class If(Node):
#    __slots__ = ('cond', 'iftrue', 'iffalse', 'coord', '__weakref__')
    def __init__(self, cond, iftrue, iffalse, coord=None):
        self.cond = cond
        self.iftrue = iftrue
        self.iffalse = iffalse
        self.coord = coord
    attr_names = ()

class InitList(Node):
#    __slots__ = ('exprs', 'coord', '__weakref__')
    def __init__(self, exprs, coord=None):
        self.exprs = exprs
        self.coord = coord
    attr_names = ()

class Label(Node):
#    __slots__ = ('name', 'stmt', 'coord', '__weakref__')
    def __init__(self, name, stmt, coord=None):
        self.name = name
        self.stmt = stmt
        self.coord = coord
    attr_names = ('name', )

class NamedInitializer(Node):
#    __slots__ = ('name', 'expr', 'coord', '__weakref__')
    def __init__(self, name, expr, coord=None):
        self.name = name
        self.expr = expr
        self.coord = coord
    attr_names = ()

class ParamList(Node):
#    __slots__ = ('params', 'coord', '__weakref__')
    def __init__(self, params, coord=None):
        self.params = params
        self.coord = coord
    attr_names = ()

class PtrDecl(Node):
#    __slots__ = ('quals', 'type', 'coord', '__weakref__')
    def __init__(self, quals, type, coord=None):
        self.quals = quals
        self.type = type
        self.coord = coord
    attr_names = ('quals', )

class Return(Node):
#    __slots__ = ('expr', 'coord', '__weakref__')
    def __init__(self, expr, coord=None):
        self.expr = expr
        self.coord = coord
    attr_names = ()

class Struct(Node):
#    __slots__ = ('name', 'decls', 'coord', '__weakref__')
    def __init__(self, name, decls, coord=None):
        self.name = name
        self.decls = decls
        self.coord = coord
    attr_names = ('name', )

class StructRef(Node):
#    __slots__ = ('name', 'type', 'field', 'coord', '__weakref__')
    def __init__(self, name, type, field, coord=None):
        self.name = name
        self.type = type
        self.field = field
        self.coord = coord
    attr_names = ('type', )

class Switch(Node):
#    __slots__ = ('cond', 'stmt', 'coord', '__weakref__')
    def __init__(self, cond, stmt, coord=None):
        self.cond = cond
        self.stmt = stmt
        self.coord = coord
    attr_names = ()

class TernaryOp(Node):
#    __slots__ = ('cond', 'iftrue', 'iffalse', 'coord', '__weakref__')
    def __init__(self, cond, iftrue, iffalse, coord=None):
        self.cond = cond
        self.iftrue = iftrue
        self.iffalse = iffalse
        self.coord = coord
    attr_names = ()

class TypeDecl(Node):
#    __slots__ = ('declname', 'quals', 'type', 'coord', '__weakref__')
    def __init__(self, declname, quals, type, coord=None):
        self.declname = declname
        self.quals = quals
        self.type = type
        self.coord = coord
    attr_names = ('declname', 'quals', )

class Typedef(Node):
#    __slots__ = ('name', 'quals', 'storage', 'type', 'coord', '__weakref__')
    def __init__(self, name, quals, storage, type, coord=None):
        self.name = name
        self.quals = quals
        self.storage = storage
        self.type = type
        self.coord = coord
    attr_names = ('name', 'quals', 'storage', )

class Typename(Node):
#    __slots__ = ('name', 'quals', 'type', 'coord', '__weakref__')
    def __init__(self, name, quals, type, coord=None):
        self.name = name
        self.quals = quals
        self.type = type
        self.coord = coord
    attr_names = ('name', 'quals', )

class UnaryOp(Node):
#    __slots__ = ('op', 'expr', 'coord', '__weakref__')
    def __init__(self, op, expr, coord=None):
        self.op = op
        self.expr = expr
        self.coord = coord
    attr_names = ('op', )

class Union(Node):
#    __slots__ = ('name', 'decls', 'coord', '__weakref__')
    def __init__(self, name, decls, coord=None):
        self.name = name
        self.decls = decls
        self.coord = coord
    attr_names = ('name', )

class While(Node):
#    __slots__ = ('cond', 'stmt', 'coord', '__weakref__')
    def __init__(self, cond, stmt, coord=None):
        self.cond = cond
        self.stmt = stmt
        self.coord = coord
    attr_names = ()

class Pragma(Node):
#    __slots__ = ('string', 'coord', '__weakref__')
    def __init__(self, string, coord=None):
        self.string = string
        self.coord = coord
    attr_names = ('string', )