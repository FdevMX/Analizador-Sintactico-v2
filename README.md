# Analizador-Sintactico

Este proyecto es un analizador sintáctico que incluye varias mejoras y correcciones para analizar código de manera eficiente.

## Estructura del Proyecto

- `app.py`: Contiene las funciones principales y parsers para analizar el código. Se han corregido funciones y parsers para encontrar errores específicos en el código a analizar. Ahora es posible mostrar correctamente la línea, posición y tipo de error encontrado.
- `combined.py`: Integra diferentes componentes del analizador para proporcionar una funcionalidad unificada.
- `lexer_sintactico.py`: Implementa el lexer para el análisis sintáctico.
- `lexico.py`: Contiene el análisis léxico del código.
- `sintac_pseudo.py`: Proporciona funcionalidades específicas para el análisis de pseudocódigo.
- `sintactico.py`: Implementa el análisis sintáctico del código.

## Mejoras y Correcciones

### Correcciones en `app.py`
- Se corrigieron funciones y parsers para encontrar errores específicos en el código a analizar. Ahora es posible mostrar correctamente la línea, posición y tipo de error encontrado.

### Mejoras en `lexico.py`
- Se corrigió la función para encontrar en qué línea estaba un fragmento de código. Los tokens ya se obtienen correctamente.

## Requisitos

Para instalar las dependencias necesarias, ejecute:

```sh
pip install -r requirements.txt
```

## Uso

Para ejecutar el analizador, utilice el siguiente comando:

```sh
python app.py
```

## Licencia

Este proyecto está licenciado bajo los términos de la licencia MIT. Consulte el archivo [LICENCE](LICENCE) para más detalles.