import ply.yacc as yacc
from lexic_analyzer import tokens

tabla_simbolos ={
    "variables": {}
}

variables_ocultas = {}
errores_semanticos = []
errores_sintacticos = []
retornos_pendientes = []
pila_ambitos = []

def calcular_columna(texto, lexpos):
    ultimo_salto = texto.rfind('\n', 0, lexpos)
    if ultimo_salto < 0:
        return lexpos + 1
    return lexpos - ultimo_salto

def restaurar_ambito_parametros(parametros):
    for param in parametros:
        if param in variables_ocultas:
            tabla_simbolos["variables"][param] = variables_ocultas.pop(param)
        else:
            tabla_simbolos["variables"].pop(param, None)

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
    mutabilidad = p[1]
    nombre = p[2]
    tipo_inferido = p[4]

    if nombre in tabla_simbolos["variables"]:
        errores_semanticos.append(f"Error Semántico en línea {p.lineno(2)}: La variable '{nombre}' ya ha sido declarada previamente.")
    else:
        tabla_simbolos["variables"][nombre] = {
            "tipo": tipo_inferido,
            "categoria": mutabilidad
        }

def p_asignacion_tipada(p):
    '''asignacion : mutabilidad ID COLON tipo EQUALS expression opt_semicolon'''
    mutabilidad = p[1]
    nombre = p[2]
    tipo = p[4]
    #Conversion: no se puede guardar un Float en un Int
    if tipo == "Int" and p[6] == "Float":
        errores_semanticos.append(f"Error Semántico (Conversión) en línea {p.lineno(2)}: No se permite convertir 'Float' a 'Int' de forma implícita.")
    
    if nombre in tabla_simbolos["variables"]:
        errores_semanticos.append(f"Error Semántico en línea {p.lineno(2)}: La variable '{nombre}' ya ha sido declarada previamente.")
    else:
        tabla_simbolos["variables"][nombre] = {
            "tipo": tipo,
            "categoria": mutabilidad
        }

def p_mutabilidad(p):
    '''mutabilidad : VAL
                   | VAR'''
    p[0] = p[1]

def p_tipo(p):
    '''tipo : TYPE_INT
            | TYPE_FLOAT
            | TYPE_STRING
            | TYPE_CHAR
            | TYPE_BOOLEAN
            | TYPE_ARRAY
            | TYPE_LIST'''
    p[0] = p[1]

def p_asign_existing(p):
    '''asign_existing : ID EQUALS expression opt_semicolon'''
    nombre = p[1]
    if nombre not in tabla_simbolos["variables"]:
        errores_semanticos.append(f"Error Semántico en línea {p.lineno(1)}: La variable '{nombre}' no ha sido declarada previamente.")
    else:
        simbolo = tabla_simbolos["variables"][nombre]
        if simbolo["categoria"] == "val":
            errores_semanticos.append(f"Error Semántico en línea {p.lineno(1)}: La variable '{nombre}' es inmutable y no puede ser reasignada.")

def p_compound_assignment(p):
    '''compound_assignment : ID PLUS_EQUAL expression opt_semicolon
                           | ID MINUS_EQUAL expression opt_semicolon
                           | ID TIMES_EQUAL expression opt_semicolon
                           | ID DIVIDE_EQUAL expression opt_semicolon'''
    nombre = p[1]
    if nombre not in tabla_simbolos["variables"]:
        errores_semanticos.append(f"Error Semántico en línea {p.lineno(1)}: La variable '{nombre}' no ha sido declarada previamente.")
    else:
        simbolo = tabla_simbolos["variables"][nombre]
        if simbolo["categoria"] == "val":
            errores_semanticos.append(f"Error Semántico en línea {p.lineno(1)}: La variable '{nombre}' es inmutable y no puede ser reasignada.")

def p_control_structure(p):
    '''control_structure : if_statement
                         | while_statement
                         | for_statement'''
    pass  

