reserved = {
    'auto' : 'AUTO',
    'break' : 'BREAK',
    'bool' : 'BOOL',
    'case' : 'CASE',
    'char' : 'CHAR',
    'const' : 'CONST',
    'continue' : 'CONTINUE',
    'default' : 'DEFAULT',
    'do' : 'DO',
    'double' : 'DOUBLE',    
    'else' : 'ELSE',
    'extern' : 'EXTERN',
    'float' : 'FLOAT',
    'for' : 'FOR',
    'goto' : 'GOTO',
    'if' : 'IF',
    'int' : 'INT',
    'long' : 'LONG',
    'register' : 'REGISTER',
    'return' : 'RETURN',
    'short' : 'SHORT',
    'signed' : 'SIGNED',
    'sizeof' : 'SIZEOF',
    'static' : 'STATIC',
    'struct' : 'STRUCT',
    'switch' : 'SWITCH',
    'typedef' : 'TYPEDEF',
    'union' : 'UNION',
    'unsigned' : 'UNSIGNED',
    'void' : 'VOID',
    'volatile' : 'VOLATILE',
    'while' : 'WHILE',
    'restrict' : 'RESTRICT',
    '_Complex' : 'COMPLEX', 
    '_Imaginary' : 'IMAGINARY',  
    '_Static_assert' : 'STATIC_ASSERT', 
}


tokens = list(reserved.values()) + [

    #OPERATORS 
    'RIGHT_ASSIGN','LEFT_ASSIGN','ADD_ASSIGN','SUB_ASSIGN','MUL_ASSIGN','DIV_ASSIGN',
    'MOD_ASSIGN','AND_ASSIGN','XOR_ASSIGN','OR_ASSIGN','RIGHT_OP','LEFT_OP','INC_OP','DEC_OP',
    'PTR_OP','AND_OP','OR_OP','LE_OP','GE_OP','EQ_OP','NE_OP',
    #LITERALS
    'IDENTIFIER','STRING_LITERAL', 'CONSTANT', 'CCONST',
]

literals = [';','{','}',',',':','=','(',')','[',']','.','&','!','~','-','+','*','/','%','<','>','^','|','?']

# Tokens
D = r'[0-9]'
L = r'[a-zA-Z_]'
H = r'[a-fA-F0-9]'
E = r'[Ee][+-]?{D}+'
FS = r'(f|F|l|L)'
IS = r'(u|U|l|L)*'

t_RIGHT_ASSIGN = r'>>='
t_LEFT_ASSIGN = r'<<='
t_ADD_ASSIGN = r'\+='
t_SUB_ASSIGN = r'-='
t_MUL_ASSIGN = r'\*='
t_DIV_ASSIGN = r'/='
t_MOD_ASSIGN = r'%='
t_AND_ASSIGN = r'&='
t_XOR_ASSIGN = r'\^='
t_OR_ASSIGN = r'\|='
t_RIGHT_OP = r'>>'
t_LEFT_OP = r'<<'
t_INC_OP = r'\+\+'
t_DEC_OP = r'--'
t_PTR_OP = r'->'
t_AND_OP = r'&&'
t_OR_OP = r'\|\|'
t_LE_OP = r'<='
t_GE_OP = r'>='
t_EQ_OP = r'=='
t_NE_OP = r'!='

t_ignore = " \t\v\f"

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'IDENTIFIER')    # Check for reserved words
    return t

# Integer Literal
def t_CONSTANT(t):
    r'\.?[0-9][0-9eE_lLdDa-fA-F.xXpP]*'
    return t

# String literal
def t_STRING_LITERAL(t):
    r'\"([^\\\n]|(\\.))*?\"'
    return t

# Character constant 'c' or L'c'
def t_CCONST(t): 
    r'(L)?\'([^\\\n]|(\\.))*?\''
    return t

def t_comment(t):
    r'(/\*(.|\n)*?\*/)|(//(.)*\n)'
    t.lexer.lineno += t.value.count('\n')

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_preprocessor(t):
    r'\#(.)*?\n'
    t.lexer.lineno += 1

def t_error(t):
    print("Illegal character '%s', lineno %s" % t.value[0] , t.lexer.lineno)
    t.lexer.skip(1)