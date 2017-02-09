
import pydot

tokens = (
    # RESERVED
    'AUTO', 'BREAK', 'CASE', 'CHAR', 'CONST', 'CONTINUE', 'DEFAULT', 'DO', 'DOUBLE',
    'ELSE', 'ENUM', 'EXTERN', 'FLOAT', 'FOR', 'GOTO', 'IF', 'INT', 'LONG', 'REGISTER',
    'RETURN', 'SHORT', 'SIGNED', 'SIZEOF', 'STATIC', 'STRUCT', 'SWITCH', 'TYPEDEF',
    'UNION', 'UNSIGNED', 'VOID', 'VOLATILE', 'WHILE',

    # OPERATORS 
    'ELLIPSIS','RIGHT_ASSIGN','LEFT_ASSIGN','ADD_ASIGN','SUB_ASSIGN','MUL_ASSIGN','DIV_ASSIGN',
    'MOD_ASSIGN','AND_ASSIGN','XOR_ASSIGN','OR_ASSIGN','RIGHT_OP','LEFT_OP','INC_OP','DEC_OP',
    'PTR_OP','AND_OP','OP_OP','LE_OP','GE_OP','EQ_OP','NE_OP','SEMICOLON','OPEN_CURLY','CLOSE_CURLY',
    'COMMA','COLON','EQUAL','OPEN_PAR','CLOSE_PAR','OPEN_SQUARE','CLOSE_SQUARE','DOT','AND','EXCLAIM',
    'NOT','MINUS','PLUS','MUL','DIVIDE','MOD','LESS_THAN','GREATER_THAN','XOR','OR','COND_OP',

    # LITERALS
    'ID','INT_CONST','FLOAT_CONST','STRING_CONSTANT','CHAR_CONST',
)


# Tokens

t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_AUTO = r'AUTO'
t_BREAK = r'BREAK'
t_CASE = r'CASE'
t_CHAR = r'CHAR'
t_CONST = r'CONST'
t_CONTINUE = r'CONTINUE'
t_DEFAULT = r'DEFAULT'
t_DO = r'DO'
t_DOUBLE   = r'DOUBLE'    
t_ELSE = r'ELSE'
t_ENUM = r'ENUM'
t_EXTERN = r'EXTERN'
t_FLOAT = r'FLOAT'
t_FOR = r'FOR'
t_GOTO = r'GOTO'
t_IF = r'IF'
t_INT = r'INT'
t_LONG = r'LONG'
t_REGISTER = r'REGISTER'
t_RETURN = r'RETURN'
t_SHORT = r'SHORT'
t_SIGNED = r'SIGNED'
t_SIZEOF = r'SIZEOF'
t_STATIC = r'STATIC'
t_STRUCT = r'STRUCT'
t_SWITCH = r'SWITCH'
t_TYPEDEF = r'TYPEDEF'
t_UNION = r'UNION'
t_UNSIGNED = r'UNSIGNED'
t_VOID = r'VOID'
t_VOLATILE = r'VOLATILE'
t_WHILE = r'WHILE'



def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = " \t\v\n\f"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex

lex.lex()