def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN block
                    | IF LPAREN expression RPAREN block ELSE block'''
    #Estructuras de control: la condicion del if debe ser Boolean
    if p[3] != None and p[3] != "Error" and p[3] != "Boolean":
        errores_semanticos.append(f"Error Semántico (Estructuras de control) en línea {p.lineno(1)}: La condición del 'if' debe ser de tipo Boolean, pero es '{p[3]}'.")

def p_while_statement(p):
    '''while_statement : WHILE LPAREN expression RPAREN block'''
    #Estructuras de control: la condicion del while debe ser Boolean
    if p[3] != None and p[3] != "Error" and p[3] != "Boolean":
        errores_semanticos.append(f"Error Semántico (Estructuras de control) en línea {p.lineno(1)}: La condición del 'while' debe ser de tipo Boolean, pero es '{p[3]}'.")

def p_for_header(p):
    '''for_header : FOR LPAREN ID ARROW_LEFT expression TO expression RPAREN'''
    nombre = p[3]
    if nombre in tabla_simbolos["variables"] and nombre not in variables_ocultas:
        variables_ocultas[nombre] = tabla_simbolos["variables"][nombre].copy()
    tabla_simbolos["variables"][nombre] = {
        "tipo": "Int",
        "categoria": "val",
        "es_parametro": True
    }
    p[0] = nombre

def p_for_statement(p):
    '''for_statement : for_header block'''
    restaurar_ambito_parametros([p[1]])    

def p_expression_aritmetica(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression MODULE expression'''
    tipo_izq = p[1]
    operador = p[2]
    tipo_der = p[3]
    tipos_numericos = ['Int', 'Float']
    
    if tipo_izq == "Error" or tipo_der == "Error":
        p[0] = "Error"
        return
    
    if operador == "+":
        if tipo_izq == "String" or tipo_der == "String":
            p[0] = "String"
            return
    
    if tipo_izq in tipos_numericos and tipo_der in tipos_numericos:
        p[0] = "Float" if tipo_izq == "Float" or tipo_der == "Float" else "Int"
    else:
        errores_semanticos.append(f"Error Semántico en línea {p.lineno(2)}: Operación aritmética inválida entre tipos '{tipo_izq}' y '{tipo_der}'.")
        p[0] = "Error"

def p_expression_relacional_logica(p):
    '''expression : expression EQUAL_TO expression
                  | expression NOT_EQUAL_TO expression
                  | expression LESS_THAN expression
                  | expression GREATER_THAN expression
                  | expression LESS_THAN_OR_EQUAL_TO expression
                  | expression GREATER_THAN_OR_EQUAL_TO expression
                  | expression AND expression
                  | expression OR expression'''
    p[0] = "Boolean"

def p_expression_not(p):
    '''expression : NOT expression'''
    p[0] = "Boolean"

def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]

# --- 3. Literales (Casos Base) ---
def p_expression_int(p):
    '''expression : INT_LITERAL'''
    p[0] = "Int"

def p_expression_float(p):
    '''expression : FLOAT_LITERAL'''
    p[0] = "Float"

def p_expression_string(p):
    '''expression : STRING_LITERAL'''
    p[0] = "String"

def p_expression_char(p):
    '''expression : CHAR_LITERAL'''
    p[0] = "Char"

def p_expression_bool(p):
    '''expression : TRUE
                  | FALSE'''
    p[0] = "Boolean"

def p_expression_id(p):
    '''expression : ID'''
    nombre = p[1]
    if nombre not in tabla_simbolos["variables"]:
        errores_semanticos.append(f"Error Semántico en línea {p.lineno(1)}: La variable '{nombre}' no ha sido declarada previamente.")
        p[0] = "Error"
    else:
        p[0] = tabla_simbolos["variables"][nombre]["tipo"]

def p_opt_semicolon(p):
    '''opt_semicolon : SEMICOLON
                     | empty'''
    pass

def p_empty(p):
    'empty :'
    pass

def p_tipo_array(p):
    '''tipo : TYPE_ARRAY LBRACKET tipo RBRACKET'''
    p[0] = f"{p[1]}[{p[3]}]"

def p_expression_array(p):
    '''expression : TYPE_ARRAY LPAREN argument_list RPAREN'''
    pass

def p_function_def_block(p):
    '''function_def : DEF ID LPAREN param_list RPAREN COLON tipo EQUALS function_body_start block'''
    #Retorno de funciones: revisa los return guardados contra el tipo declarado
    tipo_decl = p[7]
    for tipo_ret, linea in retornos_pendientes:
        if tipo_ret != None and tipo_ret != "Error" and tipo_ret != tipo_decl and not (tipo_decl == "Float" and tipo_ret == "Int"):
            errores_semanticos.append(f"Error Semántico (Retorno de funciones) en línea {linea}: La función declara retornar '{tipo_decl}' pero retorna '{tipo_ret}'.")
    retornos_pendientes.clear()
    antes = pila_ambitos.pop()
    for nombre in list(tabla_simbolos["variables"].keys()):
        if nombre not in antes:
            del tabla_simbolos["variables"][nombre]
    restaurar_ambito_parametros(p[4])

