import ply.yacc as yacc
import re
from lexico import tokens, lexer

errors = []

# Definir la gramática

def p_programa(p):
    '''programa : PROGRAMA IDENTIFIER LPAREN RPAREN LBRACE declaraciones instrucciones RBRACE'''
    if not errors:
        print("Estructura del programa correcta")
    p[0] = ('programa', p[2], p[6], p[7])

def p_declaraciones(p):
    '''declaraciones : declaraciones declaracion
                     | declaracion
                     | empty'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]] if p[1] else []

def p_declaracion(p):
    '''declaracion : INT IDENTIFIER lista_identificadores SEMICOLON'''
    p[0] = ('declaracion', p[2], p[3])

def p_lista_identificadores(p):
    '''lista_identificadores : COMA IDENTIFIER lista_identificadores
                             | empty'''
    if len(p) == 4:
        p[0] = [p[2]] + p[3]
    else:
        p[0] = []

def p_instrucciones(p):
    '''instrucciones : instrucciones instruccion
                     | instruccion
                     | empty'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]] if p[1] else []

def p_instruccion(p):
    '''instruccion : lectura
                   | asignacion
                   | impresion
                   | fin'''
    p[0] = p[1]

def p_lectura(p):
    '''lectura : READ IDENTIFIER SEMICOLON'''
    p[0] = ('lectura', p[2])

def p_asignacion(p):
    '''asignacion : IDENTIFIER EQUALS expresion SEMICOLON'''
    p[0] = ('asignacion', p[1], p[3])

def p_expresion(p):
    '''expresion : IDENTIFIER PLUS IDENTIFIER
                 | IDENTIFIER
                 | NUMBER'''
    if len(p) == 4:
        p[0] = ('expresion', p[1], '+', p[3])
    else:
        p[0] = ('expresion', p[1])

def p_impresion(p):
    '''impresion : PRINTF LPAREN STRING RPAREN SEMICOLON'''
    p[0] = ('impresion', p[3])

def p_fin(p):
    '''fin : END SEMICOLON'''
    p[0] = ('fin')

def p_empty(p):
    '''empty :'''
    pass

# Parsers para errores específicos

def p_lectura_error(p):
    '''lectura : READ error SEMICOLON'''
    errors.append(f"Error en la línea {p.lineno(1)}: Se esperaba un identificador después de 'read'")

def p_asignacion_error(p):
    '''asignacion : IDENTIFIER EQUALS error SEMICOLON'''
    errors.append(f"Error en la línea {p.lineno(1)}: Expresión inválida en la asignación")

def p_impresion_error(p):
    '''impresion : PRINTF LPAREN error RPAREN SEMICOLON'''
    errors.append(f"Error en la línea {p.lineno(1)}: Se esperaba una cadena entre comillas en printf")

def p_fin_error(p):
    '''fin : END error'''
    errors.append(f"Error en la línea {p.lineno(1)}: Falta punto y coma después de 'end'")

def p_error(p):
    if p:
        errors.append(f"Error de sintaxis en la línea {p.lineno}, posición {p.lexpos}: Token inesperado '{p.value}'")
        parser.errok()
    else:
        check_for_missing_elements()

def check_for_missing_elements():
    stack_types = [t.type if t else '' for t in parser.symstack]
    if 'LBRACE' in stack_types and 'RBRACE' not in stack_types:
        errors.append("Error de sintaxis: Falta la llave de cierre '}' al final del bloque")
    if 'LPAREN' in stack_types and 'RPAREN' not in stack_types:
        errors.append("Error de sintaxis: Falta el paréntesis de cierre ')' en la declaración")
    if 'SEMICOLON' not in stack_types[-3:]:
        errors.append("Error de sintaxis: Falta un punto y coma ';' al final de una declaración")
            
def check_specific_errors(code):
    lines = code.split('\n')
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if line.startswith('programa'):
            if not re.match(r'^programa\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\(\s*\)\s*{\s*$', line):
                errors.append(f"Error en la línea {i}: Formato incorrecto para la declaración del programa. Debe ser 'programa identificador() {{' ")
            elif '(' not in line or ')' not in line:
                errors.append(f"Error en la línea {i}: Faltan paréntesis en la declaración del programa")
            elif line.count('(') > 1 or line.count(')') > 1:
                errors.append(f"Error en la línea {i}: Demasiados paréntesis en la declaración del programa")
        if 'print' in line and 'printf' not in line:
            errors.append(f"Error en la línea {i}: 'print' no es correcto, ¿quizás quiso decir 'printf'?")
        if 'read' in line and not line.endswith(';'):
            errors.append(f"Error en la línea {i}: Falta punto y coma al final de la instrucción 'read'")
        if '=' in line and not line.endswith(';'):
            errors.append(f"Error en la línea {i}: Falta punto y coma al final de la asignación")

# Construir el parser
parser = yacc.yacc()

# Función para parsear el código
def parse_code(code):
    global errors
    errors = []
    lexer.lineno = 1
    check_specific_errors(code)
    result = parser.parse(code, lexer=lexer)
    if not errors:
        print("Estructura del código correcta")
    return errors

# Pseudocódigo a analizar
pseudocodigo = """
programa suma(){
    int a,b,c;
    read a;
    read b;
    c = a + b;
    printf ("la suma es");
    end;
}
"""

# Parsear el pseudocódigo
resultado = parse_code(pseudocodigo)
print(resultado)