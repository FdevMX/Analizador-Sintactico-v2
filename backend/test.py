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
        """Captura errores de sintaxis generales."""
        if p:
            self.errors.append(f"Error de sintaxis en la línea {p.lineno}, posición {p.lexpos}: Token inesperado '{p.value}'")
            self.parser.errok()
        else:
            self.check_for_missing_elements()
            
    # def p_error(self, p):
    #     """Captura errores de sintaxis generales."""
    #     if p:
    #         self.errors.append(f"Error de sintaxis en la línea {p.lineno}, posición {p.lexpos}: Token inesperado '{p.value}'")
    #         # Intenta recuperarse del error
    #         while True:
    #             tok = self.parser.token()
    #             if not tok or tok.type == 'SEMICOLON': 
    #                 break
    #         self.parser.restart()
    #     else:
    #         self.check_for_missing_elements()

    def check_for_missing_elements(self):
        """Verifica si faltan llaves, paréntesis o puntos y comas al final de las declaraciones."""
        stack_types = [t.type if t else '' for t in self.parser.symstack]
        if 'LBRACE' in stack_types and 'RBRACE' not in stack_types:
            self.errors.append("Error de sintaxis: Falta la llave de cierre '}' al final del bloque")
        if 'LPAREN' in stack_types and 'RPAREN' not in stack_types:
            self.errors.append("Error de sintaxis: Falta el paréntesis de cierre ')' en una declaración")
        if 'SEMICOLON' not in stack_types[-3:]:
            self.errors.append("Error de sintaxis: Falta un punto y coma ';' al final de una declaración")

    def check_specific_errors(self, code):
        """Método que puede ser sobrescrito para verificar errores específicos del pseudocódigo."""
        pass


