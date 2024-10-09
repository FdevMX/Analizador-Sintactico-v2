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

    def check_for_missing_elements(self):
        """Verifica si faltan llaves, paréntesis o puntos y comas al final de las declaraciones."""
        stack_types = [t.type if t else '' for t in self.parser.symstack]
        
        # Verificar llaves desbalanceadas
        lbrace_count = stack_types.count('LBRACE')
        rbrace_count = stack_types.count('RBRACE')
        if lbrace_count > rbrace_count:
            self.errors.append(f"Error de sintaxis: Faltan {lbrace_count - rbrace_count} llave(s) de cierre '}}' al final del bloque")
        
        # Verificar paréntesis desbalanceados
        lparen_count = stack_types.count('LPAREN')
        rparen_count = stack_types.count('RPAREN')
        if lparen_count > rparen_count:
            self.errors.append(f"Error de sintaxis: Faltan {lparen_count - rparen_count} paréntesis de cierre ')' en una declaración")
        
        # Verificar punto y coma faltante
        last_relevant_tokens = [t for t in stack_types[-5:] if t in ['IDENTIFIER', 'NUMBER', 'RPAREN', 'RBRACE']]
        if last_relevant_tokens and last_relevant_tokens[-1] != 'SEMICOLON':
            self.errors.append("Error de sintaxis: Falta un punto y coma ';' al final de una declaración")
            
    def p_error(self, p):
        """Captura errores de sintaxis generales con posiciones corregidas."""
        if p:
            # Obtener el código original
            code = p.lexer.lexdata
            # Dividir el código en líneas
            lines = code.split('\n')
            # Obtener la línea del error
            error_line = lines[p.lineno - 1]
            # Calcular la posición dentro de la línea
            relative_pos = p.lexpos - sum(len(l) + 1 for l in lines[:p.lineno - 1])
            
            # Añadir el error con posición corregida
            self.errors.append(
                f"Error de sintaxis en la línea {p.lineno}, posición {relative_pos}: Token inesperado '{p.value}'"
            )

            # Intentar recuperarse del error buscando el siguiente punto y coma
            while True:
                tok = self.parser.token()
                if not tok or tok.type == 'SEMICOLON':
                    break
            self.parser.restart()
        else:
            self.check_for_missing_elements()

    def check_specific_errors(self, code):
        """Método que puede ser sobrescrito para verificar errores específicos del pseudocódigo."""
        pass


# Define los parsers específicos para pseudocódigo
class PseudocodeAnalyzer(SyntacticAnalyzer):
# class CSyntacticAnalyzer(SyntacticAnalyzer):

    def p_programa(self, p):
        '''programa : include using funcion_main'''
        if not self.errors:
            print("Estructura del programa correcta")
        p[0] = ('programa', p[1], p[2], p[3])

    def p_include(self, p):
        '''include : INCLUDE LESS_THAN IOSTREAM GREATER_THAN'''
        p[0] = ('include', p[3])

    def p_using(self, p):
        '''using : USING NAMESPACE IDENTIFIER SEMICOLON'''
        p[0] = ('using', p[3])

    def p_funcion_main(self, p):
        '''funcion_main : INT MAIN LPAREN RPAREN LBRACE instrucciones RBRACE'''
        p[0] = ('funcion_main', p[6])

    def p_instrucciones(self, p):
        '''instrucciones : instrucciones instruccion
                         | instruccion'''
        if len(p) == 3:
            p[0] = p[1] + [p[2]]
        else:
            p[0] = [p[1]]

    def p_instruccion(self, p):
        '''instruccion : impresion
                       | retorno'''
        p[0] = p[1]

    def p_impresion(self, p):
        '''impresion : COUT DOUBLE_LESS_THAN STRING SEMICOLON'''
        p[0] = ('impresion', p[3])

    def p_retorno(self, p):
        '''retorno : RETURN NUMBER SEMICOLON'''
        p[0] = ('retorno', p[2])

    def p_error(self, p):
        if p:
            self.errors.append(f"Error de sintaxis en la línea {p.lineno}, posición {p.lexpos}: Token inesperado '{p.value}'")
        else:
            self.errors.append("Error de sintaxis: Fin inesperado del archivo")
            
    def check_specific_errors(self, code):
        lines = code.split('\n')
        in_function = False
        for i, line in enumerate(lines, 1):
            line = line.strip()

            # Verificar la inclusión de iostream
            if i == 1 and not line.startswith('#include'):
                self.errors.append(f"Error en la línea {i}: Se espera '#include <iostream>' al inicio del programa")

            # Verificar el uso de namespace std
            if i == 2 and not line.startswith('using namespace std'):
                self.errors.append(f"Error en la línea {i}: Se espera 'using namespace std;'")

            # Verificar la declaración de main
            if 'main' in line and not re.match(r'int\s+main\s*\(\s*\)', line):
                self.errors.append(f"Error en la línea {i}: Formato incorrecto para la declaración de main. Debe ser 'int main()'")

            # Verificar el uso correcto de cout
            if 'cout' in line and '<<' not in line:
                self.errors.append(f"Error en la línea {i}: Uso incorrecto de 'cout'. Debe usarse con '<<'")

            # Verificar que las instrucciones terminen con punto y coma
            if in_function and line and not line.endswith('{') and not line.endswith('}'):
                if not line.endswith(';') and not line.startswith('#') and not re.match(r'\s*\w+:$', line):
                    # Excluir líneas que son etiquetas (terminan con :)
                    if not any(line.startswith(keyword) for keyword in ['if', 'else', 'while', 'for', 'switch', 'case']):
                        self.errors.append(f"Error en la línea {i}: Falta punto y coma al final de la instrucción")

            # Detectar si estamos dentro de una función
            if line.endswith('{'):
                in_function = True
            elif line.endswith('}'):
                in_function = False

        # Verificar la presencia de la función main
        if 'int main()' not in code and 'int main(void)' not in code:
            self.errors.append("Error: Falta la función main() en el programa")

        # Verificar el retorno en la función main
        if 'return' not in code:
            self.errors.append("Error: Falta la instrucción de retorno en la función main")