def p_function_body_start(p):
    '''function_body_start : empty'''
    pila_ambitos.append(set(tabla_simbolos["variables"].keys()))

def p_return_statement(p):
    '''statement : RETURN expression opt_semicolon'''
    #Retorno de funciones: guarda el tipo y la linea del return
    retornos_pendientes.append((p[2], p.lineno(1)))

def p_statement_expression(p):
    '''statement : expression opt_semicolon'''
    pass
#-----Inicio de reglas de David Olvera -----

#estructura de datos: List
def p_tipo_list(p):
    '''tipo : TYPE_LIST LBRACKET tipo RBRACKET'''
    p[0] = f"{p[1]}[{p[3]}]"

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
    #Estructuras de control: la condicion del else if debe ser Boolean
    if p[3] != None and p[3] != "Error" and p[3] != "Boolean":
        errores_semanticos.append(f"Error Semántico (Estructuras de control) en línea {p.lineno(1)}: La condición del 'if' debe ser de tipo Boolean, pero es '{p[3]}'.")

#funciones
def p_param_list(p):
    '''param_list : param_list COMMA param
                  | param'''
    if len(p) == 4:
        if p[3] in p[1]:
            errores_semanticos.append(f"Error Semántico en línea {p.lineno(3)}: Parámetro duplicado'{p[3]}' en la misma funcion.")
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_param(p):
    '''param : ID COLON tipo'''
    nombre = p[1]
    tipo = p[3]

    if nombre in tabla_simbolos["variables"] and not tabla_simbolos["variables"][nombre].get("es_parametro"):
        variables_ocultas[nombre] = tabla_simbolos["variables"][nombre].copy()

    tabla_simbolos["variables"][nombre] = {
        "tipo": tipo,
        "categoria": "val",
        "es_parametro": True
    }
    p[0] = nombre

def p_function_def_inline(p):
    '''function_def : DEF ID LPAREN param_list RPAREN COLON tipo EQUALS expression opt_semicolon
                    | DEF ID LPAREN RPAREN COLON tipo EQUALS expression opt_semicolon'''
    if len(p) == 11:
        tipo_decl = p[7]
        tipo_ret = p[9]
        restaurar_ambito_parametros(p[4])
    else:
        tipo_decl = p[6]
        tipo_ret = p[8]
    #Retorno de funciones: el tipo de la expresion debe coincidir con el declarado
    if tipo_ret != None and tipo_ret != "Error" and tipo_ret != tipo_decl and not (tipo_decl == "Float" and tipo_ret == "Int"):
        errores_semanticos.append(f"Error Semántico (Retorno de funciones) en línea {p.lineno(2)}: La función declara retornar '{tipo_decl}' pero retorna '{tipo_ret}'.")

def p_expression_lambda(p):
    '''expression : LPAREN param_list RPAREN ARROW_RIGHT expression
                  | LPAREN RPAREN ARROW_RIGHT expression'''
    if len(p) == 6:
        restaurar_ambito_parametros(p[2])

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
    p[0] = p[1]

def p_input_expression(p):
    '''input_expression : stdin_prefix read_function LPAREN RPAREN
                        | read_function LPAREN RPAREN'''
    p[0] = p[2] if len(p) == 5 else p[1]

def p_stdin_prefix(p):
    '''stdin_prefix : ID DOT ID DOT ID DOT'''
    pass

def p_read_function(p):
    '''read_function : READLINE
                     | READINT'''
    p[0] = "Int" if p[1] == "readInt" else "String"

#Función de manejo de errores
def p_error(p):
    if p:
        # Tipo 1: Token inesperado en la entrada
        columna = calcular_columna(p.lexer.lexdata, p.lexpos)
        errores_sintacticos.append(
            f"Error sintáctico en línea {p.lineno}, columna {columna}: "
            f"Token inesperado '{p.value}' (Tipo: {p.type}). "
            f"Verifique la estructura de la sentencia o delimitadores faltantes."
        )
        # Recuperación de errores: descarta el token problemático para seguir analizando el resto del archivo
        parser.errok()
    else:
        # Tipo 2: Fin de archivo (EOF) inesperado
        errores_sintacticos.append(
            "Error sintáctico al final del archivo (EOF): "
            "Se esperaba cerrar un bloque '}', paréntesis ')' o completar una expresión antes de finalizar."
        )

parser = yacc.yacc()