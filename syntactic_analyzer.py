import ply.yacc as yacc
from lexic_analyzer import tokens

precedence = (
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
    '''asignacion : mutabilidad ID EQUALS expression opt_semicolon 
                    | mutabilidad ID COLON tipo EQUALS expression opt_semicolon'''

def p_mutabilidad(p):
    '''mutabilidad : VAL
                   | VAR'''
    pass

def p_tipo(p):
    '''tipo : TYPE_INT
            | TYPE_FLOAT
            | TYPE_STRING
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



#Función de manejo de errores
def p_error(p):
    print("Error sintáctico en la línea %d: '%s'" % (p.lineno, p.value))

parser = yacc.yacc()

while True:
    try:
        s = input('scala> ')
    except EOFError:
        break
    if not s:
        continue
    result = parser.parse(s)
    print(result)