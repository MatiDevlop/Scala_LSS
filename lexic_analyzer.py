import ply.lex as lex


reserved = {
    #tipos de datos
    "Int" : "TYPE_INT",
    "Float" : "TYPE_FLOAT",
    "Boolean" : "TYPE_BOOLEAN",
    "String" : "TYPE_STRING",    
    "Array" : "TYPE_ARRAY",
    "List" : "TYPE_LIST",
    #variables y funciones
    "val" : "VAL",
    "var" : "VAR",
    "def" : "DEF",
    #valores booleanos
    "true": "TRUE",
    "false": "FALSE",
    #condicionales
    "if" : "IF",
    "else" : "ELSE",
    #bucles
    "while" : "WHILE",
    "for" : "FOR",
    "to" : "TO",
    #retorno
    "return" : "RETURN",
}


tokens =[
    #Identificadores y tipos literales
    "ID",
    "INT_LITERAL",
    "FLOAT_LITERAL",
    "STRING_LITERAL",
    #Operadores aritmeticos
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "MODULE",
    #Operadores de asignacion
    "EQUALS",
    "PLUS_EQUAL",
    "MINUS_EQUAL",
    "TIMES_EQUAL",
    "DIVIDE_EQUAL",
    #Operadores logicos
    "AND",
    "OR",
    "NOT",
    #Operadores de comparacion
    "EQUAL_TO",
    "NOT_EQUAL_TO",
    "LESS_THAN",
    "GREATER_THAN",
    "LESS_THAN_OR_EQUAL_TO",
    "GREATER_THAN_OR_EQUAL_TO",
    #Delimitadores
    "LPAREN",
    "RPAREN",
    "LBRACKET",
    "RBRACKET",
    "LBRACE",
    "RBRACE",
    "COLON",
    "SEMICOLON",
    "COMMA",
    "DOT",
    "ARROW_LEFT",
    "ARROW_RIGHT",
] + list(reserved.values())


#RegEx para operadores aritmeticos
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULE = r'%'
#RegEx para operadores de asignacion
t_EQUALS = r'='
t_PLUS_EQUAL = r'\+='
t_MINUS_EQUAL = r'-='
t_TIMES_EQUAL = r'\*='
t_DIVIDE_EQUAL = r'/='
#RegEx para operadores logicos
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'
#RegEx para operadores de comparacion
t_EQUAL_TO = r'=='
t_NOT_EQUAL_TO = r'!='
t_LESS_THAN = r'<'
t_GREATER_THAN = r'>'
t_LESS_THAN_OR_EQUAL_TO = r'<='
t_GREATER_THAN_OR_EQUAL_TO = r'>='
#RegEx para delimitadores
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COLON = r':'
t_SEMICOLON = r';'
t_COMMA = r','
t_DOT = r'\.'
t_ARROW_LEFT = r'<-'
t_ARROW_RIGHT = r'=>'

#comentarios
def t_COMMENT_SINGLE(t):
    r'//[^\n]*'
    pass

def t_COMMENT_MULTI(t):
    r'/\*[\s\S]*?\*/'
    t.lexer.lineno += t.value.count('\n')

def t_COMMENT_UNCLOSED(t):
    r'/\*'
    lista_errores.append(
        f"Línea {t.lineno}: Comentario multilínea sin cerrar ('*/' no encontrado)."
    )
    t.lexer.lexpos = len(t.lexer.lexdata)

#literales (numeros y cadenas)
def t_FLOAT_LITERAL(t):
    r'\d+\.\d+[fF]'
    t.value = float(t.value[:-1])
    return t

def t_INT_LITERAL(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING_LITERAL(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]
    return t

#identificadores y palabras reservadas
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, "ID")
    return t

#saltos de linea y caracteres ignorados
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

lista_errores = []

def obtener_columna(token):
    texto_fuente = token.lexer.lexdata
    inicio_linea = texto_fuente.rfind('\n', 0, token.lexpos)
    if inicio_linea < 0:
        inicio_linea = -1
    return (token.lexpos - inicio_linea)

def t_error(t):
    col = obtener_columna(t)
    caracter = t.value[0]
    mensaje = (
        f"Línea {t.lineno}, Columna {col}: "
        f"Carácter no reconocido '{caracter}'. "
        f"Símbolo no definido en el alfabeto de Scala."
    )
    lista_errores.append(mensaje)
    t.lexer.skip(1)

lexer = lex.lex()