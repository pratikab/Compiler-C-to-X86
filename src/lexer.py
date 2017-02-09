reserved = {
    'auto' : 'AUTO',
    'break' : 'BREAK',
    'case' : 'CASE',
    'char' : 'CHAR',
    'const' : 'CONST',
    'continue' : 'CONTINUE',
    'default' : 'DEFAULT',
    'do' : 'DO',
    'double' : 'DOUBLE',    
    'else' : 'ELSE',
    'enum' : 'ENUM',
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
}


tokens = list(reserved.values()) + [
    # RESERVED
    #'AUTO', 'BREAK', 'CASE', 'CHAR', 'CONST', 'CONTINUE', 'DEFAULT', 'DO', 'DOUBLE',
    #'ELSE', 'ENUM', 'EXTERN', 'FLOAT', 'FOR', 'GOTO', 'IF', 'INT', 'LONG', 'REGISTER',
    #'RETURN', 'SHORT', 'SIGNED', 'SIZEOF', 'STATIC', 'STRUCT', 'SWITCH', 'TYPEDEF',
    #'UNION', 'UNSIGNED', 'VOID', 'VOLATILE', 'WHILE',

    #OPERATORS 
    'ELLIPSIS','RIGHT_ASSIGN','LEFT_ASSIGN','ADD_ASIGN','SUB_ASSIGN','MUL_ASSIGN','DIV_ASSIGN',
    'MOD_ASSIGN','AND_ASSIGN','XOR_ASSIGN','OR_ASSIGN','RIGHT_OP','LEFT_OP','INC_OP','DEC_OP',
    'PTR_OP','AND_OP','OP_OP','LE_OP','GE_OP','EQ_OP','NE_OP','SEMICOLON','OPEN_CURLY','CLOSE_CURLY',
    'COMMA','COLON','EQUAL','OPEN_PAR','CLOSE_PAR','OPEN_SQUARE','CLOSE_SQUARE','DOT','AND','EXCLAIM',
    'NOT','MINUS','PLUS','MUL','DIVIDE','MOD','LESS_THAN','GREATER_THAN','XOR','OR','COND_OP',
    #LITERALS
    'ID','SCONST','CONSTANT',
]


# Tokens
D = r'[0-9]'
L = r'[a-zA-Z_]'
H = r'[a-fA-F0-9]'
E = r'[Ee][+-]?{D}+'
FS = r'(f|F|l|L)'
IS = r'(u|U|l|L)*'

t_ELLIPSIS = r'\.\.\.'
t_RIGHT_ASSIGN = r'>>='
t_LEFT_ASSIGN = r'<<='
t_ADD_ASIGN = r'\+='
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
t_OP_OP = r'\|\|'
t_LE_OP = r'<='
t_GE_OP = r'>='
t_EQ_OP = r'=='
t_NE_OP = r'!='
t_SEMICOLON = r';'
t_OPEN_CURLY = r'\{'
t_CLOSE_CURLY = r'\}'
t_COMMA = r','
t_COLON = r':'
t_EQUAL = r'='
t_OPEN_PAR = r'\('
t_CLOSE_PAR = r'\)'
t_OPEN_SQUARE = r'\['
t_CLOSE_SQUARE = r']'
t_DOT = r'.'
t_AND = r'&'
t_EXCLAIM = r'!'
t_NOT = r'~'
t_MINUS = r'-'
t_PLUS = r'\+'
t_MUL = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'
t_LESS_THAN = r'<'
t_GREATER_THAN = r'>'
t_XOR = r'\^'
t_OR = r'\|'
t_COND_OP = r'\?'

t_ignore = " \t\v\n\f"

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

def t_SCONST(t):
    r'L?\"(\\.|[^\\"])*\"'

def t_CONSTANT(t):
    r'(0[xX]{H}+{IS}?)|(0{D}+{IS}?)|({D}+{IS}?)|({D}+{E}{FS}?)|({D}*"."{D}+({E})?{FS}?)|({D}+"."{D}*({E})?{FS}?)'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)