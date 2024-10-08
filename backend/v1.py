import ply.yacc as yacc
import re
from lexico import tokens, lexer

class SyntacticAnalyzer:
    tokens = tokens
    def __init__(self):
        self.errors = []
        self.parser = yacc.yacc(module=self)

    def parse(self, code):
        self.errors = []
        lexer.lineno = 1
        self.check_specific_errors(code)
        result = self.parser.parse(code, lexer=lexer)
        return self.errors

    def p_error(self, p):
        if p:
            self.errors.append(f"Error de sintaxis en la línea {p.lineno}, posición {p.lexpos}: Token inesperado '{p.value}'")
            self.parser.errok()
        else:
            self.check_for_missing_elements()

    def check_for_missing_elements(self):
        stack_types = [t.type if t else '' for t in self.parser.symstack]
        if 'LBRACE' in stack_types and 'RBRACE' not in stack_types:
            self.errors.append("Error de sintaxis: Falta la llave de cierre '}' al final del bloque")
        if 'LPAREN' in stack_types and 'RPAREN' not in stack_types:
            self.errors.append("Error de sintaxis: Falta el paréntesis de cierre ')' en la declaración")
        if 'SEMICOLON' not in stack_types[-3:]:
            self.errors.append("Error de sintaxis: Falta un punto y coma ';' al final de una declaración")

    def check_specific_errors(self, code):
        pass  # To be implemented in subclasses

class PseudocodeAnalyzer(SyntacticAnalyzer):
    def p_programa(self, p):
        '''programa : PROGRAMA IDENTIFIER LPAREN RPAREN LBRACE declaraciones instrucciones RBRACE'''
        if not self.errors:
            print("Estructura del programa correcta")
        p[0] = ('programa', p[2], p[6], p[7])

    def p_declaraciones(self, p):
        '''declaraciones : declaraciones declaracion
                         | declaracion
                         | empty'''
        if len(p) == 3:
            p[0] = p[1] + [p[2]]
        else:
            p[0] = [p[1]] if p[1] else []

    def p_declaracion(self, p):
        '''declaracion : INT IDENTIFIER lista_identificadores SEMICOLON'''
        p[0] = ('declaracion', p[2], p[3])

    def p_lista_identificadores(self, p):
        '''lista_identificadores : COMA IDENTIFIER lista_identificadores
                                 | empty'''
        if len(p) == 4:
            p[0] = [p[2]] + p[3]
        else:
            p[0] = []

    def p_instrucciones(self, p):
        '''instrucciones : instrucciones instruccion
                         | instruccion
                         | empty'''
        if len(p) == 3:
            p[0] = p[1] + [p[2]]
        else:
            p[0] = [p[1]] if p[1] else []

    def p_instruccion(self, p):
        '''instruccion : lectura
                       | asignacion
                       | impresion
                       | fin'''
        p[0] = p[1]

    def p_lectura(self, p):
        '''lectura : READ IDENTIFIER SEMICOLON'''
        p[0] = ('lectura', p[2])

    def p_asignacion(self, p):
        '''asignacion : IDENTIFIER EQUALS expresion SEMICOLON'''
        p[0] = ('asignacion', p[1], p[3])

    def p_expresion(self, p):
        '''expresion : IDENTIFIER PLUS IDENTIFIER
                     | IDENTIFIER
                     | NUMBER'''
        if len(p) == 4:
            p[0] = ('expresion', p[1], '+', p[3])
        else:
            p[0] = ('expresion', p[1])

    def p_impresion(self, p):
        '''impresion : PRINTF LPAREN STRING RPAREN SEMICOLON'''
        p[0] = ('impresion', p[3])

    def p_fin(self, p):
        '''fin : END SEMICOLON'''
        p[0] = ('fin')

    def p_empty(self, p):
        '''empty :'''
        pass

    def p_declaracion_error(self, p):
        '''declaracion : INT NUMBER lista_identificadores SEMICOLON'''
        self.errors.append(f"Error en la línea {p.lineno(2)}: No se puede usar un número como nombre de variable")

    def p_lectura_error(self, p):
        '''lectura : READ NUMBER SEMICOLON
                | READ error SEMICOLON'''
        if len(p) == 4 and isinstance(p[2], int):
            self.errors.append(f"Error en la línea {p.lineno(2)}: No se puede usar un número como identificador en 'read'")
        else:
            self.errors.append(f"Error en la línea {p.lineno(1)}: Se esperaba un identificador después de 'read'")

    def p_asignacion_error(self, p):
        '''asignacion : NUMBER EQUALS expresion SEMICOLON
                    | IDENTIFIER EQUALS error SEMICOLON'''
        if len(p) == 5 and isinstance(p[1], int):
            self.errors.append(f"Error en la línea {p.lineno(2)}: No se puede usar un número como nombre de variable en la asignación")
        else:
            self.errors.append(f"Error en la línea {p.lineno(1)}: Expresión inválida en la asignación")

    def p_impresion_error(self, p):
        '''impresion : PRINTF LPAREN error RPAREN SEMICOLON'''
        self.errors.append(f"Error en la línea {p.lineno(1)}: Se esperaba una cadena entre comillas en printf")

    def p_fin_error(self, p):
        '''fin : END error'''
        self.errors.append(f"Error en la línea {p.lineno(1)}: Falta punto y coma después de 'end'")

    def check_specific_errors(self, code):
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if line.startswith('programa'):
                if not re.match(r'^programa\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\(\s*\)\s*{\s*$', line):
                    self.errors.append(f"Error en la línea {i}: Formato incorrecto para la declaración del programa. Debe ser 'programa identificador() {{' ")
            elif 'print' in line and 'printf' not in line:
                self.errors.append(f"Error en la línea {i}: 'print' no es correcto, ¿quizás quiso decir 'printf'?")
            elif 'read' in line and not line.endswith(';'):
                self.errors.append(f"Error en la línea {i}: Falta punto y coma al final de la instrucción 'read'")
            elif '=' in line and not line.endswith(';'):
                self.errors.append(f"Error en la línea {i}: Falta punto y coma al final de la asignación")
        
        self.check_identifiers(lines)
    
    def check_identifiers(self, lines):
        int_identifiers = []
        read_identifiers = []
        sum_operands = []

        for line in lines:
            line = line.strip()
            if line.startswith('int '):
                int_identifiers = [identifier.strip() for identifier in line[4:].strip(';').split(',')]
            elif line.startswith('read '):
                read_identifiers.append(line[5:].strip(';'))
            elif '=' in line and '+' in line:
                sum_operands = [operand.strip() for operand in line.split('=')[1].strip(';').split('+')]

        # Check if all read identifiers are in int identifiers
        for identifier in read_identifiers:
            if identifier not in int_identifiers:
                self.errors.append(f"Error: Identificador '{identifier}' en la instrucción 'read' no declarado en 'int'")

        # Check if all sum operands are in int identifiers
        for operand in sum_operands:
            if operand not in int_identifiers:
                self.errors.append(f"Error: Identificador '{operand}' en la operación de suma no declarado en 'int'")

