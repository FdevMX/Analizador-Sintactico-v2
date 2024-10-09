import ply.lex as lex

# Lista de nombres de tokens
tokens = [
    'INCLUDE', 'IOSTREAM', 'USING', 'NAMESPACE', 'INT', 'MAIN', 'COUT',
    'STRING', 'RETURN', 'NUMBER', 'IDENTIFIER', 'SEMICOLON', 'LPAREN',
    'RPAREN', 'LBRACE', 'RBRACE', 'LESS_THAN', 'GREATER_THAN', 'DOUBLE_LESS_THAN'
]

# Palabras reservadas
reserved = {
    'include': 'INCLUDE',
    'iostream': 'IOSTREAM',
    'using': 'USING',
    'namespace': 'NAMESPACE',
    'int': 'INT',
    'main': 'MAIN',
    'cout': 'COUT',
    'return': 'RETURN'
}

# Reglas para tokens simples
t_SEMICOLON = r';'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LESS_THAN = r'<'
t_GREATER_THAN = r'>'
t_DOUBLE_LESS_THAN = r'<<'

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
    lexer.lineno = 1
    lexer.input(code)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        
        wordReserv = "x" if tok.type in reserved.values() else ""
        identifier = "x" if tok.type == "IDENTIFIER" else ""
        cadena = "x" if tok.type == "STRING" else ""
        numero = "x" if tok.type == "NUMBER" else ""
        simbolo = "x" if tok.type in ["SEMICOLON", "LPAREN", "RPAREN", "LBRACE", "RBRACE", "LESS_THAN", "GREATER_THAN", "DOUBLE_LESS_THAN"] else ""
        
        tokens.append((tok.type, tok.value, wordReserv, identifier, cadena, numero, simbolo, tok.lineno))
    return tokens

# Función para contar las ocurrencias de cada tipo de token
def contar_repeticiones(tokens):
    counts = {
        "wordReserv": 0,
        "identifier": 0,
        "cadena": 0,
        "numero": 0,
        "simbolo": 0
    }
    
    for token in tokens:
        if token[2] == "x":
            counts["wordReserv"] += 1
        if token[3] == "x":
            counts["identifier"] += 1
        if token[4] == "x":
            counts["cadena"] += 1
        if token[5] == "x":
            counts["numero"] += 1
        if token[6] == "x":
            counts["simbolo"] += 1
    
    return counts