# archivo: lexer_sintactico.py

from lexico import lexer

# Definir las columnas de la tabla
columns = ["Token", "PR", "Identificador", "Cadena", "Numero", "Simbolo", "Tipo", "Numero Linea"]

# Función para analizar el pseudocódigo y generar la tabla
def analizar_pseudocodigo(pseudocodigo):
    lexer.input(pseudocodigo)
    table = []

    while True:
        tok = lexer.token()
        if not tok:
            break

        row = [""] * len(columns)
        row[0] = tok.type  # Token

        if tok.type in ["FOR", "INT", "SYSTEM", "OUT", "PRINTLN", "END", "PRINTF", "PROGRAMA", "READ"]:
            row[1] = "x"  # PR
        if tok.type == "IDENTIFIER":
            row[2] = "x"  # Identificador
        if tok.type == "STRING":
            row[3] = "x"  # Cadena
        if tok.type == "NUMBER":
            row[4] = "x"  # Numero
        if tok.type in ["LPAREN", "RPAREN", "LBRACE", "RBRACE", "SEMICOLON", "EQUALS", "LESS_EQUAL", "INCREMENT", "PLUS", "DOT", "COMA"]:
            row[5] = "x"  # Simbolo

        # Mostrar el tipo de lexema en la columna "Tipo"
        row[6] = tok.value

        # Agregar el número de línea
        row[7] = str(tok.lineno)

        table.append(row)

    return table

# Función para imprimir la tabla
def imprimir_tabla(table):
    # Imprimir encabezados
    print("\t".join(columns))
    # Imprimir filas
    for row in table:
        print("\t".join(row))

# Pseudocódigo a analizar
pseudocodigo = """
programa suma(){
    int a,b,c;
    read a;
    read b;
    c = a + b;
    printf ("la suma es")
    end;
}
"""

# Analizar el pseudocódigo y generar la tabla
tabla = analizar_pseudocodigo(pseudocodigo)

# Imprimir la tabla
imprimir_tabla(tabla)