class CAnalyzer(SyntacticAnalyzer):
    # -----------------------------------
    # Parser for the main function
    # -----------------------------------
    def p_main_function(self, p):
        '''main_function : INCLUDE IOSTREAM USING NAMESPACE STD SEMICOLON INT MAIN LPAREN RPAREN LBRACE statements RBRACE'''
        if not self.errors:
            print("Estructura de la función 'main' correcta")

    # -----------------------------------
    # Parser for statements inside the main function
    # -----------------------------------
    def p_statements(self, p):
        '''statements : statements statement
                      | statement
                      | empty'''
        if len(p) == 3:
            p[0] = p[1] + [p[2]]
        else:
            p[0] = [p[1]] if p[1] else []

    # -----------------------------------
    # Parser for each statement (cout, return)
    # -----------------------------------
    def p_statement(self, p):
        '''statement : cout_statement
                     | return_statement'''
        p[0] = p[1]

    # -----------------------------------
    # Parser for the 'cout' statement
    # -----------------------------------
    def p_cout_statement(self, p):
        '''cout_statement : COUT INSERTION STRING SEMICOLON'''
        p[0] = ('cout', p[3])

    # -----------------------------------
    # Parser for the 'return' statement
    # -----------------------------------
    def p_return_statement(self, p):
        '''return_statement : RETURN NUMBER SEMICOLON'''
        p[0] = ('return', p[2])

    # -----------------------------------
    # Error handling for initialization
    # -----------------------------------
    def p_initialization_error(self, p):
        '''initialization : INT NUMBER EQUALS NUMBER SEMICOLON'''
        self.errors.append(f"Error en la línea {p.lineno(2)}: No se puede usar un número como nombre de variable")

    # -----------------------------------
    # Specific error checks for C code
    # -----------------------------------
    def check_specific_errors(self, code):
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            if 'cout' in line and '<<' not in line:
                self.errors.append(f"Error en la línea {i}: Posible error en 'cout', verifique la ortografía")
            if 'return' in line and not line.endswith(';'):
                self.errors.append(f"Error en la línea {i}: Falta punto y coma después de 'return'")

# Función para obtener el analizador adecuado según el lenguaje
def get_analyzer(language):
    if language.lower() == 'pseudocode':
        return PseudocodeAnalyzer()
    elif language.lower() == 'c':
        return CAnalyzer()
    else:
        raise ValueError("Lenguaje no soportado. Elija 'pseudocode'.")

# Ejemplo de uso
if __name__ == "__main__":
    pseudocode = """
    #include <iostream>
    using namespace std;
    int main()
    {
        cout << "Hello, World!";
        return 0;
    }
    """

    c_code = """
    #include <iostream>
    using namespace std;
    int main()
    {
        cout << "Hello, World!";
        return 0;
    }
    """

    pseudocode_analyzer = get_analyzer('pseudocode')
    java_analyzer = get_analyzer('java')

    print("Analizando pseudocódigo:")
    print(pseudocode_analyzer.parse(pseudocode))

    print("\nAnalizando bucle for de Java:")
    print(java_analyzer.parse(c_code))