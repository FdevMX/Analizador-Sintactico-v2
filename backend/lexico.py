import ply.lex as lex

# Lista de nombres de tokens
tokens = [
    'FOR', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'SEMICOLON',
    'INT', 'IDENTIFIER', 'NUMBER', 'EQUALS', 'LESS_EQUAL', 'INCREMENT',
    'STRING', 'PLUS', 'DOT', 'SYSTEM', 'OUT', 'PRINTLN'
]

# Palabras reservadas
reserved = {
    'for': 'FOR',
    'int': 'INT',
    'System': 'SYSTEM',
    'out': 'OUT',
    'println': 'PRINTLN'
}

# Reglas para tokens simples
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_EQUALS = r'='
t_LESS_EQUAL = r'<='
t_INCREMENT = r'\+\+'
t_PLUS = r'\+'
t_DOT = r'\.'

# Reglas para tokens más complejos
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'"[^"]*"'
    return t

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Contador de líneas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejo de errores
def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}' en la línea {t.lexer.lineno}")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

# Función para obtener todos los tokens
def get_all_tokens(code):
    # Inicializar el número de línea en 1
    lexer.lineno = 1
    lexer.input(code)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append((tok.type, tok.value, tok.lineno))
    return tokens