# Define los parsers específicos para pseudocódigo
class PseudocodeAnalyzer(SyntacticAnalyzer):

    # -----------------------------------
    # Parser para el programa principal
    # -----------------------------------
    def p_programa(self, p):
        '''programa : PROGRAMA IDENTIFIER LPAREN RPAREN LBRACE declaraciones instrucciones RBRACE'''
        if not self.errors:
            print("Estructura del programa correcta")
        p[0] = ('programa', p[2], p[6], p[7])

    # -----------------------------------
    # Parser para las declaraciones de variables
    # -----------------------------------
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

    # Parser para la lista de identificadores (variables separadas por comas)
    def p_lista_identificadores(self, p):
        '''lista_identificadores : COMA IDENTIFIER lista_identificadores
                                 | empty'''
        if len(p) == 4:
            p[0] = [p[2]] + p[3]
        else:
            p[0] = []

    # -----------------------------------
    # Parser para las instrucciones dentro del cuerpo del programa
    # -----------------------------------
    def p_instrucciones(self, p):
        '''instrucciones : instrucciones instruccion
                         | instruccion
                         | empty'''
        if len(p) == 3:
            p[0] = p[1] + [p[2]]
        else:
            p[0] = [p[1]] if p[1] else []

    # -----------------------------------
    # Parser para cada instrucción (lectura, asignación, impresión, fin)
    # -----------------------------------
    def p_instruccion(self, p):
        '''instruccion : lectura
                       | asignacion
                       | impresion
                       | fin'''
        p[0] = p[1]

    # -----------------------------------
    # Parser para la instrucción 'read'
    # -----------------------------------
    def p_lectura(self, p):
        '''lectura : READ IDENTIFIER SEMICOLON'''
        p[0] = ('lectura', p[2])

    # -----------------------------------
    # Parser para la instrucción de asignación
    # -----------------------------------
    def p_asignacion(self, p):
        '''asignacion : IDENTIFIER EQUALS expresion SEMICOLON'''
        p[0] = ('asignacion', p[1], p[3])

    # -----------------------------------
    # Parser para las expresiones (identificadores, números, suma)
    # -----------------------------------
    def p_expresion(self, p):
        '''expresion : IDENTIFIER PLUS IDENTIFIER
                     | IDENTIFIER
                     | NUMBER'''
        if len(p) == 4:
            p[0] = ('expresion', p[1], '+', p[3])
        else:
            p[0] = ('expresion', p[1])

    # -----------------------------------
    # Parser para la instrucción 'printf' (impresión de cadenas)
    # -----------------------------------
    def p_impresion(self, p):
        '''impresion : PRINTF LPAREN STRING RPAREN SEMICOLON'''
        p[0] = ('impresion', p[3])

    # -----------------------------------
    # Parser para el fin del programa
    # -----------------------------------
    def p_fin(self, p):
        '''fin : END SEMICOLON'''
        p[0] = ('fin')

    def p_empty(self, p):
        '''empty :'''
        pass

    # -----------------------------------
    # Parsers para el manejo de errores
    # -----------------------------------

    # Error en declaración (cuando se usa un número como identificador)
    def p_declaracion_error(self, p):
        '''declaracion : INT NUMBER lista_identificadores SEMICOLON'''
        self.errors.append(f"Error en la línea {p.lineno(2)}: No se puede usar un número como nombre de variable")

    # Error en 'read' (cuando se usa un número o un token inesperado)
    def p_lectura_error(self, p):
        '''lectura : READ NUMBER SEMICOLON
                   | READ error SEMICOLON'''
        if len(p) == 4 and isinstance(p[2], int):
            self.errors.append(f"Error en la línea {p.lineno(2)}: No se puede usar un número como identificador en 'read'")
        else:
            self.errors.append(f"Error en la línea {p.lineno(1)}: Se esperaba un identificador después de 'read'")

    # Error en asignación (cuando se usa un número como identificador o hay una expresión inválida)
    def p_asignacion_error(self, p):
        '''asignacion : NUMBER EQUALS expresion SEMICOLON
                      | IDENTIFIER EQUALS error SEMICOLON'''
        if len(p) == 5 and isinstance(p[1], int):
            self.errors.append(f"Error en la línea {p.lineno(2)}: No se puede usar un número como nombre de variable en la asignación")
        else:
            self.errors.append(f"Error en la línea {p.lineno(1)}: Expresión inválida en la asignación")

    # Error en impresión (cuando no se usa una cadena en printf)
    def p_impresion_error(self, p):
        '''impresion : PRINTF LPAREN error RPAREN SEMICOLON'''
        self.errors.append(f"Error en la línea {p.lineno(1)}: Se esperaba una cadena entre comillas en printf")

    # Error en fin del programa (cuando falta el punto y coma)
    def p_fin_error(self, p):
        '''fin : END error'''
        self.errors.append(f"Error en la línea {p.lineno(1)}: Falta punto y coma después de 'end'")

    # -----------------------------------
    # Verificación de errores específicos en el código
    # -----------------------------------
    
    def check_specific_errors(self, code):
        """Verifica errores específicos en el código antes de pasar al parser."""
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            line = line.strip()

            # Verificar la declaración correcta del programa
            if line.startswith('programa'):
                if not re.match(r'^programa\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\(\s*\)\s*{\s*$', line):
                    self.errors.append(f"Error en la línea {i}, posición 0: Formato incorrecto para la declaración del programa. Debe ser 'programa identificador() {{'")

            # Verificar si 'read' está mal escrito
            elif re.search(r'\bre[a-z]+\b', line) and 'read' not in line:
                position = line.find(re.search(r'\bre[a-z]+\b', line).group(0))
                self.errors.append(f"Error en la línea {i}, posición {position}: 'read' está mal escrito")

            # Verificar si 'printf' está mal escrito o mal formado
            elif 'printf' in line:
                self.check_printf_syntax(line, i)

            # Verificar si 'end' está mal escrito
            elif 'en;' in line or 'en ' in line:
                position = line.find('en')
                self.errors.append(f"Error en la línea {i}, posición {position}: ¿Quizás quiso decir 'end'?")

            # Verificar si las asignaciones no tienen punto y coma
            elif '=' in line and not line.endswith(';'):
                position = line.find('=')
                self.errors.append(f"Error en la línea {i}, posición {position}: Falta un punto y coma al final de la asignación")

        # Verificar identificadores no declarados
        self.check_identifiers(lines)

    # def check_specific_errors(self, code):
        """Verifica errores específicos en el código antes de pasar al parser."""
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            line = line.strip()

            # Verificar la declaración correcta del programa
            if line.startswith('programa'):
                if not re.match(r'^programa\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\(\s*\)\s*{\s*$', line):
                    self.errors.append(f"Error en la línea {i}, posición 0: Formato incorrecto para la declaración del programa. Debe ser 'programa identificador() {{'")

            # Verificar si 'read' está mal escrito
            elif re.search(r'\bre[a-z]+\b', line) and 'read' not in line:
                position = line.find(re.search(r'\bre[a-z]+\b', line).group(0))
                self.errors.append(f"Error en la línea {i}, posición {position}: 'read' está mal escrito")

            # Verificar si 'printf' está mal escrito o mal formado
            elif 'printf' in line:
                self.check_printf_syntax(line, i)

            # Verificar si 'end' está mal escrito
            elif 'en;' in line or 'en ' in line:
                position = line.find('en')
                self.errors.append(f"Error en la línea {i}, posición {position}: ¿Quizás quiso decir 'end'?")
                
            elif 'ed;' in line or 'ed ' in line:
                position = line.find('ed')
                self.errors.append(f"Error en la línea {i}, posición {position}: ¿Quizás quiso decir 'end'?")

            # Verificar si las asignaciones no tienen punto y coma
            elif '=' in line and not line.endswith(';'):
                position = line.find('=')
                self.errors.append(f"Error en la línea {i}, posición {position}: Falta un punto y coma al final de la asignación")

        # Verificar identificadores no declarados
        self.check_identifiers(lines)

    def check_printf_syntax(self, line, line_number):
        """Verifica si el uso de printf es correcto."""
        if not re.match(r'printf\s*\(\s*".*"\s*\)\s*;', line):
            if not line.endswith(';'):
                self.errors.append(f"Error en la línea {line_number}: Falta un punto y coma ';' al final de 'printf'")
            if '"' not in line:
                self.errors.append(f"Error en la línea {line_number}: Falta comillas en la instrucción 'printf'")
            if '(' not in line or ')' not in line:
                self.errors.append(f"Error en la línea {line_number}: Falta un paréntesis en 'printf'")

    def check_identifiers(self, lines):
        """Verifica que todos los identificadores usados en 'read' y asignaciones estén declarados."""
        declared_identifiers = set()  # Para almacenar identificadores declarados
        used_identifiers = []         # Para almacenar identificadores usados

        for i, line in enumerate(lines, 1):
            line = line.strip()

            # Detectar declaraciones de variables
            if line.startswith('int '):
                # Extraer y guardar los identificadores declarados
                identifiers = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', line[4:].strip(';'))
                declared_identifiers.update(identifiers)

            # Detectar uso de identificadores en 'read'
            elif line.startswith('read '):
                identifier = line.split()[1].strip(';')
                used_identifiers.append((identifier, i, line.find(identifier)))

            # Detectar uso de identificadores en asignaciones
            elif '=' in line:
                identifier = line.split('=')[0].strip()
                used_identifiers.append((identifier, i, line.find(identifier)))

                # Añadir también los identificadores usados en la parte de la expresión
                expression_identifiers = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', line.split('=')[1])
                for expr_id in expression_identifiers:
                    used_identifiers.append((expr_id, i, line.find(expr_id)))

        # Verificar si los identificadores usados han sido declarados
        for identifier, line_num, position in used_identifiers:
            if identifier not in declared_identifiers:
                self.errors.append(f"Error en la línea {line_num}, posición {position}: Identificador '{identifier}' no declarado")

# Función para obtener el analizador adecuado según el lenguaje
def get_analyzer(language):
    if language.lower() == 'pseudocode':
        return PseudocodeAnalyzer()
    else:
        raise ValueError("Lenguaje no soportado. Elija 'pseudocode'.")

# Ejemplo de uso
if __name__ == "__main__":
    pseudocode = """
    programa suma(){
        int a,b,c;
        read a;
        rea b;  # Error en la palabra read
        c = a + b;
        printf ("la suma es");
        end;
    }
    """

    pseudocode_analyzer = get_analyzer('pseudocode')
    
    print("Analizando pseudocódigo:")
    print(pseudocode_analyzer.parse(pseudocode))