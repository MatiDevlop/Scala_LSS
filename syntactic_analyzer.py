import ply.yacc as yacc
from lexic_analyzer import tokens

precedence = (
    ('right', 'ARROW_RIGHT'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'LESS_THAN', 'GREATER_THAN', 'LESS_THAN_OR_EQUAL_TO', 'GREATER_THAN_OR_EQUAL_TO'),
    ('nonassoc', 'EQUAL_TO', 'NOT_EQUAL_TO'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULE'),
    ('right', 'NOT'),
)

def p_statement_list(p):
    '''statement_list : statement_list statement
                      | statement'''
    pass

def p_statement(p):
    '''statement : asignacion
                 | asign_existing
                 | compound_assignment
                 | control_structure'''
    pass

def p_block(p):
    '''block : LBRACE statement_list RBRACE
                | LBRACE RBRACE'''
    pass

def p_asignacion(p):
    '''asignacion : mutabilidad ID EQUALS expression opt_semicolon'''
    pass

def p_asignacion_tipada(p):
    '''asignacion : mutabilidad ID COLON tipo EQUALS expression opt_semicolon'''
    pass

def p_mutabilidad(p):
    '''mutabilidad : VAL
                   | VAR'''
    pass

def p_tipo(p):
    '''tipo : TYPE_INT
            | TYPE_FLOAT
            | TYPE_STRING
            | TYPE_CHAR
            | TYPE_BOOLEAN
            | TYPE_ARRAY
            | TYPE_LIST'''
    pass

def p_asign_existing(p):
    '''asign_existing : ID EQUALS expression opt_semicolon'''
    pass

def p_compound_assignment(p):
    '''compound_assignment : ID PLUS_EQUAL expression opt_semicolon
                           | ID MINUS_EQUAL expression opt_semicolon
                           | ID TIMES_EQUAL expression opt_semicolon
                           | ID DIVIDE_EQUAL expression opt_semicolon'''
    pass

def p_control_structure(p):
    '''control_structure : if_statement
                         | while_statement
                         | for_statement'''
    pass

def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN block
                    | IF LPAREN expression RPAREN block ELSE block'''
    pass

def p_while_statement(p):
    '''while_statement : WHILE LPAREN expression RPAREN block'''
    pass

def p_for_statement(p):
    '''for_statement : FOR LPAREN ID ARROW_LEFT expression TO expression RPAREN block'''
    pass

def p_expression(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression MODULE expression
                  | expression EQUAL_TO expression
                  | expression NOT_EQUAL_TO expression
                  | expression LESS_THAN expression
                  | expression GREATER_THAN expression
                  | expression LESS_THAN_OR_EQUAL_TO expression
                  | expression GREATER_THAN_OR_EQUAL_TO expression
                  | expression AND expression
                  | expression OR expression
                  | NOT expression
                  | LPAREN expression RPAREN
                  | INT_LITERAL
                  | FLOAT_LITERAL
                  | STRING_LITERAL
                  | CHAR_LITERAL
                  | TRUE
                  | FALSE
                  | ID'''
    pass

def p_opt_semicolon(p):
    '''opt_semicolon : SEMICOLON
                     | empty'''
    pass

def p_empty(p):
    'empty :'
    pass

def p_tipo_array(p):
    '''tipo : TYPE_ARRAY LBRACKET tipo RBRACKET'''
    pass

def p_expression_array(p):
    '''expression : TYPE_ARRAY LPAREN argument_list RPAREN'''
    pass

def p_function_def_block(p):
    '''function_def : DEF ID LPAREN param_list RPAREN COLON tipo EQUALS block'''
    pass

def p_return_statement(p):
    '''statement : RETURN expression opt_semicolon'''
    pass

def p_statement_expression(p):
    '''statement : expression opt_semicolon'''
    pass
#-----Inicio de reglas de David Olvera -----

#estructura de datos: List
def p_tipo_list(p):
    '''tipo : TYPE_LIST LBRACKET tipo RBRACKET'''
    pass

def p_expression_list(p):
    '''expression : TYPE_LIST LPAREN argument_list RPAREN
                  | TYPE_LIST LPAREN RPAREN'''
    pass

def p_argument_list(p):
    '''argument_list : argument_list COMMA expression
                     | expression'''
    pass

#nuevas sentencias
def p_statement_david(p):
    '''statement : function_def
                 | print_statement'''
    pass

#estructura de control: else if
def p_if_else_if(p):
    '''if_statement : IF LPAREN expression RPAREN block ELSE if_statement'''
    pass

#funciones
def p_param_list(p):
    '''param_list : param_list COMMA param
                  | param'''
    pass

def p_param(p):
    '''param : ID COLON tipo'''
    pass

def p_function_def_inline(p):
    '''function_def : DEF ID LPAREN param_list RPAREN COLON tipo EQUALS expression opt_semicolon
                    | DEF ID LPAREN RPAREN COLON tipo EQUALS expression opt_semicolon'''
    pass


def p_expression_lambda(p):
    '''expression : LPAREN param_list RPAREN ARROW_RIGHT expression
                  | LPAREN RPAREN ARROW_RIGHT expression'''
    pass

def p_expression_call(p):
    '''expression : ID LPAREN argument_list RPAREN
                  | ID LPAREN RPAREN'''
    pass



#impresion
def p_print_statement(p):
    '''print_statement : PRINTLN LPAREN expression RPAREN opt_semicolon
                       | PRINT LPAREN expression RPAREN opt_semicolon
                       | PRINTLN LPAREN RPAREN opt_semicolon'''
    pass

#entrada por teclado
def p_expression_input(p):
    '''expression : input_expression'''
    pass

def p_input_expression(p):
    '''input_expression : stdin_prefix read_function LPAREN RPAREN
                        | read_function LPAREN RPAREN'''
    pass

def p_stdin_prefix(p):
    '''stdin_prefix : ID DOT ID DOT ID DOT'''
    pass

def p_read_function(p):
    '''read_function : READLINE
                     | READINT'''
    pass
#-----FIN David Olvera -----

#Función de manejo de errores
def p_error(p):
    print("Error sintáctico en la línea %d: '%s'" % (p.lineno, p.value))

parser = yacc.yacc()