class JavaForLoopAnalyzer(SyntacticAnalyzer):
    def p_for_loop(self, p):
        '''for_loop : FOR LPAREN initialization condition increment RPAREN LBRACE statement RBRACE'''
        if not self.errors:
            print("Estructura del bucle 'for' correcta")

    def p_initialization(self, p):
        '''initialization : INT IDENTIFIER EQUALS NUMBER SEMICOLON
                          | IDENTIFIER EQUALS NUMBER SEMICOLON'''

    def p_condition(self, p):
        '''condition : IDENTIFIER LESS_EQUAL NUMBER SEMICOLON'''

    def p_increment(self, p):
        '''increment : IDENTIFIER INCREMENT
                     | INCREMENT IDENTIFIER'''

    def p_statement(self, p):
        '''statement : SYSTEM DOT OUT DOT PRINTLN LPAREN STRING PLUS IDENTIFIER RPAREN SEMICOLON'''

    def p_initialization_error(self, p):
        '''initialization : INT NUMBER EQUALS NUMBER SEMICOLON'''
        self.errors.append(f"Error en la línea {p.lineno(2)}: No se puede usar un número como nombre de variable")

    def p_increment_error(self, p):
        '''increment : IDENTIFIER PLUS'''
        self.errors.append(f"Error en la línea {p.lineno(2)}: Incremento incorrecto, use '++' en lugar de '+'")

    def check_specific_errors(self, code):
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            if 'System' in line and 'System.out.println' not in line:
                self.errors.append(f"Error en la línea {i}: Posible error en 'System.out.println', verifique la ortografía")
            if 'printn' in line:
                self.errors.append(f"Error en la línea {i}: 'printn' no es correcto, ¿quizás quiso decir 'println'?")

def get_analyzer(language):
    if language.lower() == 'pseudocode':
        return PseudocodeAnalyzer()
    elif language.lower() == 'java':
        return JavaForLoopAnalyzer()
    else:
        raise ValueError("Lenguaje no soportado. Elija 'pseudocode' o 'java'.")

# Ejemplo de uso
if __name__ == "__main__":
    pseudocode = """
    programa suma(){
        int a,b,c;
        read a;
        read b;
        c = a + b;
        printf ("la suma es");
        end;
    }
    """

    java_code = """
    for (int i = 0; i <= 5; i++) {
        System.out.println("Iteration: " + i);
    }
    """

    pseudocode_analyzer = get_analyzer('pseudocode')
    java_analyzer = get_analyzer('java')

    print("Analizando pseudocódigo:")
    print(pseudocode_analyzer.parse(pseudocode))

    print("\nAnalizando bucle for de Java:")
    print(java_analyzer.parse(java_code))