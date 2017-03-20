import ply.yacc as yacc
from lexer import *
import ply.lex as lex
import sys
# lex.lex()

from ast_generator import *

# import pydot
# graph = pydot.Dot(graph_type='graph')

# def add_edge(node_parent,node_child):
#   graph.add_edge(pydot.Edge(node_parent, node_child))

# k = 0
# def add_node(p):
#   global k
#   node = pydot.Node(k,label = p)
#   graph.add_node(node)
#   k = k + 1
#   return node

# def draw_graph(p):
#     for x in range (1,len(p)):
#         add_edge(p[0],p[x])
class CParser():
  def __init__(
        self,
        lex_optimize=True,
        lexer=CLexer,
        lextab='pycparser.lextab',
        yacc_optimize=True,
        yacctab='pycparser.yacctab',
        yacc_debug=False,
        taboutputdir=''):
    """ Create a new CParser.

        Some arguments for controlling the debug/optimization
        level of the parser are provided. The defaults are
        tuned for release/performance mode.
        The simple rules for using them are:
        *) When tweaking CParser/CLexer, set these to False
        *) When releasing a stable parser, set to True

        lex_optimize:
            Set to False when you're modifying the lexer.
            Otherwise, changes in the lexer won't be used, if
            some lextab.py file exists.
            When releasing with a stable lexer, set to True
            to save the re-generation of the lexer table on
            each run.

        lexer:
            Set this parameter to define the lexer to use if
            you're not using the default CLexer.

        lextab:
            Points to the lex table that's used for optimized
            mode. Only if you're modifying the lexer and want
            some tests to avoid re-generating the table, make
            this point to a local lex table file (that's been
            earlier generated with lex_optimize=True)

        yacc_optimize:
            Set to False when you're modifying the parser.
            Otherwise, changes in the parser won't be used, if
            some parsetab.py file exists.
            When releasing with a stable parser, set to True
            to save the re-generation of the parser table on
            each run.

        yacctab:
            Points to the yacc table that's used for optimized
            mode. Only if you're modifying the parser, make
            this point to a local yacc table file

        yacc_debug:
            Generate a parser.out file that explains how yacc
            built the parsing table from the grammar.

        taboutputdir:
            Set this parameter to control the location of generated
            lextab and yacctab files.
    """
    self.clex = lexer(
        error_func=self._lex_error_func,
        on_lbrace_func=self._lex_on_lbrace_func,
        on_rbrace_func=self._lex_on_rbrace_func,
        type_lookup_func=self._lex_type_lookup_func)

    self.clex.build(
        optimize=lex_optimize,
        lextab=lextab,
        outputdir=taboutputdir)
    self.tokens = self.clex.tokens

    rules_with_opt = [
        'abstract_declarator',
        'assignment_expression',
        'declaration_list',
        'declaration_specifiers_no_type',
        'designation',
        'expression',
        'identifier_list',
        'init_declarator_list',
        'id_init_declarator_list',
        'initializer_list',
        'parameter_type_list',
        'block_item_list',
        'type_qualifier_list',
        'struct_declarator_list'
    ]

    for rule in rules_with_opt:
        self._create_opt_rule(rule)

    self.cparser = yacc.yacc(
        module=self,
        start='translation_unit_or_empty',
        debug=yacc_debug,
        optimize=yacc_optimize,
        tabmodule=yacctab,
        outputdir=taboutputdir)

    # Stack of scopes for keeping track of symbols. _scope_stack[-1] is
    # the current (topmost) scope. Each scope is a dictionary that
    # specifies whether a name is a type. If _scope_stack[n][name] is
    # True, 'name' is currently a type in the scope. If it's False,
    # 'name' is used in the scope but not as a type (for instance, if we
    # saw: int name;
    # If 'name' is not a key in _scope_stack[n] then 'name' was not defined
    # in this scope at all.
    self._scope_stack = [dict()]

    # Keeps track of the last token given to yacc (the lookahead token)
    self._last_yielded_token = None

  def parse(self, text, filename='', debuglevel=0):
    """ Parses C code and returns an AST.

    text:
    A string containing the C source code

    filename:
    Name of the file being parsed (for meaningful
    error messages)

    debuglevel:
    Debug level to yacc
    """
    self.clex.filename = filename
    self.clex.reset_lineno()
    self._scope_stack = [dict()]
    self._last_yielded_token = None
    return self.cparser.parse(
          input=text,
          lexer=self.clex,
          debug=debuglevel)

  def _add_typedef_name(self, name):
    """ Add a new typedef name (ie a TYPEID) to the current scope
    """
    if not self._scope_stack[-1].get(name, True):
      self._parse_error(
        "Typedef %r previously declared as non-typedef "
        "in this scope" % name)
    self._scope_stack[-1][name] = True

  def _add_identifier(self, name):
    """ Add a new object, function, or enum member name (ie an ID) to the
        current scope
    """
    if self._scope_stack[-1].get(name, False):
      self._parse_error(
        "Non-typedef %r previously declared as typedef "
        "in this scope" % name)
    self._scope_stack[-1][name] = False

  def _fix_decl_name_type(self, decl, typename):
    """ Fixes a declaration. Modifies decl.
    """
    # Reach the underlying basic type
    #
    type = decl
    while not isinstance(type, c_ast.TypeDecl):
      type = type.type

    decl.name = type.declname
    type.quals = decl.quals

    # The typename is a list of types. If any type in this
    # list isn't an IdentifierType, it must be the only
    # type in the list (it's illegal to declare "int enum ..")
    # If all the types are basic, they're collected in the
    # IdentifierType holder.
    #
    for tn in typename:
      if not isinstance(tn, c_ast.IdentifierType):
        if len(typename) > 1:
          self._parse_error("Invalid multiple types specified")
        else:
          type.type = tn
          return decl

    if not typename:
      # Functions default to returning int
      #
      # if not isinstance(decl.type, c_ast.FuncDecl):
      #   self._parse_error("Missing type in declaration")
      type.type = c_ast.IdentifierType(
              ['int'])
    else:
        # At this point, we know that typename is a list of IdentifierType
        # nodes. Concatenate all the names into a single list.
        #
        type.type = c_ast.IdentifierType(
            [name for id in typename for name in id.names])
    return decl

  def _is_type_in_scope(self, name):
    """ Is *name* a typedef-name in the current scope?
    """
    for scope in reversed(self._scope_stack):
      # If name is an identifier in this scope it shadows typedefs in
      # higher scopes.
      in_scope = scope.get(name)
      if in_scope is not None: return in_scope
    return False


  def _build_declarations(self, spec, decls, typedef_namespace=False):
    """ Builds a list of declarations all sharing the given specifiers.
        If typedef_namespace is true, each declared name is added
        to the "typedef namespace", which also includes objects,
        functions, and enum constants.
    """
    is_typedef = 'typedef' in spec['storage']
    declarations = []

    # Bit-fields are allowed to be unnamed.
    #
    if decls[0].get('bitsize') is not None:
      pass

    # When redeclaring typedef names as identifiers in inner scopes, a
    # problem can occur where the identifier gets grouped into
    # spec['type'], leaving decl as None.  This can only occur for the
    # first declarator.
    #
    elif decls[0]['decl'] is None:
      if len(spec['type']) < 2 or len(spec['type'][-1].names) != 1 or \
          not self._is_type_in_scope(spec['type'][-1].names[0]):
        coord = '?'
        for t in spec['type']:
          if hasattr(t):
            # coord = t.coord
            break
        # self._parse_error('Invalid declaration', coord)

      # Make this look as if it came from "direct_declarator:ID"
      decls[0]['decl'] = c_ast.TypeDecl(
        declname=spec['type'][-1].names[0],
        type=None,
        quals=None)
      # Remove the "new" type's name from the end of spec['type']
      del spec['type'][-1]

    # A similar problem can occur where the declaration ends up looking
    # like an abstract declarator.  Give it a name if this is the case.
    #
    elif not isinstance(decls[0]['decl'],
        (c_ast.Struct, c_ast.Union, c_ast.IdentifierType)):
      decls_0_tail = decls[0]['decl']
      while not isinstance(decls_0_tail, c_ast.TypeDecl):
        decls_0_tail = decls_0_tail.type
      if decls_0_tail.declname is None:
        decls_0_tail.declname = spec['type'][-1].names[0]
        del spec['type'][-1]

    for decl in decls:
      assert decl['decl'] is not None
      if is_typedef:
        declaration = c_ast.Typedef(
          name=None,
          quals=spec['qual'],
          storage=spec['storage'],
          type=decl['decl'])
      else:
        declaration = c_ast.Decl(
          name=None,
          quals=spec['qual'],
          storage=spec['storage'],
          funcspec=spec['function'],
          type=decl['decl'],
          init=decl.get('init'),
          bitsize=decl.get('bitsize'))

      if isinstance(declaration.type,
          (c_ast.Struct, c_ast.Union, c_ast.IdentifierType)):
        fixed_decl = declaration
      else:
        fixed_decl = self._fix_decl_name_type(declaration, spec['type'])

      # Add the type name defined by typedef to a
      # symbol table (for usage in the lexer)
      #
      if typedef_namespace:
        if is_typedef:
          self._add_typedef_name(fixed_decl.name)
        else:
          self._add_identifier(fixed_decl.name)

      declarations.append(fixed_decl)
    return declarations

  def _build_function_definition(self, spec, decl, param_decls, body):
    """ Builds a function definition.
    """
    assert 'typedef' not in spec['storage']

    declaration = self._build_declarations(
    spec=spec,
    decls=[dict(decl=decl, init=None)],
    typedef_namespace=True)[0]

    return c_ast.FuncDef(
    decl=declaration,
    param_decls=param_decls,
    body=body)

  def p_primary_expression(p):
    '''primary_expression   : constant
                            | identifier
                            | string
                            | '(' expression ')'
                            | generic_selection
                            '''
    p[0] = p[1]

  def p_identifier(p):
    '''identifier   : IDENTIFIER
                     '''
    p[0] = ast_generator.ID(p[1])  

  def p_constant(p):
    '''constant             : ICONST
                            | FCONST
                            | CCONST
                            '''
    p[0] = ast_generator.Constant('int', p[1])

  def p_string(p):
    '''string               : STRING_LITERAL
                            | FUNC_NAME
                             '''
  def p_generic_selection(p):
    '''generic_selection    :  GENERIC '(' assignment_expression ',' generic_assoc_list ')'
                            '''
            
  def p_generic_assoc_list(p):
    '''generic_assoc_list   : generic_association
                            | generic_assoc_list ',' generic_association
                            '''
  def p_generic_association(p):
    '''generic_association  : type_name ':' assignment_expression
                            | DEFAULT ':' assignment_expression
                            '''
  def p_postfix_expression(p):
    '''postfix_expression   : primary_expression
                            | postfix_expression '[' expression ']'
                            | postfix_expression '(' ')'
                            | postfix_expression '(' argument_expression_list ')'
                            | postfix_expression '.' IDENTIFIER
                            | postfix_expression PTR_OP IDENTIFIER
                            | postfix_expression INC_OP
                            | postfix_expression DEC_OP
                            | '(' type_name ')' '{' initializer_list '}'
                            | '(' type_name ')' '{' initializer_list ',' '}'
                            '''
    p[0] = p[1]
  def p_argument_expression_list(p):
    '''argument_expression_list   : assignment_expression
                                  | argument_expression_list ',' assignment_expression
                                  '''

  def p_unary_expression(p):
    '''unary_expression   : postfix_expression
                          | INC_OP unary_expression
                          | DEC_OP unary_expression
                          | unary_operator cast_expression
                          | SIZEOF unary_expression
                          | SIZEOF '(' unary_expression ')'
                          | SIZEOF '(' struct_or_union_specifier ')'
                          | ALIGNOF '(' type_name ')'
                          '''

    p[0] = p[1]

    # p[0] = c_ast.UnaryOp(p[1], p[2], p[2].coord)

    # p[0] = c_ast.UnaryOp(
    #     p[1],
    #     p[2] if len(p) == 3 else p[3],
    #     self._token_coord(p, 1))


  def p_unary_operator(p):
    '''unary_operator : '&'
                      | '*'
                      | '+'
                      | '-'
                      | '~'
                      | '!'
                      '''

  def p_cast_expression(p):
    '''cast_expression  : unary_expression
                        | '(' type_name ')' cast_expression
                        '''
    p[0] = p[1] 

  def p_multiplicative_expression(p):
    '''multiplicative_expression  : cast_expression
                                  | multiplicative_expression '*' cast_expression
                                  | multiplicative_expression '/' cast_expression
                                  | multiplicative_expression '%' cast_expression
                                  '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ast_generator.BinaryOp(p[2], p[1], p[3])

  def p_additive_expression(p):
    '''additive_expression  : multiplicative_expression
                            | additive_expression '+' multiplicative_expression
                            | additive_expression '-' multiplicative_expression
                            '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ast_generator.BinaryOp(p[2], p[1], p[3])
    
  def p_shift_expression(p):
    '''shift_expression   : additive_expression
                          | shift_expression LEFT_OP additive_expression
                          | shift_expression RIGHT_OP additive_expression
                          '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ast_generator.BinaryOp(p[2], p[1], p[3])
    
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
        p[0] = ast_generator.BinaryOp(p[2], p[1], p[3])

  def p_equality_expression(p):
    '''equality_expression  : relational_expression
                            | equality_expression EQ_OP relational_expression
                            | equality_expression NE_OP relational_expression
                            '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ast_generator.BinaryOp(p[2], p[1], p[3])

  def p_and_expression(p):
    '''and_expression   : equality_expression
                        | and_expression '&' equality_expression
                        '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ast_generator.BinaryOp(p[2], p[1], p[3])

  def p_exclusive_or_expression(p):
    '''exclusive_or_expression  : and_expression
                                | exclusive_or_expression '^' and_expression
                                '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ast_generator.BinaryOp(p[2], p[1], p[3])

  def p_inclusive_or_expression(p):
    '''inclusive_or_expression  : exclusive_or_expression
                                | inclusive_or_expression '|' exclusive_or_expression
                                '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ast_generator.BinaryOp(p[2], p[1], p[3])
    

  def p_logical_and_expression(p):
    '''logical_and_expression   : inclusive_or_expression
                                | logical_and_expression AND_OP inclusive_or_expression
                                '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ast_generator.BinaryOp(p[2], p[1], p[3])
    
  def p_logical_or_expression(p):
    '''logical_or_expression  : logical_and_expression
                              | logical_or_expression OR_OP logical_and_expression
                              '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ast_generator.BinaryOp(p[2], p[1], p[3])

  def p_conditional_expression(p):
    '''conditional_expression   : logical_or_expression
                                | logical_or_expression '?' expression ':' conditional_expression
                                  '''
    if len(p) == 2:
      p[0] = p[1]
  # else:
  #   p[0] = c_ast.TernaryOp(p[1], p[3], p[5], p[1].coord)                                

  def p_assignment_expression(p):
    '''assignment_expression  : conditional_expression
                              | unary_expression assignment_operator assignment_expression
                              '''
    if len(p) == 2:
      p[0] = p[1]
    else:
      p[0] = ast_generator.Assignment(p[2], p[1], p[3])

    
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
      if not isinstance(p[1], ast_generator.ExprList):
        p[1] = ast_generator.ExprList([p[1]])
      p[1].exprs.append(p[3])
      p[0] = p[1]

  def p_constant_expression(p):
    '''constant_expression  : conditional_expression
                            '''
   
  def p_declaration(p):
    '''declaration  : declaration_specifiers ';'
                    | declaration_specifiers init_declarator_list ';'
                    | static_assert_declaration
                    '''
    spec = p[1]
    decls = self._build_declarations(
                  spec=spec,
                  decls=p[2],
                  typedef_namespace=True)
    p[0] = decls

  def p_declaration_specifiers(p):
    '''declaration_specifiers   : storage_class_specifier
                                | storage_class_specifier declaration_specifiers
                                | type_specifier
                                | type_specifier declaration_specifiers
                                | type_qualifier
                                | type_qualifier declaration_specifiers
                                | function_specifier declaration_specifiers
                                | function_specifier
                                | alignment_specifier declaration_specifiers
                                | alignment_specifier
                                '''
    p[0] = p[1]

  def p_init_declarator_list(p):
    '''init_declarator_list   : init_declarator
                              | init_declarator_list ',' init_declarator
                              '''
    p[0] = p[1]                            
  def p_init_declarator(p):
    '''init_declarator  : declarator
                        | declarator '=' initializer
                        '''
    p[0] = dict(decl=p[1], init=(p[3] if len(p) > 2 else None))
  def p_storage_class_specifier(p):
    '''storage_class_specifier  : TYPEDEF
                                | EXTERN
                                | STATIC
                                | AUTO
                                | REGISTER
                                '''
   
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
                        | struct_or_union_specifier
                        | enum_specifier
                        '''
    p[0] = ast_generator.IdentifierType([p[1]])

  def p_struct_or_union_specifier(p):
    '''struct_or_union_specifier  : struct_or_union IDENTIFIER '{' struct_declaration_list '}'
                                  | struct_or_union '{' struct_declaration_list '}'
                                  | struct_or_union IDENTIFIER
                                  '''
   

  def p_struct_or_union_(p):
    '''struct_or_union  : STRUCT
                        | UNION
                        '''


  def p_struct_declaration_list(p):
    '''struct_declaration_list  : struct_declaration
                                | struct_declaration_list struct_declaration
                                '''
   
  def p_struct_declaration(p):
    '''struct_declaration   : specifier_qualifier_list ';'
                            | specifier_qualifier_list struct_declarator_list ';' 
                            | static_assert_declaration  
                            '''
   

  def p_specifier_qualifier_list(p):
    '''specifier_qualifier_list   : type_specifier specifier_qualifier_list
                                  | type_specifier
                                  | type_qualifier specifier_qualifier_list
                                  | type_qualifier
                                  '''

  def p_struct_declarator_list(p):
    '''struct_declarator_list   : struct_declarator
                                | struct_declarator_list ',' struct_declarator
                                '''
   

  def p_struct_declarator(p):
    '''struct_declarator  : declarator
                          | ':' constant_expression
                          | declarator ':' constant_expression
                          '''
   
  def p_enum_specifier(p):
    '''enum_specifier     : ENUM '{' enumerator_list '}'
                          | ENUM '{' enumerator_list ',' '}'
                          | ENUM IDENTIFIER '{' enumerator_list '}'
                          | ENUM IDENTIFIER '{' enumerator_list ',' '}'
                          | ENUM IDENTIFIER
                          '''


  def p_enumerator_list(p):
    '''enumerator_list  : enumerator
                        | enumerator_list ',' enumerator
                        '''

  def p_enumerator(p):
    '''enumerator   : IDENTIFIER
                    | IDENTIFIER '=' constant_expression
                    '''

  def p_type_qualifier(p):
    '''type_qualifier   : CONST
                        | VOLATILE
                        | RESTRICT
                        '''
  def p_function_specifier(p):
    '''function_specifier   : INLINE
                            | NORETURN
                            '''
  def p_alignment_specifier(p):
    '''alignment_specifier   : ALIGNAS '(' type_name ')'
                            | ALIGNAS '(' constant_expression ')'
                            '''
  def p_declarator(p):
    '''declarator   : pointer direct_declarator
                    | direct_declarator
                    '''
    p[0] = p[1]                  

  def p_direct_declarator(p):
    '''direct_declarator  : identifier
                          | '(' declarator ')'
                          | direct_declarator '[' ']'
                          | direct_declarator '[' '*' ']'
                          | direct_declarator '[' STATIC type_qualifier_list assignment_expression ']'
                          | direct_declarator '[' STATIC assignment_expression ']'
                          | direct_declarator '[' type_qualifier_list '*' ']'
                          | direct_declarator '[' type_qualifier_list STATIC assignment_expression ']'
                          | direct_declarator '[' type_qualifier_list assignment_expression ']'
                          | direct_declarator '[' type_qualifier_list ']'
                          | direct_declarator '[' assignment_expression ']'
                          | direct_declarator '(' parameter_type_list ')'
                          | direct_declarator '(' ')'
                          | direct_declarator '(' identifier_list ')'
                          '''
    p[0] = p[1]

  def p_pointer(p):
    '''pointer  : '*'
                | '*' type_qualifier_list
                | '*' pointer
                | '*' type_qualifier_list pointer
                '''

  def p_type_qualifier_list(p):
    '''type_qualifier_list  : type_qualifier
                            | type_qualifier_list type_qualifier
                            '''

  def p_parameter_type_list(p):
    '''parameter_type_list  : parameter_list
                            | parameter_list ',' ELLIPSIS
                            '''

  def p_parameter_list(p):
    '''parameter_list   : parameter_declaration
                        | parameter_list ',' parameter_declaration
                        '''

  def p_parameter_declaration(p):
    '''parameter_declaration  : declaration_specifiers declarator
                              | declaration_specifiers abstract_declarator
                              | declaration_specifiers
                              '''

  def p_identifier_list(p):
    '''identifier_list  : IDENTIFIER
                        | identifier_list ',' IDENTIFIER
                        '''

  def p_type_name(p):
    '''type_name        : specifier_qualifier_list abstract_declarator
                        | specifier_qualifier_list
                        '''

  def p_abstract_declarator(p):
    '''abstract_declarator  : pointer
                            | direct_abstract_declarator
                            | pointer direct_abstract_declarator
                            '''


  def p_direct_abstract_declarator(p):
    '''direct_abstract_declarator   : '(' abstract_declarator ')'
                                    | '[' ']'
                                    | '[' '*' ']'
                                    | '[' STATIC type_qualifier_list assignment_expression ']'
                                    | '[' STATIC assignment_expression ']'
                                    | '[' type_qualifier_list STATIC assignment_expression ']'
                                    | '[' type_qualifier_list assignment_expression ']'
                                    | '[' type_qualifier_list ']'
                                    | '[' assignment_expression ']'
                                    | direct_abstract_declarator '[' ']'
                                    | direct_abstract_declarator '[' '*' ']'
                                    | direct_abstract_declarator '[' STATIC type_qualifier_list assignment_expression ']'
                                    | direct_abstract_declarator '[' STATIC assignment_expression ']'
                                    | direct_abstract_declarator '[' type_qualifier_list assignment_expression ']'
                                    | direct_abstract_declarator '[' type_qualifier_list STATIC assignment_expression ']'
                                    | direct_abstract_declarator '[' type_qualifier_list ']'
                                    | direct_abstract_declarator '[' assignment_expression ']'
                                    | '(' ')'
                                    | '(' parameter_type_list ')'
                                    | direct_abstract_declarator '(' ')'
                                    | direct_abstract_declarator '(' parameter_type_list ')'
                                    '''

  def p_initializer(p):
    '''initializer  : assignment_expression
                    | '{' initializer_list '}'
                    | '{' initializer_list ',' '}'
                    '''
    p[0] = p[1]

  def p_initializer_list(p):
    '''initializer_list   : initializer
                          | initializer_list ',' initializer
                          | designation initializer
                          | initializer_list ',' designation initializer
                          '''
  def p_designation(p):
    '''designation   : designator_list '='
                          ''' 

  def p_designator_list(p):
    '''designator_list    : designator
                          | designator_list designator
                          ''' 
  def p_designator(p):
    '''designator    : '[' constant_expression ']'
                     | '.' IDENTIFIER
                    ''' 
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

  def p_labeled_statement(p):
    '''labeled_statement  : IDENTIFIER ':' statement
                          | CASE constant_expression ':' statement
                          | DEFAULT ':' statement
                          '''

  def p_compound_statement(p):
    '''compound_statement   : '{' '}'
                            | '{'  block_item_list '}'
                            '''
    p[0] = c_ast.Compound(block_items=p[2])

  def p_block_item_list(p):
    '''block_item_list    : block_item
                          | block_item_list block_item
                            '''
  def p_block_item(p):
    '''block_item     : declaration
                      | statement
                      '''

  def p_expression_statement(p):
    '''expression_statement   : ';'
                              | expression ';'
                              '''

  def p_selection_statement(p):
    '''selection_statement  : IF '(' expression ')' statement
                            | IF '(' expression ')' statement ELSE statement
                            | SWITCH '(' expression ')' statement
                            '''

  def p_iteration_statement(p):
    '''iteration_statement  : WHILE '(' expression ')' statement
                            | DO statement WHILE '(' expression ')' ';'
                            | FOR '(' expression_statement expression_statement ')' statement
                            | FOR '(' expression_statement expression_statement expression ')' statement
                            | FOR '(' declaration expression_statement ')' statement
                            | FOR '(' declaration expression_statement expression ')' statement
                            '''

  def p_jump_statement(p):
    '''jump_statement   : GOTO IDENTIFIER ';'
                        | CONTINUE ';'
                        | BREAK ';'
                        | RETURN ';'
                        | RETURN expression ';'
                        '''

  def p_translation_unit(p):
    '''translation_unit   : external_declaration
                          | translation_unit external_declaration
                          '''
    p[0] = p[1]

  def p_external_declaration(p):
    '''external_declaration   : function_definition
                              | declaration
                              '''
    p[0] = p[1]

  def p_function_definition(p):
    '''function_definition  : declaration_specifiers declarator declaration_list compound_statement
                            | declaration_specifiers declarator compound_statement
                            '''
    spec = p[1]

    p[0] = self._build_function_definition(
        spec=spec,
        decl=p[2],
        param_decls=p[3])
  def p_declaration_list(p):
    '''declaration_list   : declaration_list declaration
                          | declaration
                          '''
    p[0] = p[1] if len(p) == 2 else p[1] + p[2]

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
    print ("Parsed successfully, writing graph to" + fd_2)
    graph.write_png(fd_2)
    print ("Write successful")
  else :
    yacc.yacc( start='translation_unit')
    yacc.parse("");
    print("Please provide file to be parsed")